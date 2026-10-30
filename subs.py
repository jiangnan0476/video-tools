#!/usr/bin/env python3
"""Generate 1080x1920 ASS subtitles.
usage: subs.py script.json timeline.json out.ass [--font-size 72] [--safe 900]
script.json : [[id, text], ...]   timeline.json : [[id, start_s, end_s], ...]
Rules: split at punctuation; a clause shorter than MIN chars merges with the NEXT clause
of the same sentence only (never across 。！？); lines wrapped by measured pixel width
(<= safe width); max 2 lines per event, otherwise split into more events.
Time inside a segment is distributed proportional to character count."""
import json,re,sys,argparse
from PIL import ImageFont
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
ap=argparse.ArgumentParser();ap.add_argument('script');ap.add_argument('timeline');ap.add_argument('out')
ap.add_argument('--font-size',type=int,default=72);ap.add_argument('--safe',type=int,default=900)
ap.add_argument('--min',type=int,default=5);ap.add_argument('--max-lines',type=int,default=2)
a=ap.parse_args()
f=ImageFont.truetype(FONT,a.font_size,index=2)
W=lambda s:f.getlength(s)
def clauses(text):
    out=[]
    for sent in re.findall(r'[^。！？!?]+[。！？!?]?',text):
        parts=[p.strip() for p in re.split(r'[，、：；,:;“”"。！？!?]',sent) if p.strip()]
        cur=[]
        for p in parts:
            if cur and len(cur[-1])<a.min: cur[-1]+=' '+p   # short clause joins next one (same sentence)
            else: cur.append(p)
        if len(cur)>1 and len(cur[-1])<a.min-2: t=cur.pop();cur[-1]+=' '+t  # tiny tail joins previous (same sentence)
        out+=cur
    return out
def wrap(c):
    if W(c)<=a.safe: return [c]
    sp=[i for i,ch in enumerate(c) if ch==' ']   # prefer breaking at a clause boundary
    best=min(sp,key=lambda i:abs(W(c[:i])-W(c[i+1:])),default=None)
    if best is not None and W(c[:best])<=a.safe and W(c[best+1:])<=a.safe: return [c[:best],c[best+1:]]
    n=1
    while True:
        n+=1;k=-(-len(c)//n)   # balanced lines, break preferably at a space
        L=[];r=c
        while r:
            cut=min(k,len(r));sp=r.rfind(' ',max(1,cut-3),cut+3)
            if len(r)>cut and sp>0: cut=sp
            L.append(r[:cut].strip());r=r[cut:].strip()
        if all(W(l)<=a.safe for l in L): return L
def ts(x):return f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
sc=dict(json.load(open(a.script)));ev=[]
for sid,st,en in json.load(open(a.timeline)):
    chunks=[]
    for c in clauses(sc[sid]):
        L=wrap(c)
        for i in range(0,len(L),a.max_lines): chunks.append(L[i:i+a.max_lines])
    tot=sum(len(''.join(c)) for c in chunks);x=st
    for c in chunks:
        y=x+(en-st)*len(''.join(c))/tot
        ev.append(f'Dialogue: 0,{ts(x)},{ts(y)},D,,0,0,0,,'+r'\N'.join(c));x=y
open(a.out,'w').write(f'''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: D,Noto Sans CJK SC,{a.font_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,6,0,2,90,90,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''+'\n'.join(ev)+'\n')
print(f'{len(ev)} events -> {a.out}')
