"""Separate exact disclosure from subtle leakage; exclusions are descriptive only."""
from pathlib import Path
import json,re
import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests
from analyze import estimate

def main():
    stories=pd.read_csv('results/story_metrics.csv');s=stories[stories.task=='word'].copy();scores=pd.read_csv('results/paired_scores.csv');scores=scores[scores.task=='word']
    s['literal_leak']=s.literal_leak.astype(bool)
    summaries=[];clean=[];heuristic=[];contrasts=[]
    for (c,present),d in s.groupby(['condition','secret_present']):
        summaries.append({'condition':c,'secret_present':bool(present),'n_literal':int(d.literal_leak.sum()),**estimate(d.literal_leak.astype(float))})
    for c,d in s.groupby('condition'):
        wide=d.pivot(index=['unit','family'],columns='secret_present',values='literal_leak')
        cleanunits=wide.index[~wide[True]&~wide[False]].get_level_values('unit')
        z=scores[(scores.condition==c)&scores.unit.isin(cleanunits)]
        clean.append({'condition':c,**estimate(z.score,center=.5),'caution':'Post-treatment exclusion; diagnostic only, not a causal estimate.'})
        h=np.where(wide[True]&~wide[False],1,np.where(~wide[True]&wide[False],0,.5))
        heuristic.append({'condition':c,**estimate(h,center=.5)})
    d=s[s.secret_present].pivot(index=['unit','family'],columns='condition',values='literal_leak').astype(float)
    for a,b in [('outline','baseline'),('outline','context'),('decoy','baseline')]:
        v=d[a]-d[b];contrasts.append({'contrast':a+' - '+b,**estimate(v),'family_cluster_sensitivity':estimate(v,v.index.get_level_values('family'))})
    for r,p in zip(contrasts,multipletests([r['p'] for r in contrasts],method='holm')[1]):r['p_holm']=float(p)
    examples=[];positions=[]
    for r in s[s.secret_present&s.literal_leak].sort_values('id').itertuples():
        m=re.search(r'\b'+re.escape(r.secret)+r'\b',r.text,re.I)
        pos=m.start()/max(1,len(r.text));positions.append(pos)
        if len(examples)<8:examples.append({'id':r.id,'secret':r.secret,'condition':r.condition,'first_mention_character_fraction':pos,'excerpt':r.text[max(0,m.start()-100):min(len(r.text),m.end()+100)]})
    out={'summaries':summaries,'contrasts':contrasts,'without_literal_pairs':clean,'exact_word_heuristic':heuristic,'examples_sorted_first_8':examples,'first_mention_fraction':{'n':len(positions),'mean':float(np.mean(positions)),'median':float(np.median(positions))},'scope':'Exact whole words, case insensitive; not aliases. Direct-disclosure contrasts are secondary outcomes; nonliteral exclusions are post-treatment diagnostics.'}
    Path('results/literal_analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
