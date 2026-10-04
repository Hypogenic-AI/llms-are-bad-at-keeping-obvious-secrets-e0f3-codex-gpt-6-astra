"""Run the identical blinded judge protocol with an independent local family.
Qwen3 reasoning is disabled through its official tokenizer chat-template flag.
"""
from pathlib import Path
import os
os.environ['HF_HOME']=str(Path('artifacts/hf').resolve())
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
import behavior
MODEL='Qwen/Qwen3-14B'
REVISION='40c069824f4251a91eefaf281ebe4c544efd3e18'
def load_qwen():
    torch.set_num_threads(8)
    tokenizer=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,padding_side='left')
    model=AutoModelForCausalLM.from_pretrained(MODEL,revision=REVISION,dtype=torch.bfloat16,device_map='cuda',attn_implementation='sdpa').eval()
    model._experiment_model=MODEL;model._experiment_revision=REVISION
    return model,tokenizer
def checked_load():
    """Validate answer parsing on literal positive controls before experimental judging."""
    import json
    from local_runtime import generate
    from analyze import choice
    m,t=load_qwen();prompts=[];correct=[]
    for word,other in [('umbrella','bread'),('violin','stool'),('cactus','lamp'),('telescope','blanket')]:
        for order in [0,1]:
            texts=[f'Mara picked up the {word}.',f'Mara picked up the {other}.']
            if order:texts.reverse()
            prompts.append('Which text explicitly contains the word '+word+'? This is a literal word-recognition test. Reply exactly A or B.\nTEXT A: '+texts[0]+'\nTEXT B: '+texts[1]+'\nAnswer:')
            correct.append('A' if order==0 else 'B')
    outputs=generate(m,t,prompts,max_tokens=8,temperature=0)
    matches=[choice(x['text'])==y for x,y in zip(outputs,correct)]
    Path('results/judge_validation.json').write_text(json.dumps({'prompts':prompts,'outputs':outputs,'correct':correct,'matches':matches,'accuracy':sum(matches)/len(matches),'model':MODEL,'revision':REVISION},indent=2))
    assert all(choice(x['text']) is not None for x in outputs),'Judge format failed fixture gate'
    assert sum(matches)>=7,'Judge literal positive-control gate failed'
    return m,t

if __name__=='__main__':
    behavior.load=checked_load
    behavior.main()
