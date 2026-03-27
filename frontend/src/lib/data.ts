import { promises as fs } from "node:fs";
import path from "node:path";
import Papa from "papaparse";

import type {
  ExplainabilitySummary,
  LogisticCoefficientRow,
  MetricRecord,
  ModelPerformanceRow,
  ModelSummary,
  OverviewMetrics,
  PriorityRow,
  PrioritySummary,
} from "@/lib/types";

const REPO_ROOT = path.resolve(process.cwd(), "..");
const OUTPUTS_DIR = path.join(REPO_ROOT, "outputs");
const TABLES_DIR = path.join(OUTPUTS_DIR, "tables");
const FIGURES_DIR = path.join(OUTPUTS_DIR, "figures");

async function readCsv<T>(filePath: string): Promise<T[]> {
  const content = await fs.readFile(filePath, "utf-8");
  const parsed = Papa.parse<T>(content, {
    header: true,
    skipEmptyLines: true,
  });

  if (parsed.errors.length > 0) {
    throw new Error(`Failed to parse CSV ${filePath}: ${parsed.errors[0].message}`);
  }

  return parsed.data;
}

import { toNumber } from "@/lib/format";

function round(value: number, digits = 3): number {
  return Number(value.toFixed(digits));
}

export async function getOverviewMetrics(): Promise<OverviewMetrics> {
  const rows = await readCsv<MetricRecord>(path.join(TABLES_DIR, "dataset_overview.csv"));
  const recordMap = new Map(rows.map((row) => [row.metric, row.value]));

  return {
    rowCount: toNumber(recordMap.get("row_count")),
    columnCount: toNumber(recordMap.get("column_count")),
    churnRate: toNumber(recordMap.get("churn_rate")),
  };
}

export async function getModelSummary(): Promise<ModelSummary> {
  const rows = await readCsv<ModelPerformanceRow>(path.join(TABLES_DIR, "model_performance_comparison.csv"));
  return {
    bestModel: rows[0] ?? null,
    rows,
  };
}

export async function getPrioritySummary(): Promise<PrioritySummary> {
  const rows = await readCsv<PriorityRow>(path.join(TABLES_DIR, "customer_priority_table.csv"));
  const highPriorityCount = rows.filter((row) => row.priority_level === "Top Priority").length;
  const averagePriorityScore =
    rows.length === 0
      ? 0
      : rows.reduce((total, row) => total + toNumber(row.priority_score), 0) / rows.length;

  return {
    rows,
    highPriorityCount,
    averagePriorityScore: round(averagePriorityScore, 2),
  };
}

export async function getTopRetentionTargets(limit = 20): Promise<PriorityRow[]> {
  const rows = await readCsv<PriorityRow>(path.join(TABLES_DIR, "top_20_retention_targets.csv"));
  return rows.slice(0, limit);
}

export async function getExplainabilitySummary(): Promise<ExplainabilitySummary> {
  const rows = await readCsv<LogisticCoefficientRow>(path.join(TABLES_DIR, "logistic_coefficients.csv"));
  const sortedByAbsolute = [...rows].sort(
    (left, right) => toNumber(right.abs_coefficient) - toNumber(left.abs_coefficient),
  );
  const strongestPositive = [...rows]
    .filter((row) => toNumber(row.coefficient) > 0)
    .sort((left, right) => toNumber(right.coefficient) - toNumber(left.coefficient))
    .slice(0, 6);
  const strongestNegative = [...rows]
    .filter((row) => toNumber(row.coefficient) < 0)
    .sort((left, right) => toNumber(left.coefficient) - toNumber(right.coefficient))
    .slice(0, 6);

  return {
    topDrivers: sortedByAbsolute.slice(0, 10),
    strongestPositive,
    strongestNegative,
  };
}

export async function getAvailableFigureNames(): Promise<string[]> {
  const entries = await fs.readdir(FIGURES_DIR, { withFileTypes: true });
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".png"))
    .map((entry) => entry.name)
    .sort();
}

export async function getBusinessNarrative() {
  const [overview, modelSummary, prioritySummary, explainability, figureNames] = await Promise.all([
    getOverviewMetrics(),
    getModelSummary(),
    getPrioritySummary(),
    getExplainabilitySummary(),
    getAvailableFigureNames(),
  ]);

  return {
    overview,
    bestModel: modelSummary.bestModel,
    highPriorityCount: prioritySummary.highPriorityCount,
    averagePriorityScore: prioritySummary.averagePriorityScore,
    strongestPositive: explainability.strongestPositive.slice(0, 3),
    strongestNegative: explainability.strongestNegative.slice(0, 3),
    figureCoverage: figureNames,
  };
}

export function getFigureUrl(fileName: string): string {
  return `/api/assets/${fileName}`;
}
