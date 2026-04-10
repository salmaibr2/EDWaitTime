# ED Wait Time Project

## Setup
1. Clone the repo.
2. Create the data directory at the project root:
	- `mkdir -p data`
3. Download the NHAMCS ED SAS dataset from years 2015-2018 an 2021-2022(not including peak covid years to avoid bias)and place it in the data folder. dowlowd the zips from https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHAMCS/sas/
4. (Needed for EDA step) Download the NHAMCS ED documentation PDF and place it in the data folder as:
	- `data/doc21-ed-508.pdf`

## Data Notes
- The notebook expects the SAS file to be located at `data/`.
- The data folder is in .gitignore to avoid taking up too much space on github.

## Notebook Workflow
The original single notebook has been split into focused notebooks:

1. `notebooks/01_data_prep.ipynb`
- Load and combine SAS files.
- Core cleaning and time conversion.
- Save `data/eda_df.csv`, `data/model_A_arrival_dataset.csv`, and `data/model_B_retrospective_dataset.csv`.

2. `notebooks/02_eda_core.ipynb`
- Core descriptive EDA and plots.
- Missingness and grouped summaries.

3. `notebooks/03_modeling_arrival_only.ipynb`
- Arrival-time prediction workflow (baseline + residual + segmented models).

4. `notebooks/04_modeling_retrospective.ipynb`
- Retrospective modeling using post-arrival features.

5. `notebooks/99_report_figures.ipynb`
- Final comparison tables/plots from saved model artifacts.

6. `notebooks/05_presentation_visuals.ipynb`
- Presentation-ready visuals and concise model comparison charts.

Recommended run order: `01 -> 02 -> 03 -> 04 -> 05 -> 99`.

