/* Seasons for the whole site: what falls from the sky and how Fu the panda is dressed.
   Season comes from the current month; ?season=winter|spring|summer|autumn overrides it (for previews). */
(function(){
  var m=new Date().getMonth();
  var q=(location.search.match(/[?&]season=(winter|spring|summer|autumn)/)||[])[1];
  var S=q||(m===11||m<2?'winter':m<5?'spring':m<8?'summer':'autumn');
  window.chamiSeason=S;
  document.documentElement.classList.add('season-'+S);

  var maple=function(c){return '<svg viewBox="-12 -12 24 26" width="100%"><path d="M0-11 2-6 6-8 5-3 10-4 7 0 9 2 4 3 5 7 1 4 0 9-1 4-5 7-4 3-9 2-7 0-10-4-5-3-6-8-2-6Z" fill="'+c+'"/><path d="M0 3V13" stroke="'+c+'" stroke-width="1.2"/><path d="M0 8V-6M0 1 5-2M0 1-5-2" stroke="rgba(0,0,0,.18)" stroke-width=".7" fill="none"/></svg>';};
  var flake=function(c){var g='';for(var k=0;k<6;k++)g+='<g transform="rotate('+(k*60)+')"><path d="M0 0V-10M0-6 3-9M0-6-3-9M0-3 2-5M0-3-2-5"/></g>';return '<svg viewBox="-12 -12 24 24" width="100%"><g stroke="'+c+'" stroke-width="1.6" stroke-linecap="round" fill="none" style="filter:drop-shadow(0 0 1px rgba(80,120,170,.55))">'+g+'</g></svg>';};
  var tealeaf=function(c){return '<svg viewBox="0 0 20 30" width="100%"><path d="M10 1C17 7 19 16 14 24 12 27 10 29 10 29S8 27 6 24C1 16 3 7 10 1Z" fill="'+c+'"/><path d="M10 4V28M10 12 14 9M10 17 6 13M10 21 14 18" stroke="rgba(255,255,255,.4)" stroke-width=".8" fill="none"/></svg>';};

  if(S==='autumn'){ window.chamiCols=['#c0392b','#e67e22','#f1c40f','#d35400','#a0522d','#b8860b']; window.chamiLeaf=maple; }
  else if(S==='winter'){ window.chamiCols=['#ffffff','#eaf3fc','#d6e8f8','#ffffff','#e3eefa']; window.chamiLeaf=flake; }
  else if(S==='summer'){ window.chamiCols=['#6f9a4a','#8db55c','#557f3c','#a6c46b','#7aa653']; window.chamiLeaf=tealeaf; }
  /* spring: the default sakura petals and blossoms stay */

  var NS='http://www.w3.org/2000/svg';
  function add(parent,markup,first){
    var g=document.createElementNS(NS,'g'); g.setAttribute('class','season-acc'); g.innerHTML=markup;
    if(first) parent.insertBefore(g,parent.firstChild); else parent.appendChild(g); return g;
  }
  function dress(){
    if(window.chamiLeaf){ var st=document.querySelectorAll('.hero svg.leaf'); for(var j=0;j<st.length;j++){ var d=document.createElement('div'); d.className='leaf'; d.setAttribute('aria-hidden','true'); d.style.cssText=st[j].style.cssText; if(!d.style.width) d.style.width='20px'; d.innerHTML=window.chamiLeaf(window.chamiCols[j%window.chamiCols.length]); st[j].replaceWith(d); } }
    var fu=document.getElementById('fu'); if(!fu||fu.dataset.dressed) return; fu.dataset.dressed='1';
    var svg=fu.querySelector('svg'), body=svg&&svg.querySelector('.body'); if(!body) return;
    var feet=svg.querySelectorAll('.footL ellipse,.footR ellipse');
    if(S==='autumn'){
      /* yellow rubber boots and a red umbrella */
      for(var i=0;i<feet.length;i++){ feet[i].setAttribute('fill','#e9b31c'); feet[i].setAttribute('stroke','#1b1714'); feet[i].setAttribute('stroke-width','1.2'); }
      add(svg.querySelector('.footL'),'<rect x="29" y="101" width="16" height="6" rx="2" fill="#e9b31c" stroke="#1b1714" stroke-width="1"/>');
      add(svg.querySelector('.footR'),'<rect x="55" y="101" width="16" height="6" rx="2" fill="#e9b31c" stroke="#1b1714" stroke-width="1"/>');
      add(body,'<g class="umb"><path d="M19 -6 15 92q-1 6 4 6" stroke="#5a3a22" stroke-width="2.4" fill="none" stroke-linecap="round"/><path d="M-22 4Q19 -40 60 4Q50-3 40 4Q30-3 19 4Q9-3-1 4Q-11-3-22 4Z" fill="#a3301c" stroke="#1b1714" stroke-width="1.2"/><path d="M19-17Q9-8 -1 4M19-17Q29-8 40 4" stroke="rgba(0,0,0,.25)" stroke-width="1" fill="none"/><circle cx="19" cy="-18" r="2.2" fill="#1b1714"/></g>',true);
    } else if(S==='winter'){
      /* knitted hat with pompom, skis and poles instead of the cup */
      var cup=body.querySelector('g[transform^="translate(66"]'); if(cup) cup.style.display='none';
      add(svg,'<g class="skis"><path d="M2 117H90q8 0 10-6" stroke="#1d5f8c" stroke-width="3.4" fill="none" stroke-linecap="round"/><path d="M8 120H94q6 0 8-5" stroke="#2a78ad" stroke-width="3.4" fill="none" stroke-linecap="round"/></g>');
      add(body,'<path d="M24 92 8 118M76 92 92 118" stroke="#6b4a2b" stroke-width="2" stroke-linecap="round"/><circle cx="10" cy="115" r="2.4" fill="none" stroke="#6b4a2b" stroke-width="1.4"/><circle cx="90" cy="115" r="2.4" fill="none" stroke="#6b4a2b" stroke-width="1.4"/>');
      add(body,'<path d="M20 30Q22 6 50 5Q78 6 80 30Z" fill="#a3301c" stroke="#1b1714" stroke-width="1.2"/><path d="M19 27h62v7H19Z" fill="#f4ead8" stroke="#1b1714" stroke-width="1"/><path d="M30 14v12M40 9v17M50 8v18M60 9v17M70 14v12" stroke="rgba(255,255,255,.25)" stroke-width="2"/><circle cx="50" cy="4" r="6" fill="#f4ead8" stroke="#1b1714" stroke-width="1"/><path d="M30 66q20 10 40 0l1 4q-21 11-42 0Z" fill="#f4ead8" opacity=".9"/>');
    } else if(S==='spring'){
      /* flower wreath and a small butterfly */
      var w='', xs=[30,38,46,54,62,70], ys=[19,15,13,13,15,19], cs=['#f4b3c2','#fde8ec','#ef9fb4','#f7c6d0','#fde8ec','#f4b3c2'];
      w+='<path d="M27 21Q50 6 73 21" stroke="#6f9a4a" stroke-width="2" fill="none"/>';
      for(var k=0;k<6;k++){ for(var p=0;p<5;p++) w+='<ellipse cx="'+xs[k]+'" cy="'+(ys[k]-3)+'" rx="2.2" ry="3.2" fill="'+cs[k]+'" transform="rotate('+(p*72)+' '+xs[k]+' '+ys[k]+')"/>'; w+='<circle cx="'+xs[k]+'" cy="'+ys[k]+'" r="1.6" fill="#f2c94c"/>'; }
      add(body,w);
      add(svg,'<g class="bfly"><path d="M86 18q-8-8-9 1 1 6 9 1Zm0 0q8-8 9 1-1 6-9 1Z" fill="#f2a541" stroke="#1b1714" stroke-width=".7"/><path d="M86 15v8" stroke="#1b1714" stroke-width="1.2"/></g>');
    } else if(S==='summer'){
      /* sunglasses and a straw panama */
      add(body,'<rect x="27" y="35" width="21" height="14" rx="6" fill="#1b1714"/><rect x="52" y="35" width="21" height="14" rx="6" fill="#1b1714"/><path d="M48 40q2-2 4 0" stroke="#1b1714" stroke-width="2" fill="none"/><path d="M31 39l5-2M56 39l5-2" stroke="rgba(255,255,255,.55)" stroke-width="1.6" stroke-linecap="round"/><path d="M27 40 20 38M73 40 80 38" stroke="#1b1714" stroke-width="1.6"/>');
      add(body,'<ellipse cx="50" cy="19" rx="40" ry="7" fill="#e3c27a" stroke="#1b1714" stroke-width="1.1"/><path d="M28 18Q30 0 50 0T72 18Z" fill="#ecd08f" stroke="#1b1714" stroke-width="1.1"/><path d="M29 14Q50 20 71 14l1 4Q50 24 28 18Z" fill="#a3301c"/>');
    }
  }
  var css=document.createElement('style');
  css.textContent='.season-winter .fu.walking .footL,.season-winter .fu.walking .footR{animation:none}.season-winter .fu.walking .body{animation-duration:.8s}'+
    '.fu .bfly{animation:bfly 1.6s ease-in-out infinite alternate;transform-origin:86px 18px}@keyframes bfly{from{transform:translate(0,0) scaleX(1)}to{transform:translate(-6px,-8px) scaleX(.6)}}'+
    '.fu .umb{transform-origin:17px 92px;animation:umb 2.4s ease-in-out infinite alternate}@keyframes umb{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}'+
    '@media (prefers-reduced-motion:reduce){.fu .bfly,.fu .umb{animation:none}}';
  (document.head||document.documentElement).appendChild(css);
  window.chamiDress=dress;
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',dress); else dress();
})();
