#!/usr/bin/env python3
"""Check the built static book and EPUB without third-party dependencies.

Run after the complete build, including Pagefind and the EPUB export. BASE_PATH and
SITE_URL follow astro.config.mjs; --base-path '' checks a root-domain build.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET
import zipfile
import os

WEBSITE_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Reference:
    value: str
    line: int
    kind: str


@dataclass
class Page:
    path: Path
    ids: Counter = field(default_factory=Counter)
    references: list[Reference] = field(default_factory=list)
    title: str = ""
    title_count: int = 0
    h1_count: int = 0
    language: str = ""
    description: str = ""
    canonical: list[str] = field(default_factory=list)
    viewport: str = ""


class PageParser(HTMLParser):
    def __init__(self, page: Page):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        page = self.page
        if attributes.get("id"):
            page.ids[attributes["id"]] += 1
        if tag == "a" and attributes.get("name") and attributes["name"] != attributes.get("id"):
            page.ids[attributes["name"]] += 1
        if tag == "html":
            page.language = attributes.get("lang", "").strip()
        if tag == "title":
            page.title_count += 1
            self.in_title = True
        if tag == "h1":
            page.h1_count += 1
        if tag == "meta":
            name = attributes.get("name", "").lower()
            if name == "description":
                page.description = attributes.get("content", "").strip()
            if name == "viewport":
                page.viewport = attributes.get("content", "").strip()
        relations = attributes.get("rel", "").lower().split()
        is_canonical = tag == "link" and "canonical" in relations
        if is_canonical:
            page.canonical.append(attributes.get("href", ""))
        for key in ("href", "src", "poster"):
            if key not in attributes:
                continue
            # The generated error document is served at arbitrary missing URLs.
            # Its canonical is metadata rather than a discoverable /404/ route.
            if is_canonical and page.path.name == "404.html":
                continue
            page.references.append(Reference(attributes[key] or "", self.getpos()[0], f"{tag}[{key}]"))
        source_set = attributes.get("srcset", "")
        if source_set and not source_set.lstrip().startswith("data:"):
            for item in source_set.split(","):
                parts = item.strip().split()
                if parts:
                    page.references.append(Reference(parts[0], self.getpos()[0], f"{tag}[srcset]"))

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.page.title += data


def document_url(path: Path, dist: Path, base: str, origin: str) -> str:
    relative = path.relative_to(dist).as_posix()
    if relative == "index.html":
        relative = ""
    elif relative.endswith("/index.html"):
        relative = relative[:-len("index.html")]
    return origin.rstrip("/") + base + "/" + relative


def map_reference(value: str, source_url: str, dist: Path, base: str, origin: str):
    """Return (local path, fragment, error), or None for a genuinely external URL."""
    value = value.strip()
    if not value or value.startswith(("data:", "mailto:", "tel:", "javascript:", "blob:")):
        return None
    try:
        supplied = urlsplit(value)
        resolved = urlsplit(urljoin(source_url, value))
        configured = urlsplit(origin)
        actual_port = resolved.port or (443 if resolved.scheme == "https" else 80)
        configured_port = configured.port or (443 if configured.scheme == "https" else 80)
    except ValueError as error:
        return None, "", f"invalid URL: {error}"
    if resolved.scheme not in {"http", "https"}:
        return None
    if (resolved.hostname, actual_port) != (configured.hostname, configured_port):
        return None
    path = unquote(resolved.path)
    inside_base = not base or path == base or path.startswith(base + "/")
    if not inside_base:
        # An absolute link to another project on this account is external. A
        # root/relative internal link escaping our configured base is a defect.
        if supplied.scheme or supplied.netloc:
            return None
        return None, "", f"escapes configured base {base or '/'}"
    relative = path[len(base):].lstrip("/") if base else path.lstrip("/")
    target = (dist / relative).resolve()
    if not target.is_relative_to(dist):
        return None, "", "escapes the output directory"
    if target.is_dir():
        target = target / "index.html"
    elif not target.exists() and not target.suffix:
        directory_index = target / "index.html"
        if directory_index.exists():
            target = directory_index
    fragment = unquote(resolved.fragment)
    if fragment.startswith(":~:text="):
        fragment = ""
    return target, fragment, ""


def check_epub(path: Path) -> list[str]:
    """Validate EPUB container/package, XML, spine and local content references."""
    issues = []
    prefix = f"{path}: "
    try:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member:
                issues.append(prefix + f"ZIP CRC failed for {bad_member}")
            infos = archive.infolist()
            names = archive.namelist()
            files = {name for name in names if not name.endswith("/")}
            if not infos or infos[0].filename != "mimetype":
                issues.append(prefix + "mimetype must be the first ZIP entry")
            if "mimetype" not in files or archive.read("mimetype") != b"application/epub+zip":
                issues.append(prefix + "missing or invalid EPUB mimetype")
            elif archive.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
                issues.append(prefix + "mimetype must be stored without compression")
            if len(names) != len(set(names)):
                issues.append(prefix + "duplicate ZIP entry names")
            for name in files:
                parts = PurePosixPath(name).parts
                if name.startswith("/") or ".." in parts or "\\" in name:
                    issues.append(prefix + f"unsafe ZIP member path {name}")
            documents = {}
            for name in sorted(files):
                if name.endswith((".xml", ".opf", ".xhtml", ".ncx")):
                    try:
                        documents[name] = ET.fromstring(archive.read(name))
                    except ET.ParseError as error:
                        issues.append(prefix + f"invalid XML in {name}: {error}")
            container = documents.get("META-INF/container.xml")
            if container is None:
                issues.append(prefix + "missing or invalid META-INF/container.xml")
                return issues
            rootfiles = container.findall(".//{*}rootfile")
            if not rootfiles:
                issues.append(prefix + "container declares no package rootfile")
                return issues
            package_name = rootfiles[0].get("full-path", "")
            package = documents.get(package_name)
            if package is None:
                issues.append(prefix + f"missing or invalid package {package_name!r}")
                return issues
            metadata = package.find("{*}metadata")
            for name in ("title", "language", "identifier"):
                element = metadata.find("{*}" + name) if metadata is not None else None
                if element is None or not "".join(element.itertext()).strip():
                    issues.append(prefix + f"package metadata missing {name}")
            unique_identifier = package.get("unique-identifier")
            if not unique_identifier or not any(node.get("id") == unique_identifier for node in package.iter()):
                issues.append(prefix + "package unique-identifier does not resolve")
            manifest = package.find("{*}manifest")
            items = list(manifest) if manifest is not None else []
            by_id = {}
            navigation_count = 0
            for item in items:
                item_id = item.get("id", "")
                if not item_id or item_id in by_id:
                    issues.append(prefix + f"empty or duplicate manifest ID {item_id!r}")
                by_id[item_id] = item
                href = urlsplit(item.get("href", ""))
                if href.scheme or href.netloc:
                    continue
                destination = posixpath.normpath(posixpath.join(posixpath.dirname(package_name), unquote(href.path)))
                if not href.path or destination not in files:
                    issues.append(prefix + f"manifest target missing: {item.get('href', '')}")
                if "nav" in item.get("properties", "").split():
                    navigation_count += 1
            if navigation_count != 1:
                issues.append(prefix + f"expected one navigation document, found {navigation_count}")
            spine = package.find("{*}spine")
            if spine is None or not list(spine):
                issues.append(prefix + "package has no reading spine")
            else:
                for itemref in spine:
                    referenced = by_id.get(itemref.get("idref", ""))
                    if referenced is None:
                        issues.append(prefix + f"spine ID not in manifest: {itemref.get('idref', '')}")
                    elif referenced.get("media-type") != "application/xhtml+xml":
                        issues.append(prefix + f"spine item is not XHTML: {itemref.get('idref', '')}")
            identifiers = {}
            for name, root in documents.items():
                counts = Counter(node.get("id") for node in root.iter() if node.get("id"))
                identifiers[name] = set(counts)
                for identity, count in counts.items():
                    if count > 1:
                        issues.append(prefix + f"duplicate ID {identity!r} in {name}")
            for name, root in documents.items():
                if not name.endswith(".xhtml"):
                    continue
                title = root.find("{*}head/{*}title")
                if title is None or not "".join(title.itertext()).strip():
                    issues.append(prefix + f"XHTML document has no title: {name}")
                # Rules EpubCheck enforces that browsers forgive; stores reject the file.
                if any(node.get("align") is not None for node in root.iter()):
                    issues.append(prefix + f"{name} uses the obsolete align attribute")
                for figure in root.findall(".//{*}figure"):
                    children = list(figure)
                    captions = [i for i, child in enumerate(children) if child.tag.endswith("figcaption")]
                    if any(i not in (0, len(children) - 1) for i in captions):
                        issues.append(prefix + f"{name} has a figcaption that is not the first or last child of its figure")
                if any(nav.get("aria-label") is not None for nav in root.findall(".//{*}nav")):
                    issues.append(prefix + f"{name} has aria-label on a navigation element")
                for node in root.iter():
                    for attribute in ("href", "src"):
                        value = node.get(attribute)
                        if not value:
                            continue
                        link = urlsplit(value)
                        if link.scheme or link.netloc:
                            continue
                        destination = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(link.path))) if link.path else name
                        if destination not in files:
                            issues.append(prefix + f"{name} references missing resource {value!r}")
                        elif link.fragment and destination in identifiers and unquote(link.fragment) not in identifiers[destination]:
                            issues.append(prefix + f"{name} references missing fragment {value!r}")
    except (OSError, zipfile.BadZipFile, KeyError, RuntimeError) as error:
        issues.append(prefix + f"cannot validate EPUB: {error}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", default=WEBSITE_ROOT / "dist", type=Path)
    parser.add_argument("--base-path", default=os.environ.get("BASE_PATH", "/ai-ml-ground-truth"))
    parser.add_argument("--site-url", default=os.environ.get("SITE_URL", "https://santoshshinde2012.github.io"))
    parser.add_argument("--epub", type=Path, help="EPUB to validate; otherwise discover EPUBs under dist")
    parser.add_argument("--json", type=Path, help="optional machine-readable check report")
    args = parser.parse_args()
    dist = args.dist.resolve()
    base = "/" + args.base_path.strip("/") if args.base_path.strip("/") else ""
    origin = args.site_url.rstrip("/")
    parsed_origin = urlsplit(origin)
    if parsed_origin.scheme not in {"http", "https"} or not parsed_origin.netloc:
        parser.error("--site-url must be an absolute HTTP(S) URL")
    if not dist.is_dir():
        print(f"Build directory not found: {dist}. Run the complete build first.", file=sys.stderr)
        return 2
    pages = {}
    failures = []
    warnings = []
    references_checked = 0
    for path in sorted(dist.rglob("*.html")):
        page = Page(path=path)
        try:
            PageParser(page).feed(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as error:
            failures.append(f"{path.relative_to(dist)}: cannot read HTML: {error}")
            continue
        pages[path] = page
        label = path.relative_to(dist).as_posix()
        if page.title_count != 1 or not page.title.strip():
            failures.append(f"{label}: expected one nonempty <title>")
        if not page.language:
            failures.append(f"{label}: missing html[lang]")
        if not page.description:
            failures.append(f"{label}: missing meta description")
        if not page.viewport:
            failures.append(f"{label}: missing responsive viewport metadata")
        if not page.h1_count:
            failures.append(f"{label}: missing h1")
        elif page.h1_count > 1 and label != "print/index.html":
            failures.append(f"{label}: expected one h1, found {page.h1_count}")
        if len(page.canonical) != 1:
            failures.append(f"{label}: expected one canonical URL")
        elif not (urlsplit(page.canonical[0]).scheme in {"http", "https"} and urlsplit(page.canonical[0]).netloc):
            failures.append(f"{label}: canonical must be an absolute HTTP(S) URL")
        for identity, count in page.ids.items():
            if count > 1:
                failures.append(f"{label}: duplicate ID {identity!r} ({count} occurrences)")
    if not pages:
        failures.append("No generated HTML pages were found")
    if not (dist / "index.html").is_file():
        failures.append("Missing dist/index.html entrypoint")
    for path, page in pages.items():
        source_url = document_url(path, dist, base, origin)
        for reference in page.references:
            mapped = map_reference(reference.value, source_url, dist, base, origin)
            if mapped is None:
                continue
            references_checked += 1
            target, fragment, error = mapped
            location = f"{path.relative_to(dist)}:{reference.line} {reference.kind}={reference.value!r}"
            if error:
                failures.append(f"{location}: {error}")
            elif not target.is_file():
                failures.append(f"{location}: target does not exist ({target.relative_to(dist)})")
            elif fragment and target in pages and fragment not in pages[target].ids:
                failures.append(f"{location}: fragment #{fragment} does not exist in {target.relative_to(dist)}")
    css_references = 0
    for path in sorted(dist.rglob("*.css")):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", content):
            value = match.group(2).strip()
            # Fragment-only URLs can point at an SVG in the embedding document.
            if not value or value.startswith("#"):
                continue
            mapped = map_reference(value, document_url(path, dist, base, origin), dist, base, origin)
            if mapped is None:
                continue
            css_references += 1
            target, _, error = mapped
            if error or not target.is_file():
                failures.append(f"{path.relative_to(dist)}: CSS resource {value!r}: {error or 'target does not exist'}")
    epubs = [args.epub.resolve()] if args.epub else sorted(dist.rglob("*.epub"))
    if not epubs:
        failures.append("No EPUB was generated under dist")
    for epub in epubs:
        failures.extend(check_epub(epub))
    report = {
        "pages": len(pages), "internal_references": references_checked,
        "css_resources": css_references, "epubs": len(epubs),
        "base_path": base or "/", "failures": failures, "warnings": warnings,
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {len(pages)} HTML pages, {references_checked} internal references, "
          f"{css_references} CSS assets and {len(epubs)} EPUB(s).")
    if failures:
        for failure in failures[:80]:
            print(f"FAIL {failure}", file=sys.stderr)
        if len(failures) > 80:
            print(f"… {len(failures) - 80} further failures; use --json for the full report.", file=sys.stderr)
        print(f"Static publication check failed: {len(failures)} issue(s).", file=sys.stderr)
        return 1
    print("Static publication checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
