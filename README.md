# NJ Latino Mortgage Application Outcomes: Code and Data

*By [Jeremy Singer-Vine](https://www.jsvine.com/), on behalf of [Futuro Investigates](https://futuroinvestigates.org/).*

This repository contains code and data supporting [Futuro Investigates’ examination of mortgage application outcomes in New Jersey](https://futuroinvestigates.org/investigative-stories/the-mortgage-wall/here-is-how-we-analyzed-mortgage-outcomes-in-new-jersey-and-their-impact-among-latinos/), published December 11, 2023. Please the [detailed methodology document](https://docs.google.com/document/d/e/2PACX-1vSkEMZ_QjaYdJV4rSq9QPLMlFDvyctzjVuZ3kjBrRplPPWFNzWoB-asw9xdw3N_jJggRsqFeyGUXSHp/pub) for essential context.

## Repository structure

The diagram below indicates the key directories and files in this repository, and briefly describes their roles:

``` sh
.
├── Makefile
├── data
│   │   # ↓ All manually-compiled data
│   ├── manual
│   │   │   # ↓ Schema for helping to load data
│   │   ├── column-types.csv
│   │   │   # ↓ Simple translation from county code → name
│   │   ├── county-names.csv
│   │   │   # ↓ Translations of the variables used in the regressions
│   │   └── variable-translations.csv
│   │   # ↓ Data generated by the scripts/ Python files
│   ├── processed
│   │   ├── census
│   │   │   ├── county-demographics.csv
│   │   │   └── tract-demographics.csv
│   │   ├── institutions.csv
│   │   └── mortgage-records
│   │       ├── columns
│   │       ├── filtered
│   │       └── raw-samples
│   │   # ↓ Raw data, directly from the government
│   └── raw
│       │   # ↓ Census data on county/tract demographics
│       ├── census
│       │   # ↓ Lender metadata from HMDA Public Panel
│       ├── institutions
│       │   # ↓ Mortgage action data from HMDA LAR
│       └── mortgage-records
│   # ↓ The main analytic notebooks and helper code
├── notebooks
│   │   # ↓ Generates the descriptive statistics
│   ├── 00-descriptive-statistics.ipynb
│   │   # ↓ Runs the statistical regressions
│   ├── 01-regression.ipynb
│   │   # ↓ Shared, boilerplate, and helper code
│   └── utils
│       ├── expressions.py
│       ├── helpers.py
│       └── loaders.py
├── output
│   │   # ↓ Results logged from the notebooks above
│   └── logs
│       ├── descriptive.txt
│       ├── regression-odds-ratios.csv
│       └── regression.txt
│   # ↓ Python library requirements
├── requirements.in
├── requirements.txt
│   # ↓ Pre-analysis data-downloading and -processing scripts
└── scripts
    │   # ↓ Download the raw HMDA LAR data
    ├── 00-download-data.py
    │   # ↓ Generate data/processed/mortgage-records/{columns,raw-samples}/
    ├── 01-generate-data-samples.py
    │   # ↓ Filter down the HMDA LAR data, save to data/processed/mortgage-records/filtered/
    ├── 02-filter-mortgages.py
    │   # ↓ Generate data/processed/institutions.csv
    ├── 03-process-institutions.py
    │   # ↓ Generate data/processed/census/{county,tract}-demographics.csv
    ├── 04-process-census.py
    └── utils
        └── load.py
```

## Reproducing the results

Take the following steps to reproduce this repository's results:

1. Ensure that you have a modern version of Python installed *and* that you have at least 40 gigabytes of available storage.
2. Clone this repository and `cd` into it.
3. Run `make venv` to create a Python virtual environment with all of the necessary external libraries installed.
4. Run `source venv/bin/activate` to activate the virtual environment.
5. Run `make data` to download and process the raw data. (The HMDA datasets are too large to store locally.)
6. Run `make analysis` to run the notebooks that conduct the analyses; examine the outputs in `outputs/logs` and/or the rendered notebooks in the `notebooks/` directory.
    - Alternatively, run `jupyter lab`, navigate within Jupyter Lab to the `notebooks/` directory and run the two analysis notebooks interactively.

## Questions / feedback?

Please send inquiries to Jeremy Singer-Vine at `jsvine@gmail.com`.