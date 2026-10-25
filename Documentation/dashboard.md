# AgriPredict AI Dashboard

## Overview

The dashboard summary and historical charts cover all 24 recorded seasons, from 2000/01 to 2023/24. When a user selects a province, the dashboard updates its historical chart, average yield and planning baseline. The three-season moving average includes each observed season and the two seasons before it. It helps show past patterns; it does not predict future yields.

The planning baseline is the selected province's average yield for 2000/01–2019/20, the same period used to fit the baseline for test evaluation. It provides a historical reference for planning. It is not a forecast for the current season. All yields are measured in tonnes per planted hectare.

The historical average was the selected approach because it had lower validation errors than the regression models and also performed better on the test data. It therefore provides the reference value for production planning.

For a planning scenario, the dashboard multiplies this baseline by the planted area entered by the user to calculate estimated production in tonnes. The area field starts blank, and the result appears after a number is entered. Users can type their own area or use the buttons to change it by one hectare. The result is a planning scenario rather than a verified forecast.

## Model Results and Assistant

The dashboard loads the regression scores from `Results/model_metrics.csv`. When `Results/neural_network_metrics.csv` is available, it also shows the experimental neural network scores, labelled as an exploratory comparison. If the regression scores are missing, the dashboard asks the user to run the model script.

The text assistant uses the existing `chatbot.respond()` function. Users can see the conversation history, but each question is handled separately, without using earlier messages to interpret follow-up questions. The updated `chatbot_data.py` describes the completed dashboard features.

## Running the Dashboard


```bash
python -m pip install -r requirements.txt
python -m streamlit run Code/dashboard.py
```

Streamlit displays a local address that can be opened in a browser. Keep `settings.py`, `preparation.py`, `chatbot.py` and `chatbot_data.py` in `Code/`, and the final dataset in `Dataset/`.
