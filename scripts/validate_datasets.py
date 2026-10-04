import csv,json,collections
from pathlib import Path
import pyarrow.parquet as pq
assert (Path.cwd()/'.git').exists()
r={}
c=json.loads(Path('datasets/suppression_concepts/concepts.json').read_text())
r['suppression_concepts']={'concepts':len(c),'fields':list(next(iter(c.values()))),'list_counts':{k:sum(len(v.get(k,[])) for v in c.values()) for k in next(iter(c.values())) if isinstance(next(iter(c.values()))[k],list)},'missing_fields':sum(set(next(iter(c.values())))-set(v)!=set() for v in c.values())}
f=json.loads(Path('datasets/freeinstruct/freeinstruct.json').read_text());keys=set(f[0]);r['freeinstruct']={'rows':len(f),'fields':sorted(keys),'missing_fields':sum(bool(keys-set(v)) for v in f),'blank_or_null_cells':sum(v in ('',None) for row in f for v in row.values()),'duplicate_stories':len(f)-len({row['story'] for row in f}),'first100_types':{k:sorted({type(row.get(k)).__name__ for row in f[:100]}) for k in keys}}
for p in Path('datasets/reboundbench').glob('*.csv'):
 rows=list(csv.DictReader(p.open()));r[p.stem]={'rows':len(rows),'unique_ids':len({v['id'] for v in rows}),'empty_cells':sum(v in ('',None) for row in rows for v in row.values()),'first100_types':{k:sorted({type(v[k]).__name__ for v in rows[:100]}) for k in rows[0]}}
t=pq.read_table('datasets/writingprompts/test.parquet');rows=t.to_pylist();r['writingprompts']={'rows':len(rows),'schema':str(t.schema),'nulls':{k:t[k].null_count for k in t.column_names},'empty_strings':sum(v=='' for row in rows for v in row.values()),'duplicate_prompts':len(rows)-len({v['prompt'] for v in rows}),'first100_min_chars':{k:min(len(row[k]) for row in rows[:100]) for k in t.column_names},'first100_max_chars':{k:max(len(row[k]) for row in rows[:100]) for k in t.column_names}}
Path('datasets/validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
