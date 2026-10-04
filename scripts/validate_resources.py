"""Validate locally gathered resources without running any model or API."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,re,subprocess,sys
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
assert Path.cwd()==root and (root/'.git').exists()
assert Path(sys.prefix).resolve()==root/'.venv', 'Use the project .venv interpreter'
required=['STATE.md','planning.md','literature_review.md','resources.md','papers/README.md','datasets/.gitignore','datasets/README.md','code/README.md','pyproject.toml','uv.lock','notes/reading_log.md']
for name in required:assert Path(name).is_file() and Path(name).stat().st_size, name
papers=json.loads(Path('notes/papers_catalog.json').read_text());data=json.loads(Path('datasets/manifest.json').read_text());repos=json.loads(Path('code/manifest.json').read_text())
assert len(papers)==23 and sum(r['user_supplied'] for r in papers)==10
assert len({r['dataset'] for r in data})==4 and len(data)==5
assert len(repos)==5
pdf_checks=[]
for r in papers:
 p=Path(r['file']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
 reader=PdfReader(p);assert len(reader.pages)==r['pages']
 for page in reader.pages:assert page.mediabox.width>0 and page.mediabox.height>0
 chunks=sorted(Path('papers/pages').glob(r['id']+'_chunk_*.pdf'))
 assert sum(len(PdfReader(c).pages) for c in chunks)==r['pages'],r['id']
 pdf_checks.append({'id':r['id'],'pages':r['pages'],'chunks':len(chunks),'sha256':'match'})
for r in data:
 p=Path(r['path']);assert p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
 ignored=subprocess.run(['git','check-ignore','-q',str(p)]).returncode==0;assert ignored,p
 assert Path(r['sample_path']).stat().st_size<100000
 assert subprocess.run(['git','check-ignore','-q',r['sample_path']]).returncode==1,r['sample_path']
repo_checks=[]
for r in repos:
 sha=subprocess.check_output(['git','-C',r['path'],'rev-parse','HEAD'],text=True).strip();assert sha==r['commit']
 assert subprocess.check_output(['git','-C',r['path'],'status','--porcelain'],text=True).strip()==''
 assert subprocess.run(['git','check-ignore','-q',r['path']+'/']).returncode==0
 repo_checks.append({'path':r['path'],'commit':sha,'working_tree':'clean'})
for p in Path('scripts').glob('*.py'):ast.parse(p.read_text(),filename=str(p))
broken=[]
for file in ['resources.md','literature_review.md','planning.md','papers/README.md','datasets/README.md','code/README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',Path(file).read_text()):
  if target.startswith(('https://','http://','#','mailto:')):continue
  dest=Path(file).parent/target.split('#')[0]
  if dest == Path('notes/resource_validation.json'):continue  # This report is generated after the checks.
  if not dest.exists():broken.append([file,target])
assert not broken,broken
# Deep-reading note count must cover every chunk for each paper marked fully read.
log=Path('notes/reading_log.md').read_text();sections=re.split(r'(?m)^## ',log)[1:];reading=[]
for r in papers:
 if r['reading']!='all chunks':continue
 sec=next(s for s in sections if s.startswith(r['id']))
 notes=len(re.findall(r'(?m)^- (?:\d{3}\b|Chunk \d+\b)',sec))
 expected=(r['pages']+2)//3
 assert notes==expected,(r['id'],notes,expected)
 reading.append({'id':r['id'],'chunks_noted':notes,'expected':expected})
validation=json.loads(Path('datasets/validation.json').read_text())
assert validation['writingprompts']['rows']==15138 and validation['freeinstruct']['rows']==1212
assert validation['suppression_concepts']['concepts']==17
report={'timestamp':datetime.now(timezone.utc).isoformat(),'status':'PASS','python':sys.version,'environment':sys.prefix,'papers':pdf_checks,'deep_reading_coverage':reading,'dataset_files':len(data),'source_datasets':4,'raw_dataset_bytes':sum(x['bytes'] for x in data),'all_data_hashes_match':True,'all_raw_data_git_ignored':True,'samples_under_100KB_and_visible_to_git':True,'repositories':repo_checks,'required_documents_present':required,'markdown_local_links':'pass','scope':'Resource integrity and documentation only; no model experiments or upstream runtime tests'}
Path('notes/resource_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['status','timestamp','source_datasets','dataset_files','raw_dataset_bytes','scope']},indent=2))
