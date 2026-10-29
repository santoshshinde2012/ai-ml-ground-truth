#!/usr/bin/env python3
"""Check public Markdown references with bounded requests and a JSON audit trail.

Only repeated 404/410 responses fail the check. Bot restrictions, TLS/network
failures and rate limits remain explicitly unverified rather than being called
broken links. Availability does not establish that a source supports a claim.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit, urlunsplit

WEBSITE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = WEBSITE_ROOT.parent


EXCLUDED_DIRECTORIES = {
    ".git", ".cache", ".astro", "node_modules", "dist", "build", "coverage",
    ".venv", "venv", "__pycache__", "output", ".next", "lab-reference", "downloads",
}


def inline_urls(line: str) -> set[str]:
    """Read inline destinations while preserving balanced URL parentheses."""
    found = set()
    for start in re.finditer(r"!?\[[^\]]*\]\(\s*", line):
        position = start.end()
        if position < len(line) and line[position] == "<":
            end = line.find(">", position + 1)
            if end >= 0:
                destination = line[position + 1:end]
            else:
                continue
        else:
            begin, depth = position, 0
            while position < len(line):
                character = line[position]
                if character == "\\" and position + 1 < len(line):
                    position += 2
                    continue
                if character.isspace() or (character == ")" and depth == 0):
                    break
                if character == "(":
                    depth += 1
                elif character == ")":
                    depth -= 1
                position += 1
            destination = re.sub(r"\\([()])", r"\1", line[begin:position])
        if destination.startswith(("https://", "http://")):
            found.add(destination)
    return found


def markdown_urls(root: Path) -> dict[str, list[dict]]:
    locations = {}
    angle = re.compile(r"<(https?://[^<>\s]+)>")
    definition = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(https?://[^\s>]+)")
    for directory, children, names in os.walk(root):
        children[:] = sorted(name for name in children if name not in EXCLUDED_DIRECTORIES)
        for name in sorted(names):
            if not name.lower().endswith(".md"):
                continue
            path = Path(directory) / name
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                candidates = inline_urls(line) | {match.group(1) for pattern in (angle, definition) for match in pattern.finditer(line)}
                for original in sorted(candidates):
                    parsed = urlsplit(original)
                    # Fragments do not change an HTTP availability request. Keep
                    # the original URL and its location in the report.
                    canonical = urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/", parsed.query, ""))
                    locations.setdefault(canonical, []).append({
                        "file": path.relative_to(root).as_posix(), "line": number, "url": original,
                    })
    return locations


def request(curl: str, url: str, method: str, timeout: float) -> dict:
    command = [curl, "--silent", "--show-error", "--location", "--max-redirs", "8",
               "--connect-timeout", str(min(10, timeout)), "--max-time", str(timeout),
               "--user-agent", "GroundTruthBook-LinkCheck/1.0", "--output", os.devnull,
               "--write-out", "%{http_code}\t%{url_effective}"]
    if method == "HEAD":
        command.append("--head")
    else:
        command.extend(["--max-filesize", str(32 * 1024 * 1024)])
    command.extend(["--url", url])
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 5, check=False)
        response = result.stdout.rsplit("\t", 1)
        status = int(response[0]) if response and response[0].isdigit() else 0
        return {
            "method": method, "status": status,
            "final_url": response[1] if len(response) > 1 else url,
            "error": result.stderr.strip()[:500] if result.returncode else "",
        }
    except (subprocess.TimeoutExpired, OSError) as error:
        return {"method": method, "status": 0, "final_url": url, "error": str(error)[:500]}


def check_url(curl: str, url: str, locations: list[dict], timeout: float) -> dict:
    parsed = urlsplit(url)
    if parsed.username or parsed.password:
        # A public book should never put credentials in a reference. Do not
        # contact that URL or reproduce its secret in a request log.
        return {"url": "[credential-bearing URL redacted]", "state": "broken",
                "reason": "embedded credentials in a public reference", "locations": [
                    {"file": item["file"], "line": item["line"]} for item in locations], "attempts": []}
    attempts = [request(curl, url, "HEAD", timeout)]
    if 200 <= attempts[-1]["status"] < 300 and not attempts[-1]["error"]:
        state, reason = "verified", "HTTP availability verified"
    else:
        attempts.append(request(curl, url, "GET", timeout))
        last = attempts[-1]
        if 200 <= last["status"] < 300 and not last["error"]:
            state, reason = "verified", "GET succeeded after HEAD was rejected or unavailable"
        else:
            negatives = {404, 410}
            if last["status"] in negatives and attempts[0]["status"] not in negatives:
                attempts.append(request(curl, url, "GET", timeout))
                last = attempts[-1]
            negative_count = sum(item["status"] in negatives and not item["error"] for item in attempts)
            if negative_count >= 2 and last["status"] in negatives and not last["error"]:
                state, reason = "broken", "404/410 confirmed on repeated requests including GET"
            elif 200 <= last["status"] < 300 and not last["error"]:
                state, reason = "verified", "GET retry succeeded"
            elif last["status"] in {401, 403, 429}:
                state, reason = "unverified", "access restriction or rate limit; manual review required"
            else:
                state, reason = "unverified", "transport/server/response limitation; manual review required"
    return {"url": url, "state": state, "reason": reason, "locations": locations, "attempts": attempts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--report", type=Path, default=WEBSITE_ROOT / ".cache/external-links.json")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--limit", type=int, help="limit the request count for a manual smoke check")
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("--workers must be between 1 and 16")
    if not 1 <= args.timeout <= 120:
        parser.error("--timeout must be between 1 and 120 seconds")
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    curl = shutil.which("curl")
    if not curl:
        print("curl is required for HTTP checks with the operating system's certificate trust.", file=sys.stderr)
        return 2
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"source directory does not exist: {root}")
    urls = markdown_urls(root)
    selected = sorted(urls.items())[:args.limit]
    results = []
    print(f"Checking {len(selected)} unique HTTP(S) references with {args.workers} workers…", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(check_url, curl, url, locations, args.timeout): url for url, locations in selected}
        for future in as_completed(pending):
            result = future.result()
            results.append(result)
            if result["state"] == "broken":
                location = result["locations"][0]
                print(f"BROKEN {location['file']}:{location['line']} {result['url']}", flush=True)
    results.sort(key=lambda item: item["url"])
    counts = Counter(result["state"] for result in results)
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(), "total_discovered": len(urls),
        "checked": len(results), "limited": args.limit is not None,
        "summary": {key: counts[key] for key in ("verified", "unverified", "broken")},
        "scope": "HTTP availability only; does not verify source content or evidentiary support",
        "results": results,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"External references: {counts['verified']} verified, {counts['unverified']} unverified, "
          f"{counts['broken']} confirmed broken. Report: {args.report}")
    if counts["unverified"]:
        print("Unverified sources require manual review; access failures are not classified as missing pages.")
    return 1 if counts["broken"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
