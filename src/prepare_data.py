"""Build deterministic, disjoint premise units without consulting writer outputs."""
from pathlib import Path
import json,random,re
import pandas as pd
SEED=20261004
rng=random.Random(SEED)
words=[x['word'] for x in json.loads(Path('datasets/derived/secret_words.json').read_text())[:15]]
df=pd.read_parquet('datasets/writingprompts/test.parquet')
premises=[]
for p in df.prompt.drop_duplicates():
    p=re.sub(r'^\s*\[[^]]+\]\s*','',p).strip()
    # Short premises; literal secret exclusions predeclared. Semantic overlap remains audited.
    if 12<=len(p.split())<=65 and not any(re.search(r'\b'+re.escape(w)+r'\b',p,re.I) for w in words): premises.append(p)
rng.shuffle(premises)
units=[]
secrets=words*6;rng.shuffle(secrets)
for i,(p,w) in enumerate(zip(premises,secrets)):
    units.append({'id':f'word_{i:03d}','task':'word','premise':p,'secret':w,'decoy':words[(words.index(w)+7)%15],'family':w,'source':'WritingPrompts test; original row text cleaned only'})
# Counterfactual future twists; common setup does not select an outcome.
plots=[
('A restoration worker meets the new manager at a small museum before an exhibition.', 'The manager is the anonymous donor who paid for the restoration.', 'The manager is an undercover investigator examining the museum accounts.'),
('A traveler shares a waiting room with a quiet stranger during a delayed departure.', 'The stranger is the traveler\'s long-lost sibling.', 'The stranger is a novelist gathering material for a book.'),
('A cook begins work at a neighborhood restaurant and meets its regular customer.', 'The customer is the restaurant\'s secret owner.', 'The customer is a food critic using an assumed name.'),
('A gardener is hired to prepare an estate for a weekend gathering.', 'The gathering is a surprise wedding.', 'The gathering is a farewell party before the estate is sold.'),
('A courier delivers a sealed parcel to a retired teacher.', 'The parcel contains letters the teacher wrote decades ago.', 'The parcel contains a medal awarded to the teacher\'s parent.'),
('A mechanic is asked to repair an old vehicle for a visitor.', 'The visitor intends to donate the vehicle to a museum.', 'The visitor intends to drive the vehicle to a family reunion.'),
('A stagehand helps an unfamiliar performer prepare for a small-town show.', 'The performer is the stagehand\'s former schoolteacher in disguise.', 'The performer is a famous actor traveling under another name.'),
('A librarian helps a visitor locate a volume in the closed stacks.', 'The visitor is searching for a message left by a deceased friend.', 'The visitor is checking a printing error for a research project.'),
('A shopkeeper receives an invitation to attend a meeting at the town hall.', 'The meeting will announce that the shopkeeper has won a civic award.', 'The meeting will reveal plans to move the town market.'),
('A volunteer works with a new colleague to prepare a community room.', 'The colleague is the volunteer\'s anonymous online friend.', 'The colleague is the incoming director of the community center.'),
('A surveyor joins a local guide to inspect an unused building.', 'The building will become a free school.', 'The building will become a rehearsal space for local musicians.'),
('A tailor makes alterations to an outfit for a nervous client.', 'The client is preparing to perform in a play for the first time.', 'The client is preparing to meet an estranged parent.')]
for family,(p,a,b) in enumerate(plots):
 for repeat in range(5):
    target=(family+repeat)%2
    units.append({'id':f'plot_{family:02d}_{repeat}','task':'plot','premise':p+f' Set the scene in { ["early spring","midsummer","late autumn","midwinter","early September"][repeat]}.','secret':[a,b][target],'candidates':[a,b],'target':target,'family':f'plot_{family:02d}','source':'New investigator-authored synthetic counterfactual fixture; not human validated'})
assert len(units)==150 and len({u['id'] for u in units})==150
Path('results/units.json').write_text(json.dumps(units,indent=2))
Path('results/data_validation.json').write_text(json.dumps({'word_units':90,'unique_word_premises':len(set(x['premise'] for x in units if x['task']=='word')),'secrets':15,'plot_units':60,'plot_families':12,'seed':SEED,'eligible_source_premises':len(premises),'plot_validation':'synthetic, unvalidated; cluster inference by 12 families'},indent=2))
print('Prepared',len(units),'units')
