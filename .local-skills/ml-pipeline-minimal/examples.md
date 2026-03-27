# ML Pipeline Minimal Skill Examples

## Example 1: Tighten preprocessing validation

**Task intent**

Add safer validation around raw data loading or cleaning in [`src/preprocess.py`](src/preprocess.py) without changing the overall pipeline structure.

**Expected behavior**

- Keep the existing cleaning flow intact.
- Preserve output to [`data/processed/`](data/processed/).
- Avoid changing unrelated modules.

## Example 2: Improve training consistency

**Task intent**

Adjust logic in [`src/train.py`](src/train.py) so model configuration or preprocessing stays consistent across Logistic Regression, Random Forest, and XGBoost.

**Expected behavior**

- Preserve current model comparison behavior.
- Avoid moving training logic into a new framework.
- Keep compatibility with [`src/evaluate.py`](src/evaluate.py).

## Example 3: Standardize evaluation outputs

**Task intent**

Extend [`src/evaluate.py`](src/evaluate.py) to export metrics or plots in a more stable format.

**Expected behavior**

- Keep outputs under [`outputs/tables/`](outputs/tables/) and [`outputs/figures/`](outputs/figures/).
- Do not change the repository structure.
- Preserve compatibility with [`src/run_pipeline.py`](src/run_pipeline.py).

## Example 4: Improve end-to-end orchestration

**Task intent**

Make a minimal, low-risk improvement to stage control or failure handling in [`src/run_pipeline.py`](src/run_pipeline.py).

**Expected behavior**

- Preserve the current stage order.
- Preserve current file paths and outputs.
- Avoid broad refactors across the codebase.

## Example 5: Extend prioritization logic safely

**Task intent**

Refine scoring or segmentation logic in [`src/prioritize.py`](src/prioritize.py) while preserving existing outputs.

**Expected behavior**

- Keep retention artifacts under [`outputs/tables/`](outputs/tables/).
- Preserve compatibility with predictions produced by the selected model.
- Do not introduce unrelated business-rule frameworks.

## Example 6: Reject out-of-scope work

**Task intent**

A request asks for frontend setup, notebook migration, or generic stack scaffolding.

**Expected behavior**

This skill should explicitly classify the request as out of scope for [`.local-skills/ml-pipeline-minimal/skill.md`](.local-skills/ml-pipeline-minimal/skill.md) and avoid generating unrelated project structure.