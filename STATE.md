# Research State

- Current phase: `None`
- Pipeline completed: `True`

## Previous phases

resource_finder (succeeded), experiment_runner (succeeded)

## Current phase context

- Phase: `experiment_runner`
- Status: `completed`
- Started: `2026-10-04T03:56:16.975924Z`
- Next steps:
  - Validate the report and experimental artifacts before finalizing.

## Workspace check

- Root: `/workspaces/llms-are-bad-at-keeping-obvious-secrets-e0f3-codex-gpt-6-astra`
- Directory usable: `True`

## Output validation

- Valid: `True`
- Expected: `REPORT.md`
- Missing: None
- Outside workspace: None

## Agent notes

<!-- NEURICO_AGENT_NOTES_START -->
### resource_finder
<!-- NEURICO_AGENT_NOTES_START:resource_finder -->
Resource-finder Phases 1–5 completed on 2026-10-04. Artifacts: literature_review.md (concise synthesis), resources.md (catalog), planning.md (ranked directions and runnable-study specification), and papers/datasets/code READMEs. 23 original PDFs; all ten supplied plus three close papers read across every chunk (notes/reading_log.md). Four source datasets/five raw files (32,535,349 bytes) validated; five official repositories pinned and inspected. Integrity/reading coverage/Git exclusions PASS: notes/resource_validation.json. Completion signal: .resource_finder_complete.
Top three directions fixed: D1 matched secret-blind/aware outline comparisons; D2 generated-token temporal decoding with identical-continuation controls; D3 selective interventions with sham, cache, quality and recall controls. Pruned alternatives and reasons remain in planning.md. Paper-finder returned 119 uniformly weak-ranked candidates; scoped selections/exclusions recorded in notes/search_screening.json.
Next: experiment_runner should read resources.md/planning.md; use project .venv and uv.lock; check model access/runtime and available A6000 memory; construct grouped splits (WritingPrompts repeats premises), run D1 pilot, validate probes before D2/D3. No model experiment or API inference was run here. Plot-secret fixture is illustrative: curate and validate counterfactual endings before claims about foreshadowing.
Unresolved: closest leakage-paper code redacted; certain source statistics/decoy formula inconsistent; ReboundBench license unspecified; old DOC interfaces need adaptation. FreeInstruct data terms are CC BY-NC 4.0 per paper, suppression data CC BY 4.0 per README. Probe failure does not prove erasure; privacy steering can collapse writing utility. These do not block resource handoff. No direction expansion or edits outside this phase's STATE notes.
<!-- NEURICO_AGENT_NOTES_END:resource_finder -->

### experiment_runner
<!-- NEURICO_AGENT_NOTES_START:experiment_runner -->
Phase 6 complete; all execution phases attempted and final documentation validated. Outputs: REPORT.md, README.md, results/report_tables.md, raw model outputs, figures, source code, pinned environment, and updated resources.md. Primary sample: 1,080 stories; outline-context word detection difference -9.4 pp (Holm p=.0155), not confirmed by secondary likelihood scoring. Exact disclosure: baseline 27/90, outline 15/90; subtle and plot leakage unresolved. Raw residual decoder failed its gate, so behavioral ablations were not run; post hoc counterfactual centering finds secret information but does not establish causal removal. Limitations include duplicate BOS, judge position bias, and small context groups. Validation: 20 structural/provenance checks passed; identical hashes across two analysis passes; exact smoke 4/4 and recorded batch 32/32 replay; all document links resolve. results/process_cleanup.json confirms no active experiment jobs. No further phase remains; scientific follow-ups are clearly separated from completed execution.
<!-- NEURICO_AGENT_NOTES_END:experiment_runner -->

<!-- NEURICO_AGENT_NOTES_END -->
