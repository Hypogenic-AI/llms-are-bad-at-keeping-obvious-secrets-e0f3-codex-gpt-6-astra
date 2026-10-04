"""Audit artifact completeness and invariants; does not replace scientific review."""
import json,hashlib,re,sys
from pathlib import Path

def read(name):return [json.loads(x) for x in Path(name).read_text().splitlines()]
def main():
    checks={};units=json.loads(Path('results/units.json').read_text());jobs=json.loads(Path('results/story_jobs.json').read_text());stories=read('results/model_outputs/stories.jsonl');judges=read('results/model_outputs/judgments.jsonl')
    checks['expected_units']=len(units)==150
    checks['complete_unique_stories']=len(stories)==1080 and len({r['id'] for r in stories})==1080
    checks['job_ids_match_outputs']={r['id'] for r in jobs}=={r['id'] for r in stories}
    checks['nonempty_stories']=all(r['text'].strip() for r in stories)
    checks['pinned_writer']=all(r['model']=='google/gemma-3-12b-it' and r['revision']=='96b6f1eccf38110c56df3a15bffe176da04bfd80' for r in stories)
    checks['context_lengths_match']=json.loads(Path('results/full_prompt_length_audit.json').read_text())['all_equal']
    checks['complete_unique_judgments']=len(judges)==1080 and len({r['id'] for r in judges})==1080
    checks['independent_judge']=all(r['model']=='Qwen/Qwen3-14B' and r['revision']=='40c069824f4251a91eefaf281ebe4c544efd3e18' for r in judges)
    pairs={}
    for r in judges:pairs.setdefault((r['unit'],r['condition']),set()).add(r['order'])
    checks['both_orders']=all(x=={0,1} for x in pairs.values()) and len(pairs)==540
    checks['all_main_judgments_parse']=json.loads(Path('results/analysis.json').read_text())['malformed_judgments']==0
    checks['positive_judge_controls']=json.loads(Path('results/judge_validation.json').read_text())['accuracy']>=.875
    checks['phase_docs_present']=all(Path(x).exists() for x in ['planning.md','REPORT.md','README.md','results/analysis.json','figures/leakage.png'])
    report=Path('REPORT.md').read_text() if Path('REPORT.md').exists() else ''
    checks['report_has_results_and_limits']='Results' in report and 'Limitations' in report
    p=Path('results/smoke_replay.json');checks['exact_model_replay']=p.exists() and all(json.loads(p.read_text())['exact_text_matches'])
    recorded=json.loads(Path('results/recorded_replay.json').read_text())
    checks['exact_recorded_batch_replay']=sum(len(r['matches']) for r in recorded)>=32 and all(all(r['matches']) for r in recorded)
    # Verify representations/interventions are actual recorded data, not placeholders.
    probe=json.loads(Path('results/mechanism/decoding.json').read_text())
    checks['complete_probe_grid']=len(probe)==27 and all(r['n_train']>0 and r['n_test']>0 for r in probe)
    checks['disjoint_probe_contexts']=all(all(c>=18 for c in r['test_contexts']) for r in probe)
    gate=json.loads(Path('results/mechanism/intervention_gate.json').read_text())
    if gate['proceed']:
        edits=read('results/model_outputs/interventions.jsonl');traces=read('results/mechanism/online_trace.jsonl')
        checks['complete_intervention_grid']=len(edits)==240 and len({r['id'] for r in edits})==240
        checks['online_traces_match_interventions']={r['id'] for r in edits}=={r['id'] for r in traces} and len(traces)==240
        checks['online_traces_have_steps']=all(r['n_valid_steps']>0 for r in traces)
        checks['intervention_analysis_exists']=Path('results/intervention_analysis.json').exists()
    checks['secondary_likelihood_complete']=len(read('results/model_outputs/choice_likelihoods.jsonl'))==(1440 if gate['proceed'] else 1200)
    checks['analysis_replay_deterministic']=json.loads(Path('results/analysis_replay.json').read_text())['identical']
    # Scan only experiment-produced text artifacts, without printing credential values.
    import os
    credentials=[os.environ[k] for k in ['HF_TOKEN','OPENROUTER_KEY','OPENAI_API_KEY'] if os.getenv(k)]
    hits=[]
    for parent in ['src','results','logs','notes']:
        for path in Path(parent).rglob('*'):
            if path.is_file() and path.suffix in ['.py','.json','.jsonl','.log','.md','.csv'] and path.stat().st_size<20_000_000:
                text=path.read_text(errors='replace')
                if any(secret in text for secret in credentials):hits.append(str(path))
    checks['no_credential_values_in_artifacts']=not hits
    hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path('results/analysis.json'),Path('results/units.json'),Path('results/model_outputs/stories.jsonl'),Path('results/model_outputs/judgments.jsonl')]}
    out={'checks':checks,'all_pass':all(checks.values()),'credential_hit_paths':hits,'sha256':hashes,'scope':'Completeness, provenance, counterbalancing, replay and documentation. Human validation and generalization are scientific limitations, not passed checks.'}
    Path('results/final_validation.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
    if not out['all_pass']:sys.exit(1)
if __name__=='__main__':main()
