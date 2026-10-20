# Data Acquisition and Preparation:

## Dataset overview:

The final dataset contains 72 records covering Free State, Mpumalanga and North West across 24 seasons, from 2000/01 to 2023/24. Each record represents one province in one season and combines commercial white and yellow maize. Yield is calculated by dividing production in tonnes by planted area in hectares.

Crop data came from Grain SA’s compilation of Crop Estimates Committee (CEC) figures. Relevant CEC reports were used to investigate differences in totals. Revised figures replaced the initial 2011/12 records, while later final publications provided updated values for 2021/22 and 2022/23.

Some differences in national totals appeared to result from rounding or figures for provinces outside the project’s scope. Provincial values were kept as published rather than adjusted to match national totals. Not every historical figure was checked against a second source.


## Weather data:

Daily rainfall and temperature data came from NASA POWER using nine fixed sampling locations, with three in each province. The three locations were given equal weight when calculating daily provincial averages.

Weather data covered 1 October to 31 January for each season. Three weather features were selected:
* October–December rainfall, measured in millimetres.
* January rainfall, measured in millimetres.
* October–January average temperature, measured in degrees Celsius.

These features support an experimental prediction date of 15 February. However, this does not confirm that all historical weather data would have been available by that date.


## Data checks and preparation:

Checks covered missing values, duplicate province-season records, units, yield calculations, weather coverage and the merging of crop and weather data. All 72 records contain the required values, so no missing values needed to be filled.

The selected weather periods contain 26,568 daily observations across the sampling locations. Supporting records retain the sampling coordinates, request URLs, original units and file hashes used to identify source files.

The script Code/preparation.py loads the final CSV, checks the required columns and sorts records by province and year. It keeps the province names and adds two numeric columns to represent province membership. It also makes the existing yield column available under the target name expected by the prototype.

The script preserves the original yield values. It does not round them, recalculate them without the required production data or add an unverified previous-season yield feature.


## Model Evaluation Plan:

 The dataset is divided chronologically so that models learn from earlier seasons and are evaluated on later ones.
 
| Role | Seasons | Rows |
| --- | --- | ---: |
| Training | 2000/01–2015/16 | 48 |
| Validation | 2016/17–2019/20 | 12 |
| Final test | 2020/21–2023/24 | 12 |

All three provinces from the same season remain in the same partition. Initial data exploration used only the training data.

Model tuning can use four expanding training folds, with 2012/13, 2013/14, 2014/15 and 2015/16 each serving as a validation season. Each fold uses only earlier seasons for training. Any scaling or other preprocessing that learns from data must also be fitted using that fold’s training data.


## Initial findings:

Average yield in the training data was 3.728 t/ha for Free State, 4.811 t/ha for Mpumalanga and 2.980 t/ha for North West.

January rainfall showed a moderate positive correlation with yield within each province, ranging from approximately 0.53 to 0.61. The temperature relationship was much weaker when provinces were examined separately, suggesting that geographic differences partly explain the association seen in the combined data.

These correlations do not establish cause and effect or guarantee useful predictions. Four unusual weather values were retained because there was insufficient evidence that they were errors. No charts, predictions or scores were produced using the final test data.

The next step is to compare simple regression models with a baseline that predicts each province’s historical average yield. After tuning on the training data and comparing results on the validation data, the model choices will be fixed. The selected approach will then be refitted using the first 20 seasons and evaluated once on the final four seasons.


## Limitations
This is a small experiment using historical data. The weather sampling locations may not capture conditions across all maize-growing areas, and each location receives equal weight regardless of the surrounding crop area.

The exact historical versions of source publications were not verified. The gap between the weather cutoff and the proposed prediction date also does not establish when the data became available. Weather after January can strongly affect yield, but it is excluded from this prediction scenario.

Results should therefore be presented as experimental provincial yield estimates. They do not establish reliable farm-level forecasts or proven benefits for agricultural cooperatives.


## Sources and supporting files:
- Grain SA crop estimates
- Provincial maize compilation
- CEC archive
- NASA POWER daily service
- NASA meteorology methodology

