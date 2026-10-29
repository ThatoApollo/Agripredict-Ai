"""Train and evaluate linear regression for maize yield. Run: python Code/yield_model.py"""
import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline

import settings
from preparation import load_data, split_data, model_data, make_preprocessor

RESULTS_DIR = settings.PROJECT_DIR / 'Results'


def calculate_errors(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return mae, rmse


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    data = load_data()
    train, validation, test = split_data(data)
    training_features, training_target = model_data(train)
    validation_features, validation_target = model_data(validation)

    selected_name = 'Linear regression'
    model_template = make_pipeline(
        make_preprocessor(scale=True), LinearRegression()
    )

    validation_results = []
    # The historical mean is a reference calculation, not a trained algorithm.
    for name in ['Historical baseline', selected_name]:
        if name == 'Historical baseline':
            predicted = np.full(len(validation_features), float(training_target.mean()))
        else:
            model = clone(model_template)
            model.fit(training_features, training_target)
            predicted = model.predict(validation_features)
        mae, rmse = calculate_errors(validation_target, predicted)
        validation_results.append({'model': name, 'MAE': mae, 'RMSE': rmse})

    validation_scores = pd.DataFrame(validation_results)
    # This winner refers only to the two retained evaluation rows.
    best_row = validation_scores['MAE'].idxmin()
    validation_winner = validation_scores.loc[best_row, 'model']
    # Linear regression remains a design choice made after the test scores were known.
    validation_scores.to_csv(RESULTS_DIR / 'validation_metrics.csv', index=False)

    # Model choices are fixed above, before accessing the test inputs/targets.
    history = pd.concat([train, validation], ignore_index=True)
    history_features, history_target = model_data(history)
    test_features, test_target = model_data(test)
    test_results = []
    prediction_tables = []
    selected_model = None
    for name in ['Historical baseline', selected_name]:
        if name == 'Historical baseline':
            predicted = np.full(len(test_features), float(history_target.mean()))
        else:
            model = clone(model_template)
            model.fit(history_features, history_target)
            predicted = model.predict(test_features)
        if not np.isfinite(predicted).all():
            raise ValueError('Model produced non-finite predictions.')
        mae, rmse = calculate_errors(test_target, predicted)
        test_results.append({'model': name, 'MAE': mae, 'RMSE': rmse})
        rows = test[['source_row', 'year']].copy()
        rows['model'] = name
        rows['actual_yield'] = test_target
        rows['predicted_yield'] = predicted
        rows['error'] = predicted - test_target
        prediction_tables.append(rows)
        if name == selected_name:
            selected_model = model

    test_scores = pd.DataFrame(test_results)
    test_scores.to_csv(RESULTS_DIR / 'test_metrics.csv', index=False)
    predictions = pd.concat(prediction_tables, ignore_index=True)
    predictions.to_csv(RESULTS_DIR / 'test_predictions.csv', index=False)

    # Save the entire fitted pipeline, including learned missing-value handling.
    joblib.dump({
        'selected_model': selected_name,
        'estimator': selected_model,
        'features': settings.FEATURES,
        'target': settings.TARGET,
        'unit': settings.UNIT,
        'prediction_context': 'experimental planting-time estimate',
        'training_years': [2016, 2017, 2018, 2019],
        'test_year': settings.TEST_YEAR,
        'validation_winner': validation_winner,
        'selection_rule': 'linear regression chosen for simplicity and explainability',
        'selection_timing': 'design decision after 2020 test results were known',
        'evaluation_status': '2020 scores are historical; not a fresh independent assessment of this choice',
        'historical_baseline_mean': float(history_target.mean()),
    }, RESULTS_DIR / 'yield_model.joblib')

    print('Validation results:')
    print(validation_scores.round(4).to_string(index=False))
    print('\nLowest validation MAE among retained results:', validation_winner)
    print('Prototype model chosen for simplicity:', selected_name)
    print('\nFinal test results:')
    print(test_scores.round(4).to_string(index=False))
    print('\nUnits:', settings.UNIT)
    print('Results saved in:', RESULTS_DIR)
    print('Do not use test scores to retune the model.')


if __name__ == '__main__':
    main()
