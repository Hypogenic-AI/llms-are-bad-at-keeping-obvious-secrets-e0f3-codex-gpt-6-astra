"""Secondary early readout–later disclosure association, not causal mediation.
Use token offsets from the replayed text: any exact mention must start at least
ten tokens after the sampled state. Main states re-encode generated text.
"""
import json,re
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests
from analyze import SEED

def main():
    states=pd.DataFrame(json.loads(Path('results/mechanism/free_scores.json').read_text()))
    s=pd.read_csv('results/story_metrics.csv');s=s[(s.task=='word')&s.secret_present].copy()
    joined=states[(states.fraction==.1)&states.secret_present].merge(s[['id','literal_leak']],on='id');joined=joined[joined.first_literal_token_position.isna()|(joined.first_literal_token_position>=joined.continuation_token_position+10)]
    out=[]
    for c,d in joined.groupby('condition'):
        x=(d.margin-d.groupby('family').margin.transform('mean')).to_numpy();raw=d.literal_leak.astype(float);y=(raw-raw.groupby(d.family).transform('mean')).to_numpy()
        rho=None;p=None
        if np.std(x)>0 and np.std(y)>0:
            rho=float(spearmanr(x,y).statistic);rng=np.random.default_rng(SEED);groups=list(d.groupby('family').indices.values());null=[]
            for _ in range(5000):
                z=y.copy()
                for ix in groups:z[ix]=rng.permutation(z[ix])
                null.append(spearmanr(x,z).statistic)
            p=float((1+(np.abs(null)>=abs(rho)).sum())/5001)
        out.append({'condition':c,'n':len(d),'n_later_literal':int(raw.sum()),'within_secret_spearman_r':rho,'p':p})
    valid=[r for r in out if r['p'] is not None]
    for r,p in zip(valid,multipletests([r['p'] for r in valid],method='holm')[1] if valid else []):r['p_holm']=float(p)
    Path('results/mechanism/early_literal_association.json').write_text(json.dumps({'secondary_post_hoc':True,'summaries':out,'caveat':__doc__},indent=2));print(out)
if __name__=='__main__':main()
