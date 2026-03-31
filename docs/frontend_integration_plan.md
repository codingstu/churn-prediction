# Frontend Integration Plan

## 1. Purpose

This document defines the presentation-layer integration baseline for the churn prediction project.

The repository now contains an implemented [`frontend/`](frontend/) Next.js application that consumes standardized analytics outputs, while keeping the Python pipeline and the presentation layer decoupled.

---

## 2. Current Position

The current project delivers:
- data cleaning outputs,
- model evaluation outputs,
- explainability outputs,
- retention prioritization outputs.

These outputs should be treated as the contract for future frontend consumption.

---

## 3. Frontend Goal

A future frontend should support the following functions:

1. View overall churn metrics
2. Compare model performance
3. Browse high-priority customers
4. Inspect customer-level explainability results
5. Display paper-ready charts in an interactive dashboard format

---

## 4. Recommended Frontend Options

### 4.1 React
Use React only if the future goal is a lightweight client-only dashboard.

Suitable when:
- the app is a simple front-end viewer,
- data is served from static files or a separate backend,
- the project remains mostly presentation-oriented.

### 4.2 Next.js
Use Next.js if the future goal is a more complete analytical product or demo system.

Suitable when:
- page routing is needed,
- server-side rendering may be useful,
- API routes may be added later,
- the project may evolve into a deployable analytics interface,
- authenticated pages, dashboard routing, and future backend integration are expected.

### 4.3 Final Recommendation
For this repository, **Next.js is the preferred and recommended frontend choice**.

Reason:
- easier to grow into a full product-like demo,
- better support for route-based dashboards,
- easier path toward integrated API endpoints,
- stronger fit for business-facing presentation,
- more suitable than plain React for the likely long-term direction of this repository.

Decision:
- **Next.js should be treated as the default future frontend stack**
- React remains only a fallback option for a smaller visualization-only layer

---

## 5. Required Backend-Friendly Output Contracts

To support future frontend integration, current analytics outputs should remain stable.

### 5.1 Table outputs
Tables in [`outputs/tables/`](outputs/tables/) should use stable file names and column names.

Examples:
- [`outputs/tables/model_performance_comparison.csv`](outputs/tables/model_performance_comparison.csv)
- [`outputs/tables/customer_priority_table.csv`](outputs/tables/customer_priority_table.csv)
- [`outputs/tables/top_20_retention_targets.csv`](outputs/tables/top_20_retention_targets.csv)

### 5.2 Figure outputs
Figures in [`outputs/figures/`](outputs/figures/) should use predictable names.

Examples:
- ROC curve comparison
- confusion matrices
- feature importance plot
- SHAP summary plot
- retention segmentation chart

### 5.3 Model outputs
Serialized models should remain under [`outputs/models/`](outputs/models/) and should not embed UI logic.

---

## 6. Frontend Directory Baseline

The implemented frontend is stored under [`frontend/`](frontend/).

Current structure baseline:

```text
frontend/
├── src/app/
├── src/components/
├── src/lib/
├── public/
├── package.json
└── next.config.ts
```

The analytics project remains separate from the frontend implementation, and the frontend consumes repository outputs instead of duplicating analytics logic.

---

## 7. Suggested Future Pages

1. **Dashboard page**  
   Overview metrics, churn rate, model summary
2. **Model comparison page**  
   ROC-AUC, Recall, Precision, F1-score, confusion matrix views
3. **Retention priority page**  
   Top-priority customers, filtering, ranking
4. **Customer explanation page**  
   Customer-level risk explanation, SHAP-based detail view
5. **Business insights page**  
   Narrative summary and management recommendations

---

## 8. Environment Rule for Frontend and Analytics Work

All Python analytics dependencies for this repository must be installed and executed inside the Conda environment defined by [`environment.yml`](environment.yml).

Rules:
- analytics commands must run under the `churn_prediction` Conda environment
- repository-related Python dependencies must not be installed into the system Python environment
- future frontend dependencies must stay isolated under a dedicated Node / Next.js toolchain and must not be mixed with Python package management

This separation is required to keep the repository reproducible and to avoid environment drift.

---

## 9. Current Implementation Status

A frontend is now implemented in the current repository.

The current state includes:
- analytics pipeline execution under Conda,
- reproducible outputs under [`outputs/`](outputs/),
- a Next.js presentation layer under [`frontend/`](frontend/),
- route-based pages for dashboard, model comparison, retention priority, explainability, and business insights,
- a frontend asset route that serves repository figures without moving analytics files into the frontend codebase,
- stable consumption of preprocessing audit output such as [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv) when needed for future UI extension,
- a refined card and table presentation baseline that reduces duplicated page markup and improves visual consistency,
- figure containers that preserve image aspect ratio to prevent dashboard chart distortion.

---

## 10. Final Decision

The project now proceeds as an analytics system with an implemented presentation layer.

The active frontend stack is **Next.js**, and it should remain the default presentation-layer technology for this repository. React remains only a fallback option for materially smaller future visualization work, not the primary baseline.

The current frontend enhancement direction should continue to follow three rules:
- prefer shared UI primitives over page-specific duplicated markup,
- keep figure rendering aspect-ratio-safe in reusable components such as [`FigureCard`](frontend/src/components/FigureCard.tsx:10),
- keep frontend styling changes decoupled from analytics logic and output contracts.