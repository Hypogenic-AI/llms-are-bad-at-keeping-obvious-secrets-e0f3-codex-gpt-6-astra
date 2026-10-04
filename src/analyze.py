"""Paired counterbalanced leakage analysis; resampling units, not judge orders."""
import json,re,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests
SEED=20261004

def read(p):return [json.loads(x) for x in Path(p).read_text().splitlines()]
def choice(text):
    m=re.fullmatch(r'\s*(?:Answer:\s*)?([AB])\s*[.!]?\s*',text,re.I)
    return m.group(1).upper() if m else None

def correct_score(answer,correct):
    """Pandas may convert parser None to NaN; neither is a wrong answer."""
    return float(answer==correct) if pd.notna(answer) else np.nan

def rating(text):
    m=re.fullmatch(r'\s*(?:(?:Rating|Score):\s*)?([1-5])\s*[.!]?\s*',text,re.I)
    return int(m.group(1)) if m else None

def estimate(values,groups=None,center=0):
    """Percentile cluster bootstrap CI and paired cluster sign-flip p-value."""
    x=np.asarray(values,float);rng=np.random.default_rng(SEED)
    if groups is None: groups=np.arange(len(x))
    groups=np.asarray(groups);g=np.unique(groups);chunks=[x[groups==z] for z in g]
    totals=np.array([a.sum() for a in chunks]);ns=np.array([len(a) for a in chunks])
    ix=rng.integers(0,len(g),size=(10000,len(g)))
    boot=totals[ix].sum(1)/ns[ix].sum(1)
    delta=totals-center*ns
    signs=rng.choice([-1,1],size=(20000,len(g)))
    null=(signs*delta).sum(1)/len(x)
    obs=x.mean()-center
    p=(1+(np.abs(null)>=abs(obs)-1e-12).sum())/(len(null)+1)
    return {'mean':float(x.mean()),'low':float(np.quantile(boot,.025)),'high':float(np.quantile(boot,.975)),'p':float(p),'n_units':len(x),'n_clusters':len(g),'sd':float(x.std(ddof=1)),'min':float(x.min()),'max':float(x.max())}

def main():
    stories=pd.DataFrame(read('results/model_outputs/stories.jsonl'))
    judges=pd.DataFrame(read('results/model_outputs/judgments.jsonl'))
    judges['choice']=judges.text.map(choice);judges['valid']=judges.choice.notna()
    judges['score']=[correct_score(a,b) for a,b in zip(judges.choice,judges.correct_letter)]
    judges.to_csv('results/judgment_scores.csv',index=False)
    scores=judges.groupby(['unit','task','family','condition'],as_index=False).agg(score=('score','mean'),n_valid=('valid','sum'))
    # Incomplete order pairs excluded from inference, explicitly counted.
    excluded=scores[scores.n_valid!=2];scores=scores[scores.n_valid==2]
    scores.to_csv('results/paired_scores.csv',index=False)
    summaries=[];contrasts=[]
    for (task,cond),d in scores.groupby(['task','condition']):
        groups=d.family if task=='plot' else None
        e=estimate(d.score,groups,center=.5)
        e.update(task=task,condition=cond)
        # Secret-cluster sensitivity also saved for word trials.
        e['family_cluster_sensitivity']=estimate(d.score,d.family,center=.5)
        summaries.append(e)
    for task,d in scores.groupby('task'):
        wide=d.pivot(index=['unit','family'],columns='condition',values='score')
        for a,b in [('outline','baseline'),('outline','context'),('decoy','baseline')]:
            if a not in wide or b not in wide:continue
            z=wide[[a,b]].dropna();delta=z[a]-z[b]
            e=estimate(delta,z.index.get_level_values('family') if task=='plot' else None)
            e.update(task=task,contrast=a+' - '+b,paired_dz=float(delta.mean()/delta.std()) if delta.std() else None)
            e['family_cluster_sensitivity']=estimate(delta,z.index.get_level_values('family'))
            contrasts.append(e)
    if contrasts:
        for x,p in zip(contrasts,multipletests([x['p'] for x in contrasts],method='holm')[1]):x['p_holm']=float(p)
    stories['word_count']=stories.text.map(lambda s:len(s.split()))
    stories['literal_leak']=[bool(re.search(r'\b'+re.escape(secret)+r'\b',text,re.I)) if task=='word' else None for text,secret,task in zip(stories.text,stories.secret,stories.task)]
    stories['unique_word_fraction']=stories.text.map(lambda s:len(set(s.lower().split()))/max(1,len(s.split())))
    stories.to_csv('results/story_metrics.csv',index=False)
    qa=stories.groupby(['task','condition','secret_present']).agg(n=('id','count'),mean_words=('word_count','mean'),sd_words=('word_count','std'),min_words=('word_count','min'),max_words=('word_count','max'),truncated=('truncated','sum'),lexical_diversity=('unique_word_fraction','mean')).reset_index()
    qa.to_csv('results/quality_summary.csv',index=False)
    bias=judges.groupby(['task','condition','order']).agg(n=('id','count'),n_valid=('valid','sum'),accuracy=('score','mean'),a_rate=('choice',lambda s:(s.dropna()=='A').mean())).reset_index()
    bias.to_csv('results/order_bias.csv',index=False)
    disagreement=[]
    for (task,c),d in judges.groupby(['task','condition']):
        p=d.pivot(index='unit',columns='order',values='score').dropna()
        disagreement.append({'task':task,'condition':c,'n_valid_pairs':len(p),'order_disagreement_rate':float((p[0]!=p[1]).mean()) if len(p) else None})
    out={'summaries':summaries,'contrasts':contrasts,'malformed_judgments':int((~judges.valid).sum()),'excluded_order_pairs':len(excluded),'order_disagreement':disagreement,'n_stories':len(stories),'n_judgments':len(judges),'seed':SEED}
    Path('results/analysis.json').write_text(json.dumps(out,indent=2,allow_nan=False))
    fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
    for ax,task in zip(axes,['word','plot']):
        ss=sorted([s for s in summaries if s['task']==task],key=lambda z:['baseline','outline','context','decoy'].index(z['condition']))
        if ss:
            y=np.array([s['mean'] for s in ss]);ax.bar([s['condition'] for s in ss],y,color=[{'baseline':'#526e89','outline':'#806f9e','context':'#c58e45','decoy':'#648c72'}[s['condition']] for s in ss])
            ax.errorbar(range(len(ss)),y,yerr=[y-[s['low'] for s in ss],np.array([s['high'] for s in ss])-y],fmt='none',color='black',capsize=4)
        ax.axhline(.5,ls='--',color='gray');ax.set(title=task+' secrets',ylim=(0,1),ylabel='Counterbalanced 2AFC accuracy (95% CI)')
    fig.tight_layout();fig.savefig('figures/leakage.png',dpi=180);plt.close(fig)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
