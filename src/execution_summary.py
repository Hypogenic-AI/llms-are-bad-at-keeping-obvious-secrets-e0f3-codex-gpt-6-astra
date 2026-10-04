"""Summarize recorded local work; report no invented cloud dollar cost."""
import json,time
from pathlib import Path
from datetime import datetime,timezone
from behavior import read

def main():
    names=['outlines','outlines_length_pilot','stories','stories_before_length_fix','anchor_stories','judgments','anchor_gemma_judgments','anchor_qwen_judgments','plot_forecasts','target_blind_judgments','quality']
    rows=[]
    for name in names:
        records=read('results/model_outputs/'+name+'.jsonl')
        rows.append({'artifact':name,'rows':len(records),'output_tokens':sum(r.get('tokens',0) for r in records),'truncated':sum(r.get('truncated',False) for r in records),'distinct_recorded_batch_seeds':len({r.get('seed') for r in records})})
    # The archived story file shares 448 retained rows with primary outputs.
    combined=read('results/model_outputs/stories_before_length_fix.jsonl')+read('results/model_outputs/stories.jsonl');unique={(r['id'],r['seed']):r for r in combined}
    batches={}
    for r in unique.values():batches[r['seed']]=max(batches.get(r['seed'],0),r['seconds_batch'])
    start=datetime.fromisoformat('2026-10-04T03:56:16.975924+00:00');now=datetime.now(timezone.utc)
    out={'session_start_utc':start.isoformat(),'summary_time_utc':now.isoformat(),'elapsed_hours':(now-start).total_seconds()/3600,'main_writer_unique_generations_including_superseded':len(unique),'main_writer_sum_recorded_batch_seconds':sum(batches.values()),'artifact_counts':rows,'stages':json.load(open('results/stage_timings.json')),'successful_paid_api_inference_calls':0,'api_inference_cost_usd':0,'local_gpu_cost_usd':None,'note':'Local hardware cost/energy not metered. Timing is actual recorded wall time, no CPU-vs-GPU training comparison: no training of model weights was performed. Archived story outputs overlap primary data; do not sum their rows as independent observations.'}
    Path('results/execution_summary.json').write_text(json.dumps(out,indent=2));print(out['elapsed_hours'],out['main_writer_unique_generations_including_superseded'])
if __name__=='__main__':main()
