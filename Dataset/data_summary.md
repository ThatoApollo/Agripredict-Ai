# Phase 2: data acquisition and preparation

The final dataset contains 72 province-season records for Free State, Mpumalanga and North West over 2000/01–2023/24. Each record represents commercial maize, combining white and yellow maize. Yield is production in tonnes divided by planted area in hectares.

Crop figures came from Grain SA's CEC provincial compilation. Relevant CEC reports were checked when totals differed. The 2011/12 records in the first extraction were replaced with revised figures; later final crop publications also supplied updated 2021/22 and 2022/23 values. Some national summary differences were consistent with rounding or concerned provinces outside our scope. Provincial values were not scaled to force agreement with national totals. Not every historical figure was independently checked against a second publication.

NASA POWER supplied daily rainfall and temperature at nine fixed sample locations, three per province. Daily values were averaged equally within each province, then summarised over 1 October–31 January. The three initial weather predictors are October–December rainfall (mm), January rainfall (mm) and October–January mean temperature (degrees Celsius). This supports a provisional 15 February prediction scenario.

Checks covered missing values, duplicate province-season keys, units, crop arithmetic, weather completeness and the final join. All 72 rows have the required values; no missing values were imputed. The selected weather windows contain 26,568 point-day records. The retained sampling metadata records the points, request URLs, source units and source file hashes.

`Code/preparation.py` loads the final CSV, checks required fields, sorts records by province/year, keeps the original province labels and adds two numeric province indicator columns. It exposes the existing yield under the prototype's target name. It does not recalculate yield from unavailable production fields, round training targets or add an unverified previous-yield feature.

## Chronological evaluation

| Role | Seasons | Rows |
| --- | --- | ---: |
| Training | 2000/01–2015/16 | 48 |
| Validation | 2016/17–2019/20 | 12 |
| Final test | 2020/21–2023/24 | 12 |

Keep all provinces from a season together. Initial exploration used the training partition only. Four expanding training folds are available for tuning: validate on 2012/13, 2013/14, 2014/15 and 2015/16, using only earlier seasons in each case. Fit any scaler or other learned preprocessing on the permitted training portion.

Mean training yield was 3.728 t/ha in Free State, 4.811 in Mpumalanga and 2.980 in North West. January rainfall had a moderate positive correlation with yield within each province (approximately 0.53–0.61). Pooled temperature correlations were much weaker within individual provinces, suggesting geographic differences partly explain that association. Correlation is not evidence of causation or future predictive performance. Four unusual weather values were retained because they did not establish data errors. No final test charts, predictions or scores were produced.

The next modelling step compares a province-specific historical mean baseline with simple regression models. After training-only tuning and validation comparison, freeze the choices, refit on the first 20 seasons and evaluate once on the final four. Do not tune using final test outcomes.

## Limits

This is a small retrospective experiment. Weather sampling is not crop-area-weighted and may miss local conditions. Exact historical publication versions were not verified. The 15-day gap between the weather cutoff and forecast date does not prove historical data availability. Later-season weather can strongly affect yield but is intentionally excluded. Results must be presented as experimental provincial estimates, not dependable farm forecasts or verified cooperative benefits.

## Sources

- Grain SA crop estimates: https://grainsa.co.za/applied-economics/crop-estimates/
- Provincial compilation: https://grainsa.co.za/wp-content/uploads/2025/11/NOK-Wit-geelmielies-white-and-yellow-maize-per-provinsie-1.xlsx
- CEC archive: https://www.sagis.org.za/crop-estimates-committee-2/
- NASA POWER daily service: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- NASA meteorology methodology: https://power.larc.nasa.gov/docs/methodology/meteorology/

`weather_sampling_points.csv` and `crop_source_checks.csv` retain supporting provenance. The full raw-data and acquisition archive is retained separately from this starter repository.
