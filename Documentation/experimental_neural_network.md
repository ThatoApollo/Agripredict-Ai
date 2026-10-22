# Experimental Neural Network

A small feed-forward neural network was built to explore whether it could improve maize yield estimates. It uses the same rainfall, temperature and province inputs as the regression models.

## Model and Evaluation

The model uses scikit-learn's MLPRegressor with two hidden layers containing eight and four neurons. It uses ReLU activation, the L-BFGS solver and regularisation of 1.0. The random seed is 42, with a maximum of 2,000 training iterations. One architecture was tested; no search for better settings was carried out.

Inputs and yield targets are standardised using only the fitting records. Predictions are converted back to tonnes per planted hectare before evaluation.

The network was first fitted on 48 training records and evaluated on 12 validation records. It was then fitted again on the 60 combined training and validation records and evaluated on the 12 test records. All provinces from a season remain together. Neither fit produced a convergence warning.

The test period had already been examined during the regression task. This is therefore an exploratory comparison, rather than a new independent test. The network settings were fixed before running this experiment, and its results were not used to tune them.

## Results

MAE and RMSE are in tonnes per planted hectare. Lower values indicate smaller errors.

| Period | Approach | MAE | RMSE |
| --- | --- | --- | --- |
| Validation | Historical baseline | 1.491 | 1.615 |
| Validation | Experimental neural network | 1.593 | 1.654 |
| Test | Historical baseline | 1.511 | 1.614 |
| Test | Experimental neural network | 1.695 | 2.014 |

The neural network did not improve on the historical baseline. Its test predictions differed from observed yields by about 1.70 tonnes per planted hectare on average, compared with 1.51 for the baseline. The baseline remains the preferred approach, while the network is retained as an experimental comparison.

## Limitations

The dataset is small for a neural network, and the test period covers only four seasons. Results may also vary with the random seed. This experiment does not establish that neural networks are generally unsuitable for maize prediction; it shows that this particular model did not improve on the baseline with the available inputs and evaluation periods.

The model is an in-season yield estimator using weather through January, rather than a forecast of future weather. Its results describe provincial averages, not individual farms. A fresh chronological evaluation plan would be needed for further model selection.

## Running the Script

Run this command from the project root:

```bash
python Code/deep_learning.py
```

The script uses the existing `settings.py`, `preparation.py` and `yield_model.py` in `Code/`. It needs no additional packages beyond NumPy, pandas, scikit-learn and joblib.
