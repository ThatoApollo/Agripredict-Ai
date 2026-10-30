"""Train and evaluate the maize yield model."""
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline

import settings
from preparation import load_data, split_data, model_data, make_preprocessor

RESULTS_DIR = settings.PROJECT_DIR / 'Results'
MODEL_NAME = 'Linear regression'

def calculate_errors(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return mae, rmse

def evaluate(fitting_rows, evaluation_rows):
    fitting_features, fitting_target = model_data(fitting_rows)
    evaluation_features, evaluation_target = model_data(evaluation_rows)

    # Create and fit a fresh pipeline for each evaluation.
    model = make_pipeline(
        make_preprocessor(scale=True),
        LinearRegression(),
    )
    model.fit(fitting_features, fitting_target)

    predictions = {
        'Historical baseline': np.full(
            len(evaluation_features), float(fitting_target.mean())
        ),
        MODEL_NAME: model.predict(evaluation_features),
    }

    results = []
    for name, predicted in predictions.items():
        if not np.isfinite(predicted).all():
            raise ValueError('Model produced non-finite predictions.')

        mae, rmse = calculate_errors(evaluation_target, predicted)
        results.append({'model': name, 'MAE': mae, 'RMSE': rmse})

    return model, pd.DataFrame(results)

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    data = load_data()
    train, validation, test = split_data(data)

    _, validation_scores = evaluate(train, validation)

    # Refit on 2016–2019, then evaluate against the 2020 records.
    history = pd.concat([train, validation], ignore_index=True)
    model, test_scores = evaluate(history, test)

    best_row = validation_scores['MAE'].idxmin()
    validation_winner = validation_scores.loc[best_row, 'model']

    # Keep the pipeline and metadata required by the dashboard.
    joblib.dump({
        'selected_model': MODEL_NAME,
        'estimator': model,
        'features': settings.FEATURES,
        'target': settings.TARGET,
        'unit': settings.UNIT,
        'prediction_context': 'experimental planting-time estimate',
        'training_years': [2016, 2017, 2018, 2019],
        'test_year': settings.TEST_YEAR,
        # Lowest validation MAE among these two retained comparisons.
        'validation_winner': validation_winner,
        'selection_rule': (
            'linear regression chosen for simplicity and explainability'
        ),
        'selection_timing': (
            'design decision after 2020 test results were known'
        ),
        'evaluation_status': (
            '2020 scores are historical; '
            'not a fresh independent assessment of this choice'
        ),
        'historical_baseline_mean': float(history[settings.TARGET].mean()),
    }, RESULTS_DIR / 'yield_model.joblib')

    print('Validation results:')
    print(validation_scores.round(4).to_string(index=False))
    print('\nLowest validation MAE among retained results:', validation_winner)
    print('Prototype model chosen for simplicity:', MODEL_NAME)

    print('\nFinal test results:')
    print(test_scores.round(4).to_string(index=False))
    print('\nUnits:', settings.UNIT)
    print('Model saved to:', RESULTS_DIR / 'yield_model.joblib')
    print('Update the chatbot’s fixed scores if data or modelling changes.')
    print('Do not use test scores to retune the model.')

if __name__ == '__main__':
    main()
