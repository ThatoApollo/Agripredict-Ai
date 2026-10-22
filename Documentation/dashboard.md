# AgriPredict AI Dashboard

## Data and Estimates

The summary and historical charts show all 24 recorded seasons, 2000/01–2023/24. Selecting a province changes its historical chart, average yield and planning baseline. The three-season moving average includes the current observed season and is not a forecast.

The planning baseline uses the selected province's average yield from 2000/01–2019/20. This matches the fitting period used for baseline test evaluation. It is a historical reference, not a forecast for the current season. All yields are in tonnes per planted hectare.

The planning scenario multiplies this baseline by the user's assumed planted area. An assumed delivery percentage estimates the share reaching the cooperative. These are scenarios rather than verified production or delivery forecasts.

## Model Results and Assistant

The dashboard reads regression scores from `Results/model_metrics.csv`. If available, it also displays the experimental network from `Results/neural_network_metrics.csv`, labelled as an exploratory comparison. Missing regression scores produce an instruction to run the model script.

The assistant calls the existing `chatbot.respond()` function. It displays conversation history but does not interpret follow-up questions using earlier messages. The updated `chatbot_data.py` describes the completed dashboard features.

## Running the Dashboard

Add `streamlit>=1.50` to the existing `requirements.txt`, keeping the other packages. Then run from the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run Code/dashboard.py
```

Streamlit provides a local browser address. Keep `settings.py`, `preparation.py`, `chatbot.py` and `chatbot_data.py` in `Code/`, and the final dataset in `Dataset/`.

## Checks Completed

Streamlit's app test runner loaded the dashboard without application exceptions. Checks passed for changing the province, calculating a zero-area scenario, asking about saved model scores and clearing the conversation. These checks verify behaviour; the appearance still needs review in your browser at your screen size.

A demonstration video will show how the final model performs.
