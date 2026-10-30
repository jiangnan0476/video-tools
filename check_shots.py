#!/usr/bin/env python3
"""Storyboard check. usage: check_shots.py storyboard.json
storyboard.json: [{"id":"S1","type":"portrait","text":"...","prompt":"..."}, ...]
types: portrait(人物近景) wide(全景/场面) object(物件特写) card(信息卡) action(动作/冲突) detail(环境细节)
Fails if: unknown/missing type; adjacent shots same type; <3 distinct types;
any type >40% of shots; >2 cards in a row-window of 3; first shot is detail."""
import json,sys,collections
T={'portrait','wide','object','card','action','detail'}
S=json.load(open(sys.argv[1]));err=[]
for s in S:
    if s.get('type') not in T: err.append(f"{s.get('id')}: type '{s.get('type')}' not in {sorted(T)}")
for p,q in zip(S,S[1:]):
    if p.get('type')==q.get('type'): err.append(f"{p['id']}->{q['id']}: adjacent same type '{p['type']}'")
c=collections.Counter(s.get('type') for s in S)
if len(c)<3: err.append(f'only {len(c)} distinct types (need >=3)')
for t,n in c.items():
    if len(S)>=5 and n/len(S)>0.4: err.append(f"type '{t}' is {n}/{len(S)} shots (>40%)")
for i in range(len(S)-2):
    if sum(s.get('type')=='card' for s in S[i:i+3])>=2: err.append(f"{S[i]['id']}..: >=2 cards within 3 shots")
if S and S[0].get('type')=='detail': err.append('first shot should hook: not a quiet detail shot')
print('types:',dict(c))
print('\n'.join(err) if err else 'OK');sys.exit(1 if err else 0)
