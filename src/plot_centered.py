"""Compare fixed raw and post hoc counterfactual-centered layer-32 readouts."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
raw=json.load(open('results/mechanism/decoding.json'));centered=json.load(open('results/mechanism/centered_decoding.json'))['summaries'];fig,axes=plt.subplots(1,3,figsize=(11,3.8),sharey=True)
for ax,c in zip(axes,['baseline','outline','context']):
 for name,data,color in [('Raw residual',raw,'#999999'),('Counterfactual-centered (post hoc)',centered,'#806f9e')]:
  rows=sorted([r for r in data if r['condition']==c and r['layer']==32],key=lambda r:r['token_position']);x=[r['token_position'] for r in rows];y=[r['accuracy'] for r in rows];lo=[r.get('low',r.get('context_bootstrap_ci',{}).get('low')) for r in rows];hi=[r.get('high',r.get('context_bootstrap_ci',{}).get('high')) for r in rows]
  ax.plot(x,y,'o-',label=name,color=color);ax.fill_between(x,lo,hi,color=color,alpha=.15)
 ax.axhline(1/15,color='black',ls='--',label='Chance');ax.set(title=c,xlabel='Continuation token',xticks=[32,256,512],ylim=(0,1.05))
axes[0].set_ylabel('Held-out 15-secret identification accuracy');handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=3,frameon=False,fontsize=9);fig.tight_layout(rect=[0,.12,1,1]);fig.savefig('figures/centered_decoding.png',dpi=180)
