#!/usr/bin/env bash
# Run from the workspace root after uv sync. Existing checkpoints are reused.
set -euo pipefail
pwd
test -f pyproject.toml
test -f STATE.md
export HF_HOME="$PWD/artifacts/hf"
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=8
PYTHON_BIN=.venv/bin/python
"$PYTHON_BIN" src/prepare_data.py
"$PYTHON_BIN" src/test_protocol.py
"$PYTHON_BIN" src/local_runtime.py
"$PYTHON_BIN" src/behavior.py outlines --batch-size 24
"$PYTHON_BIN" src/behavior.py stories --batch-size 32
"$PYTHON_BIN" src/anchor.py
"$PYTHON_BIN" src/independent_judge.py judge --batch-size 16
"$PYTHON_BIN" src/analyze.py
"$PYTHON_BIN" src/robustness.py
"$PYTHON_BIN" src/diagnostics.py
"$PYTHON_BIN" src/analyze_diagnostics.py
"$PYTHON_BIN" src/outline_adherence.py
"$PYTHON_BIN" src/literal_analysis.py
"$PYTHON_BIN" src/mechanism.py extract
"$PYTHON_BIN" src/mechanism.py analyze
"$PYTHON_BIN" src/free_states.py
"$PYTHON_BIN" src/intervene.py
"$PYTHON_BIN" src/analyze_interventions.py
"$PYTHON_BIN" src/analyze_online.py
"$PYTHON_BIN" src/choice_likelihood.py
"$PYTHON_BIN" src/exposure_audit.py
"$PYTHON_BIN" src/probe_literal_association.py
"$PYTHON_BIN" src/plot_literal.py
"$PYTHON_BIN" src/plot_diagnostics.py
"$PYTHON_BIN" src/plot_mechanism.py

"$PYTHON_BIN" src/probe_diagnostics.py
"$PYTHON_BIN" src/centered_probe.py
"$PYTHON_BIN" src/plot_centered.py
