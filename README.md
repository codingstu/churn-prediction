# Churn Prediction Project

This project implements an explainable churn prediction and retention prioritization workflow for subscription-based service providers.

## Project Orientation

The project is organized around three integrated goals:

1. Predict which customers are likely to churn.
2. Explain the main drivers of churn at both global and customer levels.
3. Prioritize retention actions using predicted churn probability and customer value proxy.

The current baseline is:
- **Conda-managed environment**
- **pure script-based analytics pipeline**
- **proposal files separated from implementation**
- **documentation centralized under `docs/`**
- **future-compatible with a presentation layer where Next.js is preferred and React is only a lightweight fallback**

## Documentation Baseline

All planning and architecture documents are stored under [`docs/`](docs/).

Key documents:
- [`docs/final_execution_plan.md`](docs/final_execution_plan.md)
- [`docs/dataset_selection_and_validation.md`](docs/dataset_selection_and_validation.md)
- [`docs/frontend_integration_plan.md`](docs/frontend_integration_plan.md)
- [`docs/project_structure.md`](docs/project_structure.md)
- [`docs/proposal_to_implementation_mapping.md`](docs/proposal_to_implementation_mapping.md)

Proposal source materials are stored under [`proposal/`](proposal/):
- [`proposal/Proposal_form.docx`](proposal/Proposal_form.docx)
- [`proposal/Proposal_form.md`](proposal/Proposal_form.md)

## Project Structure

```text
churn_prediction/
├── docs/
├── proposal/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── models/
├── src/
├── frontend/
├── environment.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Environment Setup with Conda

### 1. Create the environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate churn_prediction
```

### 3. Verify core dependencies

```bash
python -c "import pandas, sklearn, xgboost, shap; print('environment ready')"
```

## Data Placement

### Primary dataset
The primary thesis dataset is:
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

Expected target column:
- `Churn`

Expected identifier column:
- `customerID`

### Extension dataset
A secondary extension dataset is also available under:
- [`data/raw/Telco Customer Churn/`](data/raw/Telco%20Customer%20Churn/)

This RavenStack dataset is multi-table and synthetic. It is retained for future SaaS extension work, not as the current main thesis dataset.

Dataset selection rationale is documented in [`docs/dataset_selection_and_validation.md`](docs/dataset_selection_and_validation.md).

## Implementation Modules

Current implemented modules:
- [`src/preprocess.py`](src/preprocess.py)
- [`src/eda.py`](src/eda.py)
- [`src/train.py`](src/train.py)
- [`src/evaluate.py`](src/evaluate.py)
- [`src/explain.py`](src/explain.py)
- [`src/prioritize.py`](src/prioritize.py)
- [`src/run_pipeline.py`](src/run_pipeline.py)

## Current Workflow Baseline

### Step 1: Data Cleaning
Use [`src/preprocess.py`](src/preprocess.py) to:
- inspect raw IBM churn data,
- validate the expected IBM Telco schema,
- validate [`customerID`](src/preprocess.py:38) completeness and uniqueness,
- validate raw [`Churn`](src/preprocess.py:37) labels,
- clean `TotalCharges`,
- encode `Churn`,
- export cleaned output to [`data/processed/cleaned_churn.csv`](data/processed/cleaned_churn.csv),
- export preprocessing audit output to [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv).

### Step 2: Exploratory Data Analysis
Use [`src/eda.py`](src/eda.py) to:
- analyze churn distribution,
- inspect churn patterns by tenure, contract, payment method, and charges,
- export paper-ready figures and summary tables.

### Step 3: Modeling
Use [`src/train.py`](src/train.py) to:
- prepare features,
- train Logistic Regression,
- train Random Forest,
- train XGBoost,
- save trained pipelines.

### Step 4: Evaluation
Use [`src/evaluate.py`](src/evaluate.py) to:
- compare ROC-AUC, Recall, Precision, and F1-score,
- generate confusion matrices,
- generate ROC curve comparisons,
- export result tables and figures.

### Step 5: Explainability
Use [`src/explain.py`](src/explain.py) to:
- export Logistic coefficients when applicable,
- export tree-based feature importance,
- generate SHAP summary and local explanation figures.

### Step 6: Retention Prioritization
Use [`src/prioritize.py`](src/prioritize.py) to:
- compute priority score,
- segment customers by risk and value,
- export retention ranking tables.

Priority scoring formula:

```text
PriorityScore = ChurnProbability × MonthlyCharges
```

### Step 7: End-to-End Pipeline
Use [`src/run_pipeline.py`](src/run_pipeline.py) to run the main IBM Telco workflow end to end.

## Core Output Files

Expected outputs include:
- [`data/processed/cleaned_churn.csv`](data/processed/cleaned_churn.csv)
- [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv)
- [`outputs/tables/dataset_overview.csv`](outputs/tables/dataset_overview.csv)
- [`outputs/tables/model_performance_comparison.csv`](outputs/tables/model_performance_comparison.csv)
- [`outputs/models/`](outputs/models/)
- [`outputs/tables/customer_priority_table.csv`](outputs/tables/customer_priority_table.csv)
- [`outputs/tables/top_20_retention_targets.csv`](outputs/tables/top_20_retention_targets.csv)
- figures under [`outputs/figures/`](outputs/figures/)

## Data Cleaning Acceptance Rules

The current IBM Telco preprocessing baseline is considered valid only if all of the following hold:

- raw input path remains [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)
- the raw dataset contains the expected 21-column IBM Telco schema checked by [`validate_raw_schema()`](src/preprocess.py:59)
- [`customerID`](src/preprocess.py:38) is present, non-null, and unique under [`validate_customer_ids()`](src/preprocess.py:74)
- raw [`Churn`](src/preprocess.py:37) values only contain `Yes` and `No` under [`validate_target_values()`](src/preprocess.py:90)
- `TotalCharges` blank strings are normalized before numeric conversion in [`clean_telco_data()`](src/preprocess.py:116)
- the known blank-`TotalCharges` records are removed from the cleaned output, yielding 7032 rows for the current dataset version
- the preprocessing audit table in [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv) explains the retained and dropped counts

## Environment Transition Note

[`requirements.txt`](requirements.txt) is still present temporarily, but the official environment baseline is now [`environment.yml`](environment.yml).

## Frontend Application

A full Next.js frontend is now implemented under [`frontend/`](frontend/).

Current frontend characteristics:
- consumes standardized tables from [`outputs/tables/`](outputs/tables/)
- serves visual artifacts from [`outputs/figures/`](outputs/figures/) through a frontend asset route
- provides route-based pages for dashboard, model comparison, retention priority, explainability, and business insights
- remains decoupled from the Python analytics pipeline under [`src/`](src/)

Frontend commands:

```bash
cd frontend && npm install
cd frontend && npm run dev
```

Recommended active stack:
- **default and implemented**: Next.js
- **acceptable only for lightweight dashboards**: React

## Local Skill

A repository-local minimal skill has been installed at [`.local-skills/ml-pipeline-minimal/`](.local-skills/ml-pipeline-minimal/).

Included files:
- [`.local-skills/ml-pipeline-minimal/skill.md`](.local-skills/ml-pipeline-minimal/skill.md)
- [`.local-skills/ml-pipeline-minimal/checklist.md`](.local-skills/ml-pipeline-minimal/checklist.md)
- [`.local-skills/ml-pipeline-minimal/examples.md`](.local-skills/ml-pipeline-minimal/examples.md)

This local skill is intentionally limited to the machine learning engineering workflow of this repository, centered on [`src/preprocess.py`](src/preprocess.py), [`src/train.py`](src/train.py), [`src/evaluate.py`](src/evaluate.py), [`src/explain.py`](src/explain.py), [`src/prioritize.py`](src/prioritize.py), and [`src/run_pipeline.py`](src/run_pipeline.py).

It is not intended for frontend scaffolding, generic stack generation, or academic writing workflows.

## Notes

- Raw and processed data are excluded from version control by default via [`.gitignore`](.gitignore).
- Generated figures, tables, and serialized models are also ignored by default.
- The main execution and planning baseline is [`docs/final_execution_plan.md`](docs/final_execution_plan.md).
- Dataset validation and selection decisions are documented in [`docs/dataset_selection_and_validation.md`](docs/dataset_selection_and_validation.md).
