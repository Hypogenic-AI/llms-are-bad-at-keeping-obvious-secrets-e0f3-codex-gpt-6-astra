"""Analyze plot specificity, prior bias, target-blind style and quality controls."""
import json,re
from pathlib import Path
import pandas as pd
from statsmodels.stats.multitest import multipletests
from analyze import choice,rating,estimate,correct_score
from behavior import read

def main():
    f=pd.DataFrame(read('results/model_outputs/plot_forecasts.jsonl'));f['choice']=f.text.map(choice)
    f['score']=[correct_score(a,b) for a,b in zip(f.choice,f.correct_letter)]
    p=f.groupby(['unit','family','condition','secret_present'],as_index=False).agg(score=('score','mean'),n_valid=('score','count'));p=p[p.n_valid==2];p.to_csv('results/plot_forecast_scores.csv',index=False)
    summaries=[];contrasts=[];differences={}
    for (c,present),d in p.groupby(['condition','secret_present']):
        summaries.append({'condition':c,'secret_present':bool(present),**estimate(d.score,d.family,center=.5)})
    for c,d in p[p.condition!='premise_only'].groupby('condition'):
        wide=d.pivot(index=['unit','family'],columns='secret_present',values='score').dropna();delta=wide[True]-wide[False];differences[c]=delta
        contrasts.append({'contrast':c+' private-minus-no-secret',**estimate(delta,delta.index.get_level_values('family'))})
    for a,b in [('outline','baseline'),('outline','context')]:
        d=(differences[a]-differences[b]).dropna();contrasts.append({'contrast':'forecast difference-in-differences '+a+' - '+b,**estimate(d,d.index.get_level_values('family'))})
    for x,pval in zip(contrasts,multipletests([x['p'] for x in contrasts],method='holm')[1]):x['p_holm']=float(pval)
    b=pd.DataFrame(read('results/model_outputs/target_blind_judgments.jsonl'));b['choice']=b.text.map(choice);b['score']=[correct_score(a,c) for a,c in zip(b.choice,b.correct_letter)]
    b=b.groupby(['unit','family'],as_index=False).agg(score=('score','mean'),n=('score','count'));b=b[b.n==2]
    primary=pd.read_csv('results/paired_scores.csv');primary=primary[(primary.task=='word')&(primary.condition=='baseline')]
    joined=b.merge(primary,on=['unit','family'],suffixes=('_blind','_aware'))
    blind={'accuracy':estimate(b.score,center=.5),'aware_minus_blind':estimate(joined.score_aware-joined.score_blind),'n':len(b)}
    q=pd.DataFrame(read('results/model_outputs/quality.jsonl'));q['rating']=q.text.map(rating)
    q.to_csv('results/quality_ratings.csv',index=False)
    quality=q.groupby(['task','condition']).agg(n=('rating','count'),mean=('rating','mean'),median=('rating','median'),sd=('rating','std'),minimum=('rating','min'),maximum=('rating','max')).reset_index().to_dict(orient='records')
    out={'plot_forecast_summaries':summaries,'plot_forecast_contrasts':contrasts,'malformed_forecasts':int(f.choice.isna().sum()),'target_blind':blind,'quality':quality,'malformed_quality':int(q.rating.isna().sum())}
    Path('results/diagnostics_analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
