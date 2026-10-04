# Research execution plan

Consolidated before any leakage judgments. [Full prospective decisions and corrections](notes/planning_history.md) and [resource-finder handoff](notes/resource_planning.md) preserve the history. This is an exploratory controlled study, not a registered confirmatory trial.

## Motivation & Novelty Assessment

### Why This Research Matters
Fiction writers need to withhold future revelations without making stories generic. An explicit outline could reduce unintended hints by fixing content decisions, or merely dilute a secret through extra context. Separating these explanations matters for useful confidentiality controls.

### Gap in Existing Work
Holtzman and West (2605.10794) establish involuntary leakage in free writing. They do not test matched outline interventions, counterfactual plot secrets, or selective activation ablations. Suppression decoding is already prior art; decodability alone is not a new causal explanation.

### Our Novel Contribution
Compare secret-blind outlines with no outline and exactly length-matched irrelevant context; distinguish word secrecy from future-twist predictability. Measure secret information in generated-position residuals and test a constrained causal intervention with utility controls.

### Experiment Justification
D1 separates content constraints from context length. D2 uses identical continuation tokens to separate hidden conditioning from visible-word differences. D3 asks whether a target projection contributes to leakage beyond random and other-concept edits while preserving writing quality.

## Research Question and Hypothesis Decomposition

H1: explicit secret-blind outlines reduce signed secret-detection accuracy versus baseline and irrelevant context. H1b: they reduce the extra predictability of a private plot twist beyond no-secret priors. H2: secret identity remains decodable at early, middle and late continuation positions. H3: removing a target projection reduces leakage more than control edits without degrading quality. Below-chance guessing can carry avoidance information; it is not equivalent to privacy.

## Direction Budget

Scores are evidence/relevance/information gain/feasibility, each 1–5.

|Direction|Scores|Total|Decision|
|---|---|---:|---|
|D1 matched outline behavior|5/5/5/5|20|Keep|
|D2 temporal residual decoding|5/5/4/4|18|Keep|
|D3 selective intervention|4/5/5/3|17|Keep|
|Private-memory architecture|4/3/3/3|13|Prune: different retention problem|
|Broad model scaling|4/3/2/2|11|Prune: already studied|
|Fine-tuning/myopic pretraining|4/4/2/1|11|Prune: costly and indirect|
|Adversarial extraction|5/2/1/3|11|Prune: induced disclosure|
|Literary-quality optimization|4/2/2/3|11|Prune: quality is a control|

Rankings remain unchanged. Additional diagnostics stay within these three directions.

## Proposed Methodology

### D1: behavioral experiment
Use Gemma 3 12B, the smallest model previously reported to leak strongly, in local BF16 inference at a pinned revision. Main sample: **90 unique WritingPrompts premises**, six per published secret word, and **60 synthetic plot cases in 12 families**. Word conditions: baseline, blind outline, irrelevant context, decoy. Plot conditions: baseline, blind outline, irrelevant context. Generate separate secret-present/no-secret texts for every condition: **1080 main stories**. Target about 450 words, temperature .8, top_p .95, top_k 64, ceiling 850 tokens. Retain refusals, truncations and literal leaks.

Outline prompts receive only premise and task type, never the secret or candidate twists. Assignments are already fixed in the manifest, so blinding is computational rather than chronological. Match the **complete chat-template token count** of outline/context inputs, separately for both presence states, using the same reference body within a pair. The decoy affects both private and no-secret versions identically.

An auxiliary **60-pair free-writing anchor** checks leakage without a premise, judged by both Gemma and Qwen; keep it separate from causal outline comparisons. The primary independent judge is local Qwen3-14B, greedy with thinking disabled. Both presentation orders are required; average them within the story pair. Validate literal recognition and parsing before judging. The main task adapts the paper's secret/no-secret *detection* variant, not its different-secret discrimination variant.

Diagnostics: target-blind judgment of baseline word pairs; both-order candidate-twist forecasting on private/no-secret stories and premises alone; blinded 1–5 coherence ratings; exact-word disclosure, length, repetition and lexical outline overlap. Synthetic plot fixtures lack human validation.

### D2: representation and association
Replay identical 512-token neutral continuations under all 15 secret assignments using final experimental prompts. Read residual layers 16/32/48 at positions 32/256/512, excluding prompt tokens. Context IDs <14 train; 14–17 are reserved; 18–23 test. Skip a context only if its neutral continuation is too short. Use standardized logistic regression, fixed C=.1, context-bootstrap intervals, shuffled labels, and a prompt-length-only baseline. Identical continuation text provides a chance text-only baseline.

Apply the fixed baseline layer-32 decoder to real generated stories from disjoint units 24–89 at 10/50/90% positions. Report pooled and within-secret centered associations with judge accuracy. Decode conditioning information; do not equate it with active planning or persistent private memory. Main story replays re-tokenize text; D3 also records actual online decoder traces.

### D3: causal pilot
Proceed only if the fixed held-out layer-32/position-256 decoder exceeds .20 accuracy, its shuffled-label control, and its length-only baseline. Use training-only mean-difference directions; audit their decoder effect on reserved contexts without tuning. Select two held-out premises per word when available. Compare target, random, other-concept and sham edits on secret-present/no-secret generations, with paired sampling seeds. Intervene only on incremental generation after prefill; original prompt KV cache remains. Direction controls use the target projection magnitude at their current state. One fixed unit projection strength; no outcome-based tuning.

Require target coherence noninferiority (paired CI lower bound above -0.5), mean length within 20% of sham, and truncation increase ≤10 percentage points before calling an effect selective. Judge with Qwen. Dose-response, rescue, direct recall and plot-secret activation interventions remain outside this pilot.

## Statistical Analysis Plan

Seed 20261004; archive actual batch seeds, prompts and outputs. Unit is the premise/secret pair, never the individual judgment order. Use 10,000 bootstrap samples, 20,000 paired sign flips, percentage-point effects and 95% intervals. Word inference is conditional on the fixed inventory, with secret-cluster sensitivity; plot inference clusters by 12 families. Holm-correct the five primary contrasts: outline–baseline and outline–context for both tasks, plus word decoy–baseline.

Calibrate any direction inversion on word units 0–29 / plot families 0–3, evaluate on the remainder. For plot forecasts, compare private-minus-neutral accuracy across conditions; Holm within five secondary contrasts. Within-secret associations use 5000 permutations and Holm across three conditions. D3 uses secret-cluster estimates and Holm across three target-control contrasts. Report missing/parsing failures and truncation sensitivity explicitly. Do not stop based on significance.

## Resources, Timeline and Challenges

Use only project .venv and uv.lock. Hardware: RTX A6000, 49,140 MiB reported. BF16 generation batches up to 32; reduce only on memory failure and log the change. OpenRouter daily quota and direct OpenAI authentication failed; real local models replace API inference. Record exact HF revisions and live-catalog evidence. Public prompts may overlap pretraining; no human evaluation is available.

Allow 20–40 minutes setup, 1–3 hours generation, 30–60 minutes evaluation/mechanism, and 30 minutes analysis/documentation, including debugging buffer. A 90-unit pilot may not resolve a 15-point change; independent 80% versus 65% rates require roughly 137 per group before clustering/multiplicity. Report uncertainty rather than claiming equivalence.

## Expected Outcomes and Success Criteria

Support requires reduced leakage beyond irrelevant context, not mere output degradation. Decoding without a selective intervention supports availability, not causality. Deliver actual outputs, uncertainty, negative/failed gates, REPORT.md, README.md and reproducible analysis. Preserve every implementation correction and superseded output in the history; do not broaden directions or substitute a ≤9B writer.

## Recorded execution deviations
The writer encoding audit found two BOS tokens (template plus tokenizer default), constant in all generated inputs. Preserve that protocol for aligned probes/interventions and disclose noncanonical prompting. After anchor position bias became apparent, add secondary both-order next-token log-odds scoring for every main/anchor/intervention pair; original generated-choice outcomes remain primary. Details and timing are in notes/planning_history.md.
