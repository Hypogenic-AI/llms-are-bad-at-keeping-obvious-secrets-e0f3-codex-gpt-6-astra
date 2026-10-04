"""Render report tables directly from saved statistical results."""
from pathlib import Path
import json

def read(p):return json.loads(Path(p).read_text())
def pct(x):return f'{100*x:.1f}%'
def ci(r):return f"{pct(r['mean'])} [{100*r['low']:.1f}, {100*r['high']:.1f}]"
def effect(r):return f"{100*r['mean']:+.1f} [{100*r['low']:+.1f}, {100*r['high']:+.1f}]"
def pval(x):return '<0.0001' if x<.0001 else f'{x:.4f}'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)
def tables():
 a=read('results/analysis.json');l=read('results/literal_analysis.json');d=read('results/diagnostics_analysis.json');c=read('results/mechanism/centered_decoding.json');q=read('results/likelihood_analysis.json')
 out={}
 out['primary']=table(['Task','Condition','Pairs','Detection accuracy [95% CI]'],[[r['task'],r['condition'],r['n_units'],ci(r)] for r in a['summaries']])
 out['contrasts']=table(['Task','Contrast','Difference, percentage points [95% CI]','Holm p'],[[r['task'],r['contrast'],effect(r),pval(r['p_holm'])] for r in a['contrasts']])
 out['literal']=table(['Condition','Secret supplied: exact disclosures / 90','No secret: exact disclosures / 90','Detection without literal pairs [95% CI]'],[[cond,next(r['n_literal'] for r in l['summaries'] if r['condition']==cond and r['secret_present']),next(r['n_literal'] for r in l['summaries'] if r['condition']==cond and not r['secret_present']),ci(next(r for r in l['without_literal_pairs'] if r['condition']==cond))] for cond in ['baseline','outline','context','decoy']])
 out['plot']=table(['Forecast contrast','Complete pairs','Difference, pp [95% CI]','Holm p'],[[r['contrast'],r['n_units'],effect(r),pval(r['p_holm'])] for r in d['plot_forecast_contrasts']])
 raw=read('results/mechanism/decoding.json')
 out['probe']=table(['Condition','Token','Raw layer-32 accuracy','Centered accuracy [95% CI]','Centered shuffled-label accuracy'],[[r['condition'],r['token_position'],pct(next(z['accuracy'] for z in raw if z['condition']==r['condition'] and z['layer']==32 and z['token_position']==r['token_position'])),f"{pct(r['accuracy'])} [{100*r['low']:.1f}, {100*r['high']:.1f}]",pct(r['shuffled_accuracy'])] for r in c['summaries']])
 out['likelihood']=table(['Study','Task','Condition','Order-balanced log-odds decision accuracy [95% CI]'],[[r['study'],r['task'],r['condition'],ci(r)] for r in q['summaries']])
 out['likelihood_contrasts']=table(['Task','Secondary contrast','Difference, pp [95% CI]','Holm p'],[[r['task'],r['contrast'],effect(r),pval(r['p_holm'])] for r in q['contrasts']])
 return out
if __name__=='__main__':
 out=tables();Path('results/report_tables.md').write_text('\n\n'.join('## '+k+'\n\n'+v for k,v in out.items()))
