# ED Wait Time Project

## Setup
1. Clone the repo.
2. Create the data directory at the project root:
	- `mkdir -p data`
3. Download the NHAMCS ED SAS dataset and place it in the data folder as:
	- `data/ed2022_sas.sas7bdat`
4. (Optional for EDA step) Download the NHAMCS ED documentation PDF and place it in the data folder as:
	- `data/doc21-ed-508.pdf`

## Data Notes
- The notebook expects the SAS file to be located at `data/ed2022_sas.sas7bdat`.
- If you use a different year or filename, update the path in the notebook accordingly.
