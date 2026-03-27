import { FigureCard } from "@/components/FigureCard";
import { MetricCard } from "@/components/MetricCard";
import { getBusinessNarrative, getFigureUrl } from "@/lib/data";
import { formatDecimal, formatPercent } from "@/lib/format";

export default async function InsightsPage() {
  const narrative = await getBusinessNarrative();

  return (
    <div className="page-section">
      <section className="page-header">
        <div>
          <p className="eyebrow">Business Insights</p>
          <h1>Management-ready interpretation layer</h1>
          <p>
            This page translates analytics artifacts into a business narrative aligned with the proposal scope:
            churn understanding, model-based prediction, explainability, and retention prioritization.
          </p>
        </div>
      </section>

      <section className="grid grid--metrics">
        <MetricCard
          label="Churn rate"
          value={formatPercent(narrative.overview.churnRate, 2)}
          hint="Observed on the cleaned IBM Telco dataset."
        />
        <MetricCard
          label="Best model ROC-AUC"
          value={narrative.bestModel ? formatDecimal(narrative.bestModel.roc_auc) : "N/A"}
          hint="Top score from the current comparison table."
        />
        <MetricCard
          label="High-priority customers"
          value={narrative.highPriorityCount.toLocaleString("en-US")}
          hint="Immediate retention focus candidates."
        />
        <MetricCard
          label="Figure artifacts"
          value={narrative.figureCoverage.length.toLocaleString("en-US")}
          hint="Named visual outputs currently available to the frontend."
        />
      </section>

      <section className="grid grid--two">
        <article className="card insight-block">
          <h3>Executive summary</h3>
          <ul className="list">
            <li>
              The current processed dataset contains {narrative.overview.rowCount.toLocaleString("en-US")} valid customer records across {narrative.overview.columnCount} columns.
            </li>
            <li>
              {narrative.bestModel?.model ?? "The best available model"} currently leads the benchmark table and should anchor downstream business review.
            </li>
            <li>
              {narrative.highPriorityCount.toLocaleString("en-US")} customers are already marked as Top Priority, with an average priority score of {formatDecimal(narrative.averagePriorityScore, 2)}.
            </li>
            <li>
              Explainability is production-visible because SHAP and coefficient artifacts are both present in the repository outputs.
            </li>
          </ul>
        </article>

        <article className="card insight-block">
          <h3>Recommended management actions</h3>
          <ul className="list">
            <li>Target the Top Priority cohort first with retention outreach, contract review, and tailored offers.</li>
            <li>Use the model comparison page to justify model choice during reporting and governance discussions.</li>
            <li>Use the explainability page to convert model behavior into customer-facing or manager-facing narratives.</li>
            <li>Preserve stable output names under [`outputs/`](../outputs/) so the frontend remains synchronized with analytics reruns.</li>
          </ul>
        </article>
      </section>

      <section className="grid grid--two">
        <article className="card insight-block">
          <h3>Key positive churn drivers</h3>
          <ul className="list">
            {narrative.strongestPositive.map((row) => (
              <li key={row.feature}>
                <strong>{row.feature}</strong> increases churn pressure with coefficient {formatDecimal(row.coefficient)}.
              </li>
            ))}
          </ul>
        </article>
        <article className="card insight-block">
          <h3>Key negative churn drivers</h3>
          <ul className="list">
            {narrative.strongestNegative.map((row) => (
              <li key={row.feature}>
                <strong>{row.feature}</strong> reduces churn pressure with coefficient {formatDecimal(row.coefficient)}.
              </li>
            ))}
          </ul>
        </article>
      </section>

      <section className="grid grid--two">
        <FigureCard
          title="Payment method vs churn"
          description="Payment behavior patterns inform intervention strategy and customer communications."
          src={getFigureUrl("payment_method_vs_churn.png")}
          alt="Payment method versus churn figure"
        />
        <FigureCard
          title="Correlation heatmap"
          description="Numerical relationships provide cross-feature context for business interpretation."
          src={getFigureUrl("correlation_heatmap.png")}
          alt="Correlation heatmap"
        />
      </section>
    </div>
  );
}
