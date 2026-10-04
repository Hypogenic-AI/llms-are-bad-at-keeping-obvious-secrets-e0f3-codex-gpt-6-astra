"""Secondary order-balanced forced-choice log-odds, prompted by position bias.
This measures real next-token logits, not simulated responses. Primary generated
choices remain unchanged. A constant additive position preference cancels.
"""
import json,time
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from independent_judge import load_qwen,MODEL,REVISION
from behavior import read
from analyze import estimate
from statsmodels.stats.multitest import multipletests

def score():
    m,t=load_qwen();a=t.encode('A',add_special_tokens=False);b=t.encode('B',add_special_tokens=False)
    assert len(a)==len(b)==1,(a,b)
    path=Path('results/model_outputs/choice_likelihoods.jsonl');done={r['id'] for r in read(path)}
    jobs=[]
    sources=[('main','judgments'),('anchor','anchor_qwen_judgments')]
    if Path('results/model_outputs/intervention_judgments.jsonl').exists():sources.append(('intervention','intervention_judgments'))
    for study,file in sources:
        for r in read('results/model_outputs/'+file+'.jsonl'):
            jobs.append({k:r[k] for k in ['id','unit','family','condition','order','correct_letter','prompt'] if k in r}|{'id':study+'_'+r['id'],'study':study,'task':r.get('task','word')})
    todo=[r for r in jobs if r['id'] not in done];bs=16
    for start in range(0,len(todo),bs):
        rows=todo[start:start+bs]
        texts=[t.apply_chat_template([{'role':'user','content':r['prompt']}],tokenize=False,add_generation_prompt=True,enable_thinking=False) for r in rows]
        inp=t(texts,return_tensors='pt',padding=True).to('cuda');begin=time.time()
        with torch.inference_mode():out=m(**inp,position_ids=(inp.attention_mask.long().cumsum(-1)-1).clamp_min(0),logits_to_keep=1,use_cache=False).logits[:,-1].float()
        logits=out[:,[a[0],b[0]]].cpu().numpy()
        with path.open('a') as f:
            for r,l in zip(rows,logits):
                f.write(json.dumps({**r,'logit_a':float(l[0]),'logit_b':float(l[1]),'log_odds_a_over_b':float(l[0]-l[1]),'choice_token_ids':[a[0],b[0]],'model':MODEL,'revision':REVISION,'timestamp':time.time(),'seconds_batch':time.time()-begin})+'\n');f.flush()
        print('likelihood',start+len(rows),'/',len(todo),flush=True)

def analyze():
    d=pd.DataFrame(read('results/model_outputs/choice_likelihoods.jsonl'))
    # Anchor rows do not need a condition field in their original raw schema.
    d['condition']=d['condition'].fillna('baseline') if 'condition' in d else 'baseline'
    d['correct_log_odds']=d.log_odds_a_over_b*np.where(d.correct_letter=='A',1,-1)
    p=d.groupby(['study','task','unit','family','condition'],as_index=False).agg(log_odds=('correct_log_odds','mean'),n=('id','count'))
    assert (p.n==2).all();p['score']=np.where(p.log_odds>0,1,np.where(p.log_odds<0,0,.5))
    p.to_csv('results/likelihood_pair_scores.csv',index=False);summaries=[];contrasts=[]
    for (study,task,c),r in p.groupby(['study','task','condition']):
        e=estimate(r.score,r.family if task=='plot' or study=='intervention' else None,center=.5)
        summaries.append({'study':study,'task':task,'condition':c,**e,'family_cluster_sensitivity':estimate(r.score,r.family,center=.5),'mean_correct_log_odds':float(r.log_odds.mean())})
    for task,r in p[p.study=='main'].groupby('task'):
        wide=r.pivot(index=['unit','family'],columns='condition',values='score')
        for a,b in [('outline','baseline'),('outline','context'),('decoy','baseline')]:
            if a not in wide:continue
            z=wide[[a,b]].dropna();v=z[a]-z[b]
            contrasts.append({'task':task,'contrast':a+' - '+b,**estimate(v,z.index.get_level_values('family') if task=='plot' else None),'family_cluster_sensitivity':estimate(v,z.index.get_level_values('family'))})
    for row,pval in zip(contrasts,multipletests([x['p'] for x in contrasts],method='holm')[1]):row['p_holm']=float(pval)
    intervention_contrasts=[]
    if (p.study=='intervention').any():
        wide=p[p.study=='intervention'].pivot(index=['unit','family'],columns='condition',values='score')
        for c in ['sham','random','other']:
            z=(wide.target-wide[c]).dropna();intervention_contrasts.append({'contrast':'target - '+c,**estimate(z,z.index.get_level_values('family'))})
        for row,pval in zip(intervention_contrasts,multipletests([r['p'] for r in intervention_contrasts],method='holm')[1]):row['p_holm']=float(pval)
    clean=[]
    metrics=pd.read_csv('results/story_metrics.csv')
    for condition,r in p[(p.study=='main')&(p.task=='word')].groupby('condition'):
        bad=set(metrics[(metrics.task=='word')&(metrics.condition==condition)&(metrics.literal_leak==True)].unit)
        z=r[~r.unit.isin(bad)]
        clean.append({'condition':condition,**estimate(z.score,center=.5),'note':'Post-treatment literal exclusion; descriptive only.'})
    out={'without_literal_pairs':clean,'exact_log_odds_ties':int((p.log_odds==0).sum()),'intervention_contrasts':intervention_contrasts,'secondary_post_hoc':True,'n_order_scores':len(d),'n_pairs':len(p),'summaries':summaries,'contrasts':contrasts,'caveat':'Cancels constant additive log-odds position bias only. Not independently validated as a measure of semantic leakage.'}
    Path('results/likelihood_analysis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':
    import sys
    if len(sys.argv)==1 or sys.argv[1]=='score':score()
    analyze()
