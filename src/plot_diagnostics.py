"""Plot both-order twist forecast accuracy with no-secret and premise controls."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.load(open('results/diagnostics_analysis.json'));rows=r['plot_forecast_summaries'];order=['baseline','outline','context'];fig,ax=plt.subplots(figsize=(7,4))
for present,offset,color,label in [(True,-.18,'#806f9e','Private future twist supplied'),(False,.18,'#999999','No private twist')]:
 s=[next(x for x in rows if x['condition']==c and x['secret_present']==present) for c in order];y=np.array([x['mean'] for x in s]);pos=np.arange(3)+offset
 ax.bar(pos,y,.34,color=color,label=label);ax.errorbar(pos,y,yerr=[y-np.array([x['low'] for x in s]),np.array([x['high'] for x in s])-y],fmt='none',capsize=3,color='black')
prior=next(x for x in rows if x['condition']=='premise_only');ax.axhline(prior['mean'],ls=':',color='#c58e45',label='Premise only');ax.axhline(.5,ls='--',color='black',alpha=.4)
ax.set(xticks=np.arange(3),xticklabels=order,ylabel='Assigned-twist forecast accuracy (95% CI)',ylim=(0,1));ax.legend(frameon=False,fontsize=9);fig.tight_layout();fig.savefig('figures/plot_forecasts.png',dpi=180)
