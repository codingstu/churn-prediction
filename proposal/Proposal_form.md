# Explainable Churn Prediction and Retention Prioritization for Subscription-Based Service Providers

## 1. Basic Information

- **Course / Lab**: ABW508 / ABW508D Analytics Lab
- **Document Type**: Expanded proposal in Markdown format

---

## 2. Project Title

**Explainable Churn Prediction and Retention Prioritization for Subscription-Based Service Providers**

---

## 3. Project Background

Customer churn is a major business concern for subscription-based service providers because revenue depends heavily on retaining existing customers over time. When customers leave, firms do not only lose recurring income, but they may also need to spend more on marketing and sales to acquire replacements. In many real-world business settings, retention actions are often taken too late, when customers are already close to leaving. As a result, intervention becomes less effective and more costly.

This project is developed from a business and company perspective. Its purpose is to support managers in identifying high-risk customers earlier and making more focused retention decisions. Instead of treating all customers equally, the project aims to provide a practical analytical approach that helps firms understand which customers are more likely to churn, what factors are associated with churn, and how retention efforts can be prioritized more effectively.

---

## 4. Problem Statement

Customer churn is an important issue for subscription-based service providers because losing existing customers affects recurring revenue and increases the cost of acquiring new customers. In many cases, firms only react after customers are already likely to leave, which makes retention efforts less effective.

Therefore, this project focuses on developing a machine learning model to identify customers with a high risk of churn in advance. In addition to predicting churn, the analysis will examine the main factors related to churn and provide simple retention prioritization support so that managers can focus their efforts on the customer groups that matter most.

This is a closed-end business problem because the project is designed to deliver a practical decision-support solution for a specific business need: identifying likely churners and supporting targeted retention action.

---

## 5. Business Relevance and Solution Buyer

The proposed solution is mainly intended for:

- managers responsible for customer retention,
- CRM managers,
- marketing decision-makers in subscription-based service providers,
- customer success teams, and
- business managers who need data-driven support for retention planning.

From a business perspective, the value of the solution lies in three main areas:

1. **Early identification of churn risk** so that companies can intervene before customers leave.
2. **Better understanding of churn drivers** so that managers can design more relevant actions.
3. **Retention prioritization** so limited time and budget can be directed toward higher-risk or higher-value customer groups.

---

## 6. Proposal Compliance Summary

Based on the original proposal form, the project satisfies the following requirements:

- [x] The project addresses a business problem from a business / firm / company perspective.
- [x] The project identifies a clear solution buyer or target business entity.
- [x] The problem to be solved is a closed-end problem with a clear practical solution.
- [x] The project uses at least one analytical tool listed in the guidelines.

---

## 7. Project Aim

The overall aim of this project is to build an explainable churn prediction framework for subscription-based service providers and to translate prediction results into practical retention prioritization insights for business decision-makers.

---

## 8. Project Objectives

The project will pursue the following objectives:

1. **To understand the churn problem in a subscription-based service context** using customer-level business data.
2. **To perform exploratory data analysis (EDA)** in order to identify customer profiles, service characteristics, and churn patterns.
3. **To prepare the dataset for modelling** by cleaning the data, handling missing values, encoding categorical variables, and selecting relevant features.
4. **To develop and compare multiple classification models** for customer churn prediction.
5. **To evaluate model performance** using appropriate classification metrics such as accuracy, precision, recall, F1-score, and ROC-AUC.
6. **To identify and interpret key variables associated with churn** so that the model findings remain understandable from a business perspective.
7. **To provide simple retention prioritization support** that helps managers focus on higher-risk customer groups.

---

## 9. Proposed Methodology

The project methodology will consist of several stages.

### 9.1 Business Understanding

The study will begin by clarifying the business problem of customer churn in subscription-based services. The focus will be on understanding why churn matters for revenue stability, customer lifetime value, and retention planning.

### 9.2 Data Understanding

The selected churn dataset will be reviewed to understand its structure, variable types, and business meaning. This stage will identify the available customer-level information and assess how the variables may relate to churn behaviour.

### 9.3 Exploratory Data Analysis

Exploratory data analysis will be conducted to examine:

- customer demographic patterns,
- service subscription characteristics,
- account and billing behaviour,
- tenure distribution, and
- churn distribution across different customer groups.

This stage is important for detecting trends, anomalies, imbalance issues, and early indications of factors that may influence churn.

### 9.4 Data Preparation

The dataset will then be cleaned and prepared for modelling. This stage may include:

- handling missing values,
- checking data consistency,
- encoding categorical variables,
- transforming variables where necessary, and
- selecting relevant features for predictive modelling.

The purpose of this step is to ensure that the dataset is suitable for machine learning analysis and that the modelling results are reliable.

### 9.5 Predictive Modelling

Several classification models will be tested and compared, including:

- **Logistic Regression**
- **Decision Tree**
- **Random Forest**
- **a boosting-based model**, where appropriate

These models are selected because they provide a useful balance between predictive capability and interpretability for churn analysis.

### 9.6 Model Evaluation

Model performance will be evaluated using common classification measures, including:

- **Accuracy**
- **Precision**
- **Recall**
- **F1-score**
- **ROC-AUC**

The comparison of these metrics will help identify which model is most suitable for the business objective of detecting likely churners while maintaining practical decision usefulness.

### 9.7 Interpretation and Retention Prioritization

Beyond prediction accuracy, the study will examine important variables associated with churn so that the results can be interpreted from a business perspective. Based on these findings, the project will suggest a practical way to prioritize retention efforts for higher-risk customer groups.

The prioritization logic is intended to support managerial action rather than serve as a purely technical output. This means the final analysis should help decision-makers understand not only **who is at risk**, but also **why they may be at risk** and **which customer groups should receive attention first**.

---

## 10. Proposed Analytical Tools

The project will use the following tools:

- **Python** for data cleaning, exploratory analysis, feature preparation, model building, and performance evaluation.
- **Tableau** for presenting important patterns and findings in a clearer and more business-friendly visual form.

Python is suitable for implementing predictive analytics workflows, while Tableau can help communicate insights effectively to non-technical stakeholders.

---

## 11. Dataset and Data Source

This study will use the **IBM Telco Customer Churn dataset**, which is a publicly available secondary dataset commonly used in churn-related studies.

### 11.1 Dataset Characteristics

The dataset includes customer-level information from a subscription-based service setting, such as:

- demographic details,
- service subscriptions,
- account information,
- billing records,
- customer tenure, and
- churn status.

### 11.2 Reason for Dataset Selection

This dataset is appropriate for the project because it supports both predictive modelling and business interpretation. Specifically, it can be used to:

- build and compare churn prediction models,
- examine the factors related to customer churn, and
- explore how customers may be prioritized for retention efforts.

### 11.3 Research Suitability

As the dataset is publicly available and does not contain personally identifiable information, it is appropriate for academic research use.

---

## 12. Expected Practical Output

Based on the proposal, the expected output of the project includes:

1. A cleaned and analysed churn dataset.
2. Comparative results from several churn prediction models.
3. Identification of key churn-related variables.
4. Business-oriented interpretation of churn drivers.
5. A simple retention prioritization approach for higher-risk customer groups.
6. Visual presentation of important findings using dashboards or charts.

---

## 13. Project Scope

The scope of the project is limited to a business-oriented churn prediction and interpretation exercise using a secondary dataset from a subscription-based service context. The project is not intended to solve a macroeconomic, governmental, or NGO-related problem. It is designed as a practical business analytics solution for firm-level decision support.

In addition, the project focuses on model comparison, interpretation, and prioritization support rather than on building a production-ready deployment system.

---

## 14. Significance of the Study

This project is significant because it connects machine learning prediction with practical business decision-making. In many churn studies, predictive accuracy is emphasized, but managerial actionability is less clearly addressed. By combining churn prediction with explainable insights and retention prioritization, the project aims to produce findings that are more useful for business managers.

For subscription-based service providers, such an approach may improve the efficiency of retention efforts and support more informed allocation of customer management resources.

---

## 15. Supervisor Acknowledgement

- **Supervisor's Name**: To be filled
- **Date**: To be filled

---

## 16. Original Proposal Traceability Note

This Markdown document is an expanded and structured version of the content extracted from [`Proposal_form.docx`](proposal/Proposal_form.docx). It preserves the original proposal meaning while presenting the content in a clearer format for further writing and revision.