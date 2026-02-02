# ED Wait Time Project

Starter structure for exploratory data analysis (EDA) and predictive modeling of ED wait times, plus a simple website to present the project.

## Suggested workflow
1. Keep raw data files in `data/`.
2. Use notebooks in `notebooks/` for exploration.
3. Put reusable code in `src/`.
4. Save models to `models/` and figures/reports to `reports/`.
5. Put presentation assets in `website/`.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run example training pipeline
```bash
python -m src.train --input data/ed2022_sas.sas7bdat --target TARGET_COLUMN
```

Replace `TARGET_COLUMN` with the column you want to predict.
