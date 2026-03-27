import { DataTable } from "@/components/DataTable";
import { FigureCard } from "@/components/FigureCard";
import { getFigureUrl, getModelSummary } from "@/lib/data";
import { formatDecimal } from "@/lib/format";

export default async function ModelsPage() {
  const { bestModel, rows } = await getModelSummary();

  return (
    <div className="page-section">
      <section className="page-header">
        <div>
          <p className="eyebrow">Model Comparison</p>
          <h1>Performance benchmarking across classifiers</h1>
          <p>
            The model comparison page maps the evaluation outputs into an executive view, preserving the
            standardized metric files generated under the analytics pipeline.
          </p>
        </div>
        <div className="status-badge status-badge--success">
          Best model: {bestModel?.model ?? "Unavailable"}
        </div>
      </section>

      <section className="card">
        <h3>Model performance table</h3>
        <p className="muted" style={{ margin: "8px 0 16px" }}>
          Metrics are loaded directly from the repository output contract and displayed without re-computing the models.
        </p>
        <DataTable
          rows={rows}
          columns={[
            { key: "model", header: "Model" },
            {
              key: "roc_auc",
              header: "ROC-AUC",
              render: (row) => formatDecimal(row.roc_auc),
            },
            {
              key: "f1_score",
              header: "F1 Score",
              render: (row) => formatDecimal(row.f1_score),
            },
            {
              key: "recall",
              header: "Recall",
              render: (row) => formatDecimal(row.recall),
            },
            {
              key: "precision",
              header: "Precision",
              render: (row) => formatDecimal(row.precision),
            },
          ]}
        />
      </section>

      <section className="grid grid--two">
        <FigureCard
          title="ROC curve comparison"
          description="Visual comparison of ranking performance for all fitted classifiers."
          src={getFigureUrl("roc_curve_comparison.png")}
          alt="ROC curve comparison"
        />
        <FigureCard
          title="Logistic regression confusion matrix"
          description="Confusion matrix for the current top-performing model."
          src={getFigureUrl("confusion_matrix_logistic_regression.png")}
          alt="Logistic regression confusion matrix"
        />
      </section>

      <section className="grid grid--two">
        <FigureCard
          title="Random forest confusion matrix"
          description="Error distribution for the random forest baseline."
          src={getFigureUrl("confusion_matrix_random_forest.png")}
          alt="Random forest confusion matrix"
        />
        <FigureCard
          title="XGBoost confusion matrix"
          description="Error distribution for the XGBoost benchmark model."
          src={getFigureUrl("confusion_matrix_xgboost.png")}
          alt="XGBoost confusion matrix"
        />
      </section>
    </div>
  );
}
