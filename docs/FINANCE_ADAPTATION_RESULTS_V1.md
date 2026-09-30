## Executive summary (read this first)

The frozen GEPA pilot is complete. These are prompt-adaptation results for one
actor/provider on 48 fresh released questions and24 researcher-authored questions.
No model weights changed; template/family selection limits generalization.

| Strategy | Source parsed/48 | Source financially valid/48 | Released credits/48 | Transfer parsed/24 | Transfer financially valid/24 |
|---|---:|---:|---:|---:|---:|
| seed | 48 | 47 | 24 | 24 | 23 |
| manual | 48 | 48 | 25 | 24 | 23 |
| source-0 | 48 | 47 | 24 | 24 | 23 |
| source-1 | 48 | 48 | 25 | 24 | 23 |
| repaired-0 | 48 | 47 | 24 | 24 | 21 |
| repaired-1 | 48 | 48 | 25 | 24 | 22 |

Adaptation consequence gate by optimizer seed: `{'0': False, '1': False}`.
Repair gate by optimizer seed: `{'0': False, '1': False}`.

Accounted API cost: $0.162813161; calls: 942.
All failed attempts remain in denominators. Transfer has no released target;
its released-label reward is undefined. The original800-answer study is unchanged.
The independent evaluation reports numerical validity, not trace certification.
See the prospective protocol and independent validation for assumptions and gates.

Full development trajectories, per-family counts, selected prompts and raw API
records are retained under outputs/finance-adaptation-v1. Both development
objectives retain the exact source-label cent window on the two passing controls.

Execution note: these are V2 results after a disclosed logging repair. The incomplete V1 attempt remains intact with459 calls and no holdouts. The repeat uses unchanged scientific rules and a separate prospective execution freeze; it is a feasibility rerun after observed development outputs. See FINANCE_ADAPTATION_EXECUTION_AMENDMENT.md.
