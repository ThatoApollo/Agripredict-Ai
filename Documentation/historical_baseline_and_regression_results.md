# Historical Baseline and Regression Results

## Data and Evaluation

The models were tested using 72 records covering three provinces over 24 maize seasons. Yield is measured in tonnes per planted hectare.

The data were split chronologically:

- Training: 2000/01–2015/16 — 48 records.
- Validation: 2016/17–2019/20 — 12 records.
- Testing: 2020/21–2023/24 — 12 records.

All provinces from the same season were kept together. Validation results were used to select an approach before evaluating it on the test data.

## Models Compared

The historical baseline uses each province’s average yield from the training period. Linear regression and random forest use seasonal rainfall, average temperature and province indicators.

After validation, the models were fitted again using the combined training and validation records. The final test records were kept separate.

## Results

Lower MAE and RMSE values indicate smaller prediction errors. Both measures are expressed in tonnes per planted hectare.

| Approach | Validation MAE | Validation RMSE | Test MAE | Test RMSE |
| --- | --- | --- | --- | --- |
| Historical baseline | 1.491 | 1.615 | 1.511 | 1.614 |
| Linear regression | 1.678 | 1.734 | 1.650 | 1.785 |
| Random forest | 1.664 | 1.736 | 1.660 | 1.880 |

The historical baseline performed best on both validation and test data. Its test predictions differed from the recorded yields by about 1.51 tonnes per planted hectare on average. Neither regression model improved on this result.

The baseline will therefore remain the preferred approach at this stage. These results do not yet show that the predictions are accurate enough for practical procurement or storage decisions.

## Limitations

The dataset is small, and the test period covers only four seasons. Weather values also represent an average of three sample points per province, which may miss local differences.

The records use weather through January for a prediction dated 15 February. We still need to confirm when the original weather data would have been available. Time series analysis and the experimental neural network remain separate tasks.

## Running the Script

From the project’s main folder, run:

python Code/yield_model.py

The script saves evaluation scores, test predictions and the selected model information in the Results folder.
