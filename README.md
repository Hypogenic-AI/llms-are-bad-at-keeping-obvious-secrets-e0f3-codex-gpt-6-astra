# Outlines, secrets, and hidden states

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
