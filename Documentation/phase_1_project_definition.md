##### AgriPredict AI: Phase 1 - Project Definition



###### 1.Project Background:



AgriPredict AI is a proposed Python-based decision-support system that will use artificial intelligence to predict seasonal maize yields across selected South African provinces. Its initial coverage will include Free State, Mpumalanga and North West,which the Crop Estimates Committee identified as the country’s three main maize-producing provinces in its March 2025 forecast. The system will combine historical maize yield records with suitable weather data to generate provincial yield estimates and display historical trends through an accessible dashboard. The system is intended for farming cooperative that needs regional information to support maize procurement and storage planning. The project addresses the assessment theme, “an AI Solution for Industries,” by applying machine learning to an agricultural business problem. Predictions will represent provincial averages and shouldn't be interpreted as expected yields for individual farms.







###### 2.Problem Definition:



The farming cooperative needs to plan maize procurement and storage before final harvest volumes are known. Uncertainty about provincial yields can make it difficult to anticipate supply and prepare appropriate procurement and storage arrangements. Historical production records and weather observations can inform these decisions, but converting them into consistent yield estimates requires data preparation and analytical skills.



This project addresses a proposed need for a prototype that combines relevant historical data, estimates provincial maize yields and presents the results clearly. The business case uses a farming cooperative; its needs have not yet been verified through stakeholder interviews.



AgriPredict AI will generate provincial yield estimates and present historical comparisons, model performance and limitations. These outputs are intended to support better-informed regional procurement and storage planning. The system will support human judgement and will not guarantee future harvest outcomes.







###### 3.Project Objectives:



3.1 Main Objective

To develop and evaluate a Python-based AI prototype that predicts seasonal maize yield, measured in tonnes per hectare, across selected South African provinces to support regional agricultural planning.



3.2 Specific Objectives

1\. Define and document a farming cooperative’s business requirements, using stakeholder feedback where available and clearly stated assumptions where it is unavailable.

2\. Assemble and validate historical maize yield records and suitable weather data.

3\. Analyse maize yield trends across the selected provinces and agricultural seasons.

4\. Develop suitable machine learning models and compare their predictions with a historical baseline.

5\. Evaluate prediction performance on later, unseen seasons using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

6\. Present predictions, historical comparisons and model limitations through an accessible dashboard.

7\. Incorporate a bounded text assistant and an experimental deep learning model relevant to the assessment requirements.



3.3 Business Success Criteria

The project will be considered successful when:

\* The prototype produces clearly labelled yield estimates for the selected provinces.

\* Users can compare provincial yields and complete a documented planning scenario.

\* Outputs state their units, prediction periods, assumptions and limitations.

\* Model evaluation establishes whether the AI models improve on the historical baseline.

\* Claims about business benefits are supported by stakeholder feedback or documented planning scenarios.





###### 4.Project Scope:



4.1 Included in Scope(must be in table form)

\*Crop = Maize, combining white and yellow maize where consistent records permit.

\*Geographic Coverage = Free State, Mpumalanga and North West, subject to dataset suitability.

\*Prediction Level = Provincial maize yield per agricultural season, expressed in tonnes per hectare.

\*Data = Historical maize yield records and suitable weather variables. Production and harvested-area records may be used to derive or validate yield.

\*Analysis = Historical trends, provincial comparisons and model evaluation.

\*AI Techniques = Regression models, a small experimental neural network and basic natural language intent classification.

\*Decision Support = Yield comparisons and production-volume scenarios based on explicitly stated area assumptions.

\*User Interface = A Python-based dashboard with a text assistant.

\*Project Management = GitHub for version control and GitHub Projects for tracking work.



4.2 Excluded in Scope 

\*Predictions for individual farms or fields.

\*Crops other than maize.

\*Guaranteed coverage of all nine provinces.

\*Drone, sensor or satellite-image integration.

\*Automated irrigation, fertiliser prescriptions or planting recommendations.

\*Crop-price forecasting and guaranteed financial returns.

\*Commercial deployment or development of a mobile application.



4.3 Initial Requirements

The system must allow users to select a province, view historical yield trends, generate a yield estimate where sufficient data are available, compare provincial results and inspect model performance.



It must validate inputs, use consistent units, document data sources and support reproducible data processing. The text assistant must respond to a limited range of questions using approved project information and available results.





4.4 Constraints and Risks



4.4.1 Limited historical observations:

\*Issue = The dataset may contain relatively few records, even if it covers several provinces and seasons. Records from the same season may also share similar conditions.

\*Planned response = We will assess the available data before choosing models, starting with a historical baseline and simpler approaches. The experimental neural network will be evaluated cautiously, and any limits on prediction reliability will be reported.



4.4.2 Missing or inconsistent data:

\*Issue = data	Historical records may contain gaps, duplicates or differences in units and season labels. Confusing planted area with harvested area could also lead to incorrect yield calculations.

\*Planned response = We will check and standardise the records, preserve the original data and document cleaning decisions. Where missing values require estimation, the method will use training data only.



4.4.3 Misaligned weather records and agricultural seasons:

\*Issue = Weather records usually follow calendar dates, while a maize season may span two years. Assigning weather to the wrong season could produce misleading relationships.

\*Planned response = We will define the weather period for each season and include only observations available by the prediction cutoff. Any limitations of provincial weather averages will be explained.



4.4.4 Data leakage:

\*Issue = this occurs when information that would not be available at the intended prediction time influences model training/evaluation, making the model appear accurate in training but giving unrealistic results in actual use.

\*Planned response = We will set a prediction cutoff and check when each input became available. Earlier seasons will be used for training and later seasons for evaluation, keeping all provinces from the same season together. Data preparation and tuning will exclude the final test period.                                                 



4.4.5 Overfitting:

\*Issue = With limited data, a complex model may perform well on historical training records but produce large errors for a new season, particularly when conditions differ from those previously observed.\*Planned response = We will keep the number of predictors and model complexity manageable, compare training and validation errors, and evaluate each model against the baseline. More complex models will be selected only when the results support their use.



4.4.6 Misinterpretation of provincial estimates

\*Issue = Users may mistake provincial averages for farm-level predictions or confuse yield with total production.

\*Planned response = Outputs will clearly identify the province, season and units. Production scenarios will state their area assumptions, while historical prediction errors and explanations will communicate limitations.



4.4.7 Unverified business assumptions

\*Issue = Without the stakeholders' input, the project cannot establish the cooperative’s actual workflow, preferred prediction timing, acceptable error level or information requirements. There is a risk of developing a technically functional prototype that does not adequately support the intended business decision.

\*Planned response = We will record these assumptions and seek relevant stakeholder feedback where possible. If feedback is unavailable, documented scenarios will demonstrate how the prototype could be used without claiming proven business benefits.





4.5 Initial Tools and Techniques(must be in table form)

\*Python, pandas and NumPy = Prepare, validate and analyse data.

\*Historical baseline, linear regression and random forest regression = Compare prediction approaches. 

\*Chronological evaluation, MAE and RMSE = Measure prediction error on unseen seasons

\*Historical trend analysis and suitable lagged features = Examine changes over time and support prediction.

\*Small feed-forward neural network = Evaluate an experimental deep learning approach.

\*Natural language intent classification = Interpret a limited range of user questions.

\*Bounded text assistant = Explain project concepts and retrieve available results.

\*Streamlit = Present the prototype dashboard.

\*GitHub and GitHub Projects = Maintain version history and track project tasks.







###### 5\. Expected Business Benefits:



\*Better-informed procurement planning = Provincial yield estimates may help a cooperative compare expected maize supply across sourcing regions. This information can support decisions about where to source maize and how to adjust procurement plans when lower yields are anticipated.



\*Improved storage planning = Yield estimates can be combined with clearly stated harvested-area assumptions to explore possible production volumes. These scenarios may help a cooperative assess storage needs and prepare for changes in maize deliveries.



\*Reduced manual analysis = A single dashboard can bring together historical trends, yield predictions and provincial comparisons. This may reduce the time users spend combining separate records and make routine analysis easier.



\*Greater visibility of regional variation = Provincial comparisons can show how maize yields differ across regions and seasons. Understanding these differences may help a cooperative identify potential supply pressures and consider alternative sourcing regions.



\*More transparent decision support = The system will present model performance, assumptions and limitations alongside its predictions. This can help users judge how much confidence to place in the results and when additional information is needed.






