# Time Series Analysis

This analysis examines maize yields for the three provinces from 2000/01 to 2019/20. It uses 60 training and validation records across 20 seasons. The final test seasons, 2020/21–2023/24, are excluded.

## Historical Patterns

| Province | Average yield | Lowest yield (season) | Highest yield (season) |
| --- | --- | --- | --- |
| Free State | 4.05 | 2.76 (2000/01) | 6.35 (2016/17) |
| Mpumalanga | 5.09 | 3.10 (2000/01) | 7.00 (2016/17) |
| North West | 3.27 | 1.81 (2006/07) | 5.02 (2016/17) |

All yields are in tonnes per planted hectare.

The three-season moving average smooths short-term changes to make the longer-term pattern easier to see. Each average includes the current season and the previous two seasons, so it is a description of observed yields rather than a forecast.

- Free State: the average was 2.92 t/ha in the first three seasons (2000/01–2002/03), compared with 5.03 t/ha in the last three (2017/18–2019/20).
- Mpumalanga: the average was 3.43 t/ha in the first three seasons (2000/01–2002/03), compared with 5.96 t/ha in the last three (2017/18–2019/20).
- North West: the average was 2.41 t/ha in the first three seasons (2000/01–2002/03), compared with 4.21 t/ha in the last three (2017/18–2019/20).

## What This Means

Yields fluctuate between seasons. Comparing early and later averages helps describe change, but does not establish a steady trend or explain its causes. These patterns support considering time-related features in later modelling; they do not prove those features will improve predictions.

The records are annual, with one observation per province per season. They cannot show monthly planting or growing-season patterns. Provincial averages also hide differences between individual farms.

No new prediction model was fitted in this task, and the earlier model scores remain unchanged. Future model development needs a separate chronological evaluation plan because the original test results have already been inspected.

## Run the Analysis

From the repository root:

```bash
python -m pip install matplotlib
python Code/time_series.py
```

The script creates the chart in `Documentation/Figures/` and the summary and season-by-season values in `Results/`.
