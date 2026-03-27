import { MetricCard } from "@/components/MetricCard";
import { RetentionExplorer } from "@/components/RetentionExplorer";
import { getPrioritySummary, getTopRetentionTargets } from "@/lib/data";
import { formatDecimal } from "@/lib/format";

export default async function RetentionPage() {
  const [prioritySummary, topTargets] = await Promise.all([getPrioritySummary(), getTopRetentionTargets(20)]);

  return (
    <div className="page-section">
      <section className="page-header">
        <div>
          <p className="eyebrow">Retention Priority</p>
          <h1>Actionable customer intervention queue</h1>
          <p>
            This page operationalizes the repository retention scoring logic by exposing searchable customer-level
            prioritization outputs for business review.
          </p>
        </div>
        <div className="status-badge status-badge--warning">Priority score = churn probability × monthly charges</div>
      </section>

      <section className="grid grid--metrics">
        <MetricCard
          label="Scored customers"
          value={prioritySummary.rows.length.toLocaleString("en-US")}
          hint="Customers available in the scored test partition output."
        />
        <MetricCard
          label="Top Priority count"
          value={prioritySummary.highPriorityCount.toLocaleString("en-US")}
          hint="High-risk and high-value customers requiring immediate attention."
        />
        <MetricCard
          label="Average priority score"
          value={formatDecimal(prioritySummary.averagePriorityScore, 2)}
          hint="Average across the exported customer priority table."
        />
        <MetricCard
          label="Previewed top targets"
          value={topTargets.length.toLocaleString("en-US")}
          hint="High-priority rows highlighted for management review."
        />
      </section>

      <section className="card">
        <h3>Interactive retention explorer</h3>
        <p className="muted" style={{ margin: "8px 0 16px" }}>
          Filter by customer identifier, risk segment, and priority level without changing the underlying analytics outputs.
        </p>
        <RetentionExplorer rows={prioritySummary.rows} />
      </section>
    </div>
  );
}
