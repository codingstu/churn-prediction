# Dataset Selection and Validation

## 1. Purpose

This document records the validation status, authenticity signals, usability assessment, and selection decision for the datasets currently placed under [`data/raw/`](data/raw/).

It exists to keep dataset decisions aligned with the approved proposal in [`proposal/Proposal_form.md`](proposal/Proposal_form.md).

---

## 2. Datasets Currently Available

### 2.1 IBM Telco Customer Churn
Path:
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

Observed structure:
- 7043 rows
- 21 columns
- target column: `Churn`
- identifier column: `customerID`

Observed key columns include:
- `customerID`
- `tenure`
- `Contract`
- `PaymentMethod`
- `MonthlyCharges`
- `TotalCharges`
- `Churn`

Validation observations:
- column structure matches the well-known IBM Telco churn schema
- target values are consistent with binary churn labels: `Yes` / `No`
- `TotalCharges` contains 11 blank values, which is a known and expected cleaning issue for this dataset
- row count and schema are internally consistent with the standard public version
- the repository preprocessing baseline now treats schema validation, `customerID` uniqueness, and raw `Churn` label validation as mandatory acceptance checks before cleaning proceeds

Authenticity assessment:
- strong authenticity signal from schema consistency
- strong usability signal for binary churn modeling
- suitable for direct use in the current proposal without changing the research scope

Conclusion:
- **selected as the primary dataset**

---

## 2.2 Rivalytics / RavenStack Synthetic SaaS Dataset
Directory:
- [`data/raw/Telco Customer Churn/`](data/raw/Telco%20Customer%20Churn/)

Observed files:
- [`data/raw/Telco Customer Churn/ravenstack_accounts.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_accounts.csv)
- [`data/raw/Telco Customer Churn/ravenstack_subscriptions.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_subscriptions.csv)
- [`data/raw/Telco Customer Churn/ravenstack_feature_usage.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_feature_usage.csv)
- [`data/raw/Telco Customer Churn/ravenstack_support_tickets.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_support_tickets.csv)
- [`data/raw/Telco Customer Churn/ravenstack_churn_events.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_churn_events.csv)
- [`data/raw/Telco Customer Churn/README.md`](data/raw/Telco%20Customer%20Churn/README.md)

Observed structure from the included README:
- explicitly described as **synthetic**
- multi-table relational design
- event-driven SaaS scenario
- accounts, subscriptions, usage, support, and churn events linked by keys

Observed validation results:
- `accounts`: 500 rows
- `subscriptions`: 5000 rows
- `feature_usage`: 25000 rows
- `support_tickets`: 2000 rows
- `churn_events`: 600 rows
- no orphan foreign-key records were detected across the main joins
- `accounts.churn_flag` contains both `True` and `False`

Authenticity assessment:
- the dataset itself openly states that it is synthetic
- therefore it is **not authentic real-world observational business data** in the same sense as IBM Telco
- however, it is structurally coherent and technically usable for extension analysis, pipeline stress testing, and future SaaS product demo scenarios

Usability assessment:
- useful for future multi-table churn engineering
- useful for frontend demo scenarios because it contains richer account-level and event-level context
- not ideal as the main thesis dataset if the proposal is currently centered on the IBM Telco churn framing
- would require a separate entity-resolution and label-construction pipeline before becoming the main dataset

Conclusion:
- **accepted as an extension dataset, not the primary thesis dataset**

---

## 3. Selection Decision

### Primary dataset
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

Reason:
- closest fit to the approved proposal in [`proposal/Proposal_form.md`](proposal/Proposal_form.md)
- already matches the current cleaning, modeling, explainability, and prioritization assumptions
- has an explicit churn label and direct business features needed for the current pipeline

### Extension dataset
- [`data/raw/Telco Customer Churn/`](data/raw/Telco%20Customer%20Churn/)

Reason:
- useful for a later research extension toward multi-table SaaS churn analytics
- useful for future React / Next.js presentation-layer demos
- should not replace the IBM dataset in the current mainline without rewriting the proposal scope and methods

---

## 4. Proposal Alignment Decision

The approved proposal in [`proposal/Proposal_form.md`](proposal/Proposal_form.md) emphasizes:
- subscription-based customer churn prediction
- explainability
- practical retention prioritization
- a closed-end, manager-oriented business solution

The IBM Telco dataset supports this directly because it provides:
- a ready classification target,
- customer-level explanatory variables,
- revenue proxy variables such as `MonthlyCharges` and `TotalCharges`,
- a clean path to the current priority score definition.

The RavenStack dataset is valuable, but it changes the complexity of the project from:
- **single-table interpretable churn modeling**

to:
- **multi-table synthetic SaaS event modeling**

That change is meaningful enough to risk scope drift.

Decision:
- keep IBM Telco as the mainline dataset
- treat RavenStack as a controlled extension path under the current repository strategy

---

## 5. Immediate Implementation Impact

### 5.1 Mainline implementation should target
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

### 5.2 Current scripts that need path alignment
- [`src/preprocess.py`](src/preprocess.py)
- [`src/run_pipeline.py`](src/run_pipeline.py)
- [`README.md`](README.md)
- [`docs/final_execution_plan.md`](docs/final_execution_plan.md)

### 5.3 Future extension path
If later expanding into SaaS multi-table modeling, add dedicated modules such as:
- [`src/saas_preprocess.py`](src/saas_preprocess.py)
- [`src/saas_feature_builder.py`](src/saas_feature_builder.py)
- [`src/saas_pipeline.py`](src/saas_pipeline.py)

This should be handled as a separate branch of work, not merged into the current thesis mainline prematurely.

---

## 6. Cleaning Acceptance Baseline

The current repository should treat the IBM Telco cleaning stage as accepted only when all of the following are true:

- the raw file at [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv) matches the expected 21-column schema
- [`customerID`](src/preprocess.py:38) is non-null and unique
- raw [`Churn`](src/preprocess.py:37) values are limited to `Yes` and `No`
- `TotalCharges` blank strings are converted to missing values and then coerced to numeric in [`clean_telco_data()`](src/preprocess.py:116)
- the cleaned output in [`data/processed/cleaned_churn.csv`](data/processed/cleaned_churn.csv) contains 7032 rows for the current raw dataset version
- the audit table in [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv) records raw rows, retained rows, dropped rows, blank `TotalCharges`, invalid target values, and duplicate identifiers

These checks are intended to catch silent schema drift and make preprocessing behavior auditable without changing the project modeling scope.

---

## 7. Final Decision Summary

- IBM Telco dataset: **validated, usable, primary**
- RavenStack synthetic SaaS dataset: **validated structurally, usable, extension only**
- Current repository should continue implementation on the IBM path first
- This decision keeps the project aligned with [`proposal/Proposal_form.md`](proposal/Proposal_form.md) and reduces scope drift risk
