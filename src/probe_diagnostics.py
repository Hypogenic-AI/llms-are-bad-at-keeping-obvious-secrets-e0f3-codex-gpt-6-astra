"""Post hoc probe failure diagnostics; do not alter the prespecified D3 gate.
Counterfactual centering uses all 15 unlabeled states for each context at test,
so it is a transductive diagnostic, not a deployable single-story readout.
"""
import json
from pathlib import Path
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from threadpoolctl import threadpool_limits
threadpool_limits(4)
from analyze import SEED,estimate

def main():
    meta=json.load(open('results/mechanism/metadata.json'));x=np.load('results/mechanism/residuals.npy');y=np.array([r['label'] for r in meta]);ctx=np.array([r['context'] for r in meta]);cond=np.array([r['condition'] for r in meta]);out=[]
    for c in ['baseline','outline','context']:
        select=cond==c;a=x[select,1,1].copy();labels=y[select];contexts=ctx[select];train=contexts<14;test=contexts>=18
        centered=a.copy()
        for z in np.unique(contexts):centered[contexts==z]-=centered[contexts==z].mean(0)
        for method,h in [('raw',a),('within_counterfactual_context_centered',centered)]:
            clf=make_pipeline(StandardScaler(),LogisticRegression(C=.1,max_iter=1500,random_state=SEED)).fit(h[train],labels[train]);pred=clf.predict(h[test])
            out.append({'condition':c,'method':method,'layer':32,'position':256,'train_accuracy':float((clf.predict(h[train])==labels[train]).mean()),'test_accuracy':float((pred==labels[test]).mean()),'test_context_ci':estimate((pred==labels[test]).astype(float),contexts[test],center=1/15),'n_unique_test_predictions':int(len(set(pred)))})
    norms=np.linalg.norm(x,axis=-1)
    result={'finite_features':bool(np.isfinite(x).all()),'shape':list(x.shape),'residual_norm_min_mean_max':[float(norms.min()),float(norms.mean()),float(norms.max())],'readouts':out,'status':'Post hoc diagnosis only; original gate and primary probe grid unchanged.'}
    Path('results/mechanism/probe_diagnostics.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
