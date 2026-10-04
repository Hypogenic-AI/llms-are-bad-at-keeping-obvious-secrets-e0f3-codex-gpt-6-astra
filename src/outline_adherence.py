"""Descriptive lexical coupling to supplied outline, plus truncation sensitivity."""
import json
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from behavior import read
from analyze import estimate

def main():
    plans={r['id']:r['text'] for r in read('results/model_outputs/outlines.jsonl')};rows=read('results/model_outputs/stories.jsonl')
    keys=list(plans);v=TfidfVectorizer(stop_words='english');x=v.fit_transform([plans[k] for k in keys]+[r['text'] for r in rows]);index={k:i for i,k in enumerate(keys)}
    out=[]
    for i,r in enumerate(rows):
        cosine=float(x[len(keys)+i].multiply(x[index[r['unit']]]).sum());out.append({'id':r['id'],'unit':r['unit'],'family':r['family'],'task':r['task'],'condition':r['condition'],'secret_present':r['secret_present'],'outline_cosine':cosine,'truncated':r['truncated']})
    df=pd.DataFrame(out);df.to_csv('results/outline_overlap.csv',index=False)
    summaries=df.groupby(['task','condition','secret_present']).outline_cosine.mean().reset_index().to_dict(orient='records')
    scores=pd.read_csv('results/paired_scores.csv');bad=set(df[df.truncated].unit+'|'+df[df.truncated].condition)
    scores['complete']=~(scores.unit+'|'+scores.condition).isin(bad)
    sensitivity=[]
    for (task,c),d in scores[scores.complete].groupby(['task','condition']):
        sensitivity.append({'task':task,'condition':c,**estimate(d.score,d.family if task=='plot' else None,center=.5)})
    Path('results/outline_and_truncation.json').write_text(json.dumps({'outline_overlap_means':summaries,'excluding_truncated_pairs':sensitivity,'excluded_pairs':len(bad),'note':'Secondary sensitivity only; primary analysis retains every parseable pair, including truncated stories.'},indent=2))
    print('Outline overlap and truncation diagnostics saved')
if __name__=='__main__':main()
