# Project Structure Baseline

## 1. Purpose

This document defines the intended directory responsibilities for the churn prediction project.

It is used to prevent mixing proposal files, implementation logic, generated artifacts, and future frontend code.

---

## 2. Target Structure

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
├── frontend/              # implemented Next.js presentation layer
├── environment.yml
├── requirements.txt       # transitional only, to be deprecated
├── .gitignore
└── README.md
```

---

## 3. Directory Responsibilities

### [`docs/`](docs/)
Stores all planning, architecture, execution, and integration documentation.

Examples:
- [`docs/final_execution_plan.md`](docs/final_execution_plan.md)
- [`docs/frontend_integration_plan.md`](docs/frontend_integration_plan.md)
- [`docs/project_structure.md`](docs/project_structure.md)
- [`docs/proposal_to_implementation_mapping.md`](docs/proposal_to_implementation_mapping.md)

### [`proposal/`](proposal/)
Stores the original proposal files and proposal-derived writing materials.

Examples:
- [`proposal/Proposal_form.docx`](proposal/Proposal_form.docx)
- [`proposal/Proposal_form.md`](proposal/Proposal_form.md)

### [`data/raw/`](data/raw/)
Stores raw source datasets.

Expected example:
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

### [`data/processed/`](data/processed/)
Stores cleaned or transformed datasets.

Expected example:
- [`data/processed/cleaned_churn.csv`](data/processed/cleaned_churn.csv)

### [`outputs/figures/`](outputs/figures/)
Stores figure outputs for the paper and future dashboard usage.

### [`outputs/tables/`](outputs/tables/)
Stores tabular outputs such as model comparison, priority ranking tables, and preprocessing audit artifacts.

Expected examples:
- [`outputs/tables/dataset_overview.csv`](outputs/tables/dataset_overview.csv)
- [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv)
- [`outputs/tables/model_performance_comparison.csv`](outputs/tables/model_performance_comparison.csv)

### [`outputs/models/`](outputs/models/)
Stores serialized trained models.

### [`src/`](src/)
Stores core analytics implementation.

Current and planned examples:
- [`src/preprocess.py`](src/preprocess.py)
- [`src/eda.py`](src/eda.py)
- [`src/train.py`](src/train.py)
- [`src/evaluate.py`](src/evaluate.py)
- [`src/explain.py`](src/explain.py)
- [`src/prioritize.py`](src/prioritize.py)
- [`src/run_pipeline.py`](src/run_pipeline.py)

### [`frontend/`](frontend/)
Stores the implemented Next.js presentation layer. It consumes stable analytics outputs from [`outputs/`](outputs/) through a dedicated frontend data-access layer and remains separate from the Python analytics codebase.

Current examples include:
- reusable display components such as [`FigureCard`](frontend/src/components/FigureCard.tsx:10), [`MetricCard`](frontend/src/components/MetricCard.tsx:7), and [`DataTable`](frontend/src/components/DataTable.tsx:15)
- shared layout and styling under [`frontend/src/app/layout.tsx`](frontend/src/app/layout.tsx:29) and [`frontend/src/app/globals.css`](frontend/src/app/globals.css)
- route-based pages under [`frontend/src/app/`](frontend/src/app/)

---

## 4. Structural Rules

1. Proposal documents must not remain in the root directory.
2. Planning documents must not be stored in [`plans/`](plans/); use [`docs/`](docs/) instead.
3. Analytics logic must not be mixed into frontend files.
4. Generated outputs must not be committed as core source code.
5. Future frontend code must consume outputs, not rewrite core analytics logic.

---

## 5. Current Transition Notes

The following items remain transitional and should be cleaned up in later steps:
- [`requirements.txt`](requirements.txt) is still present but should be superseded by [`environment.yml`](environment.yml)
- [`plans/final_execution_plan.md`](plans/final_execution_plan.md) remains only as a historical artifact

---

## 6. Final Principle

This project should remain organized around four separated concerns:
- documentation,
- proposal materials,
- analytics implementation,
- future presentation layer.