"""Exploratory comparison of a small neural network and historical baseline."""
import warnings

import joblib
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import settings
from preparation import train, validation, test
from yield_model import baseline_predict, score


def make_model():
    # Both input and target scaling are fitted only on the supplied fitting data.
    return TransformedTargetRegressor(
        regressor=make_pipeline(
            StandardScaler(),
            MLPRegressor(
                hidden_layer_sizes=(8, 4), activation="relu", solver="lbfgs",
                alpha=1.0, max_iter=2000, max_fun=50000, random_state=42,
            ),
        ),
        transformer=StandardScaler(),
    )


def fit_model(rows):
    model = make_model()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(rows[settings.FEATURES], rows[settings.TARGET])
    notes = [str(w.message) for w in caught
             if issubclass(w.category, ConvergenceWarning)]
    return model, notes


def main():
    results = settings.PROJECT_DIR / "Results"
    results.mkdir(exist_ok=True)
    metrics, predictions = [], []
    history = pd.concat([train, validation], ignore_index=True)

    # One fixed architecture and seed; no settings are chosen against test scores.
    # This reuses an already-inspected test period, so it is exploratory evidence.
    for split, fitting, evaluation in [
        ("Validation", train, validation), ("Test", history, test)
    ]:
        model, notes = fit_model(fitting)
        for name, predicted in [
            ("Historical baseline", baseline_predict(fitting, evaluation)),
            ("Experimental neural network", model.predict(evaluation[settings.FEATURES])),
        ]:
            metrics.append({
                "split": split, "model": name,
                **score(evaluation[settings.TARGET], predicted),
                "fit_rows": len(fitting), "evaluation_rows": len(evaluation),
                "convergence_warning": " | ".join(notes) if name != "Historical baseline" else "",
            })
            rows = evaluation[["province", "season", settings.TARGET]].copy()
            rows = rows.rename(columns={settings.TARGET: "actual_yield"})
            rows["split"], rows["model"] = split, name
            rows["predicted_yield"] = predicted
            rows["error"] = rows["predicted_yield"] - rows["actual_yield"]
            predictions.append(rows)
        if split == "Test":
            # Separate experimental artifact; does not replace the selected baseline.
            joblib.dump({
                "estimator": model, "features": settings.FEATURES,
                "unit": settings.UNIT, "training_end_year": int(fitting.harvest_year.max()),
                "evaluation_status": "exploratory; test period previously inspected",
            }, results / "experimental_neural_network.joblib")
        if notes:
            print(f"{split} convergence warning:", " | ".join(notes))

    metrics = pd.DataFrame(metrics)
    metrics.to_csv(results / "neural_network_metrics.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(
        results / "neural_network_predictions.csv", index=False
    )
    print(metrics[["split", "model", "MAE", "RMSE"]].to_string(
        index=False, float_format=lambda value: f"{value:.3f}"
    ))
    print("Units:", settings.UNIT)
    print("Exploratory comparison: the test period was previously inspected.")
    print("The existing selected baseline is unchanged.")


if __name__ == "__main__":
    main()
