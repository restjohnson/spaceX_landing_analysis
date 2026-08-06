# SpaceX Falcon 9 Landing Analysis

Predicting whether a SpaceX Falcon 9 first stage will land successfully, using launch data scraped from Wikipedia and IBM. The project moves through the full pipeline: scraping → cleaning → exploratory analysis → feature engineering → interactive visualization → classification.

## Pipeline

| Step | Notebook / Script | What it does | Reads | Writes |
| --- | --- | --- | --- | --- |
| 1. Scrape | [data_wrangling.ipynb](data_wrangling.ipynb) | Scrapes the "List of Falcon 9 and Falcon Heavy launches" Wikipedia table with `requests`/`BeautifulSoup`, parses each launch row (booster version, site, payload, orbit, outcome, etc.) | Wikipedia (live) | `spacex_scraped.csv` |
| 2. Clean & label | [data_wrangling.ipynb](data_wrangling.ipynb) | Reloads the scraped data, checks null rates/dtypes, and derives the binary `Class` label (1 = landed, 0 = did not land) from the free-text `Outcome` column (`True Ocean`/`RTLS`/`ASDS` = success, `False *`/`None *` = failure) | `spacex_scraped.csv` | `dataset_part_2.csv` (cleaned + labeled) |
| 3. EDA & feature engineering | [eda.ipynb](eda.ipynb) | Visualizes success rate vs. flight number, launch site, payload mass, orbit type, and year; one-hot encodes categorical columns (`Orbit`, `LaunchSite`, `Serial`, `LandingPad`) and casts numeric columns to `float64` | `dataset_part_2.csv` | `spacexdataset_eng.csv`, `dataset_part_3.csv` (model-ready feature matrix) |
| 4. Map visualization | [interactive_viz.ipynb](interactive_viz.ipynb) | Builds `folium` maps of launch sites with success/failure markers, marker clustering, and distance calculations (haversine) from each site to the coastline, nearest city, highway, and railway | `spacex_launch_geo.csv` | — |
| 5. Interactive dashboard | [dash_interactivity.py](dash_interactivity.py) | Plotly Dash app: a dropdown to filter by launch site, a pie chart of success counts, and a payload-mass-vs-outcome scatter plot with a payload range slider | `spacex_launch_dash.csv` | — |
| 6. Prediction | [prediction.ipynb](prediction.ipynb) | Trains and tunes four classifiers via `GridSearchCV` (10-fold CV) — Logistic Regression, SVM, Decision Tree, KNN — and compares test-set performance | `dataset_part_2.csv` (labels), `dataset_part_3.csv` (features) | — |

> Note: `dataset_part_2.csv` and `dataset_part_3.csv` are the cleaned and feature-engineered datasets that `prediction.ipynb` depends on directly.

## Data files

| File | Description |
| --- | --- |
| `spacex_scraped.csv` | Raw table scraped from Wikipedia, before cleaning |
| `dataset_part_2.csv` | Cleaned launch data with the derived `Class` (landing success) label |
| `spacexdataset_eng.csv` | One-hot encoded feature set produced in `eda.ipynb` |
| `dataset_part_3.csv` | Final one-hot encoded feature matrix (83 columns) used to train the models in `prediction.ipynb` |
| `spacex_launch_geo.csv` | Launch records with latitude/longitude, used for the Folium map |
| `spacex_launch_dash.csv` | Launch records formatted for the Plotly Dash app |

## Results

Each model was tuned with `GridSearchCV` (`cv=10`, `scoring='accuracy'`) and evaluated on a held-out 20% test split (`random_state=42`):

| Model | Best CV accuracy | Test accuracy |
| --- | --- | --- |
| Logistic Regression | 0.818 | 0.89 |
| SVM | — | 0.89 |
| Decision Tree | 0.88 | 0.78 |
| **KNN** (k=7, p=1) | **0.832** | **0.94** |

KNN performed best on the held-out test set.

