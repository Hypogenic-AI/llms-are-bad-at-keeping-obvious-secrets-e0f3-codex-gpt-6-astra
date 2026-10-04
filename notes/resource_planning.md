# Research direction budget and experiment handoff

## Scope and ranking (Phase 1, 2026-10-04)
Question: does an outline reduce unintended secret information in a story, and does a causally relevant secret representation explain leakage? Distinguish arbitrary secret words from future plot revelations. Scores 1–5; total is evidence + hypothesis relevance + information gain + feasibility (equal weights). Scores are reasoned priorities, not results.

|Rank|Direction|Evidence|Relevance|Gain|Feasibility|Total|Decision|
|---|---|---:|---:|---:|---:|---:|---|
|1|Matched outline vs no-outline behavioral experiment|5|5|5|5|20|Keep D1|
|2|Layer/time secret decoding across outline conditions|5|5|4|4|18|Keep D2|
|3|Targeted activation intervention with quality and recall controls|4|5|5|3|17|Keep D3|
|4|Private-memory multi-agent architecture|4|3|3|3|13|Prune: different retention problem, architecture confounds|
|5|Broad model scaling survey|4|3|2|2|11|Prune: already studied; only small feasibility pilot|
|6|Fine-tune/myopic pretraining to disentangle planning|4|4|2|1|11|Prune: costly and indirect|
|7|Adversarial secret extraction benchmark|5|2|1|3|11|Prune: induced disclosure differs from involuntary leakage|
|8|Optimize literary quality/suspense|4|2|2|3|11|Prune: use quality as control, not primary objective|

Evidence: 2605.10794 motivates D1; DOC 2212.10077 and 2402.17119 establish useful but potentially hint-producing outlines. 2510.01070, 2605.28639 and 2502.06258 support D2. 2505.16505, 2604.00209 and 2604.12493 support D3. 2404.00859 cautions against inferring planning from prediction.

Novelty refinement during initial Phase 1: suppressed concepts have already been decoded (2605.28639), so D2 contributes plan-conditioned temporal analysis tied to D3. Rankings unchanged. Do not add implementation directions without evidence that invalidates this ranking.

## Shared design and decision gates

This is an experiment specification, not a report of experiments run. Resources are ready; no checkpoint, paid inference, judge call, or GPU experiment has been run. Start with one open-weight instruction model whose layer activations can be inspected (7–12B if hardware permits); add one independent writer only after the pilot works. Fix model revision, chat template, dtype, sampling seed/temperature, generation length, and library versions. Do not compare API models' inaccessible activations to local activations as if they were identical systems.

### D1 — Does an explicit outline reduce leakage?

**Primary task:** replicate unrelated-secret-word writing using the 30 words transcribed from 2605.10794. Randomize a secret independently of a WritingPrompts premise; exclude premises already containing the secret or obvious synonyms using a predeclared rule. Retain the identical premise across secret assignments. Use one randomly assigned secret per matched unit, with balanced alternatives for judge discrimination. Generate a ~450-word standalone story, explicitly prohibiting direct and indirect mention of the secret. Word count is a target; record actual token/word counts and truncation.

**Conditions:** (a) secret + no outline; (b) secret + externally supplied secret-blind outline; (c) secret + secret-aware outline; (d) no secret + no outline; (e) no secret + the same blind outline. Add a length-matched irrelevant-context control to distinguish extra context from planning. Make the blind outline before randomizing secrets; reuse it unchanged across all secret assignments. Keep the secrecy instruction and secret position constant. Secret-aware outlines must be judged separately for leakage; their effect is a total pipeline effect and cannot by itself show that planning/prose disentanglement caused improvement. Self-planning also changes compute and supplies a secret-bearing intermediate artifact; treat it as an auxiliary condition only, not a new direction.

For arbitrary words, the blind and secret-aware outlines both plan the full story. For future-plot secrets, give the writer two counterfactual endings with matched plausibility, privately designate one, and request only the opening/middle before a fixed reveal boundary. Blind outlines specify common events without selecting an ending; aware outlines may include the ending after that boundary. Independently check candidate-ending priors and the outline's own disclosure. No downloaded dataset labels this exact task: curated counterfactual endings and a blinded human validation set must be constructed before claiming results about foreshadowing. The supplied fixture is a schema/example, not benchmark evidence. Keep word and plot-secret results separate.

**Readouts:** exact/normalized word and alias disclosure; blinded 2-alternative secret inference from story only; candidate order counterbalanced; prefix inference at 25/50/75/100% of eligible text. Judge sees only the output and candidate secrets, never the writer prompt, plan, condition, or metadata. Use independent judge/model plus a blinded human subset. Calibrate judge biases on no-secret stories. Report raw accuracy and a direction-calibrated held-out discrimination metric: systematic below-chance performance may encode the secret through avoidance. Choose any inversion on validation data, never on the test set. Embedding similarity is secondary and needs secret-absent controls. Record refusals, length, diversity, repetition, coherence, premise/outline adherence, and retained secret recall in a separate branch after generation.

**Pilot and inference:** begin with 30 secrets × 3 distinct premises (90 independent secret/premise units), paired across six conditions: 540 generations per writer before repeat seeds. This is a feasibility pilot, not a powered confirmatory sample. Reserve disjoint premise/template groups for validation/test; use a larger fresh sample sized from pilot variance and a declared minimum effect before confirmatory testing. Estimate paired outline effects with intervals, clustering by reused premise and secret (or crossed mixed effects); 420 judge comparisons of reused stories are not 420 independent trials. Pre-register one primary D1 contrast (blind outline vs no outline), keep awareness/length interactions secondary, and correct the three directional primary tests (e.g. Holm). Report failures as failures, not silently remove literal leaks.

### D2 — Is the secret represented throughout generation?

Capture generated-token residual states across layers and normalized story positions under the D1 conditions. Train a simple linear classifier on a disjoint training set; choose layers/regularization on validation only. Use group splits so near-identical templates and variants never straddle partitions. Report multiclass balanced accuracy and one-vs-rest AUROC, uncertainty, shuffled-label controls, text-only prediction, and performance relative to secret-absent prompts. For held-out secret concepts, train a contrastive/embedding readout that can generalize to those concepts; a closed-label classifier cannot test unseen labels.

Analyze free generation and a separate **teacher-forced identical neutral continuation**. The latter holds token content fixed across secret assignments and isolates conditioning effects; the former measures the actual deployed process. Do not pool secret-bearing prompt tokens into a claim about persistence during prose. Separate prompt-end, generated-token, and cumulative pooling analyses. Logit-lens top-k recovery and sparse features are supporting readouts, not ground truth. Check whether the secret is strongest only in assistant-control tokens (as in 2510.01070), and whether outline effects survive the text-only baseline. Decodability alone neither establishes active planning nor a causal source of leakage.

### D3 — Does selectively perturbing the representation change leakage?

Fit a secret-concept direction/subspace from independent contrastive contexts or use an appropriate pretrained SAE. At validated layers subtract the projection or edit selected features; preserve SAE reconstruction residual if applicable. Select intervention strength using validation data only. Compare zero intervention, norm-matched random directions, unrelated-concept directions, and the same intervention in secret-absent prompts. Track writing quality, secret recall, leakage, and decoder scores jointly; define acceptable quality loss before testing. Include dose-response and a rescue (restore/add the direction) where feasible. Privacy-norm steering from CI-Steering is an implementation reference, not proof of secret erasure.

Specify hook position, tokens affected, caching, and whether interventions alter prompt processing, generated states, or both. A secret in prompt KV cache can reintroduce information at later steps. Distinguish transient suppression from persistent removal, and distinguish lower readout accuracy from absence of all secret information. Pair intervention/no-intervention seeds, but acknowledge trajectories diverge. A credible result reduces semantic leakage beyond sham controls while preserving useful prose; loss of secret recall and generic degraded outputs are competing explanations. Test interaction with the blind-outline condition after establishing a stable intervention, within D3 rather than adding a fourth direction.

## Implementation order and stopping criteria

1. Read `resources.md`, `datasets/README.md`, and code entry-point notes. Run resource validation; check local accelerator/memory before selecting model size. Obtain model access independently if gated.
2. Build input manifest from downloaded data, preserve stable IDs, group splits, assignment seeds and exclusions. Implement judge parsing/order controls; test against literal-leak, no-leak, refusal and malformed-output fixtures.
3. Run D1 pilot first. If the selected model does not show a measurable baseline leakage signal, report that boundary and try the preselected second writer; do not fish over unlimited models.
4. Run D2 only with a validated readout and D3 only with a validated, tolerable intervention. No interpreting unsuccessful probes as knowledge deletion.
5. Freeze pilot-informed sample size and analysis before the main run. Save raw outputs, judge calls, activation indices, errors and costs. Report all three directions even if results are null. Broaden the direction budget only if new evidence invalidates the ranking and update STATE.md first.
