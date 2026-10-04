"""Summarize genuinely online layer-32 decoder traces from the intervention pilot."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from behavior import read
from analyze import estimate

def main():
    path=Path('results/mechanism/online_trace.jsonl')
    if not path.exists():return
    records=read(path);samples=[]
    for r in records:
        n=r['n_valid_steps']
        if not n:continue
        for fraction in [.1,.5,.9]:
            i=round(fraction*(n-1))
            for when in ['before','after']:
                samples.append({'id':r['id'],'unit':r['unit'],'family':r['family'],'condition':r['condition'],'secret_present':r['secret_present'],'fraction':fraction,'when':when,'tokens_seen':i+1,'correct':float(r[when+'_pred'][i]==r['label']),'margin':r[when+'_margin'][i]})
    df=pd.DataFrame(samples);df.to_csv('results/mechanism/online_samples.csv',index=False);summaries=[]
    for (condition,present,fraction,when),d in df.groupby(['condition','secret_present','fraction','when']):
        summaries.append({'condition':condition,'secret_present':bool(present),'fraction':fraction,'when':when,**estimate(d.correct,d.family),'mean_margin':float(d.margin.mean())})
    joins=df[(df.secret_present)&(df.fraction==.5)&(df.when=='after')].merge(pd.read_csv('results/intervention_scores.csv'),on=['unit','condition'],suffixes=('','_judge'))
    correlations=[]
    for condition,d in joins.groupby('condition'):
        result=spearmanr(d.margin,d.score)
        correlations.append({'condition':condition,'n':len(d),'rho':float(result.statistic) if np.isfinite(result.statistic) else None,'p_exploratory':float(result.pvalue) if np.isfinite(result.pvalue) else None})
    Path('results/mechanism/online_analysis.json').write_text(json.dumps({'n_traced_stories':len(records),'n_unique_ids':len({r['id'] for r in records}),'summaries':summaries,'correlations':correlations,'note':'Actual incremental generation states; excludes prompt and finished padding. Correlations are exploratory and unadjusted, not causal mediation estimates.'},indent=2))
    print('Online traces summarized:',len(records))
if __name__=='__main__':main()
