"""Build final documentation from completed, actual experiment artifacts."""
from pathlib import Path
import json,hashlib

# Narrative interpretations below are specific to this recorded experiment.
EXPECTED_DATA = {'results/analysis.json': '1c6822fe1b327616e46782cd377833d7d1db2b2be35fa8c073892951df2faa48', 'results/literal_analysis.json': '91cac1a8afbdc06a319eadb502d636b6947a2c8971ba03d65530befa80746c41', 'results/diagnostics_analysis.json': 'b0e175b16821d33c4eef5b62e43ee8161f57629a5e4f8101af85a15493940671', 'results/anchor_analysis.json': 'a051475bce3a7da5b4266f3bddfb4f5de2f5192f6d46b91149b16863da5eae77', 'results/likelihood_analysis.json': '31bb9c5d9473ea2a9f50f7e7d3b8d07a680217f051356fbe07fff7e128a70f3b', 'results/mechanism/decoding.json': '418a04ec4b5ad6cd274e2fedb1f27eeff9d801c074e349d7e0a6f820899579ce', 'results/mechanism/centered_decoding.json': '5c7dd63d8495e236eb9837fbccdbb6e06dbaaec43abaa524ff214a0dd197d8fe', 'results/mechanism/margin_correlations.json': '9c62111c0b1ca3d0dd3016c8dbb904fed48f72142a87021f438f7871675395df', 'results/mechanism/early_literal_association.json': 'ae43b50fa4adc6fec26ddd23fd835d16bef9dd58b94755fa60c89c45daf32593', 'results/mechanism/intervention_validation.json': '253a309cf4e9b529b338fa1bffc86d6b06e4fc9f9ba9a2db91a8e992d616dd83', 'results/outline_and_truncation.json': '7956869d28630aaea9933652ce68be3ba7725238d8e589daf11a1efac8a8e88c', 'results/model_outputs/stories.jsonl': 'fbdd18947e74bbf0be871eb405c6a199087361dd7b8797156bc5b241049056cb', 'results/model_outputs/judgments.jsonl': 'a4b9903ddfd6de7eec97295741809d43bb8a465156bd19d1b799485f699722ce'}
from report_tables import tables,pct,pval

def read(p):return json.loads(Path(p).read_text())
def main():
 for path,expected in EXPECTED_DATA.items():
  assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected, f'Results changed: {path}; write a new interpretation rather than reuse this report.'
 t=tables();a=read('results/analysis.json');ex=read('results/execution_summary.json');gate=read('results/mechanism/intervention_gate.json');replay=read('results/recorded_replay.json');assert not gate['proceed'],'Revise report for a run with actual interventions'
 q=read('results/likelihood_analysis.json');anchor=next(r for r in q['summaries'] if r['study']=='anchor');rr=sum(sum(r['matches']) for r in replay);rn=sum(len(r['matches']) for r in replay)
 report=f'''# Do outlines help language models keep secrets?

Exploratory execution report — 4 October 2026. [Plan](planning.md), [decision/correction history](notes/planning_history.md), [raw outputs](results/model_outputs/), and [machine-readable results](results/) accompany this report.

## 1. Executive Summary

We tested secret-blind outlines against a plain secrecy instruction, exactly length-matched irrelevant context, and a decoy-word control using a real local Gemma 3 12B writer. Across 90 word-secret cases, counterbalanced Qwen detection accuracy was **60.6% at baseline, 54.4% with an outline, 63.9% with irrelevant context, and 54.4% with a decoy**. The outline–context contrast was −9.4 percentage points (95% CI −15.0 to −3.9; Holm p=.0155); the outline–baseline contrast did not survive correction. Crucially, this signal largely reflects **literal instruction failures**: the forbidden word appeared in 27/90 baseline stories, 15/90 outline stories, 31/90 context stories, and 10/90 decoy stories. The secondary probability-based detector did not confirm any multiplicity-corrected contrast. This is not a clean replication of the published nonliteral leakage effect.

A prespecified cross-context residual decoder failed its intervention gate: 8.9% accuracy for 15 identities, versus 6.7% chance. A **post hoc counterfactual-centering diagnostic** recovered identity at 82.2%, 91.1%, and 84.4% at early, middle, and late baseline continuation positions. Thus secret-conditioned information is present in controlled residual differences, but the original single-state readout did not generalize reliably. Its baseline midpoint margin correlated with detection scores, while early margins did not predict later literal mentions. Neither association establishes behavioral causation.

The 60 plot cases gave no multiplicity-corrected evidence of an outline benefit. The judge was strongly position-biased, synthetic plot families were not human-validated, and all Gemma inputs contained a constant **duplicated BOS token**, discovered in an encoding audit. These limitations prevent broad claims about normal Gemma behavior or practical privacy. **No behavioral activation-ablation experiment was run:** the readout gate failed, and offline projection checks did not validate selective removal. The supported result is narrower: outlines reduced exact-word disclosure under this recorded protocol; subtle leakage, plot-level generalization, and causal erasure remain unresolved.

## 2. Research Question, Motivation, and Literature

The hypothesis is that external content planning reduces involuntary hints because prose generation no longer needs to prepare its own future. The competing explanation is simpler salience dilution from extra context. This matters for fiction authors withholding twists and for understanding whether suppression instructions remove information or only alter its expression.

Holtzman and West's [Can You Keep a Secret?](https://arxiv.org/abs/2605.10794) supplies the behavioral anchor, 15-word inventory, detection/discrimination distinction, and decoy precedent. Its reported strong Gemma 3 12B effect motivated the historical writer selection instead of a ≤9B model likely to show a floor. Their paper reports no literal secret mentions; our frequent exact disclosures are a material protocol difference, not confirmation of their subtle effect. We use secret-versus-no-secret **detection**, not their different-secret discrimination task.

The pre-gathered [literature review](literature_review.md) also identifies [semantic leakage](https://arxiv.org/abs/2408.06518), [Taboo model organisms](https://arxiv.org/abs/2505.14352), [ironic negation](https://arxiv.org/abs/2511.12381), and [The Attentional White Bear Effect](https://arxiv.org/abs/2605.28639). The latter already probes suppressed concepts: decodability by itself is not novel. Our intended contribution was the outline-versus-context comparison, plot controls, and a utility-preserving causal test. The last component was not achieved. Work on [future-token planning](https://arxiv.org/abs/2404.00859) motivates a mechanism question, but our probes cannot identify planning specifically.

## 3. Experimental Setup and Methodology

### Models, access, and compute

|Role|Exact model|Pinned Hugging Face revision|
|---|---|---|
|Writer and residual model|`google/gemma-3-12b-it`|`96b6f1eccf38110c56df3a15bffe176da04bfd80`|
|Independent judge|`Qwen/Qwen3-14B`|`40c069824f4251a91eefaf281ebe4c544efd3e18`|

The live OpenRouter catalog was queried before selection; snapshots and access attempts are in [notes](notes/live_models.json) and [judge catalog](notes/judge_catalog.json). OpenRouter inference returned a daily-key-limit 403; direct OpenAI authentication also failed. Real, unquantized local checkpoints supplied every model output. These are historical, accessible research models, not a contemporary frontier evaluation. The gated Gemma download succeeded. No simulated agents or invented responses were used.

All work used project `.venv`, `pyproject.toml`, and `uv.lock`: Python 3.12.8, PyTorch 2.8.0+cu128, Transformers 4.57.6, NumPy 2.5.3, pandas 3.0.6, SciPy 1.18.1, scikit-learn 1.9.1. GPU: **RTX A6000, 49,140 MiB reported**, BF16 inference with SDPA. Batches: main stories 32, outlines 24, primary judgments 16, diagnostic judgments 24, controlled residuals 12, free-story replays 8. No model-weight training occurred; logistic probes ran on CPU, so no CPU/GPU training-speed comparison is claimed. Main generation, including superseded outputs, took approximately **{ex['main_writer_sum_recorded_batch_seconds']/60:.1f} minutes** of recorded batch time. Stage timings and output-token counts are in [execution_summary.json](results/execution_summary.json). Successful paid API inference cost was $0; local GPU cost and energy were not metered.

Writer sampling: temperature .8, top_p .95, inherited top_k 64, 850-token ceiling for stories; seed 20261004 with actual batch seeds recorded. Outlines used a 400-token ceiling. Qwen was greedy with thinking disabled and an eight-token answer ceiling; sampling defaults do not affect greedy decoding. Full effective settings are in [generation_config.json](results/generation_config.json).

**Encoding deviation:** rendering the Gemma chat template and then tokenizing with default special tokens produced two BOS tokens. Every writer condition uses this same format; probes and replays reproduce it. This preserves internal comparability but limits external validity. We retained the recorded protocol rather than silently mixing corrected and original encodings. [Token audit](results/tokenization_audit.json).

### Cases and conditions

- **Word secrets:** 90 unique WritingPrompts test premises, six per published secret word. Premises were deduplicated, restricted to 12–65 words, and excluded exact occurrences of any inventory word. Public prompts may have appeared in pretraining; this is not a contamination-free benchmark.
- **Plot secrets:** 60 agent-authored synthetic cases, 12 premise/twist families × five seasonal variants. Two plausible candidate developments were counterbalanced, 30 assignments to each candidate position overall. These fixtures are synthetic and lack human plausibility validation.
- Word conditions were baseline, outline, irrelevant context, and decoy; plot conditions omitted decoy. Each condition produced separate secret-present and no-secret texts: **1,080 main stories, 540 pairs**.
- Outlines specified concrete content without receiving the assigned secret or candidate twists. Assignment already existed in the manifest, so blinding was computational, not chronological. One outline incidentally used its assigned word; one irrelevant reference did likewise. These cases remain in the primary sample.
- Irrelevant context was another premise's outline, truncated/padded to match the **entire actual chat input** of the outline condition, separately for secret/no-secret prompts. All 300 comparisons matched exactly. This controls token count, not semantic content, task effort, or output length.
- A decoy word seven positions away in the inventory was encouraged to influence themes in both secret/no-secret stories. This adapts the published mitigation rather than reproducing its precise prompt.

Exact prompts and assignments are in [story_jobs.json](results/story_jobs.json), [units.json](results/units.json), and [behavior.py](src/behavior.py). Secret instructions said not to mention, reveal, or hint; plot outputs were to stop before revelation. The main story target was about 450 words. Initial outlines exceeded the requested 70–90 words, so the capped pilot was archived and all final outlines regenerated. An input-length audit found a 9–11-token framing mismatch; before any judgments, all 160 affected context outputs were archived and regenerated. The final sample retains 448 unchanged outputs and 632 later outputs with a distinct seed offset. This correction was uniform, not outcome-selected.

An auxiliary free-writing anchor used 60 pairs without premises and both Gemma and Qwen judges. It is separate from the causal outline comparison. Qwen passed eight literal-recognition fixtures, but this did not validate subtle inference: its anchor first-position choice rate was 95.8%.

### Measurements and inference

The primary judge saw the secret and two texts, never their experimental condition. Both orders were evaluated and averaged **within each pair**. Scores are 0, .5, or 1; orders are not independent trials. Invalid order pairs are excluded from inferential scoring; primary judgments had none. Counterbalancing controls inflated positional accuracy but cannot repair low sensitivity. Below-chance accuracy can still encode avoidance information and is not privacy. A separate direction-calibration check used word units 0–29 / plot families 0–3 and evaluated on the remainder; no primary condition selected an inversion (results/direction_calibrated.json).

Use 10,000 bootstrap resamples and 20,000 sign flips, fixed seed. Word primary inference conditions on the fixed inventory and resamples premise units, with 15-secret cluster sensitivity. Plot inference clusters by 12 families. Holm correction covers five primary contrasts. We report percentage-point differences and unadjusted 95% intervals; an interval excluding zero can coexist with a nonsignificant adjusted p-value. Bootstrap/sign-flip uncertainty does not capture model-version or evaluator-validity uncertainty. The study is exploratory; 90 word pairs may not resolve a 15-point difference reliably, especially after clustering and multiplicity.

Secondary diagnostics include literal disclosure, no-literal subsets, target-blind detection, both-order plot forecasting and premise priors, 1–5 blinded coherence ratings, outline lexical overlap, and truncation sensitivity. Following observed position bias, we added **post hoc next-token A/B log-odds scoring** on every main and anchor pair. For secret-first log-odds z0 and secret-second z1, the score uses sign((z0−z1)/2), with exact ties worth .5. This cancels a constant additive position bias only. Forward scoring uses explicit non-padding position IDs; an earlier partial set was uniformly superseded before aggregate analysis.

### Representation protocol and intervention gate

Teacher-force the same 512 neutral continuation tokens under all 15 secrets and three conditions, across 24 contexts. Save layer 16/32/48 residuals at continuation tokens 32/256/512: **1,080 × 3 × 3 × 3,840** features. Contexts 0–13 train (210 labeled states per condition/position), 14–17 are reserved, 18–23 test (90 states, only six independent narrative clusters). Standardized multinomial logistic regression uses fixed C=.1. Prompt tokens are never pooled; shuffled-label and token-length-only baselines accompany the readout. The original secret remains available in the prompt/cache; this is not a private-memory test.

A fixed layer-32/token-256 decoder also reads 396 separate generated-story replays from units 24–89, at 10/50/90% of continuation length. These re-tokenize saved text, approximating original generation states; **they are not online traces**. Within-secret permutation tests relate midpoint margin to detection scores. An additional post hoc early-margin analysis screens out mentions already present or within ten tokens of the sampled state.

The behavioral intervention required the fixed readout to exceed .20 accuracy, shuffled labels, and length-only prediction. Planned edits were target, random, other-concept, and sham projections, with quality/length/truncation checks. The gate failed. Offline projection of measured reserved-context residuals was evaluated, but no intervention story, behavioral ablation result, or online trace is claimed.

## 4. Results

### Primary detection

{t['primary']}

{t['contrasts']}

![Primary detection, both orders averaged within each pair](figures/leakage.png)

Word outline–context survives the planned correction. Secret-cluster sensitivity gives the same −9.4-point estimate with CI −14.4 to −3.9; its unadjusted sign-flip p is .0094 and is not substituted for the primary Holm analysis. Plot order disagreement was 98.3% in every condition; the narrow intervals near chance reflect evaluator behavior, not proof of secrecy. The free-writing anchor was 55.0% with Gemma and 52.5% with Qwen, both compatible with chance. None of its 60 secret-bearing texts contained the literal secret, versus four spontaneous mentions among its no-secret controls; this further distinguishes the premise-conditioned experiment from the free-writing anchor.

### Direct disclosure dominates the observed word signal

{t['literal']}

![Exact forbidden-word disclosure](figures/literal_disclosure.png)

In the separate three-comparison literal-outcome family, outline–baseline was −13.3 points (CI −23.3 to −3.3; Holm p=.0168), outline–context −17.8 (CI −27.8 to −7.8; p=.0025), and decoy–baseline −18.9 (CI −26.7 to −11.1; p<.0001). The median first mention was at 90.4% of story characters. For example, `word_003_baseline_1` ends with an emphasized “justice”; `word_006_context_1` ends with “internal bracket.” Systematically selected examples are in [error_analysis.md](results/error_analysis.md).

The no-literal subsets have 61 baseline, 74 outline, 59 context, and 79 decoy pairs. Their scores are near chance, but excluding literal cases selects on a post-treatment outcome; these rows diagnose the detector signal and **do not estimate a causal effect on subtle leakage**. Aliases and paraphrases are not covered by the exact-word check.

### Plot controls and writing utility

{t['plot']}

![Forecasting the assigned twist, with controls](figures/plot_forecasts.png)

Nine of 840 forecast responses were malformed; requiring both orders and both private/no-secret stories leaves 57 baseline and 55 context paired differences. No plot contrast survives Holm correction. Premise-only forecasts provide a bias control, but cannot validate literary plausibility. Target-blind word detection was exactly 50% because Qwen always selected A.

There were 44 capped plot excerpts and zero capped word stories. Capped pairs stay in the primary analysis; [truncation sensitivity](results/outline_and_truncation.json) does not turn the insensitive plot detector into evidence of privacy. Word secret-bearing outputs averaged 459 words at baseline, 454 with outlines, 409 with context, and 447 with decoys. Input matching therefore did not match output length. Coherence ratings averaged 4.01–4.10/5 across word conditions and 4.02–4.05 for plots; the near-ceiling coarse ratings are weak utility evidence, not human literary evaluation. Outline lexical overlap was substantially higher when outlines were supplied, confirming content uptake descriptively.

### Secondary order-balanced likelihood measurement

This analysis was added after observing calibration position bias; it is not confirmatory and does not replace the primary scores. Its free-writing anchor accuracy is **{pct(anchor['mean'])}**.

{t['likelihood']}

{t['likelihood_contrasts']}

Raw logits, token IDs, both orders, and complete prompts are in [choice_likelihoods.jsonl](results/model_outputs/choice_likelihoods.jsonl). Among literal-free pairs, secondary accuracies ranged from 48.0% to 58.5%, with every interval including 50%; these are again post-treatment subsets. There were 17 exact log-odds ties across the 600 main/anchor pairs. No contrast in this secondary family survives Holm correction; it does not confirm the significant primary outline–context comparison. It corrects only a constant positional log-odds offset, not semantic evaluator errors or content-dependent ordering effects.

### Secret representations and failed causal gate

The raw fixed probe achieved 8/90 correct identities (8.9%, CI 6.7–13.3%), with shuffled and length-only controls both 6.7%. Raw training accuracy was 99.5%, indicating poor transfer across narratives. Post hoc centering subtracts the unlabeled mean of a context's 15 counterfactual states before fitting/evaluation; this reduces narrative nuisance but requires a set of test states and was chosen after observing failure.

{t['probe']}

![Raw versus post hoc counterfactual-centered decoding](figures/centered_decoding.png)

The centered readout is far above its shuffled controls at all sampled positions. This is evidence of secret-dependent residual information even when continuation text is identical. The condition-specific probes do not measure a shared concept-magnitude scale. Lower outline accuracy is suggestive, but six test contexts and post hoc methodology do not establish that outlines causally erase the representation. All raw layers are shown in [secret_decoding.png](figures/secret_decoding.png).

In separate generated-story replays, baseline midpoint margin correlated with detection score (within-secret rho=.351, Holm p=.0156, n=66); context and outline associations did not survive correction. The early readout did not predict later exact disclosure (all three Holm p=1). The weak decoder and direct-disclosure-heavy detector limit interpretation; this is not mediation evidence. Full [associations](results/mechanism/margin_correlations.json), [early checks](results/mechanism/early_literal_association.json), and [free-story readouts](results/mechanism/free_summary.csv) are saved.

The offline projection check changed reserved-context accuracy from 13.3% (sham) to **35.0% (target)**, 11.7% (random), and 6.7% (other concept). A supposed erasure direction that increases this readout is not validated as selective removal. Combined with the failed prespecified gate, this prevented behavioral intervention execution. **Whether removing the secret representation removes leakage remains unanswered.**

## 5. Analysis and Discussion

The strongest observation is a reduction in exact-word violations under an outline relative to both baseline and irrelevant context. Together with higher outline uptake, this is consistent with content constraints reducing opportunities to insert a secret. The irrelevant-context condition did not reduce disclosure, which argues against a simple token-count dilution explanation under these prompts. However, different output lengths, content choices, and instruction semantics remain alternative explanations; we did not identify disentangled planning as the cause.

The distinction between literal and nonliteral leakage changes the scientific conclusion. Our primary detection contrast alone might look like support for the original hypothesis, but nearly all confident detections can be explained by direct mentions. The published phenomenon concerns hints without the word itself. Failure to detect subtle leakage with this position-biased judge does not show that subtle leakage is absent.

The representation results illustrate a separate distinction: failed cross-context decoding does not imply absent information. Counterfactual centering reveals strong identity information that the raw probe missed. Yet a transductive contrast and an online removal direction are different objects. Keeping the intervention gate fixed avoids presenting an unvalidated edit as evidence for or against a causal mechanism.

## 6. Limitations and Validation

1. One historical 12B writer and one primary 14B judge; no contemporary frontier comparison, human ratings, or multi-seed model-level replication. New sampled texts and inference versions can change estimates.
2. Duplicated Gemma BOS tokens and frequent direct mentions prevent a clean canonical-prompt replication. A corrected-format replication is necessary before generalizing these effects.
3. Strong judge position bias, a weak free-writing positive anchor, coarse quality ratings, and finite answer ceilings limit measurement validity. Passing literal fixtures is insufficient validation of subtle inference.
4. Secret-blind outlines do not test secret-aware plans that organize an eventual revelation. Twelve unvalidated plot families and only six residual test contexts limit generalization and precision.
5. Exact input lengths do not match output length, semantic relevance, attentional processing, or narrative difficulty. One incidental word exposure per added-context type remains.
6. Probes identify a closed set of 15 words, not necessarily abstract concepts. Counterfactual centering is post hoc and transductive; generated-story states are text replays. No validated online ablation, SAE feature intervention, dose response, rescue, or private-state architecture was tested.
7. Bootstrap intervals condition on this dataset and evaluator. Secondary/post hoc families are labeled; their p-values must not be combined into a confirmatory narrative.

Validation: 1,080 unique main outputs and 1,080 primary judgments; all 540 order pairs present; 300 exact input-length matches; explicit model revisions and raw prompts; malformed-value regression checks; four-of-four exact smoke replays; **{rr}/{rn} exact outputs in the recorded full-batch replay**. Deterministic CPU analysis is rerun and compared by hashes in [analysis_replay.json](results/analysis_replay.json). [final_validation.json](results/final_validation.json) audits completeness/provenance and records scientific limits separately. Corrections—including length matching, parser prefixes, pandas missing values, and forward position IDs—are archived rather than concealed. No omitted intervention result is represented as zero leakage.

## 7. Conclusions and Next Steps

Under the recorded protocol, secret-blind outlines reduced **literal disclosure**, including relative to equally long irrelevant context. This does not establish a general reduction of involuntary nonliteral hints or plot foreshadowing. Secret identity remains recoverable from controlled residual differences, but a deployable readout and selective behavioral intervention were not established.

A focused follow-up should first use canonical Gemma encoding and a calibrated stronger judge or blinded human evaluation to reproduce a nonliteral positive anchor. Then repeat outline/context contrasts with sufficient paired power, human-validated plot alternatives, and secret-aware outlines. For mechanism, fit a context-robust readout on substantially more narratives, validate actual online removal with target/random/other controls and quality noninferiority, and only then interpret behavioral changes causally.

## References and Artifacts

- Holtzman & West. [Can You Keep a Secret? Involuntary Information Leakage in Language Model Writing](https://arxiv.org/abs/2605.10794), 2026.
- Gonen et al. [Does Liking Yellow Imply Driving a School Bus? Semantic Leakage in Language Models](https://arxiv.org/abs/2408.06518), arXiv 2024 / NAACL 2025.
- Cywinski et al. [Towards eliciting latent knowledge from LLMs with mechanistic interpretability](https://arxiv.org/abs/2505.14352), 2025.
- Ramnauth & Scassellati. [The Attentional White Bear Effect in Transformer Language Models](https://arxiv.org/abs/2605.28639), 2026.
- Mann et al. [Don't think of the white bear](https://arxiv.org/abs/2511.12381), 2025.
- [Do Language Models Plan Ahead for Future Tokens?](https://arxiv.org/abs/2404.00859), 2024; [Emergent Response Planning in LLMs](https://arxiv.org/abs/2502.06258), 2025.
- Model cards: [Gemma 3 12B IT](https://huggingface.co/google/gemma-3-12b-it), [Qwen3 14B](https://huggingface.co/Qwen/Qwen3-14B).
- Data provenance/downloads: [datasets/README.md](datasets/README.md). Full literature, repository pins, and available resources: [resources.md](resources.md).
- Reproduction and file map: [README.md](README.md). All numeric tables: [report_tables.md](results/report_tables.md).
'''
 Path('REPORT.md').write_text(report)
 readme='''# Outlines, secrets, and hidden states

An exploratory study of whether explicit outlines reduce secret leakage in fiction. Real local Gemma 3 12B generations are evaluated by Qwen3 14B; controlled residual probes examine secret information. See [REPORT.md](REPORT.md) for methods, uncertainty, and limitations.

## Findings

- 1,080 main stories: word detection was 60.6% at baseline, 54.4% with outlines, and 63.9% with matched irrelevant context. Only outline–context survived the five-comparison primary correction.
- Literal disclosure fell from 27/90 baseline stories to 15/90 with outlines; the evidence mainly concerns direct instruction failures, not subtle hints.
- Plot effects remain unresolved. The judge is strongly position-biased, and the writer protocol used duplicated BOS tokens.
- A post hoc counterfactual-centered probe recovered secret identity at 82–91% across baseline continuation positions. The original raw probe failed its gate; **behavioral ablations were not run**.

## Reproduce

Run from this workspace root. All Python work uses its isolated environment:

```bash
pwd
uv sync --frozen
source .venv/bin/activate
bash src/reanalyze.sh  # CPU analysis of recorded outputs and local residual arrays
python src/validate_experiment.py
```

The workspace contains the data and activation arrays. Large downloaded weights and `.npy` arrays are excluded from Git. If those arrays are absent, regenerate them using the GPU workflow below. Data download instructions are in [datasets/README.md](datasets/README.md).

```bash
export HF_HOME="$PWD/artifacts/hf"
# HF_TOKEN must have access to google/gemma-3-12b-it for an uncached download.
bash src/reproduce.sh
python src/replay_recorded.py --limit 1  # exact recorded batch, including its seed/order
```

The recorded protocol intentionally preserves the duplicated BOS for replay. Correcting that format is a follow-up experiment, not a change to these archived results. Fresh sampling with the final configuration differs from the original mixed-batch sample produced during the documented length correction; `replay_recorded.py --limit 0` replays all recorded original batches instead. Checkpoints skip completed IDs. Do not mix unrelated runs in the same results directory.

Hardware used: RTX A6000 (~48 GiB), BF16, ~51 GB of cached model weights. GPU inference and download can take several hours; CPU reanalysis takes roughly a minute or two with local arrays. Results include actual stage timings rather than a guaranteed runtime. No paid API inference succeeded; local hardware cost was not metered.

The report builder checks artifact hashes and intentionally rejects new experimental data: its narrative conclusions are specific to this recorded study. New runs require a new interpretation.

To rebuild documentation after analysis:

```bash
python src/report_tables.py
python src/execution_summary.py
python src/build_report.py
python src/validate_experiment.py
```

## Files

- `planning.md`, `notes/planning_history.md`: hypotheses, three ranked directions, corrections and post hoc diagnostics.
- `src/`: generation, judging, probing, analysis, validation, and report scripts.
- `results/model_outputs/`: complete prompts and real responses; superseded outputs are explicitly archived.
- `results/analysis.json`, `literal_analysis.json`, `diagnostics_analysis.json`, `likelihood_analysis.json`: behavioral estimates.
- `results/mechanism/`: residual metadata, readouts, controls, and failed intervention gate.
- `figures/`: actual-result plots used in the report.
- `uv.lock`, `pyproject.toml`, `results/environment.json`: environment and model provenance.
- `STATE.md`: phase handoff; `resources.md`, `literature_review.md`: gathered research resources.

The final validation audit checks reproducibility and artifact integrity; it does not certify evaluator validity or causal conclusions.
'''
 Path('README.md').write_text(readme)
 print('Final report and README generated from actual artifacts.')
if __name__=='__main__':main()
