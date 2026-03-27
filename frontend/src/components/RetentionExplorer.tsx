"use client";

import { useMemo, useState } from "react";

import { DataTable } from "@/components/DataTable";
import { formatCurrency, formatDecimal } from "@/lib/format";
import type { PriorityRow } from "@/lib/types";

type RetentionExplorerProps = {
  rows: PriorityRow[];
};

export function RetentionExplorer({ rows }: RetentionExplorerProps) {
  const [query, setQuery] = useState("");
  const [priorityLevel, setPriorityLevel] = useState("ALL");
  const [riskSegment, setRiskSegment] = useState("ALL");

  const filteredRows = useMemo(() => {
    return rows.filter((row) => {
      const matchesQuery = row.customerID.toLowerCase().includes(query.toLowerCase());
      const matchesPriority = priorityLevel === "ALL" || row.priority_level === priorityLevel;
      const matchesRisk = riskSegment === "ALL" || row.risk_segment === riskSegment;
      return matchesQuery && matchesPriority && matchesRisk;
    });
  }, [priorityLevel, query, riskSegment, rows]);

  return (
    <section className="page-section">
      <div className="filter-bar">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search customer ID"
          aria-label="Search customer ID"
        />
        <select value={priorityLevel} onChange={(event) => setPriorityLevel(event.target.value)} aria-label="Priority level">
          <option value="ALL">All priority levels</option>
          <option value="Top Priority">Top Priority</option>
          <option value="Secondary Priority">Secondary Priority</option>
          <option value="Low Priority">Low Priority</option>
        </select>
        <select value={riskSegment} onChange={(event) => setRiskSegment(event.target.value)} aria-label="Risk segment">
          <option value="ALL">All risk segments</option>
          <option value="High Risk">High Risk</option>
          <option value="Low Risk">Low Risk</option>
        </select>
      </div>

      <DataTable
        rows={filteredRows}
        emptyText="No customers matched the selected filters."
        columns={[
          { key: "customerID", header: "Customer ID" },
          {
            key: "churn_probability",
            header: "Churn Probability",
            render: (row) => formatDecimal(row.churn_probability),
          },
          {
            key: "MonthlyCharges",
            header: "Monthly Charges",
            render: (row) => formatCurrency(row.MonthlyCharges),
          },
          {
            key: "priority_score",
            header: "Priority Score",
            render: (row) => formatDecimal(row.priority_score, 2),
          },
          {
            key: "risk_segment",
            header: "Risk Segment",
            render: (row) => (
              <span className={`segment-pill ${row.risk_segment === "High Risk" ? "segment-pill--high" : "segment-pill--low"}`}>
                {row.risk_segment}
              </span>
            ),
          },
          {
            key: "priority_level",
            header: "Priority Level",
            render: (row) => {
              const className =
                row.priority_level === "Top Priority"
                  ? "priority-pill priority-pill--top"
                  : row.priority_level === "Secondary Priority"
                    ? "priority-pill priority-pill--secondary"
                    : "priority-pill priority-pill--low";
              return <span className={className}>{row.priority_level}</span>;
            },
          },
        ]}
      />
    </section>
  );
}
