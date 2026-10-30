#!/usr/bin/env python3
"""Cover/title template for 华夏辉煌历史.
usage: cover.py bg.png out.png "主标题" "副标题" [--series 华夏辉煌历史] [--no 01]
Darkens bottom, draws series tag, big gold title (auto-shrink to 920px), subtitle."""
import argparse
from PIL import Image,ImageDraw,ImageFont,ImageOps
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc";F=lambda s:ImageFont.truetype(B,s,index=2)
GOLD=(232,190,110);W,H=1080,1920
ap=argparse.ArgumentParser();ap.add_argument('bg');ap.add_argument('out');ap.add_argument('title');ap.add_argument('sub')
ap.add_argument('--series',default='华夏辉煌历史');ap.add_argument('--no',default='')
a=ap.parse_args()
im=ImageOps.fit(Image.open(a.bg).convert('RGB'),(W,H))
g=Image.linear_gradient('L').resize((W,H));ov=Image.new('RGB',(W,H),(10,10,14))
im=Image.composite(ov,im,g.point(lambda v:int(max(0,v-90)*1.4)))
d=ImageDraw.Draw(im)
tag=a.series+(f' · {a.no}' if a.no else '');tf=F(54);tw=d.textlength(tag,font=tf)
d.rectangle([70,140,70+tw+60,240],fill=GOLD);d.text((100,150),tag,font=tf,fill=(20,16,10))
s=170
while d.textlength(a.title,font=F(s))>920:s-=6
d.text(((W-d.textlength(a.title,font=F(s)))/2,1280),a.title,font=F(s),fill=GOLD,stroke_width=4,stroke_fill=(0,0,0))
sf=F(64);d.text(((W-d.textlength(a.sub,font=sf))/2,1300+s+40),a.sub,font=sf,fill=(240,240,240),stroke_width=3,stroke_fill=(0,0,0))
im.save(a.out);print(a.out)
