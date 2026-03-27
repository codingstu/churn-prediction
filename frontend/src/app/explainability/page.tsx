import { DataTable } from "@/components/DataTable";
import { FigureCard } from "@/components/FigureCard";
import { getExplainabilitySummary, getFigureUrl, getTopRetentionTargets } from "@/lib/data";
import { formatDecimal } from "@/lib/format";

export default async function ExplainabilityPage() {
  const [explainability, topTargets] = await Promise.all([getExplainabilitySummary(), getTopRetentionTargets(8)]);

  return (
    <div className="page-section">
      <section className="page-header">
        <div>
          <p className="eyebrow">Customer Explanation</p>
          <h1>Global and local explainability review</h1>
          <p>
            Explainability combines coefficient-level evidence and SHAP visuals so that high-risk customers can be
            interpreted in business language rather than only by raw model scores.
          </p>
        </div>
        <div className="status-badge status-badge--success">SHAP artifacts detected in current outputs</div>
      </section>

      <section className="grid grid--two">
        <FigureCard
          title="SHAP summary"
          description="Global view of feature contributions across the evaluated sample."
          src={getFigureUrl("logistic_regression_shap_summary.png")}
          alt="Logistic regression SHAP summary"
        />
        <FigureCard
          title="Local SHAP waterfall"
          description="Single-customer explanation for an example high-risk prediction."
          src={getFigureUrl("logistic_regression_shap_local_waterfall.png")}
          alt="Logistic regression SHAP local waterfall"
        />
      </section>

      <section className="grid grid--two">
        <article className="card">
          <h3>Top absolute churn drivers</h3>
          <p className="muted" style={{ margin: "8px 0 16px" }}>
            Largest coefficients by absolute magnitude from the logistic model explain which signals dominate the decision boundary.
          </p>
          <DataTable
            rows={explainability.topDrivers}
            columns={[
              { key: "feature", header: "Feature" },
              {
                key: "coefficient",
                header: "Coefficient",
                render: (row) => formatDecimal(row.coefficient),
              },
              {
                key: "abs_coefficient",
                header: "Absolute Coefficient",
                render: (row) => formatDecimal(row.abs_coefficient),
              },
            ]}
          />
        </article>

        <article className="card">
          <h3>Suggested customers for explanation review</h3>
          <p className="muted" style={{ margin: "8px 0 16px" }}>
            The current pipeline does not export per-customer SHAP tables yet, so the frontend pairs the local SHAP figure with top-risk customers for analyst review.
          </p>
          <DataTable
            rows={topTargets}
            columns={[
              { key: "customerID", header: "Customer ID" },
              {
                key: "churn_probability",
                header: "Churn Probability",
                render: (row) => formatDecimal(row.churn_probability),
              },
              {
                key: "priority_score",
                header: "Priority Score",
                render: (row) => formatDecimal(row.priority_score, 2),
              },
              { key: "priority_level", header: "Priority Level" },
            ]}
          />
        </article>
      </section>

      <section className="grid grid--two">
        <article className="card insight-block">
          <h3>Strongest positive churn signals</h3>
          <ul className="list">
            {explainability.strongestPositive.map((row) => (
              <li key={row.feature}>
                <strong>{row.feature}</strong>: coefficient {formatDecimal(row.coefficient)}
              </li>
            ))}
          </ul>
        </article>
        <article className="card insight-block">
          <h3>Strongest negative churn signals</h3>
          <ul className="list">
            {explainability.strongestNegative.map((row) => (
              <li key={row.feature}>
                <strong>{row.feature}</strong>: coefficient {formatDecimal(row.coefficient)}
              </li>
            ))}
          </ul>
        </article>
      </section>
    </div>
  );
}
