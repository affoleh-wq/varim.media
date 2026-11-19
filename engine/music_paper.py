"""Спокойный lo-fi бит 90 BPM для газетного формата (12.2 с) + SFX: перелистывание, штамп, печатная машинка."""
import numpy as np, os
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
SR=44100; BPM=90; B=60/BPM; DUR=12.2; N=int(SR*DUR); rng=np.random.default_rng(5)
CUTS=[3.2,6.4,9.6]; STAMP=3.2+1.75; STRIKE=6.4+.75; SLAM1=.95
def f(x,k,fr,o=2): return sosfilt(butter(o,fr,k,fs=SR,output="sos"),x)
def add(b,t,s,g=1.):
    i=int(round(t*SR))
    if 0<=i<len(b): s=s[:len(b)-i]; b[i:i+len(s)]+=s*g
def kick():
    t=np.arange(int(.35*SR))/SR; fr=45+90*np.exp(-t/.03)
    return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t/.16)
def snare():
    n=int(.25*SR); t=np.arange(n)/SR
    return f(rng.standard_normal(n),"band",[900,5000])*np.exp(-t/.06)*.7+np.sin(2*np.pi*190*t)*np.exp(-t/.04)*.5
def hat():
    n=int(.06*SR); t=np.arange(n)/SR
    return f(rng.standard_normal(n),"high",7000)*np.exp(-t/.015)
def keys(freqs,dur):
    n=int(dur*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for fr in freqs:
        x+=np.sin(2*np.pi*fr*t)+.3*np.sin(4*np.pi*fr*t)*np.exp(-t/.4)
    return x*(1+.15*np.sin(2*np.pi*4.5*t))*np.minimum(t/.02,1)*np.exp(-t/2.2)/len(freqs)
mus=np.zeros(N); drums=np.zeros(N)
m=lambda n:440*2**((n-69)/12)
prog=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]   # Am9-ish, Fmaj7, Cmaj7, G7
bar=4*B
for i in range(int(DUR/bar)+1):
    ch=prog[i%4]; add(mus,i*bar,keys([m(n) for n in ch],bar+.3),.5)
    add(mus,i*bar,keys([m(ch[0]-24)],bar),.7)
beats=int(DUR/B)+1
for k in range(beats):
    t=k*B; sw=.06 if k%2 else 0
    if k%4 in (0,) or (k%4==2 and k%8==6): add(drums,t,kick(),.9)
    if k%4 in (1,3): add(drums,t,snare(),.45)
    add(drums,t,hat(),.18); add(drums,t+B/2+B*.08,hat(),.12)
mus=f(mus,"low",2200)
crack=np.zeros(N); idx=rng.integers(0,N,900); crack[idx]=rng.standard_normal(900)*.5
crack=f(crack,"band",[1500,8000])+f(rng.standard_normal(N),"band",[300,3000])*.01
sfx=np.zeros(N)
def page():
    n=int(.4*SR); t=np.arange(n)/SR; sweep=np.sin(np.pi*np.minimum(t/.4,1))**2
    return f(rng.standard_normal(n),"band",[600,6000])*sweep*.55
def thud(g=1):
    n=int(.35*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*(60+80*np.exp(-t/.02))*t)*np.exp(-t/.09)+f(rng.standard_normal(n),"band",[200,2500])*np.exp(-t/.03)*.6)*g
def type_(t0,k):
    for j in range(k):
        n=int(.05*SR); t=np.arange(n)/SR
        add(sfx,t0+j*.075+rng.uniform(0,.02),f(rng.standard_normal(n),"band",[1500,7000])*np.exp(-t/.008)*.35)
for c in CUTS: add(sfx,c-.38,page())
add(sfx,STAMP,thud(1.3)); add(sfx,SLAM1,thud(.8)); add(sfx,STRIKE,page()[:int(.2*SR)]*1.2)
type_(.0,6); type_(1.6,7); type_(9.7,6)
out=mus*.55+drums*.6+crack*.25+sfx*.9
fade=np.ones(N); fl=int(.6*SR); fade[-fl:]=np.linspace(1,0,fl); out*=fade
out=out/np.max(np.abs(out))*.89
wavfile.write(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sound_paper.wav"),SR,(np.stack([out,out],1)*32767).astype(np.int16))
print("ok")
