# ML Pipeline Minimal Skill Checklist

## Pre-Task Checks

- Confirm the task is limited to the machine learning engineering workflow.
- Confirm the task maps to one or more of:
  - [`src/preprocess.py`](src/preprocess.py)
  - [`src/eda.py`](src/eda.py)
  - [`src/train.py`](src/train.py)
  - [`src/evaluate.py`](src/evaluate.py)
  - [`src/explain.py`](src/explain.py)
  - [`src/prioritize.py`](src/prioritize.py)
  - [`src/run_pipeline.py`](src/run_pipeline.py)
- Read [`README.md`](README.md), [`environment.yml`](environment.yml), and [`docs/final_execution_plan.md`](docs/final_execution_plan.md) before proposing changes.

## Data and Path Checks

- Raw dataset path remains under [`data/raw/`](data/raw/).
- Processed dataset path remains under [`data/processed/`](data/processed/).
- Generated figures, tables, and models remain under [`outputs/`](outputs/).
- No new path convention conflicts with the current repository layout.

## Change-Safety Checks

- Prefer the smallest correct edit.
- Avoid broad refactors unless explicitly required.
- Preserve current function responsibilities.
- Preserve current script entry behavior in [`src/run_pipeline.py`](src/run_pipeline.py) unless the task explicitly changes orchestration.
- Preserve compatibility with existing output consumers.

## Environment Checks

- Use [`environment.yml`](environment.yml) as the dependency baseline.
- Do not introduce a conflicting environment-management workflow.
- Do not add dependencies without clear need.

## Out-of-Scope Checks

Reject or defer work that is mainly about:

- frontend setup
- full-stack scaffolding
- notebook-centric redesign
- academic writing workflows
- generic reusable framework extraction

## Completion Checks

- The affected pipeline stage is clear.
- The modified files are explicit.
- Output file locations remain consistent.
- Risks, assumptions, and limitations are stated when needed.
- The resulting change fits the project baseline defined in [`docs/final_execution_plan.md`](docs/final_execution_plan.md).