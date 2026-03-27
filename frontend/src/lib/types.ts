export type MetricRecord = {
  metric: string;
  value: string;
};

export type ModelPerformanceRow = {
  model: string;
  roc_auc: string;
  f1_score: string;
  recall: string;
  precision: string;
};

export type PriorityRow = {
  customerID: string;
  churn_probability: string;
  MonthlyCharges: string;
  priority_score: string;
  risk_segment: string;
  value_segment: string;
  priority_level: string;
};

export type LogisticCoefficientRow = {
  feature: string;
  coefficient: string;
  abs_coefficient: string;
};

export type OverviewMetrics = {
  rowCount: number;
  columnCount: number;
  churnRate: number;
};

export type ModelSummary = {
  bestModel: ModelPerformanceRow | null;
  rows: ModelPerformanceRow[];
};

export type PrioritySummary = {
  rows: PriorityRow[];
  highPriorityCount: number;
  averagePriorityScore: number;
};

export type ExplainabilitySummary = {
  topDrivers: LogisticCoefficientRow[];
  strongestPositive: LogisticCoefficientRow[];
  strongestNegative: LogisticCoefficientRow[];
};
