## primary

| Task | Condition | Pairs | Detection accuracy [95% CI] |
|---|---|---|---|
| plot | baseline | 60 | 49.2% [47.5, 50.0] |
| plot | context | 60 | 49.2% [47.5, 50.0] |
| plot | outline | 60 | 49.2% [47.5, 50.0] |
| word | baseline | 90 | 60.6% [56.1, 65.0] |
| word | context | 90 | 63.9% [58.9, 68.9] |
| word | decoy | 90 | 54.4% [51.1, 57.8] |
| word | outline | 90 | 54.4% [51.7, 57.8] |

## contrasts

| Task | Contrast | Difference, percentage points [95% CI] | Holm p |
|---|---|---|---|
| plot | outline - baseline | +0.0 [-2.5, +2.5] | 1.0000 |
| plot | outline - context | +0.0 [+0.0, +0.0] | 1.0000 |
| word | outline - baseline | -6.1 [-11.1, -1.1] | 0.1340 |
| word | outline - context | -9.4 [-15.0, -3.9] | 0.0155 |
| word | decoy - baseline | -6.1 [-11.7, -1.1] | 0.1340 |

## literal

| Condition | Secret supplied: exact disclosures / 90 | No secret: exact disclosures / 90 | Detection without literal pairs [95% CI] |
|---|---|---|---|
| baseline | 27 | 2 | 51.6% [48.4, 54.9] |
| outline | 15 | 2 | 50.7% [50.0, 52.0] |
| context | 31 | 1 | 52.5% [49.2, 56.8] |
| decoy | 10 | 1 | 50.6% [50.0, 51.9] |

## plot

| Forecast contrast | Complete pairs | Difference, pp [95% CI] | Holm p |
|---|---|---|---|
| baseline private-minus-no-secret | 57 | +8.8 [+2.6, +14.8] | 0.1960 |
| context private-minus-no-secret | 55 | +6.4 [-1.9, +14.3] | 0.7312 |
| outline private-minus-no-secret | 60 | -0.8 [-5.8, +5.0] | 1.0000 |
| forecast difference-in-differences outline - baseline | 57 | -8.8 [-16.4, +0.0] | 0.4076 |
| forecast difference-in-differences outline - context | 55 | -5.5 [-13.9, +3.6] | 0.7312 |

## probe

| Condition | Token | Raw layer-32 accuracy | Centered accuracy [95% CI] | Centered shuffled-label accuracy |
|---|---|---|---|---|
| baseline | 32 | 6.7% | 82.2% [61.1, 96.7] | 7.8% |
| baseline | 256 | 8.9% | 91.1% [83.3, 97.8] | 10.0% |
| baseline | 512 | 14.4% | 84.4% [73.3, 93.3] | 8.9% |
| outline | 32 | 6.7% | 68.9% [56.7, 81.1] | 10.0% |
| outline | 256 | 6.7% | 66.7% [48.9, 83.3] | 11.1% |
| outline | 512 | 8.9% | 67.8% [52.2, 83.3] | 10.0% |
| context | 32 | 11.1% | 85.6% [68.9, 97.8] | 10.0% |
| context | 256 | 12.2% | 93.3% [86.7, 98.9] | 3.3% |
| context | 512 | 11.1% | 87.8% [82.2, 93.3] | 3.3% |

## likelihood

| Study | Task | Condition | Order-balanced log-odds decision accuracy [95% CI] |
|---|---|---|---|
| anchor | word | free_anchor | 54.2% [41.7, 66.7] |
| main | plot | baseline | 40.8% [28.3, 53.3] |
| main | plot | context | 42.5% [27.5, 59.2] |
| main | plot | outline | 40.8% [26.7, 56.7] |
| main | word | baseline | 62.8% [52.8, 72.8] |
| main | word | context | 72.8% [63.3, 81.7] |
| main | word | decoy | 61.1% [51.1, 71.1] |
| main | word | outline | 56.1% [46.1, 66.1] |

## likelihood_contrasts

| Task | Secondary contrast | Difference, pp [95% CI] | Holm p |
|---|---|---|---|
| plot | outline - baseline | +0.0 [-19.2, +20.8] | 1.0000 |
| plot | outline - context | -1.7 [-26.7, +24.2] | 1.0000 |
| word | outline - baseline | -6.7 [-19.4, +6.1] | 1.0000 |
| word | outline - context | -16.7 [-30.6, -1.7] | 0.1650 |
| word | decoy - baseline | -1.7 [-13.9, +10.6] | 1.0000 |