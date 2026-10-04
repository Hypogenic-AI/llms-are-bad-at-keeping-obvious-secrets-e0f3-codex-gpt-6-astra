"""Post hoc context-centered temporal readout; not a single-state deployable probe.
No test labels enter centering: each known context's 15 counterfactual residuals
are centered by their unlabeled mean. Training and test narratives remain disjoint.
"""
from pathlib import Path
import json
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits
threadpool_limits(4)
from analyze import SEED,estimate

def main():
    meta=json.load(open('results/mechanism/metadata.json'));x=np.load('results/mechanism/residuals.npy');labels=np.array([r['label'] for r in meta]);contexts=np.array([r['context'] for r in meta]);conditions=np.array([r['condition'] for r in meta]);out=[]
    for c in ['baseline','outline','context']:
        select=conditions==c;ctx=contexts[select];y=labels[select];train=ctx<14;test=ctx>=18
        for pi,pos in enumerate([32,256,512]):
            h=x[select,1,pi].copy()
            for z in np.unique(ctx):h[ctx==z]-=h[ctx==z].mean(0)
            model=lambda:make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1500,random_state=SEED))
            clf=model().fit(h[train],y[train]);pred=clf.predict(h[test]);shuffle=y[train].copy();np.random.default_rng(SEED).shuffle(shuffle);null=model().fit(h[train],shuffle)
            e=estimate((pred==y[test]).astype(float),ctx[test],center=1/15)
            out.append({'condition':c,'layer':32,'token_position':pos,'accuracy':float((pred==y[test]).mean()),'low':e['low'],'high':e['high'],'shuffled_accuracy':float((null.predict(h[test])==y[test]).mean()),'n_train':int(train.sum()),'n_test':int(test.sum()),'n_test_contexts':len(set(ctx[test])),'test_predictions':pred.tolist(),'test_labels':y[test].tolist(),'test_contexts':ctx[test].tolist()})
    Path('results/mechanism/centered_decoding.json').write_text(json.dumps({'secondary_post_hoc':True,'caveat':__doc__,'summaries':out},indent=2));print(out)
if __name__=='__main__':main()
