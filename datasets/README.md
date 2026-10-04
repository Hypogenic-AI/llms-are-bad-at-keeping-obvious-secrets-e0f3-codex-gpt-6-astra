# Downloaded datasets

Four source datasets are locally available (five raw files; about 32.5 MB total). Raw data are ignored by Git; small samples, validation results and provenance manifests are tracked. Checksums and immutable download URLs are in [manifest.json](manifest.json). [validation.json](validation.json) records schemas, counts, missing values and duplication. Downloaded on 2026-10-04. No generated model outputs are represented as collected experimental data.

## Reproduce downloads and validation

From the repository root (verify `pwd` and `.git` first):

```bash
uv sync
.venv/bin/python scripts/download_datasets.py
.venv/bin/python scripts/validate_datasets.py
```

The downloader uses pinned GitHub commits/Hugging Face revisions and validates JSON, CSV and Parquet loading. It skips existing files; compare hashes against the recorded manifest before replacing local copies. For an individual file, copy its `source` URL from the manifest and use `curl -fL URL -o datasets/NAME/FILENAME` after checking the working directory. No Kaggle credentials or Hugging Face token is required for these data.

## 1. Suppression concept library — primary D2/D3 calibration

- Source: [Ramnauth & Scassellati implementation](https://github.com/rramnauth2220/representational-suppression), pinned commit `1b44dfc61c6e7c3acb21874a940670238bf44d54`.
- Local: `suppression_concepts/concepts.json` (71,964 bytes), JSON object keyed by 17 concepts; no predefined train/test split.
- Fields: category, aliases, direct_aliases, indirect_descriptions, contexts, positive, negative, negative_hard. Counts: 113 aliases, 107 direct aliases (overlap; do not sum), 102 indirect descriptions, 136 contexts, 408 positive, 408 negative, 170 hard-negative sentences. The probe corpus has 986 labeled sentences before any deduplication, not 986 independent concepts.
- License: concept library CC BY 4.0; repository code Apache-2.0 (upstream README explicitly distinguishes them). [Small actual sample](suppression_concepts/concepts_sample.json).
- Example: knife has context “Describe a kitchen.” and positive/negative/hard-negative sentence lists. These are non-narrative concept probes, not plot secrets.
- Validation: all concepts have the expected fields; split by context/template family and evaluate hard negatives. Avoid training and evaluating on near-identical positive/negative substitutions.

## 2. FreeInstruct — narrative constraint/utility checks

- Source: [Concise-SAE](https://github.com/Chacioc/Concise-SAE), commit `ac735478607ebecf3b1ebc4c34c57279c12956d9`.
- Local: `freeinstruct/freeinstruct.json` (1,850,993 bytes), 1,212 records, no source split.
- String fields: story, user_input, expected_output, resolution_strategy, normal_input. [Actual samples](freeinstruct/freeinstruct_sample.json).
- Example: a realistic detective story is challenged by a request to use psychic powers; the expected answer maintains ordinary-world constraints. The reference continuation is not a hidden-ending ground truth.
- License: paper 2505.16505 Appendix D states CC BY-NC 4.0 for the data; the inspected repository has no LICENSE file. Preserve the noncommercial attribution terms and source statement.
- Validation: no blank/null cells or missing fields; one duplicate story. Group duplicate and semantically templated settings before splitting. Use for instruction adherence and quality controls, not as direct evidence of spontaneous leakage under benign writing instructions.

## 3. ReboundBench released prompt files — suppression baseline

- Source: [Don't Think of the White Bear](https://github.com/cesium132dot9/Dont-Think-of-the-White-Bear), commit `c6187468e380fc44869ddfd414c8efcd46d94da9`.
- Local: `reboundbench/prompts_negation.csv` (5,000 rows, 401,168 bytes) and `prompts_multi_question.csv` (500 rows, 233,242 bytes). These are two released collections, not independent train/test splits or a claim to reproduce every paper experiment.
- Negation columns: id, prompt_type, topic, forbidden_concept, proxy_concept, prompt_text, is_single_token. Multi-question columns: id, category, topic, forbidden_concept, mentioned_concept, negative_prompt, neutral_prompt, positive_prompt.
- [Negation samples](reboundbench/prompts_negation_sample.json), [multi-question samples](reboundbench/prompts_multi_question_sample.json). Example: a hospital description with “doctor” prohibited versus matched neutral and positive prompts.
- License: no explicit repository license located. Unique IDs and no missing cells in either file. CSV booleans are strings; re-tokenize `is_single_token` for the selected model instead of trusting the supplied flag. Proxy strings such as `car_proxy` are labels, not natural-language replacement concepts.
- Apply only as lexical/load controls within D1/D2. The paper's rebound definition is relative to a high-load suppression baseline and differs from secret-present versus secret-absent semantic leakage.

## 4. WritingPrompts — source premises for D1

- Source: [Hugging Face mirror](https://huggingface.co/datasets/euclaise/writingprompts), revision `35f0aa359452ba8147b34d925684fccee26679cc`; original [Fan et al. paper](https://arxiv.org/abs/1805.04833).
- Local: `writingprompts/test.parquet` (29,977,982 bytes); full published test split of 15,138 prompt/story pairs. Train (272,600) and validation (15,620) were not downloaded; the full mirror is about 605 MB and unnecessary for this pilot.
- Schema: prompt:string, story:string. [Actual samples](writingprompts/test_sample.json). No null/empty strings. There are 5,478 distinct prompt strings and 9,660 repeated prompt occurrences (multiple stories respond to the same prompt); split and sample by prompt, not row. Preserve original row indices and a normalized prompt hash.
- Mirror card labels MIT; underlying Reddit story rights were not independently resolved. Retain provenance. Prompts contain formatting markers, public-figure references, mature material, and sometimes explicit twists. Use only premises that satisfy a fixed eligibility rule; don't let a publicly stated twist become the private secret.
- Existing stories are reference material only, not labeled leakage examples. Do not show their endings to an evaluator of newly generated openings.

## Loading examples

```python
import json, csv
from pathlib import Path
import pyarrow.parquet as pq
concepts = json.loads(Path('datasets/suppression_concepts/concepts.json').read_text())
freeinstruct = json.loads(Path('datasets/freeinstruct/freeinstruct.json').read_text())
with open('datasets/reboundbench/prompts_negation.csv') as f:
    negation = list(csv.DictReader(f))
stories = pq.read_table('datasets/writingprompts/test.parquet').to_pylist()
```

## Derived inputs (not additional downloaded datasets)

- `derived/secret_words.json`: 30 words transcribed from 2605.10794's published appendix (15 curated + 15 reported COCA-sampled words). COCA was not downloaded or resampled. Follow the paper's word list; its decoy table and stated offset disagree, so pre-register a random decoy mapping rather than silently reproducing an ambiguous formula.
- `derived/plot_secret_fixture.json`: one hand-written example specifying public premise, shared outline, two candidate endings and a reveal boundary. It demonstrates input structure only. It has no human validation, independent leakage labels, or power for hypothesis testing.

## Search and gaps

Hugging Face was checked first for WritingPrompts and Story Cloze (`MoE-UNC/story_cloze`). WritingPrompts was chosen for diverse premises; Story Cloze's ending-choice labels do not label forbidden foreshadowing. Paper-linked datasets then supplied more direct suppression and instruction controls. Kaggle/UCI would add little for this specialized task, so no unrelated dataset was downloaded. ConFAIDE concerns socially inappropriate disclosure, and Taboo involves deliberately informative hints: both inform controls but are not substitutes for the target task. A validated corpus of paired, equally plausible plot secrets is still required for the narrative-foreshadowing extension described in [planning.md](../planning.md).
