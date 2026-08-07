\# Danish Housing Price Forecasting



A forecasting model for Danish residential property prices using public data from Statistics Denmark.
And a project for personal development and learning



\## Motivation



Denmark's housing market is a macroeconomically significant system driven by interest rates, unemployment, demographics, and supply constraints. This project builds an end-to-end forecasting pipeline — from raw API data to validated predictions with uncertainty bounds.



\## Project structure



```

danish-housing-forecast/

├── data/

│   ├── raw/          # Data as downloaded from DST API

│   └── processed/    # Cleaned, merged, feature-engineered data

├── notebooks/

├── src/

│   ├── collect\_data.py       # API data collection

│   ├── explore\_tables.py     # Helper: explore DST table metadata

├── app/

│   └── streamlit\_app.py      # Interactive dashboard

├── requirements.txt

└── README.md

```



\## Data sources



All data from \[Statistics Denmark (Statistikbanken)](https://www.statistikbanken.dk/) — free, open, publicly available.



| Table   | Description                          | Frequency |

|---------|--------------------------------------|-----------|

| EJ121   | House price index (seasonally adj.)  | Quarterly |

| DNRNURI | Mortgage interest rates              | Quarterly |

| AUP01   | Unemployment rate                    | Quarterly |

| FOLK1A  | Population by region                 | Quarterly |

| BYG5    | Building permits issued              | Quarterly |



\## Stages and status

1. Data collection and exploration

   1. Data collection [completed]
   2. Data exploration [completed]
   3. Data cleaning and feature engineering

2. Modelling

   1. Baseline models
   2. Time series models
   3. Regularised regression
   4. Uncertainty quantification

3. Presentation and deployment



\## Author



Pablo Martínez-Miravé  

\[github.com/pamarmi](https://github.com/pamarmi)

