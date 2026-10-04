"""Display observed exact disclosure rates, separate from judge detection."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.load(open('results/literal_analysis.json'));order=['baseline','outline','context','decoy'];fig,ax=plt.subplots(figsize=(7,4))
for present,shift,color,label in [(True,-.18,'#806f9e','Secret supplied'),(False,.18,'#aaaaaa','No secret supplied')]:
 rows=[next(x for x in r['summaries'] if x['condition']==c and x['secret_present']==present) for c in order];y=np.array([x['mean'] for x in rows]);positions=np.arange(4)+shift
 ax.bar(positions,y,width=.34,color=color,label=label);ax.errorbar(positions,y,yerr=[y-np.array([x['low'] for x in rows]),np.array([x['high'] for x in rows])-y],fmt='none',color='black',capsize=3)
ax.set(xticks=np.arange(4),xticklabels=order,ylabel='Exact secret-word disclosure rate (95% CI)',ylim=(0,.55));ax.legend(frameon=False);fig.tight_layout();fig.savefig('figures/literal_disclosure.png',dpi=180)
