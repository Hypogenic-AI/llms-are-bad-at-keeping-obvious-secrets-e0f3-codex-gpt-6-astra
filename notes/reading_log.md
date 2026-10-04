# Sequential PDF chunk reading log
PDFs split into three-page chunks using the supplied chunker. Each chunk rendered directly to a three-page image for visual reading; local extracted text supplements small-print lookup. Chunk IDs map to papers/pages manifests. Notes below are recorded after reading each batch, with each chunk accounted for separately.

## 2605.10794 — Holtzman & West
- 001 (pp1–3): writer/guesser setup separates exact word from thematic leakage; figures preview direction inversion; up to 20 free guesses.
- 002 (pp4–6): 15 curated secrets; five instruction conditions; 420 discrimination/450 detection comparisons with both orders and both target words. Main table 79.3% Llama, 78.1% Opus, 77.6% DeepSeek, 70.5% Sonnet, 41.9% GPT. No literal word observed.
- 003 (pp7–9): cross-model readers; Gemma 12B/27B around 83–84%; small models weak. Long jokes leak but short stock jokes do not. User placement stronger. Decoys partly redirect.
- 004 (pp10–12): entropy-budget/attention mechanism is a hypothesis, not measured activations; toy words and model judges limit generalization. Code URL redacted for review; temperatures writer 1 and judge 0.
- 005 (pp13–15): exact prompts and statistical table; examples support semantic and avoidance signals. Pair reuse means nominal binomial trials are not independent; propose cluster inference.
- 006 (pp16–18): COCA list available; strong positional bias; repeated lighthouse default under avoidance. Decoy table contradicts stated offset-7 formula (table uses offset 10). Missing Gemini responses affect denominators; appendix says neither extra model free-guessed despite Grok 1/30 table: use tables with caveat.

## 2505.14352 — Cywiński et al., early Taboo study
- 001 (pp1–3): 20 Gemma-2-9B QLoRA models with single-token secrets absent from training text; Gemini-generated hints; logit lens at layer 32 and Gemma Scope SAE. Official early repo EmilRyd/eliciting-secrets.
- 002 (pp4–6): logit-lens top-5 Pass@10 75%, SAE top-5 55%, postgame prefill 70%, another model 95%; white-box not universally best. References and single-token limitation.
- 003 (pp7–9): synthetic 3–5-turn data validation excludes target and variants; 11 hint types; rank 8, LR 2e-4, 10 epochs maximum, early stopping, one A100.
- 004 (pp10–12): moon/song examples, ten standardized starting prompts; adversarial categories and exact baseline prompts.
- 005 (pp13–15): technical, formatting and definition attacks; ten prefill phrases; postgame differs from pregame by eliciting hints first.
- 006 (pp16–18): three hint turns before prefill; SAE ground truth manually mapped, sometimes multiple features (dance); figures show logit/SAE peaks need not be continuous.
- 007 (p19): wave case has intermittent middle/late-layer signal, not evidence of a persistent invariant secret state.

## 2510.01070 — Cywiński et al., expanded benchmark (v2)
- 001 (pp1–3): Taboo, Base64 secret-side-constraint (SSC), and user-gender organisms; public model/code release; explicit benchmark for an auditor rather than story generation.
- 002 (pp4–6): Gemma-2-9B Taboo/gender, Llama-3.3-70B SSC; Alpaca unrelated-data augmentation 10x to reduce artifacts; prefill/user-persona and logit lens.
- 003 (pp7–9): activation-embedding cosine, SAE TF-IDF-like density correction, Gaussian fuzzing. Standard sets 1000 Taboo/gender, 1600 SSC; disjoint validation/test. White-box helps standard queries; prefill best on direct SSC/gender.
- 004 (pp10–12): fuzzing mostly ineffective, sometimes degrades coherence; simple organisms and SFT limit generality; references inspected.
- 005 (pp13–15): remaining references and precise tables. Standard Taboo I/O 42.1% vs logit lens 84.0%; gender SAE descriptions 85.4%; direct SSC prefill 95.89%, user persona 96.76%. These are task-specific auditor scores.
- 006 (pp16–18): 300+150 Taboo samples, 43092+5000 SSC, 500+225 gender before augmentation; example data and constraint categories.
- 007 (pp19–21): additional gender refusal data correct pronoun confusion; internalization evaluated separately using graded hint/constraint adherence; held-out SSC constraints listed.
- 008 (pp22–24): 400 binary gender internalization questions, standard/direct evaluation examples. Gender is a constructed binary task, not a general demographic inference claim.
- 009 (pp25–27): layer/token choices: Taboo 32 assistant controls, gender 23 first-person pronouns, SSC 50 Base64 positions; SAE counts and density filtering; noise/temperature sweeps on validation only.
- 010 (pp28–30): noise often harms best prefill; Taboo prefill only 0–2% validation success versus much stronger SSC/gender, caution against aggregate generalization.
- 011 (pp31–33): user-persona prefix grids and selected combinations; benchmark sensitivity to elicitation scaffolding.
- 012 (pp34–36): ~8k-token many-shot baseline weak; auditor I/O versus I/O+tokens prompts; two-stage SAE filtering for small gender auditor.
- 013 (pp37–39): gender feature descriptions can mislead; SSC staged filtering, word guessing, and instruction assembly using the same auditor.
- 014 (pp40–42): SSC five instruction guesses rated by GPT-4.1 semantic similarity 0–10; not comparable directly with single-word accuracy. Multilingual Taboo prefill introduced.
- 015 (pp43–45): multilingual prefill recovers Taboo (~43% figure) where English suppression persists; standard logit lists include gold variants; feature descriptions can be broad.
- 016 (pp46–48): SSC token alignment at completed Base64 units; SAE sparse but feature coverage incomplete; female/male readout asymmetry.
- 017 (pp49–51): detailed gender SAE descriptions/tokens; irrelevant tokens mixed with useful evidence, caution about interpreting top activations alone.
- 018 (pp52–54): direct and standard SSC raw readouts; residual-stream secret strongest on assistant control tokens, not uniformly across generation; selected gold feature IDs shown.
- 019 (p55): weak gender secret signal example concentrated on assistant control tokens; directly motivates token-time analysis rather than assuming continuous activity.

## 2603.25187 — Luo et al.
- 001 (pp1–3): twenty-questions target drift; numerical index branch query measures output distributions, not hidden-state probes. Distinguishes externally compatible answers from latent target stability.
- 002 (pp4–6): CE+KL fine-tuning Qwen-2.5-14B lowers drift; CE alone worse external consistency; reasoning does not uniformly help. Explicit context target aids persistence.
- 003 (pp7–9): top-20 API logprobs, missing target indexes assigned -999 then renormalized, potential measurement artifact. Branching dialogues; 1001 fine-tuning examples, eight A800-80GB. Full prompts.
- 004 (pp10–12): only two tasks and one fine-tuned size; authors acknowledge numeric probing may not reflect native representations; checklist.
- 005 (pp13–15): checklist states code/data will be released on acceptance; no actionable public repo in PDF; compute/statistical reporting declarations.
- 006 (pp16–17): remaining reproducibility/LLM-use checklist, no new experiments. Do not equate prompted self-report distribution with direct mechanistic readout.

## 2511.12381 — Mann et al.
- 001 (pp1–3): ReboundBench 5000 templated negation prompts, nine models, three distractor types; distinguishes matched neutral suppression score from surprisal relative to maximum-load baseline. Target single-token replacement/exclusion can change concept sets across tokenizers.
- 002 (pp4–6): reported semantic-load effects and middle-layer head amplification; polarity/persistence correlation ~0.44; attention-head ablations are closer to causality but outcome is target logprob, not semantic story leakage.
- 003 (pp7–9): source corpora This-is-not-a-dataset and NUBench; CSV fields topic,target,distractor_type,length,prompt; synthetic English/single-token limitations and regression coefficients.
- 004 (pp10–12): per-model tables; GPT-OSS exception; Appendix C Llama-3-8B head effects mostly small. Text and Figure 3 give somewhat inconsistent layer trends; inspect code before relying on precise layer recommendation. Avoid treating reduced token probability as reduced information.

## 2502.06258 — Dong et al.
- 001 (pp1–3): prompt representations predict future response length, reasoning steps, animal choices, answers, correctness; task pairs include TinyStories/ROCStories and UltraChat/AlpacaEval.
- 002 (pp4–6): two-layer MLPs, hidden widths 1–1024, 60/20/20 split, 400 epochs, three seeds; cross-dataset tests and layer sweeps. Predictability alone not causal planning.
- 003 (pp7–9): within-family scale effects, U-shaped generation-time probe accuracy; greedy labels limit transfer to sampled generation. Authors explicitly leave causal interventions to future work.
- 004 (pp10–12): references identify future-token prediction, activation engineering and myopic training as precedents.
- 005 (pp13–15): model/dataset links and full task prompts; story animal task uses first sentence and controlled animal introduction, not full narrative secrets.
- 006 (pp16–18): exclude animals in first two words; balance four most frequent animals; truncate before revealed attribute; original and augmented variants assigned same split to prevent leakage.
- 007 (pp19–20): detailed in-/cross-dataset regression plots, lower cross-domain correlations; supports held-out context evaluation and text-only baselines for our probes.

## 2404.00859 — Wu, Morris & Levine
- 001 (pp1–3): pre-caching versus breadcrumbs; future-token decodability may reflect features useful now. Official FutureGPT2-public link.
- 002 (pp4–6): myopic training blocks cross-position gradients; distinguishes myopia gap and local bonus; synthetic sine task constructed to require precomputation.
- 003 (pp7–9): vanilla vs myopic large synthetic loss difference; GPT-2 MS MARCO cross entropy 3.28 vs 3.40, local myopic 3.26, transformer bigram 5.33. Small gap favors breadcrumbs in this regime.
- 004 (pp10–12): Pythia 14M–2.8B fine-tuned on 10M Pile sequences of 64 tokens; gap grows with scale; foundation references.
- 005 (pp13–15): bonus/malus decomposition; explicit gradient paths and detached/frozen KV attention construction; model training manipulation, not single inference ablation.
- 006 (pp16–18): formal convergence proofs depend on smoothness, convexity and forward-bias assumptions; not general theorems about arbitrary trained LLM cognition.
- 007 (pp19–21): synthetic configs, 5000-example probes; GPT-2 trained from scratch vs Pythia fine-tuning; multiplication adds delayed-computation example.
- 008 (pp22–24): reverse-digit multiplication and filler-zero controls; extra padding benefits vanilla and hurts myopic; gradient magnitudes analyzed. Training reproduction too expensive and indirect for our top-three budget.

## 2402.17119 — Xie & Riedl
- 001 (pp1–3): suspense through narrowing plausible escape options, reader empathy and knowledge disparities; iterative action/failure planning; deliberately adding clues serves suspense but can violate secrecy.
- 002 (pp4–6): background → actions/failure reasons → detailed elaboration; GPT-3.5-turbo-0613, no training corpus. Human baseline study 30 story pairs, 90 participants, 30 judgments per pair, five criteria.
- 003 (pp7–9): suspense preference 84.9% against direct ChatGPT and 81.1% against Re3; Llama-2 replication, outline/elaboration ablations. Clues improve suspense; timing preference difference not significant. Limited English genres/model set.
- 004 (pp10–12): references and thriller genre inventory; no official repository URL in PDF.
- 005 (pp13–15): detailed elaboration prompts explicitly request small hints; chapter example reveals failures while protagonist unaware. This is a positive foreshadowing baseline, not a secrecy intervention.
- 006 (pp16–17): full example concludes multiple arcs; story-level coherence/effectiveness should be evaluated separately from reader uncertainty about a designated secret.

## 2310.17884 — Mireshghallah et al.
- 001 (pp1–3): ConFAIDE four tiers from sensitivity to multi-party privacy reasoning; inference-time privacy differs from training memorization. ICLR 2024.
- 002 (pp4–6): tiers 1/2 human correlations, tier 3 disclosure/access questions, tier 4 meeting action items and summaries; compare six model families, with privacy prompts.
- 003 (pp7–9): tier 4 summary leakage GPT-4 39%, ChatGPT 57%; chain-of-thought does not reliably help. Omitting useful public information is measured jointly with disclosure.
- 004 (pp10–12): references and contextual integrity foundations; generation and proxy-agent inference complementary.
- 005 (pp13–15): full generation templates and human validation; tier 3 270 scenarios, 2 removed on safety/coherence review; human disagreement reported.
- 006 (pp16–18): detailed factors; exact string matching misses 16/200 manually found paraphrased leaks, so literal filtering insufficient. Model-generated scenarios may favor their generator.
- 007 (pp19–21): benchmark examples/counts; tier 4 has 20 transcripts; average versus worst-of-ten metrics distinguished. Full transfer requires utility measurement.
- 008 (pp22–24): supplemental model/factor heatmaps and contextual leakage examples; avoid using privacy-norm judgments as interchangeable with secret-word thematic leakage.

## 2601.06973 — Baldelli et al., v3
- 001 (pp1–3): Private State Interactive Tasks; public-history-only agents cannot retain privately chosen unresolved state. The theorem's assumptions exclude an externally supplied secret kept in a private prompt.
- 002 (pp4–6): proof by indistinguishable public histories; fork-and-reveal test; Hangman and DDXPlus diagnosis; private CoT upper bound and explicit memory workflow variants.
- 003 (pp7–9): 50 episodes per model/method/task, fork turn 4, five candidate secrets; workflow memory strong, public-history baselines weak. Counts leakage, overconfirmation, state substitution and denial; private CoT costs ~10x tokens.
- 004 (pp10–12): conclusions and references; code chandar-lab/Hangman; architectural consistency guarantee is distinct from semantic noninterference.
- 005 (pp13–15): related work and memory representation goals/facts/active notes; generated private state differs from retrieval of public facts.
- 006 (pp16–18): example private states explicitly store a selected secret; retrieval baselines summarize rules and observations but omit chosen secret.
- 007 (pp19–21): commercial-interface examples are qualitative and date-specific; absent persistent secret can lead to post-hoc rationalization. Not evidence about this assistant's architecture.
- 008 (pp22–24): continued transcripts and low-entropy secret choices; avoid self-report as proof of internal state.
- 009 (pp25–27): distributions concentrate on a few words; fork-time 2/4/6/8 check broadly stable; exact Hangman prompts.
- 010 (pp28–30): diagnosis and retrieval baseline prompts; private CoT baseline retains traces while public-only removes them.
- 011 (pp31–33): workflow updates a private state separately from public generation; initial memory schema and tools.
- 012 (pp34–36): append/delete/patch/replace tool schemas with idempotence and matching rules; useful implementation details but extra agent architecture out of scope.

## 2605.28639 — Ramnauth & Scassellati (new close prior; full read)
- 001 (pp1–3): 17 concepts, positive/matched/hard negatives, five prompt conditions; Llama-3.1-8B with Mistral/Gemma replication. Linear probes with held-out prompts; exclude explicit-leak generations in suppression analysis.
- 002 (pp4–6): pooling materially changes layer profile; mean AUC .919 vs last-token .860; semantic similarity difference .012 despite no explicit aliases in retained suppression outputs. Aggregate attention decreases vs mention, some heads increase. Main-text attention mean typo contrasts with table.
- 003 (pp7–9): direct mention generally stronger than suppression, so not global hyperactivation. Authors acknowledge correlational evidence and explicitly request causal interventions; probes/attention do not prove causal leakage.
- 004 (pp10–12): 136 contexts, 680 prompt instances, library detail and head-level statistics. Positive/negative/hard-negative example counts 408/408/170 sum to 986; aliases/descriptions/contexts are additional fields, not extra training rows.
- 005 (p13): behavioral rows 408 absent/mention, 375 direct suppression, 380 indirect indicate filtering; do not report zero retained lexical leakage as unconditional perfect compliance. Table 5 proper suppression mean .00995 vs mention .01189. Use complete-denominator evaluation in our study.

## 2604.00209 additional deep reading
- Chunk 1 (pp1–3): CI norm steering, not secret-content erasure. Four model families, 500 matched concept pairs, 200 roleplay scenarios.
- Chunk 2 (pp4–6): last-token probes, logistic C=1 five-fold CV; 1,500 parametric examples; PCA1 inadequate on ConFAIDE, PCA3 better; cross-projected LDA tests. Synthetic-to-ConFAIDE probe transfer helps but judgment vs generation framing differs.
- Chunk 3 (pp7–9): Llama3.1-8B/Qwen2.5-7B/Mistral7B/Llama2-7B; top5 layers, alpha .5/1/2/4, greedy256tokens; ConFAIDE, PrivaCI. Baselines additive, LoRRA, representation tuning. Leakage and norm compliance both needed. Table1 5.0% contradicts prose/appendix0.5%; avoid overprecise headline. Three directions at same coefficient create larger perturbation than monolithic baseline.
- Chunk 4 (pp10–12): references, funding, conceptual links to RepE/ITI, ConFAIDE, GoldCoin and privacy reasoning; no additional experiment.
- Chunk 5 (pp13–15): full roleplay/judge prompts; LoRRA rank8 and rep-tuningrank16 details; appendix synthetic all-axis0.5%; need audit sign/norm across methods.
- Chunk 6 (pp16–18): 4D LDA subspaces, 5fold classification, permutation; **utility collapses**: CI alpha1 helpfulness/coherence/relevance all1.00/5 on200 Alpaca, alpha.5 helpfulness1.04 vs baseline4.58. Thus leakage reduction alone is not evidence of useful secret removal. Five-axis extension often worse; no reason to expand D3.

## 2505.16505 — Zhao et al., additional deep reading
- Chunk 1 (pp1–3): Concise-SAE identifies instruction-relevant SAE features via generated positive/negative stories and keyword-anchored attention aggregation. Not direct secret-content erasure. Pretrained SAEs, no new weight training.
- Chunk 2 (pp4–6): select top-k supportive and counter-instruction features; Bayesian optimization rewards instruction adherence, penalizes unwarranted refusal, adds quality. 1,212 human-in-loop FreeInstruct cases (~77.8-word story,17.3-word input), normal/adversarial inputs; Gemma2-2B/9B and Llama3.1-8B. Baselines direct prompting, ICL, ICV, SAIF, SPARE; WildGuard/prompt injection/XSTest secondary. Base-model self-evaluation optimizes reward; external GPT4o grades outcomes, so validation separation needed.
- Chunk 3 (pp7–9): FreeInstruct Llama8B IFR .340 no-control→.860 Concise-SAE, response rate .946,quality.932; ICL .627,ICV.787,SAIF.600,SPARE.607. Large edits cause evasiveness/repetition, so moderation essential. Supportive/opposing SAE decoder directions nearly orthogonal; BO/CMA-ES better than direct edits. Judge/model access/SAE availability are limitations.
- Chunk 4 (pp10–12): references then Appendix A: Bayesian expected-improvement, ten starting vectors,minibatch20, k15 per sign=30 features; no explicit hard coefficient bounds, post-edit magnitude check. Two PhD annotators with QwQ32B support; greedy one-output evaluation lacks sampling uncertainty. SAE checkpoint families specified per model; detailed IFR and refusal judge prompts.
- Chunk 5 (pp13–15): GPT4o quality combines language quality and adherence scores (1/.5/0); full-compliance response rate distinct from zero refusal. Bidirectional edit beats each sign alone; layer15 best in reported sweep. Appendix D says data will be released under **CC BY-NC 4.0**; no repository LICENSE is present, so record the paper-stated data terms rather than assuming unrestricted reuse. Case examples are qualitative, not independent trials.
