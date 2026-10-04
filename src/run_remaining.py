"""Serial GPU pipeline after the active writer exits; every stage is checked.
This process must finish before the research turn ends.
"""
from pathlib import Path
import os,sys,time,json,subprocess
root=Path.cwd()
assert (root/'STATE.md').exists() and (root/'src').exists()
writer_pid=int(sys.argv[1])
while Path(f'/proc/{writer_pid}').exists():time.sleep(5)
rows=[json.loads(x) for x in (root/'results/model_outputs/stories.jsonl').read_text().splitlines()]
assert len(rows)==1080 and len({r['id'] for r in rows})==1080,'Writer stage incomplete'
env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',OPENBLAS_NUM_THREADS='4',OMP_NUM_THREADS='8')
stages=[
 ('positive_anchor',['src/anchor.py']),
 ('independent_judge',['src/independent_judge.py','judge','--batch-size','16']),
 ('behavior_analysis',['src/analyze.py']),
 ('direction_calibration',['src/robustness.py']),
 ('diagnostics',['src/diagnostics.py']),
 ('mechanism_extract',['src/mechanism.py','extract']),
 ('mechanism_analyze',['src/mechanism.py','analyze']),
 ('free_states',['src/free_states.py']),
 ('interventions',['src/intervene.py']),
]
ledger=[]
for name,args in stages:
    # Read state at stage boundary; runner notes remain owned by the root agent.
    (root/'STATE.md').read_text()
    print('START',name,time.time(),flush=True);start=time.time()
    with (root/f'logs/{name}.log').open('w') as f:
        p=subprocess.run([sys.executable,*args],cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
    ledger.append({'stage':name,'returncode':p.returncode,'seconds':time.time()-start})
    (root/'results/stage_timings.json').write_text(json.dumps(ledger,indent=2))
    print('END',name,p.returncode,round(time.time()-start,1),flush=True)
    if p.returncode:sys.exit(p.returncode)
