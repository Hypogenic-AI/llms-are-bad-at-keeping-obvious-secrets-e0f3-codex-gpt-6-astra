"""Replay real generated stories to link fixed layer-32 probe margin with leakage.
Probe training contexts are excluded; layers and regularization are fixed a priori.
"""
import json,re
from pathlib import Path
import numpy as np
import torch
from scipy.stats import spearmanr
from threadpoolctl import threadpool_limits
threadpool_limits(limits=4)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from local_runtime import load,encode_prompt,SEED
from behavior import read

def main():
    meta=json.loads(Path('results/mechanism/metadata.json').read_text());x=np.load('results/mechanism/residuals.npy');sel=np.array([r['context']<14 and r['condition']=='baseline' for r in meta]);y=np.array([r['label'] for r in meta])
    clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1500,random_state=SEED)).fit(x[sel,1,1],y[sel])
    units=[u for u in json.loads(Path('results/units.json').read_text()) if u['task']=='word'];testids={u['id'] for u in units[24:]}
    words=[x['word'] for x in json.loads(Path('datasets/derived/secret_words.json').read_text())[:15]]
    rows=[r for r in read('results/model_outputs/stories.jsonl') if r['unit'] in testids and r['condition'] in ['baseline','outline','context']]
    m,t=load();layer=m.model.language_model.layers[31];state={}
    def hook(module,inp,out):
        h=out[0] if isinstance(out,tuple) else out
        ix=torch.arange(h.shape[0],device=h.device)[:,None]
        state['features']=h[ix,state['positions']].detach().float().cpu().numpy()
    handle=layer.register_forward_hook(hook);features=[];output=[];bs=8
    for start in range(0,len(rows),bs):
        batch=rows[start:start+bs];ids=[];positions=[];literal_positions=[];continuation_positions=[]
        for r in batch:
            prefix=encode_prompt(t,r['prompt'])
            encoded=t(r['text'],add_special_tokens=False,return_offsets_mapping=True)
            continuation=encoded['input_ids']
            match=re.search(r'\b'+re.escape(r['secret'])+r'\b',r['text'],re.I)
            first=next((j+1 for j,(a,b) in enumerate(encoded['offset_mapping']) if match and b>match.start() and a<match.end()),None)
            literal_positions.append(first)
            pos=[min(len(continuation)-1,int(len(continuation)*q)) for q in [.1,.5,.9]]
            ids.append(prefix+continuation);positions.append([len(prefix)+p for p in pos]);continuation_positions.append([p+1 for p in pos])
        n=max(map(len,ids));state['positions']=torch.tensor([[p+n-len(a) for p in ps] for a,ps in zip(ids,positions)],device='cuda')
        inp=torch.tensor([[t.pad_token_id]*(n-len(a))+a for a in ids],device='cuda')
        with torch.inference_mode():m(input_ids=inp,attention_mask=inp.ne(t.pad_token_id),position_ids=(inp.ne(t.pad_token_id).long().cumsum(-1)-1).clamp_min(0),logits_to_keep=1,use_cache=False)
        f=state['features'];features.extend(f)
        for i,r in enumerate(batch):
            for pi,fraction in enumerate([.1,.5,.9]):
                logits=clf.decision_function(f[i,pi][None])[0];label=words.index(r['secret']);other=logits.copy();other[label]=-np.inf
                output.append({'id':r['id'],'unit':r['unit'],'family':r['family'],'condition':r['condition'],'secret_present':r['secret_present'],'fraction':fraction,'continuation_token_position':continuation_positions[i][pi],'first_literal_token_position':literal_positions[i],'label':label,'predicted':int(logits.argmax()),'correct':bool(logits.argmax()==label),'margin':float(logits[label]-other.max())})
        if start%40==0:print('free states',start,len(rows),flush=True)
    handle.remove();np.save('results/mechanism/free_residuals.npy',np.stack(features));Path('results/mechanism/free_scores.json').write_text(json.dumps(output,indent=2))
    import pandas as pd
    frame=pd.DataFrame(output);summary=frame.groupby(['condition','secret_present','fraction']).agg(n=('correct','count'),accuracy=('correct','mean'),mean_margin=('margin','mean')).reset_index();summary.to_csv('results/mechanism/free_summary.csv',index=False)
    pairs=pd.read_csv('results/paired_scores.csv');assoc=frame[(frame.secret_present)&(frame.fraction==.5)].merge(pairs,on=['unit','condition'],suffixes=('','_judge'))
    correlations=[]
    for c,d in assoc.groupby('condition'):
        r,p=spearmanr(d.margin,d.score)
        x=(d.margin-d.groupby('family').margin.transform('mean')).to_numpy()
        y=(d.score-d.groupby('family').score.transform('mean')).to_numpy()
        within=None;permutation_p=None
        if np.std(x)>0 and np.std(y)>0:
            within=float(spearmanr(x,y).statistic)
            rng=np.random.default_rng(SEED);null=[];groups=list(d.groupby('family').indices.values())
            for _ in range(5000):
                shuffled=y.copy()
                for ix in groups:shuffled[ix]=rng.permutation(shuffled[ix])
                null.append(spearmanr(x,shuffled).statistic)
            permutation_p=float((1+(np.abs(null)>=abs(within)).sum())/5001)
        correlations.append({'condition':c,'n':len(d),'spearman_r':float(r) if np.isfinite(r) else None,'p_unadjusted':float(p) if np.isfinite(p) else None,'within_secret_r':within,'within_secret_permutation_p':permutation_p})
    from statsmodels.stats.multitest import multipletests
    valid=[r for r in correlations if r['within_secret_permutation_p'] is not None]
    if valid:
        for row,pval in zip(valid,multipletests([r['within_secret_permutation_p'] for r in valid],method='holm')[1]):row['within_secret_p_holm']=float(pval)
    Path('results/mechanism/margin_correlations.json').write_text(json.dumps(correlations,indent=2))
    print(summary.to_string(index=False));print(correlations)
if __name__=='__main__':main()
