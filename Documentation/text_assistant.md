# Text Assistant

The text assistant answers supported questions about AgriPredict AI and general maize farming. It covers platform information, yield estimates, evaluation results, data, limitations, storage scenarios, planting, soil, irrigation, fertiliser, crop rotation and crop problems.

## How It Works

TF-IDF converts example questions into numeric features, and logistic regression predicts a topic. A similarity check also compares the question with the examples. The assistant returns a predefined answer only when the classifier and similarity check agree and the similarity and topic separation meet fixed thresholds. Otherwise, it asks the user to rephrase.

The thresholds are development heuristics, not probabilities or proof that a question is understood. Questions with familiar words can still be classified incorrectly. Short, unfamiliar or multi-topic questions may receive a fallback. The assistant supports English and does not remember earlier messages.

Agricultural guidance is written separately from the yield model. It is not learned from the maize dataset and is not a finding from the prediction models. The assistant does not diagnose crop problems, recommend pesticide doses, calculate live forecasts or cover every agriculture topic.

## Project Answers

The performance answer reads the historical baseline's test MAE and RMSE from `Results/model_metrics.csv`. If the file is missing or invalid, it explains that scores are unavailable. It does not claim to provide a new yield forecast. Platform responses describe the dashboard as still under development; these should be updated when the dashboard is completed.

Yield and storage explanations use tonnes per planted hectare to match the dataset. Production scenarios must use planted hectares on the same basis, and cooperative deliveries must be estimated separately from provincial production.

## Testing

Five automated test methods passed. They check 15 supported question variants, 10 fallback inputs, greetings, reading saved scores, missing or invalid results files, and the absence of invented live forecasts. A terminal session was also checked using a model-results question, a planting question and an unrelated question.

This is a small development regression set, not an independent measure of chatbot accuracy. Further questions from users are needed to assess coverage. The tests do not guarantee correct handling of every out-of-scope question.

## Run the Assistant

From the project root:

```bash
python Code/chatbot.py
```

Type `quit` to exit. Example questions:

- How accurate are the models?
- What dataset was used?
- When should I plant maize?
- What is crop rotation?

Run the checks with:

```bash
python -m unittest discover -s Tests -p test_chatbot.py -v
```

The assistant uses pandas and scikit-learn, which are already project dependencies. No API key, online service or additional package is required at runtime. Keep `chatbot.py` and `chatbot_data.py` together in `Code/`. The future dashboard can call `chatbot.respond(question)`.

## Sources for General Guidance

The following sources were consulted when preparing the general answers on 22 October 2026. They support educational explanations rather than field-specific recommendations. Crop-problem responses request local assessment instead of making a diagnosis.

- [ARC: Soil analyses laboratory](https://www.arc.agric.za/arc-sgi/Pages/Production%20Systems/Soil-laboratory.aspx) — soil testing, nutrient management and yield targets.
- [Limpopo Department of Agriculture: Successful maize production requires right practice of planting](https://www.ldard.gov.za/index.php/news/successful-maize-production-requires-right-practice-of-planting) — local rainfall, cultivar choice and planting considerations.
- [FAO: Crop water needs](https://www.fao.org/4/s2022e/s2022e02.htm) — growth stage and climate affect crop water requirements.
- [FAO: Growing maize and soybean in rotation](https://www.fao.org/family-farming/detail/en/c/1619682/) — general maize–legume rotation principles; the example concerns Uganda and is not a South African planting prescription.
