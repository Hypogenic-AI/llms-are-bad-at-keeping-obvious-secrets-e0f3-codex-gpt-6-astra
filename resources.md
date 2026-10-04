# Resources catalog

Resource gathering completed on 2026-10-04: **23 original papers, four downloaded source datasets (five raw files), five cloned repositories**. The project has a fresh uv environment and pinned download manifests. This handoff prepares experiments; it contains no model-run results.

Start with [literature_review.md](literature_review.md), then [planning.md](planning.md). The implementation budget is fixed at D1 outline comparisons, D2 temporal decoding, and D3 causal interventions with quality controls.

## Papers

|Title|Authors|Year (first arXiv)|Local file|Use|
|---|---|---|---|---|
|[Hierarchical Neural Story Generation](https://arxiv.org/abs/1805.04833)|Fan, Angela; Lewis, Mike; Dauphin, Yann|2018|[1805.04833](papers/1805.04833.pdf)|WritingPrompts source|
|[Plan-And-Write: Towards Better Automatic Storytelling](https://arxiv.org/abs/1811.05701)|Yao, Lili; Peng, Nanyun; Weischedel, Ralph; Knight, Kevin; Zhao, Dongyan; Yan, Rui|2018|[1811.05701](papers/1811.05701.pdf)|Static versus interleaved plans|
|[Re3: Generating Longer Stories With Recursive Reprompting and Revision](https://arxiv.org/abs/2210.06774)|Yang, Kevin; Tian, Yuandong; Peng, Nanyun; Klein, Dan|2022|[2210.06774](papers/2210.06774.pdf)|Recursive reprompting baseline|
|[DOC: Improving Long Story Coherence With Detailed Outline Control](https://arxiv.org/abs/2212.10077)|Yang, Kevin; Klein, Dan; Peng, Nanyun; Tian, Yuandong|2022|[2212.10077](papers/2212.10077.pdf)|Hierarchical outline implementation|
|[Can LLMs Keep a Secret? Testing Privacy Implications of Language Models via Contextual Integrity Theory](https://arxiv.org/abs/2310.17884)|Mireshghallah, Niloofar; Kim, Hyunwoo; Zhou, Xuhui; Tsvetkov, Yulia; Sap, Maarten; Shokri, Reza; Choi, Yejin|2023|[2310.17884](papers/2310.17884.pdf)|Contextual disclosure and utility|
|[Creating Suspenseful Stories: Iterative Planning with Large Language Models](https://arxiv.org/abs/2402.17119)|Xie, Kaige; Riedl, Mark|2024|[2402.17119](papers/2402.17119.pdf)|Suspense planning; hints may increase|
|[Do language models plan ahead for future tokens?](https://arxiv.org/abs/2404.00859)|Wu, Wilson; Morris, John X.; Levine, Lionel|2024|[2404.00859](papers/2404.00859.pdf)|Decodability versus causal planning|
|[Does Liking Yellow Imply Driving a School Bus? Semantic Leakage in Language Models](https://arxiv.org/abs/2408.06518)|Gonen, Hila; Blevins, Terra; Liu, Alisa; Zettlemoyer, Luke; Smith, Noah A.|2024|[2408.06518](papers/2408.06518.pdf)|Semantic prompt leakage|
|[Do LLMs Strategically Reveal, Conceal, and Infer Information? A Theoretical and Empirical Analysis in The Chameleon Game](https://arxiv.org/abs/2501.19398)|Karabag, Mustafa O.; Sobotka, Jan; Topcu, Ufuk|2025|[2501.19398](papers/2501.19398.pdf)|Strategic conceal/reveal comparison|
|[Emergent Response Planning in LLMs](https://arxiv.org/abs/2502.06258)|Dong, Zhichen; Zhou, Zhanhui; Liu, Zhixuan; Yang, Chao; Lu, Chaochao|2025|[2502.06258](papers/2502.06258.pdf)|Pre-response and temporal decoding|
|[Towards eliciting latent knowledge from LLMs with mechanistic interpretability](https://arxiv.org/abs/2505.14352)|Cywiński, Bartosz; Ryd, Emil; Rajamanoharan, Senthooran; Nanda, Neel|2025|[2505.14352](papers/2505.14352.pdf)|Early Taboo/logit-lens baseline|
|[Sparse Activation Editing for Reliable Instruction Following in Narratives](https://arxiv.org/abs/2505.16505)|Zhao, Runcong; Cao, Chengyu; Zhu, Qinglin; Lv, Xiucheng; Shao, Shun; Gui, Lin; Xu, Ruifeng; He, Yulan|2025|[2505.16505](papers/2505.16505.pdf)|SAE editing; FreeInstruct data|
|[Eliciting Secret Knowledge from Language Models](https://arxiv.org/abs/2510.01070)|Cywiński, Bartosz; Ryd, Emil; Wang, Rowan; Rajamanoharan, Senthooran; Nanda, Neel; Conmy, Arthur; Marks, Samuel|2025|[2510.01070](papers/2510.01070.pdf)|Expanded secret readout methods|
|[ParaScopes: What do Language Models Activations Encode About Future Text?](https://arxiv.org/abs/2511.00180)|Pochinkov, Nicky; Volkova, Yulia; Vasileva, Anna; Chereddy, Sai V R|2025|[2511.00180](papers/2511.00180.pdf)|Future-context readout limits|
|[Don't Think of the White Bear: Ironic Negation in Transformer Models Under Cognitive Load](https://arxiv.org/abs/2511.12381)|Mann, Logan; Saxena, Nayan; Tandon, Sarah; Sun, Chenhao; Toteja, Savar; Zhu, Kevin|2025|[2511.12381](papers/2511.12381.pdf)|Negation/load controls; ReboundBench|
|[LLMs Can't Play Hangman: On the Necessity of a Private Working Memory for Language Agents](https://arxiv.org/abs/2601.06973)|Baldelli, Davide; Parviz, Ali; Zouaq, Amal; Chandar, Sarath|2026|[2601.06973](papers/2601.06973.pdf)|Private-memory assumptions and recall control|
|[Probing the Lack of Stable Internal Beliefs in LLMs](https://arxiv.org/abs/2603.25187)|Luo, Yifan; Xu, Kangping; Lu, Yanzhen; Yuan, Yang; Yao, Andrew Chi-Chih|2026|[2603.25187](papers/2603.25187.pdf)|Belief-drift caveat; behavioral probes|
|[Do LLMs Know What Is Private Internally? Probing and Steering Contextual Privacy Norms in Large Language Model Representations](https://arxiv.org/abs/2604.00209)|Wang, Haoran; Xiong, Li; Shu, Kai|2026|[2604.00209](papers/2604.00209.pdf)|Steering code; utility collapse caution|
|[Spoiler Alert: Narrative Forecasting as a Metric for Tension in LLM Storytelling](https://arxiv.org/abs/2604.09854)|Sui, Peiqi; Zhu, Yutong; Cheng, Tianyi; West, Peter; So, Richard Jean; Long, Hoyt; Holtzman, Ari|2026|[2604.09854](papers/2604.09854.pdf)|Prefix forecasts and tension|
|[Latent Planning Emerges with Scale](https://arxiv.org/abs/2604.12493)|Hanna, Michael; Ameisen, Emmanuel|2026|[2604.12493](papers/2604.12493.pdf)|Causal planning criterion|
|[Can You Keep a Secret? Involuntary Information Leakage in Language Model Writing](https://arxiv.org/abs/2605.10794)|Holtzman, Ari; West, Peter|2026|[2605.10794](papers/2605.10794.pdf)|Closest leakage task; word list and judge design|
|[The Attentional White Bear Effect in Transformer Language Models](https://arxiv.org/abs/2605.28639)|Ramnauth, Rebecca; Scassellati, Brian|2026|[2605.28639](papers/2605.28639.pdf)|Suppressed concept probes and data|
|[When Activation Oracles Learn Not to Read: Concept-Specific Blind Spots in Fine-Tuned Oracles](https://arxiv.org/abs/2607.23379)|Bersia, Tobias; Gaintseva, Tatiana|2026|[2607.23379](papers/2607.23379.pdf)|Activation oracle blind spots|

See [papers/README.md](papers/README.md) for reading scope, [notes/papers_catalog.json](notes/papers_catalog.json) for hashes/page counts, and [notes/reading_log.md](notes/reading_log.md) for sequential chunk notes. All ten supplied papers and three additional close papers were read in full. Other papers were screened by abstract with selected-section consultation where needed.

## Datasets

|Resource|Local location|Downloaded extent|Primary use|
|---|---|---|---|
|Suppression concepts|`datasets/suppression_concepts/`|17 concepts; 986 labeled probe sentences plus aliases/contexts|D2/D3 contrast construction|
|FreeInstruct|`datasets/freeinstruct/`|1,212 narrative cases|Narrative adherence/utility controls|
|ReboundBench released prompts|`datasets/reboundbench/`|5,000 negation + 500 multi-question rows|D1/D2 lexical suppression controls|
|WritingPrompts test|`datasets/writingprompts/`|15,138 pairs, 5,478 distinct premises|D1 source premises|

Raw files total 32,535,349 bytes. [Download and loading instructions](datasets/README.md), [pinned URLs and SHA-256](datasets/manifest.json), [structural validation](datasets/validation.json). Raw data are excluded from Git; small actual samples remain available. Concept data are CC BY 4.0; FreeInstruct paper states CC BY-NC 4.0; ReboundBench license was not located; WritingPrompts mirror labels MIT without resolving original Reddit rights.

Two **derived resources are not counted as downloaded datasets**: [30 published secret words](datasets/derived/secret_words.json) and [one illustrative plot-secret fixture](datasets/derived/plot_secret_fixture.json). The latter still requires construction/validation of a real counterfactual plot benchmark.

## Code

|Repository|Pinned commit|Location|Purpose|
|---|---|---|---|
|[cywinski/eliciting-secret-knowledge](https://github.com/cywinski/eliciting-secret-knowledge)|`45aae57930a7d6ef5503a9b9b23e0b23fd8068ca`|`code/eliciting-secret-knowledge/`|Secret readouts/logit lens/SAEs|
|[rramnauth2220/representational-suppression](https://github.com/rramnauth2220/representational-suppression)|`1b44dfc61c6e7c3acb21874a940670238bf44d54`|`code/representational-suppression/`|Matched suppression probes|
|[Chacioc/Concise-SAE](https://github.com/Chacioc/Concise-SAE)|`ac735478607ebecf3b1ebc4c34c57279c12956d9`|`code/Concise-SAE/`|Sparse instruction feature editing|
|[wang2226/CI-Steering](https://github.com/wang2226/CI-Steering)|`5c5edc3261f9cdf11319b47107894e08b2b40c60`|`code/CI-Steering/`|Compositional residual steering and utility|
|[yangkevin2/doc-story-generation](https://github.com/yangkevin2/doc-story-generation)|`9d727cdbae40c72169ab03b729bff4419a113dac`|`code/doc-story-generation/`|Hierarchical outline structures|

[code/README.md](code/README.md) records entry points, dependencies, licenses, adaptation issues and execution limits. All READMEs inspected; ten selected modules pass AST syntax parsing. No upstream model example was executed. Sparse clones omit large results/outputs/figures, and nested repositories are excluded from the outer Git repository. Recreate with `scripts/clone_resources.py`; repository pins are also in [code/manifest.json](code/manifest.json).

## Search strategy and selection

Keywords: involuntary information leakage; secret-word story writing; semantic leakage; ironic suppression/white bear; explicit narrative outlines; latent response planning; activation probing; sparse activation editing; contextual integrity; premature foreshadowing.

Paper-finder was attempted first. Its missing httpx dependency was installed in the fresh environment, and the diligent retry succeeded: 119 candidates, all relevance=1. Results are preserved in `logs/paper_finder_retry.json` and `paper_search_results/`; [screening ledger](notes/search_screening.json) records selections. Thirteen direct service candidates were downloaded, with additional supplied papers and citation-chased methods making 23 unique PDFs. Lower-priority adjacent games, storytelling UX, multimodal generation and other methods were not all downloaded; downloading all 119 would defeat the stated relevance and three-direction scope. This is an explicitly scoped selection, not a claim that every returned paper was read or downloaded.

Primary-source arXiv pages/PDFs were used to resolve every supplied unknown title and author list; official GitHub links supplied implementations. Hugging Face was checked first for narrative datasets, then paper-linked repositories for more direct probes. Story Cloze was considered but its labels do not measure forbidden foreshadowing. No staged local resources or explicit repository references were provided.

## Challenges and remaining limitations

- The closest leakage paper redacts its code URL. Its published prompts/word list are usable, but this is not an official-code reproduction. The Luo paper promises code release; a verified public implementation was not identified.
- Latest downloaded arXiv versions include differences and internal inconsistencies: decoy offset in 2605.10794; synthetic leakage decimal in 2604.00209; model naming between 2605.28639 and its repository. Hashes and chunk notes preserve the inspected evidence.
- Suppression probing is already prior art. Novelty rests on controlled outline effects and causal tests that retain writing utility; a decoder becoming inaccurate does not prove secret removal.
- WritingPrompts repeats premises; FreeInstruct has one duplicate story. Split by context/template families. Published arbitrary-word results cannot be relabeled as evidence about future plot endings.
- Five source downloads parsed successfully, but this is structural validation, not validation of benchmark labels or model quality. Some licenses need source-specific interpretation before redistribution.
- No checkpoint or SAE weights were downloaded and no inference API was called. An RTX A6000 (49,140 MiB) was visible, but model access, compatible runtime packages and actual free memory must be checked by the experiment runner. Upstream frozen dependencies conflict; install only the selected runtime components. DOC relies on legacy interfaces and should supply templates rather than a drop-in runner.

## Concrete next steps

1. Re-run `uv sync` and `.venv/bin/python scripts/validate_resources.py` from the root. Use the existing project `.venv`; no conda or shared environment.
2. Build grouped input/split manifests using the 30 words and eligible WritingPrompts premises; construct outlines before secret assignment. Pilot the six D1 conditions, separating word secrecy from the later plot-secret extension.
3. Add blinded/counterbalanced semantic inference, exact-alias checks, no-secret calibration, quality and recall controls. Size the main study from the paired pilot variance, not reused judge-pair counts.
4. Adapt the suppression repository for generated-token and identical-continuation D2 readouts. Only then apply validated D3 interventions with random/unrelated controls, cache accounting and quality limits. Full protocol and pruned alternatives are in planning.md.

## Environment and reproducibility

`pyproject.toml` and `uv.lock` capture the resource environment (Python>=3.10; actual interpreter recorded by final validation). Installed tooling: requests/httpx, pypdf, PyMuPDF, Pillow and pyarrow. Download helpers live under `scripts/`; PDF chunking uses `.codex/skills/paper-finder/scripts/pdf_chunker.py`. Original PDFs stay in papers/, data in datasets/, and clones in code/. Auxiliary extracted text and page images are reproducible and Git-ignored.

Final validation details are in [notes/resource_validation.json](notes/resource_validation.json). `.resource_finder_complete` is created only after those checks pass. STATE.md changes are confined to the resource_finder notes block.

## Experiment-runner execution (4 October 2026)

The execution used the pre-gathered WritingPrompts test parquet and published 15-word inventory, plus 60 agent-authored synthetic plot cases (12 families). Other cataloged datasets and repositories informed controls and feasibility but were not evaluated as benchmarks. Linear probes were implemented directly with Transformers/scikit-learn; no SAE claim or fine-tuning experiment is made.

- Isolated `.venv`, `pyproject.toml`, `uv.lock`, and frozen `requirements.txt`; real local BF16 inference on an RTX A6000. Live OpenRouter catalogs were saved; inference was blocked by the key's daily quota. Model IDs/revisions and access failures are recorded under `notes/` and `results/environment.json`.
- Writer: pinned `google/gemma-3-12b-it`; independent judge: pinned `Qwen/Qwen3-14B`. 1,080 main stories, 120 auxiliary free-writing stories, both-order judgments, plot priors, coherence ratings, and secondary A/B logits are preserved under `results/model_outputs/`.
- All 300 full outline/context input lengths match. Superseded context outputs, an outline-length pilot, failed parser fixtures, and superseded partial forward scores are explicitly archived. The constant duplicated Gemma BOS is an important external-validity limitation, not concealed as canonical prompting.
- Main word detection: baseline 60.6%, outline 54.4%, context 63.9%, decoy 54.4%. Only outline-context survives the primary five-comparison correction; the secondary probability-based contrast does not. Exact disclosures are 27/90, 15/90, 31/90, 10/90 respectively. Nonliteral leakage and plot effects remain unresolved.
- Controlled residuals cover 24 contexts × 15 secrets × 3 conditions, with 3 layers and 3 positions. The original decoder fails the behavioral-intervention gate. Post hoc counterfactual centering reveals secret information, but does not validate an online erasure direction. No behavioral ablation output is claimed.
- Exact replay passed 4/4 smoke stories and 32/32 recorded-batch stories. Two full saved-output analysis passes agree byte-for-byte. Validation artifacts, actual timings, costs/limitations, and reproduction commands are linked from [REPORT.md](REPORT.md) and [README.md](README.md).

The full decision and correction trail is in [notes/planning_history.md](notes/planning_history.md); [results/error_analysis.md](results/error_analysis.md) separates direct disclosure from subtle leakage and measurement failure.
