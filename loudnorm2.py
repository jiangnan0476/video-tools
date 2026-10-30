#!/usr/bin/env python3
"""Two-pass loudnorm (measure, then linear=true). Works on wav or video (video stream copied).
usage: loudnorm2.py in out [--I -14] [--TP -1.5] [--LRA 11]
Prints measured integrated loudness of the output and exits 1 if |I-target|>0.5."""
import json,re,subprocess,sys,argparse
ap=argparse.ArgumentParser();ap.add_argument('inp');ap.add_argument('out')
ap.add_argument('--I',type=float,default=-14);ap.add_argument('--TP',type=float,default=-1.5);ap.add_argument('--LRA',type=float,default=11)
a=ap.parse_args()
def run(c):return subprocess.run(c,capture_output=True,text=True).stderr
base=f'loudnorm=I={a.I}:TP={a.TP}:LRA={a.LRA}'
m=json.loads(re.findall(r'\{[^{}]+\}',run(['ffmpeg','-hide_banner','-i',a.inp,'-af',base+':print_format=json','-f','null','-']))[-1])
af=(f"{base}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
    f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json")
video=a.out.endswith(('.mp4','.mov','.mkv'))
cmd=['ffmpeg','-loglevel','error','-y','-i',a.inp,'-af',af,'-ar','48000']+(['-c:v','copy','-c:a','aac','-b:a','192k'] if video else [])+[a.out]
subprocess.run(cmd,check=True)
o=run(['ffmpeg','-hide_banner','-i',a.out,'-af','ebur128=peak=true','-f','null','-'])
I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1]);tp=re.findall(r'Peak:\s+(-?[\d.]+) dBFS',o)
for _ in range(3):
  if abs(I-a.I)<=0.2: break
  if True:   # linear mode fell back/undershot (peak-limited): gain + true-peak limiter, then re-measure
      import os,shutil;tmp=a.out+'.tmp'+os.path.splitext(a.out)[1];shutil.move(a.out,tmp)
      lim=10**((a.TP-0.8)/20)
      subprocess.run(['ffmpeg','-loglevel','error','-y','-i',tmp,'-af',f'volume={a.I-I:.2f}dB,alimiter=limit={lim:.4f}:level=false,aresample=48000']+(['-c:v','copy','-c:a','aac','-b:a','192k'] if video else [])+[a.out],check=True);os.remove(tmp)
      o=run(['ffmpeg','-hide_banner','-i',a.out,'-af','ebur128=peak=true','-f','null','-'])
      I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1]);tp=re.findall(r'Peak:\s+(-?[\d.]+) dBFS',o);print('applied gain+limiter correction')
print(f'input I={m["input_i"]} -> output I={I} LUFS, true peak={tp[-1] if tp else "?"} dBFS (target {a.I}±0.5)')
sys.exit(0 if abs(I-a.I)<=0.5 else 1)
