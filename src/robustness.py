"""Prespecified direction calibration and text/length diagnostics."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from analyze import estimate

def main():
    scores=pd.read_csv('results/paired_scores.csv');units=json.loads(Path('results/units.json').read_text());u={x['id']:x for x in units};rows=[]
    for (task,c),d in scores.groupby(['task','condition']):
        if task=='word':cal=d.unit.map(lambda s:int(s.split('_')[1])<30)
        else:cal=d.unit.map(lambda s:int(s.split('_')[1])<4)
        calibration=d[cal];test=d[~cal];sign=-1 if calibration.score.mean()<.5 else 1
        values=test.score if sign==1 else 1-test.score
        e=estimate(values,test.family if task=='plot' else None,center=.5)
        rows.append({'task':task,'condition':c,'calibration_n':len(calibration),'calibration_accuracy':float(calibration.score.mean()),'flip':sign==-1,**e})
    Path('results/direction_calibrated.json').write_text(json.dumps(rows,indent=2))
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
