#!/usr/bin/env python3
"""Reusable 1080x1920 info/number cards (PIL, Noto Sans CJK Bold).
usage as lib:  from cards import card; card('out.png','举个例子',[('套餐流量',80),('100G',230)],foot='*数字为举例')
usage as CLI:  cards.py spec.json   spec: [{"out":"C1.png","tag":"..","lines":[["text",size],...],"foot":"..","theme":"yellow"}]
Lines auto-shrink to fit safe width 920px. Themes: yellow, dark, paper."""
import json,sys,os
from PIL import Image,ImageDraw,ImageFont
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
if not os.path.exists(B):B="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
F=lambda s:ImageFont.truetype(B,s,index=2)
W,H,SAFE=1080,1920,920
THEMES={'yellow':((255,214,0),(0,0,0),(60,60,60)),'dark':((18,18,22),(255,214,0),(170,170,170)),'paper':((236,226,204),(60,30,20),(110,90,70))}
def card(out,tag,lines,foot='',theme='yellow',top=420):
    bg,fg,mut=THEMES[theme];im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
    if tag:
        tf=F(70);tw=d.textlength(tag,font=tf);d.rectangle([60,180,60+tw+60,300],fill=fg);d.text((90,190),tag,font=tf,fill=bg)
    y=top
    for txt,size in lines:
        while size>30 and d.textlength(txt,font=F(size))>SAFE:size-=4
        f=F(size);w=d.textlength(txt,font=f);d.text(((W-w)/2,y),txt,font=f,fill=fg);y+=int(size*1.35)
    if y>1250:print(f"warning {out}: content reaches y={y}, enters subtitle zone (1250-1540)",file=sys.stderr)
    if foot:
        f=F(40);w=d.textlength(foot,font=f);d.text(((W-w)/2,1620),foot,font=f,fill=mut)
    im.save(out);return out
if __name__=='__main__':
    for c in json.load(open(sys.argv[1])):card(c['out'],c.get('tag',''),c['lines'],c.get('foot',''),c.get('theme','yellow'))
