# ML Pipeline Minimal Skill

## Purpose

This local skill is a minimal, project-specific skill for the churn prediction repository. It is designed to support the existing machine learning engineering workflow only.

It must operate against the current repository structure and avoid introducing unrelated scaffolding.

## Scope

This skill is limited to work involving:

1. Data preprocessing in [`src/preprocess.py`](src/preprocess.py)
2. Exploratory analysis in [`src/eda.py`](src/eda.py)
3. Model training in [`src/train.py`](src/train.py)
4. Model evaluation in [`src/evaluate.py`](src/evaluate.py)
5. Explainability analysis in [`src/explain.py`](src/explain.py)
6. Retention prioritization in [`src/prioritize.py`](src/prioritize.py)
7. End-to-end orchestration in [`src/run_pipeline.py`](src/run_pipeline.py)

## Repository Context

Before making recommendations or code changes, inspect these files first:

- [`README.md`](README.md)
- [`environment.yml`](environment.yml)
- [`docs/final_execution_plan.md`](docs/final_execution_plan.md)
- [`src/preprocess.py`](src/preprocess.py)
- [`src/eda.py`](src/eda.py)
- [`src/train.py`](src/train.py)
- [`src/evaluate.py`](src/evaluate.py)
- [`src/explain.py`](src/explain.py)
- [`src/prioritize.py`](src/prioritize.py)
- [`src/run_pipeline.py`](src/run_pipeline.py)

## Default Workflow Model

Treat the project as this fixed pipeline:

Raw data -> preprocess -> eda -> train -> evaluate -> explain -> prioritize -> outputs

Use the pipeline entrypoint in [`src/run_pipeline.py`](src/run_pipeline.py) as the integration baseline unless the task explicitly targets an individual module.

## Constraints

Always preserve these constraints:

- Environment baseline is [`environment.yml`](environment.yml), not ad hoc environment setup.
- Raw input data belongs under [`data/raw/`](data/raw/).
- Processed data belongs under [`data/processed/`](data/processed/).
- Figures, tables, and models belong under [`outputs/`](outputs/).
- Prefer minimal-risk edits over refactors.
- Preserve current script-first architecture.
- Do not introduce notebook-first workflows.
- Do not introduce frontend code or full-stack scaffolding.
- Do not add documentation-generation workflows unless explicitly requested.
- Do not change research scope encoded in [`docs/final_execution_plan.md`](docs/final_execution_plan.md) unless explicitly requested.

## Operating Rules

When handling a task, follow this order:

1. Identify the target pipeline stage.
2. Identify the exact affected file or files.
3. Check whether the requested change is compatible with current outputs and paths.
4. Prefer the smallest correct implementation.
5. Preserve backward compatibility for existing scripts and output locations.
6. State uncertainty clearly if repository context is insufficient.

## Recommended Task Types

This skill is appropriate for:

- Adding validation around dataset loading
- Tightening preprocessing logic
- Improving train/evaluate consistency
- Standardizing output file generation
- Extending explainability artifacts
- Improving prioritization logic
- Adding safer stage orchestration in [`src/run_pipeline.py`](src/run_pipeline.py)

## Out of Scope

This skill should reject or de-prioritize:

- Frontend setup
- Generic stack scaffolding
- Academic writing support
- Multi-project template generation
- Packaging this repository as a reusable framework
- Large architectural rewrites without explicit approval

## Installation Note

This is a repository-local skill. It is intentionally stored inside [`.local-skills/ml-pipeline-minimal/`](.local-skills/ml-pipeline-minimal/) so it can be reused within this repository without turning it into a separate distributable package.