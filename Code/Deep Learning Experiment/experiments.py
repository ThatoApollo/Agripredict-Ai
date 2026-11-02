"""Deep Learning Algorithm; does not replace the dashboard model."""
import hashlib
import json
import platform
import warnings
from importlib.metadata import version

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline

import sys
from pathlib import Path

# Allow imports from the parent Code folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import settings
from preparation import load_data, split_data, model_data, make_preprocessor
from yield_model import calculate_errors


def main():
    data = load_data()
    train, validation, test = split_data(data)
    results_dir = settings.PROJECT_DIR / 'Results' / 'Experiments'
    results_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        'purpose': 'Retrospective comparisons specified after 2020 results were known',
        'dataset_sha256': hashlib.sha256(settings.DATA_FILE.read_bytes()).hexdigest(),
        'python': platform.python_version(),
        'versions': {
            name: version(name)
            for name in ['scikit-learn', 'numpy', 'pandas', 'joblib']
        },
        'fits': [],
    }

    for period, fitting, evaluation in [
        ('validation', train, validation),
        ('test', pd.concat([train, validation]), test),
    ]:
        x_fit, y_fit = model_data(fitting)
        x_eval, y_eval = model_data(evaluation)

        estimators = {'Linear regression': LinearRegression()}
        for depth in [3, 6, 10]:
            estimators[f'Random forest depth {depth}'] = RandomForestRegressor(
                n_estimators=200,
                max_depth=depth,
                random_state=42,
                n_jobs=-1,
            )

        estimators['Deep MLP 32-16'] = MLPRegressor(
            hidden_layer_sizes=(32, 16),
            alpha=0.01,
            batch_size=64,
            learning_rate_init=0.001,
            max_iter=300,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=20,
            random_state=42,
        )

        predictions = evaluation[
            ['source_row', 'year', settings.TARGET]
        ].copy()
        predictions['Historical baseline'] = float(y_fit.mean())

        for name, estimator in estimators.items():
            scale = not isinstance(estimator, RandomForestRegressor)
            model = make_pipeline(
                make_preprocessor(scale=scale),
                estimator,
            )

            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                model.fit(x_fit, y_fit)

            predictions[name] = model.predict(x_eval)
            manifest['fits'].append({
                'period': period,
                'model': name,
                'parameters': estimator.get_params(),
                'iterations': getattr(estimator, 'n_iter_', None),
                'warnings': [str(w.message) for w in caught],
            })

        scores = []
        for name in ['Historical baseline'] + list(estimators):
            mae, rmse = calculate_errors(y_eval, predictions[name])
            scores.append({
                'model': name,
                'MAE': mae,
                'RMSE': rmse,
            })

        scores = pd.DataFrame(scores)
        scores.to_csv(
            results_dir / f'{period}_metrics.csv',
            index=False,
        )
        predictions.to_csv(
            results_dir / f'{period}_predictions.csv',
            index=False,
        )
        print(period, '\n', scores.round(4).to_string(index=False))

    (results_dir / 'manifest.json').write_text(
        json.dumps(manifest, indent=2)
    )
    print('Saved separate experiments. Dashboard model unchanged.')


if __name__ == '__main__':
    main()
