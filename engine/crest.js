// VARiM crest v2: our own badge in the club's kit colours (no real club crests).
// crest({col, c2, pat, code, id, font}) -> SVG string, viewBox 0 0 200 236.
// pat: plain | stripes | hoops | halves | band | sash   (D.kit[side] = {pat, c2})
const crest=(o)=>{
  const col=o.col||'#2a2a33', c2=o.c2||'#ffffff', pat=o.pat||'plain', code=o.code||'', id=o.id||'x', font=o.font||'BS';
  const lum=c=>{const n=parseInt(c.slice(1),16);return (.299*(n>>16)+.587*(n>>8&255)+.114*(n&255))/255};
  const S='M100 4 L192 30 V112 C192 170 152 210 100 232 C48 210 8 170 8 112 V30 Z';
  const I='M100 17 L180 39 V112 C180 163 145 199 100 219 C55 199 20 163 20 112 V39 Z';
  let p='';
  if(pat=='stripes'){for(let i=0;i<7;i++)if(i%2)p+=`<rect x="${20+i*160/7}" y="0" width="${160/7+.5}" height="236" fill="${c2}"/>`}
  else if(pat=='hoops'){for(let i=0;i<9;i++)if(i%2)p+=`<rect x="0" y="${17+i*202/9}" width="200" height="${202/9+.5}" fill="${c2}"/>`}
  else if(pat=='halves'){p=`<rect x="100" y="0" width="100" height="236" fill="${c2}"/>`}
  else if(pat=='band'){p=`<rect x="76" y="0" width="48" height="236" fill="${c2}"/><rect x="70" y="0" width="6" height="236" fill="#fff"/><rect x="124" y="0" width="6" height="236" fill="#fff"/>`}
  else if(pat=='sash'){p=`<path d="M10 60 L60 10 L200 150 L150 200 Z" fill="${c2}"/>`}
  const trim=pat=='plain'?c2:'#ffffff', lt=lum(col)>.62, ring=lt?c2:col;
  return `<svg class="shield crest2" viewBox="0 0 200 236" xmlns="http://www.w3.org/2000/svg"><defs>
<linearGradient id="rim${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#c9ced6"/><stop offset=".55" stop-color="#eef1f5"/><stop offset="1" stop-color="#8d939c"/></linearGradient>
<linearGradient id="gl${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".38"/><stop offset=".42" stop-color="#fff" stop-opacity=".06"/><stop offset=".43" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
<radialGradient id="md${id}" cx=".5" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e4e7ec"/></radialGradient>
<clipPath id="cp${id}"><path d="${I}"/></clipPath></defs>
<path d="${S}" fill="url(#rim${id})"/>
<path d="${S}" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="2"/>
<g clip-path="url(#cp${id})"><rect width="200" height="236" fill="${col}"/>${p}<rect width="200" height="236" fill="url(#gl${id})"/></g>
<path d="${I}" fill="none" stroke="${trim}" stroke-width="5" stroke-opacity=".9"/>
<path d="M100 29 L170 48" stroke="#fff" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/>
<circle cx="100" cy="123" r="57" fill="rgba(0,0,0,.28)"/>
<circle cx="100" cy="118" r="57" fill="${lt?'#161a22':`url(#md${id})`}"/>
<circle cx="100" cy="118" r="51" fill="none" stroke="${ring}" stroke-width="5"/>
<circle cx="100" cy="118" r="44.5" fill="none" stroke="${ring}" stroke-opacity=".35" stroke-width="1.5"/>
<text x="100" y="${code.length>3?131:134}" text-anchor="middle" font-family="${font}" font-weight="700" font-size="${code.length>3?32:42}" textLength="${code.length>3?70:Math.min(66,code.length*22)}" lengthAdjust="spacingAndGlyphs" fill="${lt?'#ffffff':col}" letter-spacing="1">${code}</text>
</svg>`};
// Kit patterns by team code (c2 = second kit colour). D.kit[side]={pat,c2} overrides.
const KITS={SCP:['hoops','#ffffff'],CEL:['hoops','#ffffff'],QPR:['hoops','#ffffff'],
 BRU:['stripes','#111111'],INT:['stripes','#111111'],MIL:['stripes','#111111'],JUV:['stripes','#ffffff'],ATM:['stripes','#ffffff'],
 NEW:['stripes','#ffffff'],PSV:['stripes','#ffffff'],BAR:['stripes','#a50044'],ATH:['stripes','#ffffff'],SUN:['stripes','#ffffff'],
 STK:['stripes','#ffffff'],BRE:['stripes','#ffffff'],CRY:['stripes','#c4122e'],BHA:['stripes','#ffffff'],SPM:['stripes','#ffffff'],
 PSG:['band','#da291c'],AJA:['band','#d2122e'],FEY:['halves','#ffffff'],BLA:['halves','#ffffff'],
 RMA:['plain','#febe10'],ROM:['plain','#f0bc42'],MUN:['plain','#111111'],LIV:['plain','#ffffff'],ARS:['plain','#ffffff'],
 BVB:['plain','#111111'],BAY:['plain','#ffffff'],MCI:['plain','#ffffff'],CHE:['plain','#ffffff'],TOT:['plain','#132257'],
 AVL:['plain','#95bfe5'],NAP:['plain','#ffffff'],GAL:['halves','#fdb912'],FEN:['stripes','#163962'],BEN:['plain','#ffffff'],POR:['stripes','#ffffff']};
const crestFor=(side,code,col,id,font)=>{const k=(typeof D!='undefined'&&D.kit&&D.kit[side])||null,d=KITS[code]||['plain','#ffffff'];
  let pat=(k&&k.pat)||d[0],c2=(k&&k.c2)||d[1];if(c2.toLowerCase()==String(col).toLowerCase())c2=col.toLowerCase()=='#ffffff'?'#111111':'#ffffff';
  return crest({col,c2,pat,code,id,font})};
