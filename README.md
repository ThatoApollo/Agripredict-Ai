# AgriPredict AI

AgriPredict AI is a Diploma in Information Technology capstone project investigating provincial maize yield prediction in Free State, Mpumalanga and North West. It is intended to help a farming cooperative explore procurement and storage planning scenarios.

Predictions will represent provincial commercial maize yields, not individual farms. Business requirements and forecast timing are project assumptions unless confirmed by stakeholders.

## Current progress

- Phase 1: project definition documented.
- Phase 2: dataset compiled, checked and explored using training data.
- Data preparation and shared settings implemented and checked.
- Model training, performance evaluation, text assistant and dashboard still to be implemented.

The final dataset has 72 records: three provinces across 24 seasons, 2000/01–2023/24. It combines crop yield with sampled rainfall and temperature data. The initial weather inputs are October–December rainfall, January rainfall and October–January mean temperature. The provisional prediction date is 15 February, using weather ending on 31 January.

## Files

| Location | Contents |
| --- | --- |
| `Code/` | Runnable preparation script and shared settings |
| `Dataset/` | Final project CSV and a plain-text description |
| `Documentation/` | Project definition, assessment brief and Phase 2 notes |
| `Reference/Prototype/` | Original Markdown code exports and example screenshots; reference material, not runnable project code |
| `AGENTS.md` | Instructions for keeping future work within the agreed scope |

## Run the completed preparation step

Use Python 3.11 or newer. From the repository root, create a virtual environment and install the current dependencies:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Then run:

```bash
python -m pip install -r requirements.txt
python Code/preparation.py
```

Expected record counts:

```text
Prepared records: 72
Training rows: 48
Validation rows: 12
Testing rows: 12
```

The script also prints the five numeric model inputs: three weather variables and two province indicator columns. Free State is the reference category. Yield values are retained at their original precision and exposed under the prototype's `yield_t_per_ha` target name. Units are tonnes per planted hectare. The input CSV is not changed by preparation.

Only pandas and NumPy are needed for the completed code. Add scikit-learn, joblib and Streamlit when their model and interface modules are implemented, following the prototype's stack.

## Evaluation plan

| Role | Seasons | Rows |
| --- | --- | ---: |
| Training | 2000/01–2015/16 | 48 |
| Validation | 2016/17–2019/20 | 12 |
| Final test | 2020/21–2023/24 | 12 |

All provinces from a season stay together. Final test values have not been plotted, predicted or scored during the completed analysis. Keep them out of tuning. Compare models with a training-only province-average baseline using MAE and RMSE in tonnes per planted hectare.

## Limitations

Seventy-two records are a small sample, and provinces can share seasonal conditions. Weather is an equal-weight proxy from three locations per province rather than an area-weighted provincial measurement. Historical data-release versions have not been verified, so this is a retrospective experiment. Dataset selection and preparation do not establish forecast accuracy or proven business benefits.

See `Dataset/Dataset_Description.txt` and `Documentation/phase_2_data_summary.md` for sources and preparation decisions.

## Next work

Adapt the prototype's yield model to implement the historical baseline, linear regression and a constrained random forest. Later work includes time-series analysis, a small experimental neural network, a bounded intent-based assistant, a Streamlit dashboard and the remaining submission materials. Do not present the example results in the reference screenshots as measured project performance.
