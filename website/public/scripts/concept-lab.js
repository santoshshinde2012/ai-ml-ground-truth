/* Ground Truth interactive field notes. No services, tracking, or external dependencies. */
(() => {
  'use strict';
  const esc = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const text = (x, y, value, cls = '', anchor = 'start') => `<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}">${esc(value)}</text>`;
  const rect = (x,y,w,h,cls='lab-soft-fill',r=3) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" class="${cls}"/>`;
  const line = (x1,y1,x2,y2,cls='lab-path') => `<path d="M${x1} ${y1}L${x2} ${y2}" class="${cls}"/>`;
  const circle=(x,y,r,cls='lab-fill')=>`<circle cx="${x}" cy="${y}" r="${r}" class="${cls}"/>`;
  const svg = (label, content, height = 240) => `<svg viewBox="0 0 640 ${height}" role="img" aria-label="${esc(label)}">${content}</svg>`;
  const fmt = value => new Intl.NumberFormat('en-IN', {maximumFractionDigits:0}).format(value);
  function choose(root, selector, button) { root.querySelectorAll(selector).forEach(b => b.setAttribute('aria-pressed', String(b === button))); }
  function draw(root, graphic, result) { root.querySelector('[data-stage]').innerHTML = graphic; root.querySelector('[data-result]').textContent = result; }
  function bind(root, selector, event, fn) { root.querySelectorAll(selector).forEach(el => el.addEventListener(event, () => fn(el))); }

  function broadcasting(root) {
    let pair='column', revealed=false;
    function matrix(x,y,rows,cols,values,ghost=false) {
      let out=''; for(let r=0;r<rows;r++)for(let c=0;c<cols;c++) {out+=rect(x+c*31,y+r*31,27,27,ghost?'lab-muted-fill':'lab-soft-fill');out+=text(x+c*31+13.5,y+r*31+18,values[r*cols+c],'lab-svg-mono','middle');}return out;
    }
    function render() {
      const rows=pair==='column'?3:2, invalid=pair==='mismatch', cols=pair==='column'?1:3;
      let out=text(38,25,'LEFT INPUT','lab-svg-small')+text(237,25,'RIGHT INPUT','lab-svg-small')+text(443,25,revealed?'OUTPUT':'PREDICT THE SHAPE','lab-svg-small');
      out+=matrix(38,48,rows,cols,Array.from({length:rows*cols},(_,i)=>i+1));out+=text(186,92,'+','lab-svg-mono','middle');
      out+=matrix(237,48,1,invalid?2:3,invalid?[10,20]:[10,20,30]);out+=text(396,92,'→','lab-svg-mono','middle');
      const shape=pair==='column'?'(3, 1)':'(2, 3)';out+=text(38,rows*31+71,shape,'lab-svg-mono')+text(237,rows*31+71,invalid?'(2,)':'(3,)','lab-svg-mono');
      if(!revealed)out+=rect(443,48,116,rows*31-4,'lab-soft-fill')+text(501,92,'?','lab-svg-mono','middle');
      else if(invalid)out+=text(443,80,'Cannot broadcast','lab-svg-mono')+text(443,105,'3 ≠ 2, neither is 1','lab-svg-small');
      else {const vals=Array.from({length:rows*3},(_,i)=>{let r=Math.floor(i/3),c=i%3;return(pair==='column'?r+1:r*3+c+1)+10*(c+1);});out+=matrix(443,48,rows,3,vals);out+=text(443,rows*31+71,`(${rows}, 3)`,'lab-svg-mono');}
      const result=!revealed?'Compare the trailing dimensions first. What shape will the addition produce?':invalid?'The trailing dimensions are 3 and 2. Neither is 1, so NumPy raises a broadcasting error.':pair==='column'?'(3, 1) + (3,) → (3, 3). The column is repeated across three columns; the row is repeated across three rows.':'(2, 3) + (3,) → (2, 3). The same length-3 row is added to each of the two rows.';
      draw(root,svg(result,out,210),result);root.querySelector('[data-reveal]').textContent=revealed?'Hide expansion':'Reveal expansion →';
    }
    bind(root,'[data-pair]','click',b=>{pair=b.dataset.pair;revealed=false;choose(root,'[data-pair]',b);render();});bind(root,'[data-reveal]','click',()=>{revealed=!revealed;render();});render();
  }
  function timeline(root) {
    const events=[{name:'Account created',event:1,arrival:1},{name:'Purchase recorded',event:2,arrival:7},{name:'Support request',event:4,arrival:4},{name:'Refund completed',event:8,arrival:9}];
    function render(){const day=+root.querySelector('[data-clock]').value;root.querySelector('[data-clock-value]').textContent=day;const xp=d=>170+(d-1)*46;let out='';
      for(let d=1;d<=10;d++)out+=line(xp(d),23,xp(d),207)+text(xp(d),17,d,'lab-svg-small','middle');
      events.forEach((e,i)=>{const y=52+i*43,known=e.event<=day&&e.arrival<=day;out+=text(4,y+4,e.name,'lab-svg-small');out+=line(xp(e.event),y,xp(e.arrival),y,'lab-strong-path');out+=circle(xp(e.event),y,6,known?'lab-fill':'lab-muted-fill');out+=rect(xp(e.arrival)-6,y-6,12,12,known?'lab-accent-fill':'lab-muted-fill',1);});
      out+=line(xp(day),23,xp(day),207,'lab-strong-path lab-dashed')+text(170,234,'● Event time     ■ Available to system','lab-svg-small');
      const known=events.filter(e=>e.event<=day&&e.arrival<=day).map(e=>e.name.toLowerCase());const late=events.filter(e=>e.event<=day&&e.arrival>day);
      const result=`Day ${day}: ${known.length} available record${known.length===1?'':'s'}${known.length?` (${known.join(', ')})`:''}.${late.length?` Pending arrival: ${late.map(e=>e.name.toLowerCase()).join(', ')}. Exclude those records from historical features.`:' Only records that have both happened and arrived can enter this snapshot.'}`;
      draw(root,svg(result,out,250),result);
    }bind(root,'[data-clock]','input',render);render();
  }
  function validation(root){let mode='random';const records=Array.from({length:12},(_,i)=>({customer:['A','B','C'][i%3],day:Math.floor(i/3)+1}));
    function render(){const isTest=(r,i)=>mode==='time'?r.day===4:mode==='group'?r.customer==='C':[1,5,9,10].includes(i);let out=text(8,20,'TRAINING','lab-svg-small')+text(350,20,'TEST','lab-svg-small');let a=0,b=0;
      records.forEach((r,i)=>{const test=isTest(r,i),n=test?b++:a++,x=(test?350:8)+(n%3)*87,y=39+Math.floor(n/3)*51;out+=rect(x,y,76,40,test?'lab-accent-fill':'lab-soft-fill')+text(x+11,y+16,`Customer ${r.customer}`,`lab-svg-small${test?' lab-on-accent':''}`)+text(x+11,y+31,`day ${r.day}`,`lab-svg-mono${test?' lab-on-accent':''}`);});
      out+=line(317,32,317,198);const result=mode==='random'?'Random split: customers A, B and C occur in both sets, and some training records occur after test records. This does not test a future launch or unseen customers.':mode==='time'?'Chronological split: train on days 1–3 and test on day 4. Repeated customers are allowed here because the question is future activity for existing customers.':'Group split: customer C appears only in the test set. This tests unseen customers, but does not by itself test future-time performance.';
      draw(root,svg(result,out,210),result);
    }bind(root,'[data-split]','click',b=>{mode=b.dataset.split;choose(root,'[data-split]',b);render();});render();
  }
  function gradients(root){let update='add';function render(){const x=+root.querySelector('[data-x]').value,a=x*x,y=2*a,correct=4*x,computed=update==='add'?correct:2*x;root.querySelector('[data-x-value]').textContent=x;
      let out=line(103,105,278,105,'lab-strong-path')+'<path d="M338 94C405 25 455 25 515 91M338 117C405 185 455 185 515 120" class="lab-strong-path"/><path d="M515 91C455 25 405 25 338 94M515 120C455 185 405 185 338 117M278 105H103" class="lab-gradient-flow"/>';
      [[70,'x',x],[308,'a = x × x',a],[548,'y = a + a',y]].forEach(([cx,label,value])=>{out+=circle(cx,105,31,cx===548?'lab-accent-fill':'lab-soft-fill')+text(cx,111,value,`lab-svg-mono${cx===548?' lab-on-accent':''}`,'middle')+text(cx,165,label,'lab-svg-label','middle');});
      out+=text(425,43,'∂y/∂a = 1','lab-svg-small','middle')+text(425,185,'∂y/∂a = 1','lab-svg-small','middle');out+=text(183,78,`∂a/∂x = ${2*x}`,'lab-svg-small','middle')+text(308,25,update==='add'?'1 + 1 = 2':'Overwrite: only 1','lab-svg-mono','middle');
      const result=`x = ${x}, y = ${y}. Computed dy/dx = ${computed}; analytic derivative = ${correct}.${update==='add'?' Both downstream paths contribute. Gradient accumulation gives the correct answer.':' The overwritten contribution halves the gradient. A finite-difference check would catch the bug.'}`;
      draw(root,svg(result,out,211),result);
    }bind(root,'[data-x]','input',render);bind(root,'[data-gradient]','click',b=>{update=b.dataset.gradient;choose(root,'[data-gradient]',b);render();});render();}
  function retrieval(root){const docs=[{title:'Refund policy · current',topic:'refund',answer:'30 days',public:true,current:true,score:8},{title:'Refund policy · retired',topic:'refund',answer:'14 days',public:true,current:false,score:10},{title:'Internal retention exceptions',topic:'refund',answer:'60 days for selected accounts',public:false,current:true,score:11},{title:'Shipping policy · current',topic:'shipping',answer:'2 business days',public:true,current:true,score:9}];
    function render(){const q=root.querySelector('[data-query]').value,filtered=root.querySelector('[data-filter]').checked;const candidates=docs.filter(d=>d.topic===q&&(!filtered||(d.public&&d.current))).sort((a,b)=>b.score-a.score);const winner=candidates[0];let out=text(5,16,'SOURCE','lab-svg-small')+text(425,16,'ACCESS / VERSION','lab-svg-small');
      docs.forEach((d,i)=>{const y=32+i*46,chosen=d===winner,excluded=filtered&&(!d.public||!d.current);out+=rect(0,y,638,39,chosen?'lab-accent-fill':'lab-soft-fill')+text(12,y+16,d.title,chosen?'lab-on-accent':'')+text(12,y+31,d.answer,`lab-svg-small${chosen?' lab-on-accent':''}`)+text(434,y+23,excluded?'EXCLUDED':chosen?'RETRIEVED':d.topic!==q?'OTHER TOPIC':'ELIGIBLE',`lab-svg-small${chosen?' lab-on-accent':''}`);});
      const result=filtered?`With filters: cite “${winner.title}”: ${winner.answer}. Access and version checks run before retrieval selection; relevance alone is insufficient.`:`Without filters: the relevance score selects “${winner.title}”: ${winner.answer}.${!winner.public?' This source is restricted and must not be exposed to a customer.':!winner.current?' This source is retired and must not establish the current policy.':' This source happens to be eligible, but the access and freshness checks are still missing.'}`;
      draw(root,svg(result,out,225),result);
    }bind(root,'[data-query]','change',render);bind(root,'[data-filter]','change',render);render();}
  function seeded(seed){let a=seed>>>0;return()=>{a+=0x6D2B79F5;let t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;};}
  function pairedInterval(deltas){const rng=seeded(42),estimates=[];for(let b=0;b<2500;b++){let s=0;for(let i=0;i<deltas.length;i++)s+=deltas[Math.floor(rng()*deltas.length)];estimates.push(100*s/deltas.length);}estimates.sort((a,b)=>a-b);return[estimates[Math.floor(estimates.length*.025)],estimates[Math.floor(estimates.length*.975)]];}
  function evaluation(root){let mode='small';const variants={small:[38,2,4,6],clear:[38,2,10,0],regress:[28,12,2,8]};
    function render(){const counts=variants[mode],baseline=counts[0]+counts[1],candidate=counts[0]+counts[2],delta=(candidate-baseline)*2;const diffs=[...Array(counts[0]).fill(0),...Array(counts[1]).fill(-1),...Array(counts[2]).fill(1),...Array(counts[3]).fill(0)];const ci=pairedInterval(diffs);let out=text(5,15,'THE SAME 50 CASES','lab-svg-small');let n=0;
      counts.forEach((count,g)=>{for(let i=0;i<count;i++){let x=7+(n%10)*27,y=35+Math.floor(n/10)*27;out+=rect(x,y,20,20,g===0?'lab-fill':g===2?'lab-accent-fill':g===1?'lab-warn-fill':'lab-muted-fill',3);n++;}});
      const labels=['Both pass','Baseline only','Candidate only','Neither passes'];counts.forEach((count,i)=>{let y=43+i*30;out+=rect(330,y-11,10,10,['lab-fill','lab-warn-fill','lab-accent-fill','lab-muted-fill'][i],2)+text(350,y,labels[i],'lab-svg-label')+text(610,y,count,'lab-svg-mono','end');});
      out+=text(330,183,`${baseline}/50 → ${candidate}/50`,'lab-svg-mono')+text(330,206,`Difference: ${delta>0?'+':''}${delta} pp`,'lab-svg-mono');
      const signed=v=>`${v>0?'+':''}${v.toFixed(0)}`;const decision=ci[0]>0?'This example supports an improvement on the sampled task; check guardrails and representativeness before release.':ci[1]<0?'The candidate performs worse on this sample; retain the baseline and investigate.':'The interval includes zero. Defer a superiority claim and collect more independent evidence.';
      const result=`Baseline ${baseline}/50; candidate ${candidate}/50. Paired bootstrap 95% interval for the difference: ${signed(ci[0])} to ${signed(ci[1])} percentage points (2,500 resamples, seed 42). ${decision}`;
      draw(root,svg(result,out,225),result);
    }bind(root,'[data-candidate]','click',b=>{mode=b.dataset.candidate;choose(root,'[data-candidate]',b);render();});render();}
  function pricing(root){function render(){const price=+root.querySelector('[data-price]').value,stock=+root.querySelector('[data-stock]').value;root.querySelector('[data-price-value]').textContent=`₹${price}`;const demand=p=>Math.max(0,130-.65*p),profit=p=>(p-55)*Math.min(demand(p),stock);const samples=Array.from({length:81},(_,i)=>({price:80+i,value:profit(80+i)}));const max=Math.ceil(Math.max(...samples.map(p=>p.value))/1000)*1000;const xp=p=>58+(p-80)/80*560,yp=v=>180-v/max*145;let out='';
      for(let j=0;j<=4;j++){const v=max*j/4,y=yp(v);out+=line(58,y,618,y)+text(48,y+4,fmt(v),'lab-svg-small','end');}for(let p=80;p<=160;p+=20)out+=text(xp(p),204,`₹${p}`,'lab-svg-small','middle');
      out+=text(58,16,'MODELLED CONTRIBUTION (₹)','lab-svg-small')+text(618,230,'PRICE (₹)','lab-svg-small','end');out+=`<path d="${samples.map((p,i)=>`${i?'L':'M'}${xp(p.price).toFixed(2)} ${yp(p.value).toFixed(2)}`).join('')}" class="lab-strong-path"/>`;out+=line(xp(price),yp(profit(price)),xp(price),180,'lab-path lab-dashed')+circle(xp(price),yp(profit(price)),7,'lab-accent-fill');
      const best=samples.reduce((a,b)=>a.value>b.value?a:b);const result=`At ₹${price}: modelled demand ${demand(price).toFixed(1)} units; sales ${Math.min(demand(price),stock).toFixed(1)}; contribution ₹${fmt(profit(price))}. On this integer-price grid, the model's best price is ₹${best.price} (₹${fmt(best.value)}). Demand here is deterministic; uncertain demand requires integrating over the stock-capped distribution, not capping its mean.`;
      draw(root,svg(result,out,245),result);
    }bind(root,'[data-price]','input',render);bind(root,'[data-stock]','change',render);render();}
  function retention(root){let policy='risk';const customers=[{id:'A',risk:.92,uplift:.04},{id:'B',risk:.75,uplift:.28},{id:'C',risk:.62,uplift:.22},{id:'D',risk:.84,uplift:.02},{id:'E',risk:.38,uplift:.15},{id:'F',risk:.51,uplift:.08}];
    function render(){const budget=+root.querySelector('[data-budget]').value;const value=c=>c.uplift*180-20;const ranked=[...customers].sort((a,b)=>(policy==='risk'?b.risk-a.risk:value(b)-value(a)));const selected=(policy==='benefit'?ranked.filter(c=>value(c)>0):ranked).slice(0,budget);let out=text(5,18,'CUSTOMER','lab-svg-small')+text(110,18,'CHURN RISK','lab-svg-small')+text(345,18,'INCREMENTAL CONTRIBUTION','lab-svg-small');
      customers.forEach((c,i)=>{let y=43+i*31,chosen=selected.includes(c);out+=circle(13,y,10,chosen?'lab-accent-fill':'lab-soft-fill')+text(13,y+4,c.id,`lab-svg-small${chosen?' lab-on-accent':''}`,'middle');out+=rect(110,y-7,170,14,'lab-soft-fill',2)+rect(110,y-7,c.risk*170,14,chosen?'lab-accent-fill':'lab-muted-fill',2)+text(290,y+4,`${Math.round(c.risk*100)}%`,'lab-svg-small');const zero=400,scale=3.8,val=value(c);out+=line(zero,y-12,zero,y+12)+rect(val<0?zero+val*scale:zero,y-7,Math.abs(val)*scale,14,chosen?'lab-accent-fill':'lab-muted-fill',2)+text(610,y+4,`${val<0?'−':''}₹${Math.abs(val).toFixed(1)}`,'lab-svg-small','end');});
      const total=selected.reduce((s,c)=>s+value(c),0);const result=`${policy==='risk'?'Highest-risk':'Incremental-value'} policy contacts ${selected.map(c=>c.id).join(', ')}. Expected incremental contribution: ${total<0?'−':''}₹${Math.abs(total).toFixed(1)} across ${selected.length} contacts (capacity ${budget}). Contact cost is ₹20; retained contribution is ₹180. These are invented treatment effects, not effects inferred from churn risk.${selected.some(c=>value(c)<0)?' A capacity is a ceiling, not a target: the value policy can leave negative-value contacts unused.':selected.length<budget?' The remaining capacity is unused because the other contacts have negative estimated value.':''}`;
      draw(root,svg(result,out,238),result);
    }bind(root,'[data-policy]','click',b=>{policy=b.dataset.policy;choose(root,'[data-policy]',b);render();});bind(root,'[data-budget]','change',render);render();}
  const implementations={broadcasting,timeline,validation,gradients,retrieval,evaluation,pricing,retention};
  function init(){document.querySelectorAll('.concept-lab[data-lab]').forEach(root=>{if(root.dataset.initialized)return;const implementation=implementations[root.dataset.lab];if(!implementation)return;root.dataset.initialized='true';try{implementation(root);root.classList.add('is-enhanced');}catch(error){console.error('Ground Truth field note could not initialize.',error);}});}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
  document.addEventListener('astro:page-load',init);
})();
