"""Local source/PDF checks; run from the repository root."""
from pathlib import Path
import re, json, hashlib
import pymupdf
p=Path('paper_draft')
main=(p/'main.tex').read_text()
sections=list((p/'sections').glob('*.tex'))
source='\n'.join(f.read_text() for f in sections+list((p/'appendix').glob('*.tex')))
abstract=(p/'sections/abstract.tex').read_text()
abstract=re.sub(r'(?m)^%[^\n]*','',abstract)
abstract=re.sub(r'\\(?:begin|end)\{abstract\}','',abstract)
abstract_words=len(abstract.split())
cited=set()
for block in re.findall(r'\\cite[tp]?\{([^}]+)\}',source): cited.update(block.split(','))
keys=set(re.findall(r'@\w+\{([^,]+),',(p/'references.bib').read_text()))
log=(p/'main.log').read_text()
pdf=pymupdf.open(p/'main.pdf')
checks={
 'exact_author':r'\author{Ari Holtzman and NeuriCo}' in main,
 'requested_style':r'\usepackage[final]{neurips_2025}' in main,
 'clickable_references_package':r'\usepackage[hidelinks]{hyperref}' in main,
 'command_imports':all(r'\input{commands/'+name+'}' in main for name in ['math','general','macros']),
 'all_section_files':len(sections)==7,
 'section_headings':all(r'\section{' in f.read_text() for f in sections if f.stem!='abstract'),
 'standard_neurips_abstract':r'\begin{abstract}' in (p/'sections/abstract.tex').read_text(),
 'abstract_150_250_words':150<=abstract_words<=250,
 'all_citations_resolved':cited==keys,
 'no_latex_errors':'\n!' not in log,
 'no_undefined_references':'undefined' not in log.lower(),
 'no_rerun_required':not re.search(r'Warning[^\n]*(?:Rerun|rerun|changed)', log),
 'no_overfull_boxes':'Overfull' not in log,
 'no_bibtex_warnings':'Warning' not in (p/'build-bibtex.log').read_text(),
 'tables_booktabs':all(all(cmd in f.read_text() for cmd in [r'\toprule',r'\midrule',r'\bottomrule',r'\caption{']) for f in (p/'tables').glob('*.tex')),
 'pdf_has_clickable_links':sum(len(page.get_links()) for page in pdf)>50,
 'figures_unchanged':all(hashlib.sha256((p/'figures'/n).read_bytes()).digest()==hashlib.sha256((Path('figures')/n).read_bytes()).digest() for n in ['literal_disclosure.png','centered_decoding.png']),
 'no_placeholders':not re.search(r'TODO|FIXME|INSERT HERE|Your Paper Title',source),
}
# Inventory names must match the saved 15-word source in order.
words=[x['word'] for x in json.loads(Path('datasets/derived/secret_words.json').read_text())[:15]]
expected=', '.join(words[:-1])+', and '+words[-1]
checks['inventory_matches_manifest']=expected in (p/'appendix/reproducibility.tex').read_text()
# Appendix numeric columns must retain the machine-written table values.
report=Path('results/report_tables.md').read_text()
for block,name in [('likelihood','likelihood'),('likelihood_contrasts','likelihood_contrasts'),('plot','forecasts'),('probe','probes')]:
 part=report.split('## '+block+'\n',1)[1].split('## ',1)[0]
 table=(p/'tables'/f'{name}.tex').read_text().replace(r'\%','%')
 rows=[line for line in part.splitlines() if line.startswith('|') and not line.startswith('|---')][1:]
 # Compare the numeric trailing columns, excluding condition-label reformatting.
 numeric=[]
 for row in rows:
  cells=[x.strip() for x in row.strip('|').split('|')]
  numeric.extend(cells[-(3 if block=='probe' else 2 if block in ['plot','likelihood_contrasts'] else 1):])
 checks['saved_values_'+block]=all(x in table for x in numeric)
summary={'checks':checks,'all_pass':all(checks.values()),'abstract_whitespace_words':abstract_words,'bibliography_entries':len(keys),'pdf_pages':len(pdf),'pdf_link_annotations':sum(len(page.get_links()) for page in pdf),'pdf_sha256':hashlib.sha256((p/'main.pdf').read_bytes()).hexdigest()}
(p/'review/validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
assert all(checks.values())
