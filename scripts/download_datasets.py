"""Pinned resource download and structural validation; run from repository root."""
import csv,hashlib,json
from pathlib import Path
import requests
import pyarrow.parquet as pq
root=Path(__file__).resolve().parents[1]
assert Path.cwd()==root and (root/'.git').exists()
items=[
('suppression_concepts','concepts.json','https://raw.githubusercontent.com/rramnauth2220/representational-suppression/1b44dfc61c6e7c3acb21874a940670238bf44d54/concepts.json','CC BY 4.0 concept library; Apache-2.0 code'),
('freeinstruct','freeinstruct.json','https://raw.githubusercontent.com/Chacioc/Concise-SAE/ac735478607ebecf3b1ebc4c34c57279c12956d9/data/freeinstruct/freeinstruct.json','CC BY-NC 4.0 stated for data in paper Appendix D; no repository LICENSE'),
('reboundbench','prompts_negation.csv','https://raw.githubusercontent.com/cesium132dot9/Dont-Think-of-the-White-Bear/c6187468e380fc44869ddfd414c8efcd46d94da9/data/prompts_negation.csv','No explicit repository license found'),
('reboundbench','prompts_multi_question.csv','https://raw.githubusercontent.com/cesium132dot9/Dont-Think-of-the-White-Bear/c6187468e380fc44869ddfd414c8efcd46d94da9/data/prompts_multi_question.csv','No explicit repository license found'),
('writingprompts','test.parquet','https://huggingface.co/datasets/euclaise/writingprompts/resolve/35f0aa359452ba8147b34d925684fccee26679cc/data/test-00000-of-00001-16503b0c26ed00c6.parquet','Mirror card MIT; original Reddit text rights not independently resolved')]
records=[]
for name,file,url,license in items:
 print(root,flush=True);assert (root/'.git').exists()
 d=Path('datasets')/name;d.mkdir(exist_ok=True);p=d/file
 if not p.exists():
  r=requests.get(url,timeout=180);r.raise_for_status();p.write_bytes(r.content)
 rec=dict(dataset=name,path=str(p),source=url,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),license=license)
 if p.suffix=='.parquet':
  t=pq.read_table(p);rec.update(rows=t.num_rows,columns=t.column_names,nulls={k:t[k].null_count for k in t.column_names});sample=t.slice(0,3).to_pylist()
 elif p.suffix=='.csv':
  rows=list(csv.DictReader(p.open()));rec.update(rows=len(rows),columns=list(rows[0]),empty_cells=sum(v in ('',None) for row in rows for v in row.values()));sample=rows[:3]
 else:
  data=json.loads(p.read_text());rec.update(top_type=type(data).__name__,top_length=len(data));sample=data[:2] if isinstance(data,list) else {k:data[k] for k in list(data)[:1]}
 rec['sample_path']=str(d/(p.stem+'_sample.json'));Path(rec['sample_path']).write_text(json.dumps(sample,indent=2,ensure_ascii=False));assert Path(rec['sample_path']).stat().st_size<100000
 print(json.dumps(rec),flush=True);records.append(rec)
Path('datasets/manifest.json').write_text(json.dumps(records,indent=2))
