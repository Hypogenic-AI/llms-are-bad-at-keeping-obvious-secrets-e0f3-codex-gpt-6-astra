"""Offline invariants for inference units, scoring and counterbalancing."""
import json
from pathlib import Path
import numpy as np
from analyze import choice,estimate
from behavior import story_prompt
units=json.loads(Path('results/units.json').read_text())
assert len({u['id'] for u in units})==len(units)
assert choice('A')=='A' and choice(' B.')=='B'
assert choice('Answer: b')=='B'
assert choice('Answer: A and B') is None
assert choice('A or B') is None and choice('Neither') is None
u=units[0]
p=story_prompt(u,'outline',True,'ONE TWO','THREE FOUR')
q=story_prompt(u,'outline',False,'ONE TWO','THREE FOUR')
assert u['secret'] in p and u['secret'] not in q
assert 'ONE TWO' in p and 'ONE TWO' in q
assert estimate([0,0,0])['mean']==0
assert estimate([1,0],center=.5)['p']==1
# A judge that always chooses A scores exactly chance after order reversal.
assert np.mean([choice('A')==correct for correct in ['A','B']])==.5

# Regression: failed parses remain missing after pandas string inference.
import pandas as pd
import numpy as np
from analyze import correct_score
parsed=pd.Series([choice("A"),choice("ambiguous response")])
scored=[correct_score(a,"A") for a in parsed]
assert scored[0]==1 and np.isnan(scored[1])
assert pd.Series(scored).count()==1

print('Protocol invariant checks passed')
