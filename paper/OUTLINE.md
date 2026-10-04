# Paper outline and evidence map

Title: Secret-Blind Outlines Reduce Literal Disclosure in a Controlled Story-Writing Study
Author: Ari Holtzman and NeuriCo

## Abstract (150–250 words)
- Separate exact disclosure from nonliteral hints.
- 90 word and 60 plot units; 1,080 stories; matched context and decoy controls.
- Primary outline/context effect, literal counts, failed probe gate, centered diagnostic.
- State encoding and evaluator limits; no behavioral intervention.

## Introduction
- Withholding a word differs from withholding its influence.
- Prior secret-writing and suppression work leaves outline/context comparison open.
- Explain computational blinding and controlled comparison; reference method schematic.
- Preview quantitative results; three contributions and organization.

## Related work
- Involuntary/semantic leakage and suppression: Holtzman–West, Gonen, Mann, Ramnauth.
- Narrative planning: Yao, Yang (Re3/DOC), Xie; latent planning: Wu, Dong.
- Secret readouts and privacy: Cywinski (two papers), Mireshghallah, Zhao, Wang, Baldelli.
- Source: supplied literature review, local archived paper catalog and PDFs.

## Methodology
- Conditions, word/plot construction, computational blinding, exact token matching.
- Pinned local checkpoints and duplicated BOS, sampling and archived corrections.
- Pairwise score, unit/cluster bootstrap, Holm families, secondary likelihood diagnostic.
- Residual split, closed-set logistic decoder, transductive centering, fixed intervention gate.
- Sources: src/behavior.py, src/mechanism.py, REPORT.md, results/story_jobs.json.

## Results
- Primary estimates and all five contrasts: results/report_tables.md.
- Literal outcomes, post-treatment subset warning, example disclosures.
- Plot insensitivity, forecast nulls, utility, secondary nonconfirmation.
- Raw failed probe, centered success, replay associations, offline projection failure.
- No invented ablation: identify unexecuted intervention explicitly.

## Discussion and conclusion
- Content constraints consistent with result; planning causality unresolved.
- Measurement sensitivity, encoding, sample/split, output-length, transductive limitations.
- Broader implications and concrete follow-up without privacy guarantees.

## Visuals and tables
- New vector method schematic drawn from protocol (not experimental data).
- Existing literal-disclosure and centered-decoding figures copied without data changes.
- Main: detection table, primary contrast table, literal table.
- Appendix: complete likelihood/forecast/probe tables, literal contrasts, offline checks.

## Appendix
- Reproduction: revisions, software, sampling, exact prompts, inventory, artifacts, audits.
- Complete secondary numerical results and probe results.
- Correction history and intervention criteria.

## Review criteria
- Exact requested author/preamble/imports, all substantive sections complete.
- No exemplar files exist beyond paper_examples/README.md; follow supplied style guide.
- Retain original math/general templates; add necessary package dependencies.
- Check bibliography metadata against archived primary-source metadata.
- Compile through pdflatex/bibtex/pdflatex/pdflatex and inspect rendered pages.
