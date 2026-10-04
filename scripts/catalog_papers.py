import re,json,html,hashlib
from pathlib import Path
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
assert Path.cwd()==root and (root/'.git').exists()
provided={x['id'] for x in json.loads(Path('notes/paper_manifest.json').read_text())}
records=[]
for p in sorted(Path('papers').glob('*.pdf')):
 id=p.stem;s=Path(f'notes/{id}_metadata.html').read_text()
 def meta(k):return [html.unescape(x) for x in re.findall(r'<meta name="citation_'+k+r'" content="([^"]*)"',s)]
 records.append(dict(id=id,title=' '.join(meta('title')),authors=meta('author'),date=meta('date'),file=str(p),pages=len(PdfReader(p).pages),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reading='all chunks' if id in provided|{'2605.28639','2604.00209','2505.16505'} else 'abstract screening; selected sections where relevant',user_supplied=id in provided))
Path('notes/papers_catalog.json').write_text(json.dumps(records,indent=2))
lines=['# Downloaded papers','',f'{len(records)} original PDFs; downloaded 2026-10-04. All ten user-supplied papers were read in full using three-page PDF chunks. See [reading notes](../notes/reading_log.md) and [synthesis](../literature_review.md). Latest available versions are preserved by SHA-256 in [manifest](../notes/papers_catalog.json); filenames are arXiv IDs.','', '|Paper / authors|Year|Local PDF|Pages|Reading|','|---|---|---|---:|---|']
for r in records:
 lines.append(f"|[{r['title']}](https://arxiv.org/abs/{r['id']}) — {'; '.join(r['authors'])}|{r['date'][0][:4] if r['date'] else r['id'][:2]}|[{r['id']}]({r['id']}.pdf)|{r['pages']}|{'Supplied; ' if r['user_supplied'] else ''}{r['reading']}|")
lines+=['','## Reproduce','Run `.venv/bin/python scripts/gather_papers.py`, `scripts/gather_additional.py`, `scripts/gather_foundational.py`, and `scripts/gather_planning.py` from the workspace root. DOC (2212.10077) was fetched directly from https://arxiv.org/pdf/2212.10077. Original version snapshots may differ on future downloads: check the manifest hashes.','', 'Chunk PDFs and page manifests are under `pages/`. Page images and extracted text are auxiliary reading aids under `../notes/`; originals remain authoritative.']
Path('papers/README.md').write_text('\n'.join(lines)+'\n')
selected={0:'2501.19398',4:'2605.10794',5:'2402.17119',12:'2604.09854',14:'2210.06774',20:'2605.28639',22:'2604.00209',25:'2607.23379',27:'1805.04833',28:'1811.05701',78:'2604.12493',93:'2505.16505',105:'2511.00180'}
raw=json.loads(Path('logs/paper_finder_retry.json').read_text())['papers']
for i,p in enumerate(raw):
 p['search_index']=i;p['decision']='downloaded' if i in selected else 'not selected';p['resolved_arxiv']=selected.get(i)
 p['screening_reason']='Direct secret/planning/probing method or usable benchmark' if i in selected else 'Lower priority for the three-direction scope: adjacent generation, games, UX or unrelated methods; no distinct essential resource identified in title/abstract screening'
Path('notes/search_screening.json').write_text(json.dumps(raw,indent=2))
