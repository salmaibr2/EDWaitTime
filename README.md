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

