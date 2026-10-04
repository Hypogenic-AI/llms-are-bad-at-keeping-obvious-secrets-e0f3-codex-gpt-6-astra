"""Audit final inputs using the actual writer encoding, not an assumed template."""
from pathlib import Path
import os
os.environ['HF_HOME']=str(Path('artifacts/hf').resolve())
import json,collections
import pandas as pd
from transformers import AutoTokenizer
from local_runtime import MODEL,REVISION,encode_prompt
from behavior import read

def main():
    t=AutoTokenizer.from_pretrained(MODEL,revision=REVISION);jobs=json.loads(Path('results/story_jobs.json').read_text());lookup={(r['unit'],r['condition'],r['secret_present']):r for r in jobs};rows=[];deltas=[]
    for r in jobs:
        actual=encode_prompt(t,r['prompt']);canonical=t.apply_chat_template([{'role':'user','content':r['prompt']}],tokenize=True,add_generation_prompt=True)
        rows.append({'id':r['id'],'unit':r['unit'],'condition':r['condition'],'secret_present':r['secret_present'],'actual_prompt_tokens':len(actual),'canonical_template_tokens':len(canonical),'leading_bos_count':next((i for i,x in enumerate(actual) if x!=t.bos_token_id),len(actual))})
        if r['condition']=='outline':deltas.append(len(encode_prompt(t,lookup[r['unit'],'context',r['secret_present']]['prompt']))-len(actual))
    pd.DataFrame(rows).to_csv('results/prompt_token_lengths.csv',index=False)
    byid={r['id']:r for r in jobs};stories=read('results/model_outputs/stories.jsonl')
    consistent=all(r['prompt']==byid[r['id']]['prompt'] for r in stories)
    out={'n_matched_pairs':len(deltas),'difference_counts':dict(collections.Counter(deltas)),'all_equal':all(x==0 for x in deltas),'cached_prompt_consistency':consistent,'writer_bos_counts':dict(collections.Counter(r['leading_bos_count'] for r in rows)),'method':'Actual generation path: render template, then tokenizer with add_special_tokens=True. The constant duplicate Gemma BOS is included.'}
    Path('results/full_prompt_length_audit.json').write_text(json.dumps(out,indent=2));assert out['all_equal'] and consistent
    print(out)
if __name__=='__main__':main()
