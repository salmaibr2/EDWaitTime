# ED Wait Time — Bottleneck Analysis Project

Identifies operational bottlenecks (boarding, observation units, bed management, fast-track)
that drive emergency department wait times, using nationally representative CDC NHAMCS data
with PATWT survey weights applied throughout.

## Project goal

Individual ED wait time prediction is not achievable from retrospective survey data — there
is no real-time operational context (current census, bed occupancy, staffing) in NHAMCS.
Instead this project quantifies which operational conditions add the most minutes at the
national population level, so hospitals can prioritize interventions with the highest payoff.

## Setup

**1. Clone the repo**

**2. Download NHAMCS ED SAS files** (years 2015–2018, 2021, 2022) and place them in `data/`:
```
data/ed2015-sas.sas7bdat
data/ed2016_sas.sas7bdat
data/ed2017_sas.sas7bdat
data/ed2018_sas.sas7bdat
data/ed2021_sas.sas7bdat
data/ed2022_sas.sas7bdat
```
Download zips from: https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/sas/
Note: 2019 and 2020 files are not publicly available.

**3. Download the NHAMCS ED documentation PDF** and place it at `data/doc21-ed-508.pdf`

**4. Install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Notebook pipeline

Run in order — each notebook reads from `data/` and writes outputs back to `data/` and `appengine/assets/`.

| Notebook | Input | Output |
|---|---|---|
| `01_data_prep.ipynb` | Raw SAS files | `eda_df.csv`, `model_A_arrival_dataset.csv`, `model_B_retrospective_dataset.csv` |
| `02_weighted_eda.ipynb` | `eda_df.csv` | EDA plots in `appengine/assets/` |
| `03_bottleneck_analysis.ipynb` | `model_B_retrospective_dataset.csv` | `bottleneck_*.csv`, bottleneck plots in `appengine/assets/` |
| `04_modeling.ipynb` | `model_A_arrival_dataset.csv` | `model_eval_summary_v3.csv`, model plots in `appengine/assets/` |

### Key design decisions
- **PATWT required throughout**: every NHAMCS record represents thousands of national visits.
  Unweighted statistics over-represent large urban hospitals. All EDA means, model training
  (`sample_weight`), and evaluation metrics use PATWT.
- **Sentinel cleaning in one place**: `01_data_prep` defines the authoritative `sentinel_map`
  for all 29 columns. Downstream notebooks must not repeat this cleaning.
- **Temporal train/test split**: train 2015–2018, validation 2021, holdout 2022.
- **SETTYPE excluded**: 100% of records are SETTYPE=3 (General ED) — zero variance.

## Dashboard (Dash app)

The app lives in `appengine/`. It has three pages: Home, Analytics, and Methods.

**Run locally:**
```bash
cd appengine
pip install -r requirements.txt
python app4.py
```
Then open http://localhost:8050

**Deploy to Google Cloud App Engine:**
```bash
cd appengine
gcloud app deploy
```

## Data notes

- `data/` is in `.gitignore` — SAS files are too large for GitHub.
- After running `01_data_prep`, the cleaned dataset is 91,811 rows × 38 columns.
- PATWT range 40–57,926; the 91,811 records represent ~728M weighted national ED visits.
- WAITTIME is filtered to 0–480 minutes. Sentinel values are set to NaN, not dropped.

## Key results

| Bottleneck | Weighted delta (min) | SHAP rank |
|---|---|---|
| Inpatient boarding (BOARD) | +7.7 | 4th |
| Bed czar program (BEDCZAR) | +6.8 | 3rd |
| Observation unit (OBSCLIN) | +5.0 | 2nd |
| Fast-track pathway (FASTTRAK) | −3.1 | 1st (protective) |

Classifier (wait > 30 min, 2022 holdout): AUC-ROC 0.581, Avg Precision 0.376
