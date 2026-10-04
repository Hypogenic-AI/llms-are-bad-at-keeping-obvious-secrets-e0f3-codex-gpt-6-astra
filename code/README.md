# Cloned code resources

Five official repositories, selected to support the three directions in [planning.md](../planning.md). No code repository was explicitly specified by the user. All five READMEs and relevant dependencies/entry points were inspected. [manifest.json](manifest.json) pins commit IDs; [validation.json](validation.json) records syntax checks and runtime limits. Sparse checkouts omit large released results, figures and outputs; source/data shipped inside repositories retain their original layout. The experiment-facing downloaded datasets are separately under `../datasets/`.

## Reproduce

Check `pwd` and `.git` at the workspace root, then run:

```bash
.venv/bin/python scripts/clone_resources.py
```

The script clones shallow/sparse repositories and checks out the pinned commits. Existing directories are preserved. To obtain an omitted source asset, first check the repository's tree and selectively add its path with `git -C code/REPO sparse-checkout add --no-cone PATH`. These are independent nested Git repositories, ignored by the outer repository; they are not submodules or vendored source.

Use the workspace `.venv` and `uv add` for the eventual minimal runtime stack. Do not follow upstream conda setup examples. Upstream dependency snapshots conflict with each other and should not all be installed together. Model examples were **not run**: runtime dependencies, writer weights, SAE checkpoints and external evaluation API access remain experiment-runner work. The resource environment already supports download/validation scripts. An RTX A6000 with 49,140 MiB was visible at inspection; available memory during the next phase must be checked again.

## Eliciting Secret Knowledge

- [Official repository](https://github.com/cywinski/eliciting-secret-knowledge); local `eliciting-secret-knowledge/`; MIT.
- Purpose: white-box extraction (logit lens, residual/embedding similarity, SAE features) and black-box auditors for Taboo, User Gender and Secret Side Constraint models. Covers the expanded 2510.01070 benchmark; earlier 2505.14352 code is [EmilRyd/eliciting-secrets](https://github.com/EmilRyd/eliciting-secrets), not cloned because the expanded implementation supplies the relevant methods.
- Reuse `elicitation_methods/logit_lens.py`, `residual_tokens.py`, `sae.py`, `utils/sae_utils.py`, and `taboo/scripts/00_run_auditing.sh`. Logit lens applies the model's final norm and output head to intermediate layer states; its native support is architecture-specific. Token selection modes include assistant-control and response positions: adapt explicitly for D2's generated-only measurement.
- Usual sequence: run inference → collect internal readouts → ask an auditor. Do not run the full auditing shell pipeline for the benign-writing task; it includes different adversarial methods outside this project's scope. `taboo/evaluate_internalization_taboo.py --in-context` illustrates the prompt-conditioned setting.
- Dependencies inspected: torch 2.7.0, transformers 4.51.3, nnsight 0.4.10, transformer-lens 2.16.1, sae-lens, optional flash-attn, model access and evaluator APIs. Gemma SAEs need Neuronpedia feature descriptions; SSC density estimation needs additional data. Checkpoints are linked from the upstream README and have not been downloaded. Reuse readout code rather than training the large model organisms.

## Representational suppression

- [Official repository](https://github.com/rramnauth2220/representational-suppression); local `representational-suppression/`; Apache-2.0 code, **CC BY 4.0 concept library and released data** per README.
- Best starting point for D2: `exp1_recoverability.py` builds five conditions, trains layerwise logistic probes and supports last/mean/target-token pooling. `exp3_leakage.py` performs generation, alias matching and embedding similarity; `exp2_attention.py` supplies an optional attention diagnostic. `exp4_cross_model.py` aggregates existing outputs, not another model runner.
- Dependencies: torch, transformers, accelerate for auto device maps, numpy/pandas/scipy/scikit-learn/matplotlib/tqdm; sentence embedding model for exp3. Llama/Gemma may require model access. Published examples use bfloat16 and chat templates.
- Code inspection: `train_probes` uses row-level stratified `train_test_split`; if examples are too few, it falls back to fitting and testing on the same data. Replace both with group-disjoint splits and an explicit insufficient-data error. `pool_hidden` on prompt tokens cannot establish continuous secret activity during generated prose. Extend extraction to aligned continuation positions. Preserve matched concept/context IDs in bootstrap analyses.
- The copied concept library in `../datasets/suppression_concepts/` exactly matches this commit. README examples target Meta-Llama-3-8B; the paper discusses Llama-3.1-8B. Record and verify the actual model revision instead of silently treating these as identical.

## Concise-SAE

- [Official repository](https://github.com/Chacioc/Concise-SAE); local `Concise-SAE/`; no explicit repository LICENSE located; paper Appendix D states CC BY-NC 4.0 for its data.
- Relevant pipeline: `save_activations.py` → `select_neuron.py` → `bayesian_optimization.py` → `generation.py` → `evaluation.py`; prompt construction in `prompts.py`, SAE loading in `sae_repo_utils.py`, forward-hook editing in `patch_utils.py` and `generation_utils.py`.
- Useful for D3 feature selection and intervention plumbing; it steers instruction adherence, not necessarily the identity of a hidden secret. Optimization must use validation cases only. Published FreeInstruct references are available separately in datasets/.
- Heavy pinned stack includes torch/CUDA, transformers, SAE/interpretability packages and Bayesian optimization; evaluation calls an external model API. Code contains direct `.cuda()` calls. Check architecture/SAE compatibility and whether reconstruction residual is preserved before using its hooks.
- README generation command has `mmeta-llama` typo and missing shell continuation after `--length 150`; it also requires manually copying optimized values into `opt_value.py`. Treat examples as guidance, not executable commands as printed. No optimization or API evaluation was run here.

## CI-Steering

- [Official repository](https://github.com/wang2226/CI-Steering); local `CI-Steering/`; MIT.
- Reuse `src/control/ci_steering.py` (`CICompositionalSteering`), `src/control/steering.py`, `src/utils/model_utils.py`, `src/reading/`, and `src/utility_evaluation.py`. `src/generate_stimuli.py` illustrates matched contrast construction; external ConFAIDE and PrivaCI-Bench are **not** bundled/downloaded.
- Requirements: torch>=2.1, transformers>=4.40, accelerate, peft, sklearn, numerical stack; model access and an API for GPT-as-judge. ModelHelper abstracts common Hugging Face architectures.
- Inspected hook adds weighted per-axis unit directions to all hidden positions received by the hook; norm preservation is optional and defaults off. D3 must restrict tokens deliberately, normalize total perturbation across controls, and log KV-cache handling. Privacy-axis addition is conceptually different from removal of a secret direction.
- The paper's appendix utility collapse and inconsistent synthetic leakage numbers are recorded in reading notes. Keep quality evaluation in any adaptation; do not equate a low disclosure rate with successful useful erasure.

## DOC story generation

- [Official repository](https://github.com/yangkevin2/doc-story-generation); local `doc-story-generation/`; MIT.
- Reuse outline representation and prompts in `story_generation/plan_module/plan.py`, `outline.py`, and the orchestration in `scripts/main.py`. `scripts/data/save_re3_plan.py` reduces a detailed outline to a coarser Re3 plan; `scripts/rolling_baselines.py` implements rolling context controls.
- It separates hierarchical outlining and passage generation with an OPT-350M FUDGE controller. D1 can borrow outline structure without recreating controller training. Full generation additionally requires reranker/controller checkpoints not downloaded here.
- Historical environment: Python3.8/PyTorch1.13, transformers4.21.2, openai0.16.0 and legacy GPT3/Alpa serving assumptions. Do not install these old pins into the new workspace. Port the plan template to the selected writer. The README points to [doc-storygen-v2](https://github.com/facebookresearch/doc-storygen-v2) for chat-model support; this is an optional reference, not a sixth implementation direction or a validated local dependency.

## Validation scope and unresolved access

Ten selected Python entry points parsed successfully with `ast.parse`; this checks syntax only, not imports, model compatibility or numerical correctness. Repository commits match the manifest; no upstream source was modified. The closest writing-leakage paper (2605.10794) redacts its code URL; its word list and prompts can be reconstructed from the PDF. Luo et al. (2603.25187) promise later code release in the inspected paper. These gaps are explicit rather than replaced by an alleged official reproduction.
