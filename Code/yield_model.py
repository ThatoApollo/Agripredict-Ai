"""Compare a provincial historical baseline with two regression models."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

import settings
from preparation import train, validation, test

RESULTS_DIR = settings.PROJECT_DIR / "Results"


def baseline_predict(history, rows):
    # Each province's mean uses only the supplied historical training records.
    means = history.groupby("province")[settings.TARGET].mean()
    return rows["province"].map(means).to_numpy()


def score(actual, predicted):
    return {
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": np.sqrt(mean_squared_error(actual, predicted)),
    }


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    models = {
        "Linear regression": LinearRegression(),
        "Random forest": RandomForestRegressor(
            n_estimators=200, max_depth=3, min_samples_leaf=4, random_state=42
        ),
    }
    metrics = []
    predictions = []

    # Fix model settings before examining the final test results.
    for name in ["Historical baseline", *models]:
        if name == "Historical baseline":
            predicted = baseline_predict(train, validation)
        else:
            model = clone(models[name])
            model.fit(train[settings.FEATURES], train[settings.TARGET])
            predicted = model.predict(validation[settings.FEATURES])
        metrics.append({"split": "Validation", "model": name,
                        **score(validation[settings.TARGET], predicted)})

    # Choose by validation MAE; test performance does not change this choice.
    selected = min(metrics, key=lambda row: row["MAE"])["model"]
    history = pd.concat([train, validation], ignore_index=True)
    fitted_models = {}
    for name in ["Historical baseline", *models]:
        if name == "Historical baseline":
            predicted = baseline_predict(history, test)
        else:
            model = clone(models[name])
            model.fit(history[settings.FEATURES], history[settings.TARGET])
            predicted = model.predict(test[settings.FEATURES])
            fitted_models[name] = model
        metrics.append({"split": "Test", "model": name,
                        **score(test[settings.TARGET], predicted)})
        rows = test[["province", "season", settings.TARGET]].copy()
        rows = rows.rename(columns={settings.TARGET: "actual_yield"})
        rows["model"] = name
        rows["predicted_yield"] = predicted
        rows["error"] = rows["predicted_yield"] - rows["actual_yield"]
        predictions.append(rows)

    metrics = pd.DataFrame(metrics)
    metrics.to_csv(RESULTS_DIR / "model_metrics.csv", index=False)
    pd.concat(predictions, ignore_index=True).to_csv(
        RESULTS_DIR / "test_predictions.csv", index=False
    )
    # Preserve the evaluated model and its metadata for later dashboard work.
    # It is not refitted on the test data.
    joblib.dump({
        "selected_model": selected,
        "estimator": fitted_models.get(selected),
        "province_means": history.groupby("province")[settings.TARGET].mean().to_dict(),
        "features": settings.FEATURES,
        "unit": settings.UNIT,
        "training_end_year": int(history["harvest_year"].max()),
    }, RESULTS_DIR / "yield_model.joblib")
    print(f"Rows: training={len(train)}, validation={len(validation)}, test={len(test)}")
    print(metrics.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
    print("Selected using validation MAE:", selected)
    print("Units:", settings.UNIT)
    print("Results saved to", RESULTS_DIR)


if __name__ == "__main__":
    main()
