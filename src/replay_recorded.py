"""Replay original recorded writer batches, including the archived length correction.
Use --limit 1 for a short GPU validation; remove the limit for complete replay.
This reproduces recorded batch composition and seeds rather than constructing a new sample.
"""
from pathlib import Path
import argparse,json
from collections import OrderedDict
from local_runtime import load,generate
from behavior import read

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--limit',type=int,default=1);args=ap.parse_args()
    print(Path.cwd());assert Path('STATE.md').exists()
    groups=OrderedDict();seen=set()
    for file in ['results/model_outputs/stories_before_length_fix.jsonl','results/model_outputs/stories.jsonl']:
        for row in read(file):
            key=(row['seed'],row['id'])
            if key in seen:continue
            seen.add(key);groups.setdefault(row['seed'],[]).append(row)
    m,t=load();comparisons=[]
    for i,(seed,rows) in enumerate(groups.items()):
        if args.limit and i>=args.limit:break
        out=generate(m,t,[r['prompt'] for r in rows],max_tokens=rows[0]['max_new_tokens'],seed=seed,temperature=rows[0]['temperature'])
        comparisons.append({'seed':seed,'n':len(rows),'ids':[r['id'] for r in rows],'matches':[r['text']==o['text'] for r,o in zip(rows,out)],'outputs':out})
        print('Replayed',seed,'exact matches',sum(comparisons[-1]['matches']),'/',len(rows),flush=True)
    Path('results/recorded_replay.json').write_text(json.dumps(comparisons,indent=2))
if __name__=='__main__':main()
