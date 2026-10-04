"""Local BF16 Gemma inference with exact prompt and sampling metadata."""
import os
from pathlib import Path
os.environ['HF_HOME'] = str(Path('artifacts/hf').resolve())
import json, time, random
import numpy as np
import torch
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
MODEL='google/gemma-3-12b-it'
REVISION='96b6f1eccf38110c56df3a15bffe176da04bfd80'
SEED=20261004

def load():
    """Load pinned unquantized weights on the available CUDA accelerator."""
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
    torch.set_num_threads(8)
    tok=AutoTokenizer.from_pretrained(MODEL,revision=REVISION,padding_side='left')
    model=Gemma3ForConditionalGeneration.from_pretrained(MODEL,revision=REVISION,dtype=torch.bfloat16,device_map='cuda',attn_implementation='sdpa').eval()
    model._experiment_model=MODEL; model._experiment_revision=REVISION
    return model,tok

def encode_prompt(tok,prompt,model_type='gemma3'):
    """Mirror the recorded generation encoding, including tokenizer-added BOS.
    Gemma's rendered template already contains BOS, so this recorded protocol has
    two BOS tokens. Keep it fixed across conditions and align all probe replays.
    """
    kwargs={'enable_thinking':False} if model_type.startswith('qwen3') else {}
    text=tok.apply_chat_template([{'role':'user','content':prompt}],tokenize=False,add_generation_prompt=True,**kwargs)
    return tok.encode(text,add_special_tokens=True)

def generate(model,tok,prompts,max_tokens=900,seed=SEED,temperature=.8):
    """Generate batches; returned texts exclude prompts and preserve EOS diagnostics."""
    torch.manual_seed(seed)
    texts=[tok.apply_chat_template([{'role':'user','content':p}],tokenize=False,add_generation_prompt=True,**({'enable_thinking':False} if model.config.model_type.startswith('qwen3') else {})) for p in prompts]
    inp=tok(texts,return_tensors='pt',padding=True).to('cuda')
    t=time.time()
    kwargs=dict(max_new_tokens=max_tokens,do_sample=temperature>0,pad_token_id=tok.pad_token_id,use_cache=True)
    if temperature>0: kwargs.update(temperature=temperature,top_p=.95)
    with torch.inference_mode(): out=model.generate(**inp,**kwargs)
    ans=[]
    for row in out[:,inp.input_ids.shape[1]:]:
        ids=row.tolist(); eos=model.generation_config.eos_token_id
        eos=[eos] if isinstance(eos,int) else eos
        end=next((i for i,x in enumerate(ids) if x in eos),len(ids))
        ans.append({'text':tok.decode(ids[:end],skip_special_tokens=True),'tokens':end,'token_ids':ids[:end],'truncated':end==max_tokens,'seconds_batch':time.time()-t})
    return ans

if __name__=='__main__':
    m,t=load(); start=time.time()
    out=generate(m,t,['Write a story of about 450 words about a baker opening a shop. Your secret word is telescope. Do not mention or hint at the secret. Output only the story.']*4,max_tokens=800)
    Path('results/local_smoke.json').write_text(json.dumps({'outputs':out,'seconds':time.time()-start,'gpu_peak_bytes':torch.cuda.max_memory_allocated()},indent=2))
    print('SMOKE',time.time()-start,[x['tokens'] for x in out],flush=True)
