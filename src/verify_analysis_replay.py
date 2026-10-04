"""Run all saved-output analyses twice and compare deterministic artifact hashes."""
import subprocess,hashlib,json,time,sys
from pathlib import Path

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    assert Path('STATE.md').exists();Path('STATE.md').read_text()
    files=['results/analysis.json','results/literal_analysis.json','results/diagnostics_analysis.json','results/direction_calibrated.json','results/outline_and_truncation.json','results/likelihood_analysis.json','results/mechanism/probe_diagnostics.json','results/mechanism/centered_decoding.json','results/mechanism/early_literal_association.json','results/paired_scores.csv','results/likelihood_pair_scores.csv','figures/leakage.png','figures/literal_disclosure.png','figures/plot_forecasts.png','figures/centered_decoding.png']
    raw=['results/model_outputs/stories.jsonl','results/model_outputs/judgments.jsonl'];before={p:digest(p) for p in raw};runs=[];hashes=[]
    for i in range(2):
        start=time.time()
        with open(f'logs/analysis_replay_{i+1}.log','w') as f:p=subprocess.run(['bash','src/reanalyze.sh'],stdout=f,stderr=subprocess.STDOUT)
        runs.append({'pass':i+1,'returncode':p.returncode,'seconds':time.time()-start});print('Analysis pass',i+1,'returncode',p.returncode,flush=True)
        if p.returncode:
            Path('results/analysis_replay.json').write_text(json.dumps({'identical':False,'runs':runs},indent=2));sys.exit(p.returncode)
        hashes.append({p:digest(p) for p in files})
    differences=[p for p in files if hashes[0][p]!=hashes[1][p]];raw_unchanged=before=={p:digest(p) for p in raw}
    out={'identical':not differences and raw_unchanged,'differences':differences,'raw_outputs_unchanged':raw_unchanged,'runs':runs,'sha256':hashes[1]};Path('results/analysis_replay.json').write_text(json.dumps(out,indent=2));print('Identical:',out['identical'],flush=True)
    if not out['identical']:sys.exit(1)
if __name__=='__main__':main()
