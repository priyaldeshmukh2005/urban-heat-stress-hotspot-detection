# Urban Heat Mitigation and Cooling Strategy Optimization
### Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India

A geospatial machine-learning framework that predicts land surface temperature from satellite-derived indicators, validates the physical drivers of urban heat, and ranks city zones by where targeted cooling interventions deliver the greatest impact, measured both in degrees of cooling and in people protected.

Built for the **Bharatiya Antariksh Hackathon 2026 (ISRO)**, Problem Statement 01: *Optimizing Urban Heat Mitigation and Cooling Strategies via AI/ML*.

---

## What it does

Most urban-heat projects stop at detection. This one closes the loop to optimization:

1. Predicts Land Surface Temperature (LST) across the city from physical drivers.
2. Validates that the model learned real urban-climate physics, not spurious correlations, using SHAP.
3. Simulates mitigation interventions (urban greening, cool and permeable surfaces) across every zone.
4. Ranks zones by cooling potential, identifying where intervention reduces temperature the most.
5. Computes a Heat Vulnerability Index (heat hazard combined with population exposure) to find where heat affects the most people.
6. Produces interactive maps a municipal planner can act on directly.

---

## Quick start

```bash
pip install -r requirements.txt
```

Run the notebooks in `notebooks/` in order, or jump to the parts you need:

| Notebook | Purpose |
|---|---|
| `01`–`04` | Data audit, cleaning, EDA, feature engineering |
| `09_random_forest`, `10_xgboost` | LST models with spatial cross-validation |
| `07_explainable_ai` | SHAP physics validation |
| `08_scenario_simulation` | City-wide intervention simulation and zone priority ranking |
| `11_heatmap` | Interactive LST thermal map |
| `12_vulnerability` | Heat Vulnerability Index map |

All maps and reports are written to `outputs/`. Open the generated HTML files in any browser.

---

## Methodology

### Data and features

Satellite-derived indicators for Chhatrapati Sambhajinagar (about 9,900 sampled points): NDVI (vegetation), NDBI (built-up), Elevation, Population, and LST (target).

> Specify your LST source here, for example Landsat-8 thermal or MODIS, exported via Google Earth Engine.

The model uses only physical drivers (NDVI, NDBI, Elevation, Population). Latitude and longitude are deliberately **excluded** from prediction and used only for spatial grouping and mapping. Including coordinates would let the model memorize *where* is hot instead of *why*, which inflates accuracy and, more importantly, prevents the model from responding correctly when an intervention changes land cover.

### Model and validation

- Models: Linear Regression (baseline), Random Forest, and XGBoost (selected).
- **Spatial block cross-validation.** The city is divided into a grid and whole blocks are held out for testing, so spatially adjacent points cannot leak information between train and test. This is the standard pitfall in geospatial ML and the reason a naive random split over-reports accuracy.
- Honest performance (XGBoost, spatial CV): **R² approximately 0.51, MAE approximately 1.78 C, RMSE approximately 2.26 C.** This is a deliberately conservative, leakage-free estimate that prioritizes transferability and correct intervention response over an inflated in-sample score.

### Explainability and physics validation

SHAP analysis confirms the model learned correct urban-climate physics:

- **NDBI** (built-up index) is the dominant driver, with a cleanly monotonic positive relationship to LST. More impervious surface, more heat.
- **NDVI** (vegetation) reduces temperature in the vegetated range, and the model correctly separates water bodies (negative NDVI, cool) from sparse-vegetation built-up land.
- Sanity check: a simulated 20 percent increase in vegetation reduces predicted LST by about 0.34 C on average, confirming interventions move temperature in the physically correct direction.

### Mitigation simulation and zone prioritization

Two interventions are simulated across every zone:

- **Urban greening:** increased vegetation and reduced built-up surface.
- **Cool and permeable surfaces:** reduced built-up signal (cool roofs, permeable paving).

Each zone is scored by the cooling it achieves and assigned its best-performing strategy. The hottest zones are then ranked into an intervention priority list. Targeted greening of the top hotspot zones delivers up to about **0.84 C of surface cooling**, concentrated where heat is highest.

### Heat Vulnerability Index

Cooling potential alone directs resources to the hottest zones, which are often sparsely populated peripheral areas. The Heat Vulnerability Index combines heat hazard with population exposure to find where heat affects the most people.

The result is a key planning insight: **the hottest zones and the most at-risk zones are largely different.** A moderately hot but densely populated zone can carry higher human risk than the single hottest zone in the city.

---

## Key results

| Output | Result |
|---|---|
| LST model (XGBoost, spatial CV) | R² approx 0.51, MAE approx 1.78 C |
| Dominant heat driver (SHAP) | NDBI (built-up surface) |
| Best cooling per zone | up to approx 0.84 C (targeted greening) |
| Hotspot zones identified | top 10 of 96 grid zones |
| Vulnerability finding | most at-risk zones differ from hottest zones |

Generated outputs:

- `outputs/aurangabad_heat_map.html` — gridded LST thermal map with priority-zone markers.
- `outputs/aurangabad_vulnerability_map.html` — Heat Vulnerability Index map.
- `outputs/reports/intervention_priority.csv` — ranked intervention plan.
- `outputs/reports/zone_vulnerability.csv` — zones ranked by human risk.

---

## Data sources and ISRO alignment

**Current prototype:** satellite-derived indicators exported via Google Earth Engine.

**Designed for Indian Earth-observation data:**

- **Bhuvan (ISRO / NRSC geoportal):** Land Use / Land Cover and Urban Land Use thematic layers for land-cover validation and refinement.
- **NRSC LULC Atlas of India** and **NICES** Essential Climate Variables for contextual and temporal layers.
- **MOSDAC (INSAT-3D / 3DR):** meteorological context.

**TRISHNA-ready.** The pipeline is built around thermal-infrared LST as its target, so it is positioned to ingest data from TRISHNA, the upcoming ISRO and CNES thermal-infrared mission (approximately 50 to 60 m resolution, designed for urban-environment monitoring), enabling substantially higher-resolution, India-wide deployment.

---

## Technology stack

Python, pandas, NumPy, scikit-learn, XGBoost, SHAP, folium, branca, matplotlib. Data engineering via Google Earth Engine.

---

## Repository structure

```text
.
├── data/
│   ├── raw/                 # source satellite-derived dataset
│   └── processed/           # cleaned and feature-engineered data
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_baseline.ipynb
│   ├── 07_explainable_ai.ipynb
│   ├── 08_scenario_simulation.ipynb
│   ├── 09_random_forest.ipynb
│   ├── 10_xgboost.ipynb
│   ├── 11_heatmap.ipynb
│   └── 12_vulnerability.ipynb
├── outputs/
│   ├── reports/             # priority and vulnerability CSVs
│   ├── *.pkl                # trained models
│   └── *.html               # interactive maps
├── src/                     # reusable cleaning, feature, and model code
├── README.md
└── requirements.txt
```

---

## Roadmap

- Integrate Bhuvan LULC for land-cover-aware modeling.
- Add socioeconomic vulnerability layers (age, income from Census) to the Heat Vulnerability Index.
- Ingest TRISHNA thermal data for high-resolution, multi-city deployment.
- Streamlit dashboard for interactive planner use.

---

## Team

> team members and roles.

Bharatiya Antariksh Hackathon 2026, Problem Statement 01.