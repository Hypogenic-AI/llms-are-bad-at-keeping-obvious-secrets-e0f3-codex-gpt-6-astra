"""Audit incidental exact-word exposure in secret-blind task materials."""
import json,re
from pathlib import Path
import pandas as pd
from behavior import read

def main():
    units={u['id']:u for u in json.loads(Path('results/units.json').read_text())}
    plans={r['id']:r['text'] for r in read('results/model_outputs/outlines.jsonl')}
    jobs=json.loads(Path('results/story_jobs.json').read_text());rows=[]
    for j in jobs:
        u=units[j['unit']]
        if u['task']!='word' or j['secret_present']:continue
        pattern=r'\b'+re.escape(u['secret'])+r'\b'
        rows.append({'unit':u['id'],'secret':u['secret'],'condition':j['condition'],'premise_exposure':bool(re.search(pattern,u['premise'],re.I)),'outline_exposure':bool(re.search(pattern,plans[u['id']],re.I)),'no_secret_prompt_exposure':bool(re.search(pattern,j['prompt'],re.I))})
    frame=pd.DataFrame(rows);frame.to_csv('results/incidental_exposure.csv',index=False)
    summary=frame.groupby('condition').agg(n=('unit','count'),premise_exposure=('premise_exposure','sum'),outline_exposure=('outline_exposure','sum'),no_secret_prompt_exposure=('no_secret_prompt_exposure','sum')).reset_index().to_dict(orient='records')
    Path('results/incidental_exposure.json').write_text(json.dumps({'summaries':summary,'note':'Exact whole-word audit only; semantic association is not excluded. Primary sample remains unchanged.'},indent=2));print(summary)
if __name__=='__main__':main()
