const LOGO='__LOGO__';
const FLAGS={
 Germany:['0 0 3 2','<rect width="3" height="2" fill="#111"/><rect y=".667" width="3" height=".667" fill="#d00"/><rect y="1.333" width="3" height=".667" fill="#ffce00"/>'],
 Netherlands:['0 0 3 2','<rect width="3" height="2" fill="#ae1c28"/><rect y=".667" width="3" height=".667" fill="#fff"/><rect y="1.333" width="3" height=".667" fill="#21468b"/>'],
 Switzerland:['0 0 3 2','<rect width="3" height="2" fill="#da291c"/><rect x="1.3" y=".4" width=".4" height="1.2" fill="#fff"/><rect x=".9" y=".8" width="1.2" height=".4" fill="#fff"/>'],
 Scotland:['0 0 3 2','<rect width="3" height="2" fill="#005eb8"/><path d="M0 0L3 2M3 0L0 2" stroke="#fff" stroke-width=".36"/>'],
 Denmark:['0 0 37 28','<rect width="37" height="28" fill="#c8102e"/><rect x="12" width="4" height="28" fill="#fff"/><rect y="12" width="37" height="4" fill="#fff"/>'],
 Norway:['0 0 22 16','<rect width="22" height="16" fill="#ba0c2f"/><rect x="6" width="4" height="16" fill="#fff"/><rect y="6" width="22" height="4" fill="#fff"/><rect x="7" width="2" height="16" fill="#00205b"/><rect y="7" width="22" height="2" fill="#00205b"/>'],
 Poland:['0 0 8 5','<rect width="8" height="5" fill="#fff"/><rect y="2.5" width="8" height="2.5" fill="#dc143c"/>'],
 Sweden:['0 0 16 10','<rect width="16" height="10" fill="#006aa7"/><rect x="5" width="2" height="10" fill="#fecc02"/><rect y="4" width="16" height="2" fill="#fecc02"/>']
};
// клуб без флага: щит с кодом команды в её цветах (D.codes/D.code + D.colors), без серых квадратов
const _side=t=>typeof D=='undefined'?null:t==D.home?'home':t==D.away?'away':null;
const _crest=t=>{const s=_side(t),cd=(typeof D!='undefined'&&(D.codes||D.code))||{},cl=(typeof D!='undefined'&&D.colors)||{};
  const code=(s&&cd[s])||t.replace(/[^A-Za-z]/g,'').slice(0,3).toUpperCase(),c=(s&&cl[s])||'#2a2a33';
  const lum=parseInt(c.slice(1,3),16)*.299+parseInt(c.slice(3,5),16)*.587+parseInt(c.slice(5,7),16)*.114,ink=lum>150?'#111':'#fff';
  return `<svg viewBox="0 0 100 116" preserveAspectRatio="xMidYMid meet"><path d="M50 3 L95 15 V58 C95 86 74 104 50 113 C26 104 5 86 5 58 V15 Z" fill="${c}" stroke="rgba(255,255,255,.55)" stroke-width="4"/><text x="50" y="66" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-weight="900" font-size="${code.length>3?24:30}" fill="${ink}" letter-spacing="1">${code}</text></svg>`};
const flag=(t,cls='',st='')=>{const f=FLAGS[t];if(!f)return `<div class="flag crest ${cls}" style="${st}">${_crest(t)}</div>`;return `<div class="flag ${cls}" style="${st}"><svg viewBox="${f[0]}" preserveAspectRatio="xMidYMid slice">${f[1]}</svg></div>`};
const pills=(f,d0)=>f.map((r,i)=>`<b class="${r=='W'?'w':r=='L'?'l':''} flip" style="--d:${(d0+i*.08).toFixed(2)}s">${r}</b>`).join('');
const split=s=>{let i=0;return s.split(' ').map(w=>`<span style="white-space:nowrap;display:inline-block">${[...w].map(c=>`<span class="ch" style="--i:${i++}">${c}</span>`).join('')}</span>`).join(' ')};
function ENGINE(o){
  o=Object.assign({chip:'Model prediction',ticker:[],light:false,lastHeader:false},o);
  if(o.light)document.body.classList.add('light');
  document.documentElement.style.setProperty('--logo',`url(${LOGO})`);
  let seed=7;const rnd=()=>(seed=(seed*16807)%2147483647)/2147483647;
  const dots=Array.from({length:18},()=>{const s=4+rnd()*6|0;return `<i class="dot" style="left:${rnd()*100}%;width:${s}px;height:${s}px;--o:${(.1+rnd()*.25).toFixed(2)};animation-duration:${(7+rnd()*8).toFixed(1)}s;animation-delay:calc(-${(rnd()*15).toFixed(1)}s - var(--t0))"></i>`}).join('');
  const tk=o.ticker.map(t=>`<span>${t}</span>`).join('');
  document.querySelectorAll('.scene').forEach((s,i,all)=>{
    const last=i==all.length-1, w=i==0?'o':last?'i':'io';
    s.insertAdjacentHTML('afterbegin',`<div class="fx"><div class="glow"></div><div class="grid"></div><div class="ring b"></div><div class="ring"></div>${dots}<div class="vig"></div></div>`);
    let hd='';
    if(!last||o.lastHeader){hd=(o.light?'<div class="navbar"></div>':'')+`<div class="top"><img data-logo><div class="chip">${o.chip}</div></div>`;
      if(tk&&!last)hd+=`<div class="tick"><div class="tr">${tk.repeat(8)}</div></div>`;}
    s.insertAdjacentHTML('beforeend',hd+`<div class="wipe k ${w}"></div><div class="wipe ${w}"></div>`);
  });
  document.querySelectorAll('[data-logo]').forEach(i=>i.src=LOGO);
  document.querySelectorAll('[data-split]').forEach(e=>{e.innerHTML=split(e.textContent)});
  document.getElementById(location.hash.slice(1)||'s1').classList.add('on');
  window.seek=t=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})};
}
// подгоняет размер шрифта, чтобы текст влез в одну строку
const fit=(sel,min=36)=>document.querySelectorAll(sel).forEach(e=>{let s=parseFloat(getComputedStyle(e).fontSize);while(e.scrollWidth>e.clientWidth&&s>min){s-=2;e.style.fontSize=s+'px'}});
