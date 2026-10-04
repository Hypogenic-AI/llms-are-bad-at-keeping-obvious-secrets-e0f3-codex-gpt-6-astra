"""Render actual probe and intervention estimates; no synthetic data fallbacks."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    rows=json.loads(Path('results/mechanism/decoding.json').read_text());length=json.loads(Path('results/mechanism/length_baseline.json').read_text())
    fig,axes=plt.subplots(1,3,figsize=(12,3.7),sharey=True)
    for ax,c in zip(axes,['baseline','outline','context']):
        for layer,color in [(16,'#c58e45'),(32,'#526e89'),(48,'#648c72')]:
            rs=sorted([r for r in rows if r['condition']==c and r['layer']==layer],key=lambda r:r['token_position'])
            x=[r['token_position'] for r in rs];y=np.array([r['accuracy'] for r in rs]);lo=[r['context_bootstrap_ci']['low'] for r in rs];hi=[r['context_bootstrap_ci']['high'] for r in rs]
            ax.plot(x,y,'o-',label=f'Layer {layer}',color=color);ax.fill_between(x,lo,hi,color=color,alpha=.13)
        ax.axhline(1/15,color='gray',ls='--',label='Chance')
        ax.axhline(next(r['accuracy'] for r in length if r['condition']==c),color='black',ls=':',label='Length only')
        ax.set(title=c,xlabel='Continuation token',xticks=[32,256,512],ylim=(-.02,1.05))
    axes[0].set_ylabel('Held-out secret identity accuracy')
    handles,labels=axes[0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=5,frameon=False);fig.tight_layout(rect=[0,.1,1,1]);fig.savefig('figures/secret_decoding.png',dpi=180);plt.close(fig)
    f=pd.read_csv('results/mechanism/free_summary.csv');fig,axes=plt.subplots(1,2,figsize=(9,3.8),sharey=True)
    for ax,present in zip(axes,[True,False]):
        for c,color in [('baseline','#526e89'),('outline','#806f9e'),('context','#c58e45')]:
            d=f[(f.secret_present==present)&(f.condition==c)].sort_values('fraction');ax.plot(d.fraction,d.accuracy,'o-',label=c,color=color)
        ax.axhline(1/15,color='gray',ls='--');ax.set(title='Secret present' if present else 'No secret control',xlabel='Fraction of generated story',ylim=(0,1),xticks=[.1,.5,.9]);ax.legend(frameon=False)
    axes[0].set_ylabel('Fixed baseline decoder accuracy');fig.tight_layout();fig.savefig('figures/free_story_decoding.png',dpi=180);plt.close(fig)
    p=Path('results/intervention_analysis.json')
    if p.exists():
        data=json.loads(p.read_text())
        if data.get('status')=='not run':return
        fig,ax=plt.subplots(figsize=(6,4));order=['sham','target','random','other'];rs=sorted(data['summaries'],key=lambda r:order.index(r['condition']));means=[r['mean'] for r in rs]
        ax.bar(order,means,color=['#526e89','#806f9e','#999999','#c58e45']);ax.vlines(range(4),[r['low'] for r in rs],[r['high'] for r in rs],color='black');ax.axhline(.5,color='gray',ls='--');ax.set(ylabel='Counterbalanced detection accuracy (95% CI)',ylim=(0,1),title='Layer-32 intervention pilot');fig.tight_layout();fig.savefig('figures/intervention.png',dpi=180);plt.close(fig)
if __name__=='__main__':main()
