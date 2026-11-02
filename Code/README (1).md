# AgriPredict AI

AgriPredict AI is a Python prototype that estimates maize yield using Kenyan field observations from 2016–2020. It uses location, elevation, soil characteristics and hybrid seed status to produce an experimental estimate in tonnes per hectare. The Streamlit dashboard also provides a production scenario, one annual yield chart and a bounded text assistant. Linear regression powers the dashboard, while random forests and a neural network are evaluated separately.

## Code files and how they work

### `Code/settings.py`

This file stores the settings shared across the project, including the dataset location, seven input names, target column and evaluation years. It defines 2016–2018 as the training period, 2019 as validation and 2020 as the historical test period. Keeping these details in one place helps the other scripts use consistent paths, inputs and units. It also sets the input order used when training the model and submitting field details for prediction.

### `Code/prepare_dataset.py`

This script creates the prepared Kenyan dataset from the original One Acre Fund CSV file. It selects Kenyan records, retains the required columns, converts hybrid seed status into a consistent Boolean format and converts yield from kilograms per hectare to tonnes per hectare by dividing by 1,000. It also assigns the year-based split labels and retains a source-row reference so that each prepared record can be traced to the original file. Zero yields and missing soil values are preserved. The prepared output replaces the existing dataset only after the validation checks succeed.

### `Code/preparation.py`

This script loads the prepared dataset and checks that it contains the required columns, supported years, Kenyan records and first-season observations. It checks for invalid values, duplicate source-row references, incorrect split labels and missing values outside the permitted soil inputs. It then separates the records into training, validation and test periods and selects only the seven model inputs, preventing the target and metadata from entering the model. It also creates median imputation and optional standardisation steps. These steps are fitted using fitting records only, so later evaluation records do not influence the replacement values or scaling.

### `Code/yield_model.py`

This script trains and evaluates the linear regression model used by the dashboard. It first fits the model using 2016–2018 records and evaluates it on 2019, then refits it using 2016–2019 and evaluates it on 2020. At each stage, it compares regression with a historical baseline that predicts the fitting records’ average yield. Performance is measured using MAE, the average absolute prediction error, and RMSE, which gives more weight to large errors. The updated script saves the fitted pipeline, supporting metadata, evaluation scores and test predictions. Regression remains a simplicity-driven choice; the baseline has lower errors on the 2020 records.

### `Code/experiments.py`

This script provides reproducible comparisons between linear regression, random forests with maximum depths of 3, 6 and 10, and an experimental neural network. The neural network has two hidden layers containing 32 and 16 units and produces one continuous yield estimate. It uses imputation, standardisation, regularisation and early stopping to support training and limit unnecessary fitting. The script follows the same external year-based evaluation periods as the production model and saves separate scores, predictions and experiment settings under `Results/Experiments`. It does not replace the dashboard model. These experiments are retrospective comparisons because they were specified after the 2020 results were already known.

### `Code/time_series.py`

This script describes how recorded maize yields vary across the five observation years. It calculates annual summaries, including observation counts, mean yield, median yield, standard deviation and the change in mean yield from the previous year. It saves the summary as a CSV file and creates one line chart showing annual mean and median yields. This is descriptive annual analysis rather than a forecasting model. Different fields and locations may be represented each year, so the chart does not track the same identified farms or represent national Kenyan averages.

### `Code/chatbot_data.py`

This file contains the supported topics, example questions, prepared answers and fallback message used by the assistant. Its answers cover the project, dataset, inputs, units, annual analysis, model performance, limitations and selected maize farming topics. The verified performance scores are written directly into the prepared answers to keep the implementation straightforward. If retraining changes those results, the answers must be updated manually. Keeping the content separate from the matching logic makes it easier to review the information and maintain the assistant’s boundaries.

### `Code/chatbot.py`

This script matches user questions to the topics defined in `chatbot_data.py`. It handles greetings, help requests and exact supported example questions directly. For other wording, TF-IDF converts the text into numerical features, and logistic regression predicts the most suitable topic. Probability, similarity and ambiguity checks determine whether the match is strong enough to return a prepared answer. Uncertain questions receive the fallback response, while recognisable questions containing different topics may prompt the user to ask one topic at a time. The assistant does not read performance CSV files, generate new explanations or calculate field predictions, and each question is handled independently.

### `Code/dashboard.py`

This script provides the Streamlit interface through which users interact with AgriPredict. It loads the validated dataset and saved regression model, accepts the seven field inputs and checks that submitted details are complete and within the individual ranges recorded in the fitting data. A supported submission produces a yield estimate in tonnes per hectare, which can be multiplied by a user-entered area to calculate a production scenario in tonnes. The dashboard also displays the annual mean-and-median chart and the text assistant. It clears the previous estimate after an invalid submission and explains when the dataset or model is unavailable. Passing input checks does not establish that an estimate will be reliable for a particular field.

### `requirements.txt`

This file lists the Python packages and pinned versions used by the project, including Streamlit, pandas, NumPy, scikit-learn, Matplotlib and Joblib. Installing these dependencies provides the tools needed for data preparation, modelling, visualisation and the dashboard. Using the specified versions helps reduce differences between development and assessment environments, particularly when loading the saved model. The project was tested using Python 3.12.

## Installation

The following instructions are for Windows PowerShell. Install **Python 3.12**, extract the project ZIP or download the repository, and open a terminal inside the project folder containing `Code`, `Dataset`, `Results` and `requirements.txt`.

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Install the required packages:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands use the virtual environment directly, so activating it is unnecessary. Internet access is needed for installation; the dashboard can then run locally using the supplied files.

## Running the dashboard

With the prepared dataset and trained model in place, run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Code/dashboard.py
```

Open the **Local URL** printed in the terminal, normally [http://localhost:8501](http://localhost:8501). Keep the terminal open while using the application and press **Ctrl+C** to stop it. For later sessions, run the same command; installation does not need to be repeated.

## Rebuilding the model and annual analysis

Run these commands in order from the project folder:

```powershell
.\.venv\Scripts\python.exe Code/prepare_dataset.py
.\.venv\Scripts\python.exe Code/preparation.py
.\.venv\Scripts\python.exe Code/yield_model.py
.\.venv\Scripts\python.exe Code/time_series.py
```

These commands reconstruct and validate the dataset, check preprocessing, train and evaluate regression, and generate the annual summary and chart. If the dashboard is already running, stop and restart it after rebuilding. Check the chatbot’s fixed performance answers against the recalculated results and update them if the scores change.

To reproduce the separate model comparisons, run:

```powershell
.\.venv\Scripts\python.exe Code/experiments.py
```

The experiment outputs are saved under `Results/Experiments`. Running this script does not change which model powers the dashboard.

## Using the application

Enter all required field details and select whether commercial hybrid seed was used, then press **Estimate yield**. Use comparable measurements rather than guessed values. After receiving an estimate, enter planted area in hectares to calculate a production scenario. Submit the form again after changing field details, because the displayed estimate uses the last submitted inputs.

The annual chart describes the sampled records, while the assistant explains supported project topics and fixed results. Neither feature guarantees future harvest outcomes. Scenario production is calculated as yield multiplied by area and must not be interpreted as expected cooperative deliveries.

## Evaluation and limitations

The prepared dataset contains 7,258 observations: 3,212 from 2016–2018, 1,755 from 2019 and 2,291 from 2020. Each soil input contains 188 missing values, handled through fitting-data median imputation. The 144 zero-yield records are retained.

| Approach | 2019 MAE | 2019 RMSE | 2020 MAE | 2020 RMSE |
| --- | ---: | ---: | ---: | ---: |
| Historical mean baseline | 1.483 | 1.905 | 1.206 | 1.540 |
| Linear regression | 1.277 | 1.626 | 1.258 | 1.653 |

All errors are in tonnes per hectare; lower values indicate smaller prediction errors. The historical baseline performs better on 2020 records. Linear regression was retained for simplicity and explainability after those results were known, so the model choice still requires evaluation on new data. The project does not establish improved real-world farming outcomes or reliable predictions outside the sampled conditions.

## Troubleshooting

If Python is not recognised, check that Python 3.12 is installed and reopen PowerShell. If a package is missing, repeat the dependency installation command using the virtual environment. If the dataset or saved model is unavailable, confirm that the project was fully extracted and run the rebuilding commands in order. If port 8501 is occupied, start the dashboard on another port:

```powershell
.\.venv\Scripts\python.exe -m streamlit run Code/dashboard.py --server.port 8502
```

## Verification

The updated code workflow was tested on Linux, including data reconstruction, model training, experiments, annual analysis and programmatic dashboard checks. The corrected chatbot matched all 180 supplied example questions and handled the unrelated and invalid inputs tested. Matching supplied examples is a regression check, not an independent chatbot accuracy estimate. The Windows commands still need to be verified on the assessment computer, and the dashboard’s visual layout needs a browser review.

## Dataset source

Aramburu Merlos, F., Tenorio, F.A., Mashingaidze, N., Sananka, A., Aston, S. and Grassini, P. (2024). *Maize management and yield of smallholder farmers in Sub-Saharan Africa between 2016 and 2022*. Version 2 [Dataset]. Zenodo. [https://doi.org/10.5281/zenodo.11122388](https://doi.org/10.5281/zenodo.11122388).
