# Explainable Churn Prediction and Retention Prioritization 项目最终执行方案

## 1. 文档定位

本文档是当前项目的**唯一主方案基线**，后续所有方案更新、结构调整、实施约束与扩展规划，统一维护在 [`docs/`](docs/) 下。

本文档替代以往位于 [`plans/final_execution_plan.md`](plans/final_execution_plan.md) 的主方案角色，但保留原文件作为历史参考，后续以 [`docs/final_execution_plan.md`](docs/final_execution_plan.md) 为准。

---

## 2. 项目最终定位

**论文题目**  
Explainable Churn Prediction and Retention Prioritization for Subscription-Based Service Providers

**项目核心目标**  
构建一个兼具预测能力、可解释性与业务行动优先级支持能力的客户流失分析系统，用于帮助订阅制服务企业：

1. 识别高流失风险客户
2. 解释主要流失驱动因素
3. 形成可执行的客户保留优先级排序
4. 产出可直接写入论文与后续展示层的标准化结果文件

**最终交付方向**
- 流失预测模型比较与最优模型
- 全局与局部可解释性分析
- 客户保留优先级评分与分层
- 论文方法、结果、图表与表格
- 可复现的纯脚本分析 pipeline
- 为未来 React / Next.js 展示层预留稳定输出接口

---

## 3. 当前治理原则

### 3.1 文档治理
- 所有方案文档统一存放在 [`docs/`](docs/)
- proposal 原件与整理稿统一存放在 [`proposal/`](proposal/)
- [`README.md`](README.md) 只保留项目说明与运行方式，不再承担详细方案角色

### 3.2 实现治理
- 主流程采用**纯脚本 pipeline**，不再以 notebook 为主
- 结果必须标准化输出到 [`outputs/`](outputs/)
- 分析逻辑与未来展示层解耦
- 所有路径尽量固定，便于复现与前端接入

### 3.3 环境治理
- 不使用 `venv`
- 项目统一改为 **Conda** 管理环境
- 后续应以 [`environment.yml`](environment.yml) 作为环境基线文件

---

## 4. 为什么采用纯脚本 pipeline，而不是 notebook

基于 proposal 当前阶段与项目目标，notebook 不再是必要核心载体。

### 4.1 主要原因
1. 论文项目更强调复现性与流程确定性
2. notebook 容易出现执行顺序依赖与隐藏状态问题
3. 当前项目需要稳定输出图表、模型、表格与优先级名单
4. 后续还要预留前端接入，因此输出结构必须稳定
5. 答辩时用脚本化流程更容易说明工程实现逻辑

### 4.2 最终结论
项目正式基线为：
- **纯脚本分析流程**
- **标准化输出目录**
- **文档驱动的研究约束**

notebook 可以完全移除，不再作为默认方案的一部分。

---

## 5. 研究问题

建议固定为以下三个研究问题：

1. **Which customer characteristics and service-related factors are the strongest predictors of churn in subscription-based services?**
2. **Which machine learning model among Logistic Regression, Random Forest, and XGBoost provides the best churn prediction performance?**
3. **How can predicted churn probability and customer value proxy be combined to prioritize customer retention efforts?**

### 5.1 研究问题与模块映射
- RQ1 -> [`src/eda.py`](src/eda.py) + [`src/explain.py`](src/explain.py)
- RQ2 -> [`src/train.py`](src/train.py) + [`src/evaluate.py`](src/evaluate.py)
- RQ3 -> [`src/prioritize.py`](src/prioritize.py)

---

## 6. 数据方案

### 6.1 主数据集
**IBM Telco Customer Churn dataset**

主数据文件路径：
- [`data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv`](data/raw/Telco%20Customer%20Churn%20%28IBM%29/WA_Fn-UseC_-Telco-Customer-Churn.csv)

### 6.2 验证结果与选择理由
根据 [`docs/dataset_selection_and_validation.md`](docs/dataset_selection_and_validation.md) 的验证结果，IBM 数据集当前具备以下特征：
- 7043 条记录，21 个字段
- 有明确目标标签 `Churn`
- 字段结构与公开常见版本一致
- `TotalCharges` 存在 11 个空字符串，属于已知且可处理的数据质量问题
- 适合直接承接当前 proposal 中的 cleaning、EDA、建模、解释与 retention prioritization 主线

因此，当前项目正式选定 IBM 数据集作为**主数据集**。

### 6.3 扩展数据集
当前仓库还包含一个扩展型 SaaS 多表数据集：
- [`data/raw/Telco Customer Churn/`](data/raw/Telco%20Customer%20Churn/)

其内部文件包括：
- [`data/raw/Telco Customer Churn/ravenstack_accounts.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_accounts.csv)
- [`data/raw/Telco Customer Churn/ravenstack_subscriptions.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_subscriptions.csv)
- [`data/raw/Telco Customer Churn/ravenstack_feature_usage.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_feature_usage.csv)
- [`data/raw/Telco Customer Churn/ravenstack_support_tickets.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_support_tickets.csv)
- [`data/raw/Telco Customer Churn/ravenstack_churn_events.csv`](data/raw/Telco%20Customer%20Churn/ravenstack_churn_events.csv)

根据随附 [`README.md`](data/raw/Telco%20Customer%20Churn/README.md) 的说明，该数据集为**synthetic multi-table SaaS dataset**。当前已验证其主外键关系完整、结构可用，但由于它是合成数据且为多表事件模型，因此暂不作为当前论文主线数据集，仅作为后续扩展方向保留。

### 6.4 主数据集核心变量
- `customerID`
- `gender`
- `SeniorCitizen`
- `Partner`
- `Dependents`
- `tenure`
- `PhoneService`
- `InternetService`
- `Contract`
- `PaymentMethod`
- `MonthlyCharges`
- `TotalCharges`
- `Churn`

### 6.5 主数据集目标变量
- 二分类标签：`Churn`
- 建议编码：Yes = 1, No = 0

### 6.6 主数据集业务价值代理变量
由于当前主数据集不包含真实 CLV、利润或干预成本，采用：
- 主价值代理：`MonthlyCharges`
- 辅助参考：`TotalCharges`、`tenure`

这一定义适合论文写作，因为它明确承认使用的是可观察收入代理，而非真实价值函数。

### 6.7 选型结论
- **主线论文与当前脚本 pipeline**：使用 IBM Telco 数据集
- **后续扩展分析、前端展示增强、多表 SaaS 场景**：保留 RavenStack synthetic SaaS 数据集

该决策保持了与 [`proposal/Proposal_form.md`](proposal/Proposal_form.md) 的一致性，同时避免项目因多表合成数据而跑偏。

---

## 7. 方法总框架

```text
Raw Data
  -> Cleaning
  -> EDA
  -> Feature Preparation
  -> Model Training
  -> Model Evaluation
  -> Explainability
  -> Retention Prioritization
  -> Paper-ready Outputs
  -> Future Frontend Consumption
```

项目不是单纯做分类模型，而是形成三层闭环：

1. **Prediction layer**：识别谁会流失
2. **Explanation layer**：解释为什么会流失
3. **Action layer**：指导企业优先挽留谁

---

## 8. 数据预处理方案

### 8.1 必做步骤
1. 检查 `TotalCharges` 的空字符串
2. 将 `TotalCharges` 转换为数值型
3. 处理由空字符串导致的缺失
4. 将 `Churn` 编码为 0/1
5. 建模时移除 `customerID`
6. 对类别特征进行 one-hot encoding
7. 保持训练集与测试集预处理一致
8. 对 Logistic Regression 使用标准化

### 8.2 推荐补充步骤
9. 记录清洗前后样本数变化
10. 检查类别不平衡
11. 使用 stratified split
12. 导出 [`data/processed/cleaned_churn.csv`](data/processed/cleaned_churn.csv)
13. 对原始 schema、主键唯一性与目标值域执行显式校验
14. 导出可审计的清洗摘要到 [`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv)

### 8.3 对应实现
- 清洗主入口：[`clean_telco_data()`](src/preprocess.py:116)
- schema 校验：[`validate_raw_schema()`](src/preprocess.py:59)
- 主键校验：[`validate_customer_ids()`](src/preprocess.py:74)
- 目标值域校验：[`validate_target_values()`](src/preprocess.py:90)
- 建模数据准备：[`prepare_model_frame()`](src/preprocess.py:157)
- 保存清洗结果：[`save_processed_data()`](src/preprocess.py:165)
- 保存清洗审计：[`save_cleaning_audit()`](src/preprocess.py:172)

---

## 9. EDA 方案

当前项目需要新增 [`src/eda.py`](src/eda.py) 来替代原 notebook 探索流程。

### 9.1 EDA 目标
- 理解 churn rate
- 理解不同客户群体的 churn 差异
- 为模型解释建立业务叙事基础
- 生成可直接写入论文的图表

### 9.2 必做图表
1. churn class distribution
2. tenure vs churn
3. contract type vs churn
4. monthly charges vs churn
5. total charges vs churn
6. payment method vs churn
7. internet service vs churn
8. correlation heatmap

### 9.3 输出位置
- 图表输出到 [`outputs/figures/`](outputs/figures/)
- 描述性统计表输出到 [`outputs/tables/`](outputs/tables/)

---

## 10. 建模方案

### 10.1 仅保留三类模型
1. Logistic Regression
2. Random Forest
3. XGBoost

### 10.2 保留原因
- Logistic Regression：baseline 与线性解释
- Random Forest：稳定、鲁棒、树模型重要性清晰
- XGBoost：通常性能最佳，适合作为主模型候选

### 10.3 当前已存在实现基础
- 特征预处理构建：[`build_preprocessor()`](src/train.py:26)
- 模型管道构建：[`build_model_pipelines()`](src/train.py:49)
- 模型训练入口：[`train_models()`](src/train.py:84)
- 模型序列化：[`save_model()`](src/train.py:93)
- 特征与目标拆分：[`split_features_target()`](src/train.py:102)

### 10.4 建模原则
- 固定随机种子
- 仅在训练集上调参
- 使用统一指标
- 保持模型可比较性

---

## 11. 评估方案

### 11.1 核心指标
- ROC-AUC
- F1-score
- Recall
- Precision
- Confusion Matrix

### 11.2 主指标建议
- **Recall + ROC-AUC**

### 11.3 原因
对于 churn 任务，漏掉真正会流失的客户往往代价更高，因此召回率非常重要；同时排序能力也重要，因此保留 ROC-AUC 作为主指标之一。

### 11.4 当前已存在实现基础
- 概率提取：[`predict_scores()`](src/evaluate.py:17)
- 指标计算：[`evaluate_binary_classifier()`](src/evaluate.py:24)
- 指标表构建：[`build_performance_table()`](src/evaluate.py:39)
- 指标表保存：[`save_performance_table()`](src/evaluate.py:45)
- 混淆矩阵图：[`plot_confusion_matrix()`](src/evaluate.py:53)
- ROC 曲线图：[`plot_roc_curves()`](src/evaluate.py:72)

---

## 12. 可解释性方案

当前项目需要新增 [`src/explain.py`](src/explain.py) 作为 explainability 模块。

### 12.1 全局解释
用于回答哪些因素总体最重要：
- Logistic Regression coefficients
- Random Forest feature importance
- XGBoost feature importance
- SHAP summary plot

### 12.2 局部解释
用于回答单个客户为什么会被判定为高风险：
- SHAP waterfall plot
- SHAP force plot
- 1 到 3 个客户案例解释

### 12.3 论文定位
你的论文不应只写“模型可解释”，而应清晰区分：
- global interpretability for strategic understanding
- local interpretability for customer-level action

---

## 13. Retention Prioritization 方案

这是本项目 business layer 的核心模块。

### 13.1 主评分公式
`PriorityScore = ChurnProbability × MonthlyCharges`

### 13.2 含义
- `ChurnProbability` 表示流失风险
- `MonthlyCharges` 表示价值代理
- 二者相乘表示高风险且高价值客户应被优先挽留

### 13.3 分层规则
建议按风险与价值二维划分：
- High Risk + High Value -> Top Priority
- High Risk + Low Value -> Secondary Priority
- Low Risk + High Value -> Monitor
- Low Risk + Low Value -> Low Priority

### 13.4 当前已存在实现基础
- 评分计算：[`compute_priority_score()`](src/prioritize.py:11)
- 分层逻辑：[`assign_priority_segments()`](src/prioritize.py:23)
- 排序输出表：[`build_priority_table()`](src/prioritize.py:50)
- 持久化输出：[`save_priority_outputs()`](src/prioritize.py:78)

### 13.5 目标输出文件
- [`outputs/tables/customer_priority_table.csv`](outputs/tables/customer_priority_table.csv)
- [`outputs/tables/top_20_retention_targets.csv`](outputs/tables/top_20_retention_targets.csv)

---

## 14. 论文映射

### Chapter 1 Introduction
- churn 背景
- 订阅制业务中的保留问题
- explainability 与 prioritization 的必要性
- 研究问题与目标

### Chapter 2 Literature Review
- customer churn prediction
- machine learning in CRM analytics
- explainable AI in business analytics
- value-based retention prioritization

### Chapter 3 Methodology
- 数据集
- 清洗逻辑
- EDA 设计
- 模型定义
- 指标设计
- explainability 设计
- prioritization 设计

### Chapter 4 Results and Findings
- EDA 发现
- 模型比较结果
- 最优模型说明
- 特征解释
- 客户案例解释
- 保留优先级结果

### Chapter 5 Discussion and Conclusion
- 业务含义
- 管理建议
- 局限性
- 后续扩展方向

---

## 15. 面向前端接入与已实现展示层的架构要求

当前仓库已实现 [`frontend/`](frontend/) 展示层，但仍必须在方案层面持续约束结构，以避免后续返工。

### 15.1 架构分层
1. **Data layer**：[`data/`](data/)
2. **Analytics layer**：[`src/`](src/)
3. **Output layer**：[`outputs/`](outputs/)
4. **Documentation layer**：[`docs/`](docs/)
5. **Presentation layer**：已实现的 [`frontend/`](frontend/) Next.js 展示层

### 15.2 前端接入目标
当前已由 [`frontend/`](frontend/) 提供以下页面能力，并继续作为后续增强基线：
- churn dashboard
- model comparison view
- top retention targets table
- customer detail explainability page
- business summary page

### 15.3 技术建议
如果未来只是轻量单页展示，可用 React；如果未来要形成完整产品化展示层，**本仓库正式优先建议 Next.js**。

原因：
- 更适合路由化 dashboard 与多页面结果展示
- 更适合后续加入 API route 或服务端数据聚合
- 更适合把 retention table、model comparison、customer explanation 做成统一产品化界面
- 相比纯 React，更符合当前仓库的长期扩展方向

### 15.4 当前阶段必须遵守的前端友好原则
- 输出表格格式固定
- 输出字段命名稳定
- 图表与表格路径可预测
- 分析脚本不与展示逻辑耦合
- 后续如需 API，可在当前输出层之上增加服务层，而不是改写分析核心
- 未来前端默认以 [`Next.js`](docs/frontend_integration_plan.md) 为首选展示层技术

### 15.5 环境强制规则
- 本仓库的 Python 分析依赖必须安装在 [`churn_prediction`](environment.yml) 对应的 Conda 环境中
- 不允许继续在系统 Python 或非仓库专用环境中安装本仓库依赖
- 前端依赖未来应独立在 [`frontend/`](frontend/) 中通过 Node / Next.js 工具链管理，不与 Python 环境混用

---

## 16. 目录结构基线

```text
churn_prediction/
├── docs/
│   ├── final_execution_plan.md
│   ├── frontend_integration_plan.md
│   ├── project_structure.md
│   └── proposal_to_implementation_mapping.md
├── proposal/
│   ├── Proposal_form.docx
│   └── Proposal_form.md
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── models/
├── src/
│   ├── preprocess.py
│   ├── eda.py
│   ├── train.py
│   ├── evaluate.py
│   ├── explain.py
│   ├── prioritize.py
│   └── run_pipeline.py
├── docs/
├── proposal/
├── environment.yml
├── .gitignore
└── README.md
```

说明：
- [`src/eda.py`](src/eda.py)、[`src/explain.py`](src/explain.py)、[`src/run_pipeline.py`](src/run_pipeline.py) 已完成并可重复执行
- [`frontend/`](frontend/) 已完成第一版 Next.js 展示层实现，并成功接入 [`outputs/`](outputs/) 产物
- [`environment.yml`](environment.yml) 已成为正式环境基线，[`requirements.txt`](requirements.txt) 当前仅保留为过渡文件
- 项目专用 Conda 环境 `churn_prediction` 已创建并验证可见
- 当前系统 Python 中与本仓库直接相关的非 Conda 分析依赖已完成清理
- 预处理阶段现已输出[`outputs/tables/data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv)，用于记录输入行数、删除行数、`TotalCharges` 空白数量、异常标签数量与重复主键数量
- 首页与核心展示卡片已完成一轮展示层优化，图表容器改为保持原始宽高比，避免[`FigureCard`](frontend/src/components/FigureCard.tsx:10)中的图片在响应式布局下变形

---

## 17. 本轮推进后的 proposal 对照结论

对照 [`proposal/Proposal_form.md`](proposal/Proposal_form.md:71) 中的项目目标与 [`proposal/Proposal_form.md`](proposal/Proposal_form.md:83) 中的方法设计，当前实现状态如下：

1. **To perform exploratory data analysis (EDA)**
   已由 [`src/eda.py`](src/eda.py) 承接，覆盖 churn distribution、tenure、contract、payment method、charges 与 heatmap 等核心图表。
2. **To prepare the dataset for modelling**
   已由 [`clean_telco_data()`](src/preprocess.py:33)、[`prepare_model_frame()`](src/preprocess.py:56)、[`save_processed_data()`](src/preprocess.py:64) 承接。
3. **To develop and compare multiple classification models**
   已由 [`build_model_pipelines()`](src/train.py:49)、[`train_models()`](src/train.py:84)、[`build_performance_table()`](src/evaluate.py:39) 承接。
4. **To identify and interpret key variables associated with churn**
   已由 [`src/explain.py`](src/explain.py) 第一版承接，覆盖 Logistic coefficients、tree feature importance 与 SHAP summary / local waterfall。
5. **To provide simple retention prioritization support**
   已由 [`compute_priority_score()`](src/prioritize.py:11)、[`assign_priority_segments()`](src/prioritize.py:23)、[`build_priority_table()`](src/prioritize.py:50) 承接。

### 当前已闭环的部分
- 已基于真实 IBM 数据运行 [`src/run_pipeline.py`](src/run_pipeline.py)，完成 cleaning、EDA、建模、评估、解释性输出与 priority table 导出
- notebook 历史骨架已清理，不再作为正式流程的一部分
- [`xgboost`](environment.yml) 已参与当前模型对比
- [`shap`](environment.yml) 已参与 explainability 输出生成
- [`frontend/`](frontend/) 已完成完整 Next.js 展示层，并已验证页面与图像接口可访问

### 本轮真实运行结果摘要
- 清洗结果：7032 条有效记录，删除 11 条 `TotalCharges` 空值记录
- 已生成数据概览表 [`dataset_overview.csv`](outputs/tables/dataset_overview.csv) 与数值统计表 [`numeric_summary.csv`](outputs/tables/numeric_summary.csv)
- 已新增清洗审计表 [`data_cleaning_audit.csv`](outputs/tables/data_cleaning_audit.csv)，用于解释 7043 条原始记录为何保留 7032 条有效记录
- 已生成 EDA 图表到 [`outputs/figures/`](outputs/figures/)
- 模型比较结果已写入 [`model_performance_comparison.csv`](outputs/tables/model_performance_comparison.csv)，当前包含 Logistic Regression、Random Forest 与 XGBoost
- 本轮最优模型为 [`logistic_regression`](src/train.py:60)，已保存到 [`outputs/models/best_model.joblib`](outputs/models/best_model.joblib)
- 已导出 explainability 结果到 [`outputs/tables/logistic_coefficients.csv`](outputs/tables/logistic_coefficients.csv)、[`logistic_regression_shap_summary.png`](outputs/figures/logistic_regression_shap_summary.png) 与 [`logistic_regression_shap_local_waterfall.png`](outputs/figures/logistic_regression_shap_local_waterfall.png)
- 已导出 retention prioritization 结果到 [`outputs/tables/customer_priority_table.csv`](outputs/tables/customer_priority_table.csv) 与 [`outputs/tables/top_20_retention_targets.csv`](outputs/tables/top_20_retention_targets.csv)
- 前端展示层已完成卡片与表格基元收敛，并通过[`frontend/src/app/globals.css`](frontend/src/app/globals.css)中的图表容器样式修复图片拉伸问题

结论：当前推进方向与 proposal 一致，尚未出现题目跑偏；当前主线已经形成**分析 pipeline + 标准化输出 + Next.js 展示层**的可运行闭环。

---

## 18. 下一阶段实施顺序

1. 将最新前端实现状态回写到 [`docs/`](docs/) 与 [`README.md`](README.md)
2. 将关键结果表与图进一步映射到论文结果章节
3. 视需要为 [`frontend/`](frontend/) 增加更细的说明性文案、筛选器与业务标注
4. 视需要补充面向论文写作的结果解读文本
5. 视需要启动 RavenStack 扩展分支，但不替代当前 IBM 主线
6. 视部署需求再增加服务化接口或身份验证能力，但不改写分析核心

---

## 19. 当前结论

本项目当前正式基线已经明确为：
- **Conda 环境管理**
- **纯脚本 pipeline**
- **proposal 独立归档到 [`proposal/`](proposal/)**
- **方案统一维护到 [`docs/`](docs/)**
- **已落地的 Next.js 展示层与标准化输出契约**

后续所有方案更新，以 [`docs/final_execution_plan.md`](docs/final_execution_plan.md) 为唯一准据。