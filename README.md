# AgriPredict AI (Kenya)

## 1. Project Background

AgriPredict AI is a Python-based prototype that uses machine learning to estimate maize yield and support harvest-planning scenarios. It uses 7,258 Kenyan field observations from the One Acre Fund maize survey dataset, covering 2016–2020. The selected inputs are location, elevation, soil characteristics and hybrid seed status. The intended users are maize farmers and agricultural advisers who have suitable field information and need clear estimates to explore possible harvest sizes. A Streamlit dashboard presents yield estimates, annual yield patterns, a production calculator and a chatbot that explains the project and saved model results. The project follows the assessment theme, “an AI Solution for Industries,” by applying AI to planning within the agricultural sector.

## 2. Problem Definition

Maize farmers must plan for harvesting, storage and transport before knowing how much their fields will produce. Yield can vary with soil conditions, weather and farming practices, making it difficult to estimate the resources needed for agriculture. Historical field records can support planning, but analysing many observations requires time and technical skills.

AgriPredict AI investigates whether machine learning can provide useful maize yield estimates using Kenyan field records. It uses location, elevation, soil characteristics and hybrid seed information to produce an experimental estimate in tonnes per hectare. The dashboard also displays annual mean and median yields and calculates a production scenario using the estimated yield and a user-entered planted area. A text assistant explains supported project topics and saved evaluation results.

These features are intended to support procurement and storage planning, helping users source enough maize to meet demand and arrange sufficient storage to reduce the risk of shortages, overcrowding and post-harvest losses. The system supports human judgement and does not guarantee future harvest outcomes.

## 3. Project Objectives

### 3.1 Main Objective

To develop and evaluate a Python-based AI prototype that estimates maize yield from Kenyan field observations and presents the results clearly to support agricultural planning.

### 3.2 Specific Objectives

1. Define the proposed users, planning needs and system requirements, while identifying assumptions that require stakeholder feedback.
2. Prepare and validate the Kenyan maize records from 2016–2020, documenting their source, units, missing values and preparation steps.
3. Describe annual yield patterns using a line chart showing mean and median yields.
4. Develop a suitable machine learning model using location, elevation, soil characteristics and hybrid seed status.
5. Evaluate performance using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE), and explain the limitations of the results.
6. Present yield estimates, production scenarios, annual patterns and relevant limitations through a clear dashboard.
7. Include a chatbot that explains the platform, saved model results and selected maize farming topics.

### 3.3 Business Success Criteria

The prototype should:

- Accept complete field inputs and display yield estimates in tonnes per hectare.
- Reject incomplete entries and values outside the individual input ranges recorded in the data used to fit the model.
- Display one annual chart explaining the mean, median and purpose of the comparison.
- Calculate scenario production in tonnes by multiplying yield in tonnes per hectare by planted area in hectares.
- Make saved model errors available through the assistant and explain what the numbers describe.
- Answer supported questions and provide a clear response when a question cannot be matched confidently.
- Explain the assumptions and limitations users need to interpret the outputs.

These criteria assess whether the prototype provides its intended functions. Demonstrating an improvement in real farming decisions would require stakeholder feedback and practical evaluation.

## 4. Project Scope

### 4.1 Included in Scope

| Scope item | Description |
|---|---|
| Crop and coverage | Maize observations from the Kenyan locations represented in the selected dataset. |
| Study period | First-growing-season observations from 2016–2020. |
| Prediction output | An experimental yield estimate in tonnes per hectare. |
| Prediction inputs | Latitude, longitude, elevation, soil clay percentage, soil pH, soil organic carbon and commercial hybrid seed status. |
| Data preparation | Selection of Kenyan records, source-row references, unit conversion, validation and year-based data splits. |
| Yield model | Linear regression compared with a historical mean baseline. |
| Annual analysis | One line chart showing annual mean and median recorded yields. |
| Decision support | A production scenario calculated from estimated yield and user-entered planted area. |
| Interface | A Streamlit dashboard containing field inputs, estimates, annual analysis, a production calculator and a text assistant. |
| Text assistant | Prepared project information, saved performance results and selected maize farming topics. |
| Project management | GitHub for version control and GitHub Projects for task tracking, as required by the assessment. |

### 4.2 Excluded from Scope

- Crops other than maize.
- Live weather forecasts, crop-price forecasts and guaranteed harvest outcomes.
- Drone, sensor and satellite-image integration.
- Field-specific fertiliser or pesticide prescriptions, crop diagnosis and automated farm control.
- Predictions of cooperative deliveries or guaranteed financial returns.
- Tracking the same identified farm across several years.
- Forecasting future annual yields.

### 4.3 Initial Requirements

The system must allow users to enter location, elevation, soil characteristics and hybrid seed information to generate a maize yield estimate. It must display annual mean and median yield patterns, calculate a production scenario using the estimated yield and planted area, and make saved model performance results available through the text assistant.

It must validate inputs, display yield in tonnes per hectare and production in tonnes, document data sources and support reproducible data preparation. The text assistant must answer supported questions about the platform, model results and selected maize farming topics using prepared answers and saved results. It must explain when it cannot answer a question and must not invent prediction results or diagnose crop problems from a description.

### 4.4 Constraints and Risks

#### 4.4.1 Limited implementation time

**Issue:** The submission deadline limited the time available to develop, test and improve the prototype. This required compromises in the range of features included and the level of refinement possible.

**Response:** We prioritised the main functions: yield estimation, annual analysis, the production calculator and the text assistant. Further improvements should be recorded as future work, while the included features must be tested and their limitations explained clearly.

#### 4.4.2 Missing or inconsistent data

**Issue:** Missing or inconsistent values can affect data preparation and modelling. However, an unusual yield is not automatically an error, and removing zero yields could exclude genuine poor harvest outcomes.

**Response:** The original data will be preserved, and cleaning decisions will be documented. Zero yields will be retained unless there is evidence that they are invalid. Where missing inputs require imputation, replacement values will be learned from the fitting data within the model pipeline.

**Verification needed:** Confirm whether the final selected input columns contain missing values. The original draft states that soil values are missing, but this needs supporting evidence from the final dataset checks.

#### 4.4.3 Availability of field information

**Issue:** Users may not know their soil measurements or may have measurements collected differently from those in the dataset. The model also does not include the coming season’s weather.

**Response:** The dashboard will require complete field information and advise users against guessing. Outputs will be presented as experimental estimates whose usefulness depends on suitable inputs and model performance. It will also clarify on the format for typing the inputs.

#### 4.4.4 Overfitting and limited predictive value

**Issue:** A model may perform well on historical training records but produce large errors for a new season, particularly when conditions differ from those previously observed.


**Response:** We will keep model complexity manageable, compare training and validation errors, and assess performance against the historical mean baseline. Other algorithms will be used only when validation results show a clear improvement.

**Verification needed:** Support the comparison with the final calculated MAE and RMSE results.

#### 4.4.5 Misinterpretation of estimates

**Issue:** Users may confuse yield per hectare with total production or treat a production scenario as a guaranteed harvest. Passing input range checks may also be mistaken for evidence that a prediction is reliable.

**Response:** The dashboard will distinguish yield estimates from calculated production and display their units clearly. The documentation will explain that range checks identify certain input problems but do not establish prediction accuracy.

#### 4.4.6 Difficulty finding suitable data

**Issue:** Finding a dataset with recent maize yield records and relevant inputs was challenging. Detailed weather information was not available among the selected inputs, limiting the factors the model could consider. 

**Response:** We focused on the available location, elevation, soil and hybrid seed information. Future work should investigate recent observations and weather data that can be matched to the field locations and growing seasons, then test whether it improves performance.

#### 4.4.7 Limited group capacity

**Issue:** The small number of group members made it difficult to divide tasks evenly while managing development, testing and documentation. This placed pressure on the available time and workload.

**Response:** Tasks should be divided according to each member’s availability and strengths, with clear responsibilities and manageable deadlines. GitHub Projects can help track progress, identify delays and support adjustments to the workload.

### 4.5 Tools and Techniques

| Tool or technique | Purpose |
|---|---|
| Python, pandas and NumPy | Prepare and validate data, calculate summaries and handle numerical inputs. |
| Matplotlib | Produce the annual mean and median yield chart. |
| Scikit-learn linear regression | Estimate maize yield from the seven selected inputs. |
| Historical mean baseline | Provide a simple reference for evaluating model performance. |
| Standardisation | Place numerical inputs on a comparable scale within the fitted pipeline. |
| Chronological evaluation, MAE and RMSE | Measure prediction error on unseen seasons. |
| TF-IDF and logistic regression | Convert questions into numerical text features and classify them into supported assistant topics. |
| Natural language intent classification | Match user questions to supported platform and maize farming topics. |
| Bounded text assistant | Provide predefined answers about the platform and general maize farming, while explaining its limitations. |
| Joblib | Save and load the fitted yield pipeline and model metadata. |
| Streamlit | Present field inputs, predictions, annual analysis, production scenarios and the assistant. |
| GitHub and GitHub Projects | Maintain version history and track project tasks. |


## 5. Expected Business Benefits

**Support for harvest planning:** Yield estimates may help farmers and agricultural advisers discuss possible harvest sizes and related labour, storage and transport needs. Their usefulness depends on reliable predictions and suitable field information.

**Clearer production scenarios:** Multiplying estimated yield by a stated planted area makes the calculation easy to follow. It also helps users distinguish yield per hectare from total production.

**Easier access to historical information:** The annual chart summarises mean and median yields in the sampled records, giving users a clear view of how recorded yields differ between years.

**Accessible explanations:** The assistant explains project inputs, units, model errors and selected maize topics. It also explains its abilities and limits.

**Transparent model evaluation:** Comparing regression errors with the historical baseline helps show whether the model adds predictive value. Improvements in prediction accuracy and business outcomes must be demonstrated rather than assumed.

## 5. Expected Business Benefits

**1. Aramburu Merlos, F., Tenorio, F.A., Mashingaidze, N., Sananka, A., Aston, S. and Grassini, P. (2024).** Maize management and yield of smallholder farmers in Sub-Saharan Africa between 2016 and 2022. Version 2 [Dataset]. Zenodo. Available at: https://doi.org/10.5281/zenodo.11122388.

**2. Tutorials Point (I) Pvt. Ltd. (2016).** AI with Python. Available at: AI with Python tutorial.

**3. Farm Africa (2025).** Maize production training manual. Available at: Maize production training manual.

**4. Bouagnimbeck, H. and Ssebunya, B. (2011).** African Organic Agriculture Training Manual: Module 09—Crops, Unit 2—Maize. Draft version 1.0. Research Institute of Organic Agriculture (FiBL). Available at: Maize training manual.

**5. Shepherd, A.W. (1999).** A guide to maize marketing for extension officers. Marketing Extension Guide 1. Rome: Food and Agriculture Organization of the United Nations. Available at: A guide to maize marketing.

**6. The pandas development team (n.d.).** pandas documentation.

**7. NumPy developers (n.d.).** NumPy documentation.

**8. Matplotlib development team (n.d.).** Matplotlib documentation.

**9. Streamlit (n.d.).** Streamlit documentation.

**10. Joblib developers (n.d.).** Joblib documentation.

**11. Scikit-learn developers (n.d.).** Preprocessing data.

**12. Scikit-learn developers (n.d.).** Imputation of missing values.

**13. Scikit-learn developers (n.d.).** Feature extraction.

**14. Scikit-learn developers (n.d.).** Metrics and scoring: quantifying the quality of predictions.

**15. Scikit-learn developers (n.d.).** Common pitfalls and recommended practices.

**16. Scikit-learn developers (n.d.).** Linear models.
