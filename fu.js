/* Shared on all extra pages (articles): falling sakura + Fu the panda with tea wisdoms.
   The home page has its own copy of this code inside index.html. */
(function(){
var LANG='ru'; try{LANG=localStorage.getItem('chami-lang')||'ru';}catch(e){}
var D=window.__FU_D={"ru": {"fuHi": "Привет! Нажми на меня, и я расскажу чайную мудрость.", "fuAsk": "Привет! Я панда Фу. Ты готов услышать мудрость от меня?", "fuYes": "Да, готов!", "fuNo": "В другой раз", "fuBye": "Хорошо! Я буду рядом, когда захочется чаю и мудрости.", "fuMore": "Ещё мудрость", "fuThanks": "Спасибо, Фу!", "fuWait": "Завариваю мудрость…"}, "es": {"fuHi": "¡Hola! Haz clic en mí y te contaré una sabiduría del té.", "fuAsk": "¡Hola! Soy el panda Fu. ¿Estás listo para escuchar una sabiduría?", "fuYes": "¡Sí, listo!", "fuNo": "En otro momento", "fuBye": "¡Vale! Estaré cerca cuando quieras té y sabiduría.", "fuMore": "Otra sabiduría", "fuThanks": "¡Gracias, Fu!", "fuWait": "Preparando la sabiduría…"}, "ky": {"fuHi": "Салам! Мени бас, чай акылмандыгын айтып берем.", "fuAsk": "Салам! Мен панда Фумун. Менден акылман сөз угууга даярсыңбы?", "fuYes": "Ооба, даярмын!", "fuNo": "Башка жолу", "fuBye": "Макул! Чай жана акыл керек болгондо мен жаныңдамын.", "fuMore": "Дагы бир акыл", "fuThanks": "Рахмат, Фу!", "fuWait": "Акылды демдеп жатам…"}, "uz": {"fuHi": "Salom! Meni bos, senga choy hikmatini aytib beraman.", "fuAsk": "Salom! Men panda Fuman. Mendan hikmat eshitishga tayyormisan?", "fuYes": "Ha, tayyorman!", "fuNo": "Boshqa safar", "fuBye": "Yaxshi! Choy va hikmat kerak bo‘lsa, men yoningdaman.", "fuMore": "Yana hikmat", "fuThanks": "Rahmat, Fu!", "fuWait": "Hikmatni damlayapman…"}, "en": {"fuHi": "Hi! Click me and I will share a tea wisdom.", "fuAsk": "Hi! I am Fu the panda. Are you ready to hear a wisdom from me?", "fuYes": "Yes, I’m ready!", "fuNo": "Maybe later", "fuBye": "Okay! I’ll be around whenever you want tea and wisdom.", "fuMore": "Another wisdom", "fuThanks": "Thank you, Fu!", "fuWait": "Brewing a wisdom…"}}; if(!D[LANG]) LANG='ru';
var st=document.createElement('style'); st.textContent="/* global leaves */\n.sky{position:fixed;inset:0;pointer-events:none;z-index:44;overflow:hidden}\n.fall{position:absolute;top:-40px;animation:fall linear infinite}\n.fall svg{display:block;animation:sway ease-in-out infinite alternate}\n@keyframes fall{from{transform:translateY(-6vh)}to{transform:translateY(112vh)}}\n@keyframes sway{from{transform:translateX(-30px) rotate(-40deg)}to{transform:translateX(30px) rotate(60deg)}}\n\n/* Fu the roly-poly */\n.fu{position:fixed;z-index:46;bottom:calc(10px + env(safe-area-inset-bottom,0px));left:0;width:74px;cursor:pointer;border:0;background:none;padding:0;-webkit-tap-highlight-color:transparent}\n.fu svg{display:block;width:100%;height:auto;overflow:visible}\n.fu .body{transform-origin:50% 92%}\n.fu.walking .body{animation:waddle .32s ease-in-out infinite alternate}\n.fu.walking .footL{animation:stepL .32s ease-in-out infinite alternate}\n.fu.walking .footR{animation:stepL .32s ease-in-out infinite alternate-reverse}\n.fu.flip svg{transform:scaleX(-1)}\n.fu.hop .body{animation:hop .7s cubic-bezier(.3,1.6,.5,1)}\n.fu-say{position:absolute;bottom:100%;left:50%;transform:translateX(-50%);margin-bottom:8px;width:max-content;max-width:220px;background:#fbf5e8;color:#2a2118;font:14px/1.35 var(--f-body);padding:8px 12px;border-radius:12px;border:1px solid rgba(163,48,28,.4);box-shadow:0 8px 18px -10px rgba(0,0,0,.5);opacity:0;transition:opacity .3s;pointer-events:none;text-align:left}\n.fu.talk .fu-say{opacity:1}\n.fu-chat{position:fixed;z-index:47;bottom:calc(104px + env(safe-area-inset-bottom,0px));left:12px;width:min(320px,calc(100vw - 24px));background:#fbf5e8;color:#2a2118;border:1px solid rgba(163,48,28,.45);border-radius:14px;box-shadow:0 18px 40px -18px rgba(0,0,0,.6);padding:14px 16px 14px;font:15px/1.45 var(--f-body);opacity:0;transform:translateY(8px);transition:opacity .25s,transform .25s}\n.fu-chat.on{opacity:1;transform:none}\n.fu-chat[hidden]{display:none}\n.fu-chat p{margin:0 0 10px}\n.fu-x{all:unset;cursor:pointer;position:absolute;top:4px;right:8px;font-size:22px;line-height:1;color:#7a6650;padding:4px}\n.fu-zh{font-family:\"KaiTi\",\"STKaiti\",\"Kaiti SC\",\"BiauKai\",\"Noto Serif SC\",\"Noto Serif CJK SC\",\"Songti SC\",serif;font-size:21px;line-height:1.35;color:#a3301c;margin:2px 22px 4px 0}\n.fu-py{font-style:italic;font-size:13px;color:#7a6650;margin-bottom:8px}\n.fu-src{font-size:13px;color:#7a6650;margin-top:-4px}\n.fu-acts{display:flex;flex-wrap:wrap;gap:8px}\n.fu-acts button{all:unset;cursor:pointer;font:700 14px/1 var(--f-body);padding:9px 14px;border-radius:999px;border:1px solid #a3301c;color:#a3301c}\n.fu-acts button.main{background:#a3301c;color:#fbf5e8}\n.fu-acts button:focus-visible{outline:2px solid var(--gold);outline-offset:2px}\n@media (max-width:520px){.fu-chat{bottom:calc(84px + env(safe-area-inset-bottom,0px))}}\n@keyframes waddle{from{transform:rotate(-6deg) translateY(0)}to{transform:rotate(6deg) translateY(-5px)}}\n@keyframes stepL{from{transform:translateY(0)}to{transform:translateY(-4px)}}\n@keyframes hop{0%{transform:translateY(0) rotate(0)}30%{transform:translateY(-34px) rotate(-12deg)}60%{transform:translateY(0) rotate(10deg)}80%{transform:rotate(-6deg)}100%{transform:rotate(0)}}\n@media (max-width:520px){.fu{width:56px}}\n@media (prefers-reduced-motion:reduce){.fu.walking .body{animation-duration:.9s}}\n\n.fu{transition:bottom .3s}\nbody.sticky-on .fu{bottom:calc(84px + env(safe-area-inset-bottom,0px))}\nbody.sticky-on .fu-chat{bottom:calc(178px + env(safe-area-inset-bottom,0px))}\n"; document.head.appendChild(st);
var wrap=document.createElement('div'); wrap.innerHTML="<div class=\"sky\" aria-hidden=\"true\"></div>\n<div class=\"fu-chat\" id=\"fuChat\" role=\"dialog\" aria-label=\"Панда Фу\" aria-live=\"polite\" hidden><button class=\"fu-x\" type=\"button\" aria-label=\"×\">×</button><div class=\"fu-body\"></div><div class=\"fu-acts\"></div></div>\n<button class=\"fu\" id=\"fu\" type=\"button\" aria-label=\"Панда Фу\">\n  <span class=\"fu-say\">Привет! Нажми на меня, и я расскажу чайную мудрость.</span>\n  <svg viewBox=\"0 0 100 120\" aria-hidden=\"true\">\n    <ellipse cx=\"50\" cy=\"116\" rx=\"28\" ry=\"4\" fill=\"#000\" opacity=\".22\"/>\n    <g class=\"footL\"><ellipse cx=\"37\" cy=\"110\" rx=\"10\" ry=\"7\" fill=\"#1b1714\"/></g>\n    <g class=\"footR\"><ellipse cx=\"63\" cy=\"110\" rx=\"10\" ry=\"7\" fill=\"#1b1714\"/></g>\n    <g class=\"body\">\n      <ellipse cx=\"50\" cy=\"84\" rx=\"30\" ry=\"26\" fill=\"#fbf7ef\" stroke=\"#1b1714\" stroke-width=\"1.5\"/>\n      <path d=\"M22 78c-8 6-8 16 0 20 6 2 10-4 10-10\" fill=\"#1b1714\"/>\n      <path d=\"M78 78c8 6 8 16 0 20-6 2-10-4-10-10\" fill=\"#1b1714\"/>\n      <path d=\"M30 66q20 10 40 0l2 6q-22 12-44 0Z\" fill=\"#a3301c\"/>\n      <path d=\"M58 70l8 12-6 1Z\" fill=\"#a3301c\"/>\n      <circle cx=\"26\" cy=\"22\" r=\"10\" fill=\"#1b1714\"/><circle cx=\"74\" cy=\"22\" r=\"10\" fill=\"#1b1714\"/>\n      <ellipse cx=\"50\" cy=\"42\" rx=\"31\" ry=\"27\" fill=\"#fbf7ef\" stroke=\"#1b1714\" stroke-width=\"1.5\"/>\n      <ellipse cx=\"38\" cy=\"42\" rx=\"8\" ry=\"10\" transform=\"rotate(-25 38 42)\" fill=\"#1b1714\"/>\n      <ellipse cx=\"62\" cy=\"42\" rx=\"8\" ry=\"10\" transform=\"rotate(25 62 42)\" fill=\"#1b1714\"/>\n      <circle cx=\"39\" cy=\"41\" r=\"3\" fill=\"#fff\"/><circle cx=\"61\" cy=\"41\" r=\"3\" fill=\"#fff\"/>\n      <circle cx=\"39.6\" cy=\"41.6\" r=\"1.6\" fill=\"#1b1714\"/><circle cx=\"60.4\" cy=\"41.6\" r=\"1.6\" fill=\"#1b1714\"/>\n      <ellipse cx=\"50\" cy=\"52\" rx=\"4\" ry=\"3\" fill=\"#1b1714\"/>\n      <path d=\"M46 57q4 3 8 0\" stroke=\"#1b1714\" stroke-width=\"1.6\" fill=\"none\" stroke-linecap=\"round\"/>\n      <circle cx=\"31\" cy=\"54\" r=\"3.5\" fill=\"#f2a7a0\" opacity=\".7\"/><circle cx=\"69\" cy=\"54\" r=\"3.5\" fill=\"#f2a7a0\" opacity=\".7\"/>\n      <g transform=\"translate(66 86)\"><path d=\"M0 0h16c-1 8-4 11-8 11S1 8 0 0Z\" fill=\"#efe5cf\" stroke=\"#1b1714\" stroke-width=\"1\"/><ellipse cx=\"8\" cy=\"0\" rx=\"8\" ry=\"2\" fill=\"#a5582a\"/></g>\n    </g>\n  </svg>\n</button>";
while(wrap.firstChild) document.body.appendChild(wrap.firstChild);
document.querySelector('#fu .fu-say').textContent=D[LANG].fuHi;
})();
(function(){
var LANG='ru'; try{LANG=localStorage.getItem('chami-lang')||'ru';}catch(e){}
var D=window.__FU_D; if(!D[LANG]) LANG='ru';
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sky=document.querySelector('.sky'), cols=['#f7c6d0','#f4b3c2','#fbdde4','#ef9fb4','#fde8ec'];
  const petal=c=>'<svg viewBox="0 0 20 24" width="100%"><path d="M10 24C3 19 0 12 2 6 4 1 8 0 10 4 12 0 16 1 18 6 20 12 17 19 10 24Z" fill="'+c+'"/><path d="M10 21V9" stroke="rgba(190,90,120,.35)" stroke-width="1"/></svg>';
  const flower=c=>{let g='';for(let k=0;k<5;k++)g+='<path transform="rotate('+(k*72)+')" d="M0 0C-5-4-5-10-2-12L0-10 2-12C5-10 5-4 0 0Z" fill="'+c+'"/>';return '<svg viewBox="-13 -13 26 26" width="100%">'+g+'<circle r="2.6" fill="#f2c94c"/><circle r="1.2" fill="#d9822b"/></svg>';};
  const leaf=c=>Math.random()<.45?flower(c):petal(c);
  function burst(x,y,n){ for(let i=0;i<n;i++){ const el=document.createElement('div'); el.style.cssText='position:fixed;left:'+x+'px;top:'+y+'px;width:14px;pointer-events:none;z-index:47;transition:transform 1.2s cubic-bezier(.2,.7,.3,1),opacity 1.2s'; el.innerHTML=leaf(cols[i%5]); document.body.appendChild(el); const a=Math.random()*Math.PI*2,d=50+Math.random()*70; requestAnimationFrame(()=>{el.style.transform='translate('+Math.cos(a)*d+'px,'+(Math.sin(a)*d-40)+'px) rotate('+(Math.random()*400-200)+'deg)';el.style.opacity='0';}); setTimeout(()=>el.remove(),1300);} }
  if(sky){
    const n = calm ? 6 : (innerWidth<600 ? 8 : 12);
    for(let i=0;i<n;i++){
      const f=document.createElement('div'); f.className='fall';
      const w=10+Math.random()*12;
      f.style.cssText='left:'+(Math.random()*100)+'%;width:'+w+'px;opacity:'+(.65+Math.random()*.3)+';animation-duration:'+((calm?26:16)+Math.random()*16)+'s;animation-delay:-'+(Math.random()*30)+'s';
      f.innerHTML=leaf(cols[i%5]); f.firstChild.style.animationDuration=(2.5+Math.random()*2.5)+'s';
      sky.appendChild(f);
    }
  }
  const fu=document.getElementById('fu'); if(!fu) return;
  let x=40, dir=1, speed=calm?55:80, paused=0, last=performance.now();
  const say=()=>{fu.classList.add('talk'); clearTimeout(fu._t); fu._t=setTimeout(()=>fu.classList.remove('talk'),3200);};
  // ---- wisdom chat: wisdoms.json is refilled weekly ----
  const chat=document.getElementById('fuChat'), cBody=chat.querySelector('.fu-body'), cActs=chat.querySelector('.fu-acts');
  const FALLBACK=[{id:1,zh:'吃茶去',py:'chī chá qù',t:{ru:'«Иди выпей чаю».',en:'“Go and have some tea.”',es:'«Ve a tomar té».',ky:'«Барып чай ич».',uz:'«Borib choy ich».'},s:{ru:'Мастер чань Чжаочжоу',en:'Chan master Zhaozhou',es:'maestro chan Zhaozhou',ky:'Чань устаты Чжаочжоу',uz:'Chan ustozi Zhaozhou'}}];
  let W=null, deck=[], state='', cur=null;
  const L=()=>D[LANG]||D.ru, lc=()=>LANG;
  const loadW=()=>W?Promise.resolve(W):fetch('/wisdoms.json',{cache:'no-cache'}).then(r=>r.ok?r.json():Promise.reject()).then(j=>W=(j.items&&j.items.length?j.items:FALLBACK)).catch(()=>W=FALLBACK);
  const seenGet=()=>{try{return JSON.parse(localStorage.getItem('chami-wisdom-seen')||'[]')}catch(e){return[]}};
  const seenAdd=id=>{try{const a=seenGet(); if(!a.includes(id)){a.push(id); localStorage.setItem('chami-wisdom-seen',JSON.stringify(a));}}catch(e){}};
  const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  function nextW(){
    if(!deck.length){ const seen=seenGet(); let fresh=W.filter(w=>!seen.includes(w.id)); if(!fresh.length){ try{localStorage.removeItem('chami-wisdom-seen')}catch(e){} fresh=W.slice(); }
      deck=shuffle(fresh); if(cur&&deck.length>1&&deck[deck.length-1].id===cur.id) deck.unshift(deck.pop()); }
    cur=deck.pop(); seenAdd(cur.id); return cur;
  }
  const btn=(k,fn,main)=>{const b=document.createElement('button'); b.type='button'; b.textContent=L()[k]; if(main) b.className='main'; b.onclick=fn; cActs.appendChild(b); return b;};
  const esc=x=>String(x).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function render(){
    const d=L(); cActs.innerHTML='';
    if(state==='ask'){ cBody.innerHTML='<p>'+esc(d.fuAsk)+'</p>'; btn('fuYes',showW,1).focus({preventScroll:true}); btn('fuNo',bye); }
    else if(state==='wait'){ cBody.innerHTML='<p>'+esc(d.fuWait)+'</p>'; }
    else if(state==='w'&&cur){ const l=lc(); cBody.innerHTML='<div class="fu-zh" lang="zh">'+esc(cur.zh)+'</div>'+(cur.py?'<div class="fu-py">'+esc(cur.py)+'</div>':'')+'<p>'+esc(cur.t[l]||cur.t.ru)+'</p><p class="fu-src">— '+esc((cur.s&&(cur.s[l]||cur.s.ru))||'')+'</p>'; btn('fuMore',showW,1); btn('fuThanks',closeChat); }
    else if(state==='bye'){ cBody.innerHTML='<p>'+esc(d.fuBye)+'</p>'; }
  }
  window.fuRender=()=>{ if(!chat.hidden) render(); };
  function openChat(){ state='ask'; chat.hidden=false; render(); requestAnimationFrame(()=>chat.classList.add('on')); fu.classList.remove('talk'); loadW(); }
  function closeChat(){ chat.classList.remove('on'); state=''; setTimeout(()=>{ if(!state) chat.hidden=true; },260); paused=.6; }
  function bye(){ state='bye'; render(); setTimeout(()=>{ if(state==='bye') closeChat(); },2600); }
  function showW(){ if(!W){ state='wait'; render(); } loadW().then(()=>{ nextW(); state='w'; render(); }); }
  chat.querySelector('.fu-x').onclick=closeChat;
  document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&!chat.hidden) closeChat(); });
  fu.addEventListener('click',()=>{ fu.classList.remove('hop'); void fu.offsetWidth; fu.classList.add('hop'); const r=fu.getBoundingClientRect(); burst(r.left+r.width/2,r.top+10,14); if(chat.hidden||!state) openChat(); else if(state!=='w') showW(); paused=1.4; });
  setTimeout(say,2500);
  function step(t){
    const dt=Math.min(.05,(t-last)/1000); last=t;
    const max=document.documentElement.clientWidth-fu.offsetWidth-8;
    if(state&&!chat.hidden){ paused=Math.max(paused,.3); }
    if(paused>0){ paused-=dt; fu.classList.remove('walking'); }
    else{
      fu.classList.add('walking'); x+=dir*speed*dt;
      if(x>max){x=max;dir=-1;paused=1.2;} if(x<8){x=8;dir=1;paused=1.2;}
      if(Math.random()<.0015){paused=.8+Math.random()*1.5;}
    }
    fu.classList.toggle('flip',dir<0);
    fu.style.transform='translateX('+x+'px)';
    if(!chat.hidden){ const vw=document.documentElement.clientWidth, cw=chat.offsetWidth; chat.style.left=Math.max(12,Math.min(vw-cw-12,x+fu.offsetWidth/2-cw/2))+'px'; }
    requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
})();
