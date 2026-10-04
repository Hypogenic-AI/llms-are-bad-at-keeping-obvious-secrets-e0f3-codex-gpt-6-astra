"""Paired causal-pilot estimates and prespecified utility checks."""
from pathlib import Path
import json,re
import pandas as pd
from statsmodels.stats.multitest import multipletests
from analyze import choice,rating,estimate,correct_score
from behavior import read

def main():
    gate=json.loads(Path('results/mechanism/intervention_gate.json').read_text())
    if not gate['proceed']:
        Path('results/intervention_analysis.json').write_text(json.dumps({'gate':gate,'status':'not run'},indent=2));return
    j=pd.DataFrame(read('results/model_outputs/intervention_judgments.jsonl'));j['choice']=j.text.map(choice);j['score']=[correct_score(a,b) for a,b in zip(j.choice,j.correct_letter)]
    d=j.groupby(['unit','family','condition'],as_index=False).agg(score=('score','mean'),n_valid=('score','count'));d=d[d.n_valid==2];d.to_csv('results/intervention_scores.csv',index=False)
    summaries=[{'condition':c,**estimate(g.score,g.family,center=.5)} for c,g in d.groupby('condition')]
    wide=d.pivot(index=['unit','family'],columns='condition',values='score');contrasts=[]
    for c in ['sham','random','other']:
        z=(wide.target-wide[c]).dropna();contrasts.append({'contrast':'target - '+c,**estimate(z,z.index.get_level_values('family'))})
    for x,p in zip(contrasts,multipletests([x['p'] for x in contrasts],method='holm')[1]):x['p_holm']=float(p)
    rows=pd.DataFrame(read('results/model_outputs/interventions.jsonl'));rows['word_count']=rows.text.map(lambda s:len(s.split()));rows['literal_leak']=[bool(re.search(r'\b'+re.escape(w)+r'\b',txt,re.I)) for w,txt in zip(rows.secret,rows.text)];rows['unique_word_fraction']=rows.text.map(lambda s:len(set(s.lower().split()))/max(1,len(s.split())))
    quality=pd.DataFrame(read('results/model_outputs/intervention_quality.jsonl'));quality['rating']=quality.text.map(rating)
    q=quality[quality.secret_present].pivot(index='unit',columns='condition',values='rating');delta=(q.target-q.sham).dropna();families=rows.groupby('unit').family.first().to_dict();qe=estimate(delta,[families[u] for u in delta.index])
    lengths=rows[rows.secret_present].groupby('condition').word_count.mean();trunc=rows[rows.secret_present].groupby('condition').truncated.mean()
    ratios=float(lengths['target']/lengths['sham']);trunc_difference=float(trunc['target']-trunc['sham'])
    utilities={'coherence_target_minus_sham':qe,'coherence_noninferiority_established':qe['low']>-.5,'length_ratio_target_sham':ratios,'length_within_20_percent':.8<=ratios<=1.2,'truncation_rate_difference':trunc_difference,'truncation_within_10pp':trunc_difference<=.1}
    utilities['all_utility_criteria_pass']=all(utilities[k] for k in ['coherence_noninferiority_established','length_within_20_percent','truncation_within_10pp'])
    quality_summary=quality.groupby(['condition','secret_present']).rating.agg(['count','mean','std','min','max']).reset_index().to_dict(orient='records')
    descriptive=rows.groupby(['condition','secret_present']).agg(n=('id','count'),mean_words=('word_count','mean'),truncated=('truncated','sum'),literal_leaks=('literal_leak','sum'),lexical_diversity=('unique_word_fraction','mean')).reset_index().to_dict(orient='records')
    out={'gate':gate,'summaries':summaries,'contrasts':contrasts,'utility':utilities,'quality':quality_summary,'story_metrics':descriptive,'malformed_judgments':int(j.choice.isna().sum()),'malformed_quality':int(quality.rating.isna().sum()),'n_stories':len(rows),'n_units':len(d.unit.unique()),'interpretation_limit':'One projection direction at one layer, original prompt KV cache retained; not complete concept erasure.'}
    Path('results/intervention_analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
