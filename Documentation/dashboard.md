# AgriPredict AI Dashboard

## Data and Estimates

The dashboard summary and historical charts cover all 24 recorded seasons, from 2000/01 to 2023/24. When a user selects a province, the dashboard updates its historical chart, average yield and planning baseline. The three-season moving average includes the current observed season and helps show past patterns; it does not predict future yields.

The planning baseline is the selected province's average yield for 2000/01–2019/20, the same period used to fit the baseline for test evaluation. It provides a historical reference for planning. It is not a forecast for the current season. All yields are measured in tonnes per planted hectare.

For a planning scenario, the dashboard multiplies this baseline by the planted area entered by the user. The user can also enter an assumed delivery percentage to estimate how much of that production might reach the cooperative. Both figures depend on these assumptions and should be treated as scenarios rather than verified forecasts.

## Model Results and Assistant

The dashboard loads the regression scores from `Results/model_metrics.csv`. When `Results/neural_network_metrics.csv` is available, it also shows the experimental neural network scores, labelled as an exploratory comparison. If the regression scores are missing, the dashboard asks the user to run the model script.

The text assistant uses the existing `chatbot.respond()` function. Users can see the conversation history, but each question is handled separately, without using earlier messages to interpret follow-up questions. The updated `chatbot_data.py` describes the completed dashboard features.

## Running the Dashboard

Add `streamlit>=1.50` to the existing `requirements.txt`, keeping the other packages. Then run these commands from the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run Code/dashboard.py
```

Streamlit displays a local address that can be opened in a browser. Keep `settings.py`, `preparation.py`, `chatbot.py` and `chatbot_data.py` in `Code/`, and the final dataset in `Dataset/`.

## Checks Completed

The dashboard loaded in Streamlit's app test runner without application errors. Checks passed for changing the province, entering a planted area of zero, asking about saved model scores and clearing the conversation. These checks confirm the tested behaviour. The layout still needs to be reviewed in a browser at the user's screen size.

A demonstration video will show the dashboard in use and explain the final model's results.

