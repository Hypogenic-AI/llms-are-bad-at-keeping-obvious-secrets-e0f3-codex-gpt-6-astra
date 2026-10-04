#!/usr/bin/env bash
# Deterministic CPU analysis of recorded model outputs; no inference/API calls.
set -euo pipefail
pwd
test -f results/model_outputs/stories.jsonl
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=8
PYTHON_BIN=.venv/bin/python
"$PYTHON_BIN" src/test_protocol.py
"$PYTHON_BIN" src/analyze.py
"$PYTHON_BIN" src/robustness.py
"$PYTHON_BIN" src/analyze_diagnostics.py
"$PYTHON_BIN" src/outline_adherence.py
"$PYTHON_BIN" src/literal_analysis.py
"$PYTHON_BIN" src/exposure_audit.py
"$PYTHON_BIN" src/analyze_interventions.py
"$PYTHON_BIN" src/analyze_online.py
"$PYTHON_BIN" src/choice_likelihood.py analyze
"$PYTHON_BIN" src/probe_literal_association.py
"$PYTHON_BIN" src/plot_literal.py
"$PYTHON_BIN" src/plot_diagnostics.py
"$PYTHON_BIN" src/plot_mechanism.py

"$PYTHON_BIN" src/probe_diagnostics.py
"$PYTHON_BIN" src/centered_probe.py
"$PYTHON_BIN" src/plot_centered.py
