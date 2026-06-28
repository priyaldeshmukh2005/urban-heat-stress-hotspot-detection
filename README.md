# Urban Heat Mitigation and Cooling Strategy Optimization

**Study Area:** Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India
**Hackathon:** Bharatiya Antariksh Hackathon 2026
**Problem Statement:** PS-01 — Optimizing Urban Heat Mitigation and Cooling Strategies via AI/ML
**Team:** AstroByte

A geospatial machine-learning decision-support framework for identifying urban heat-stress hotspots, predicting land surface temperature (LST), analysing the physical drivers of urban heat, estimating population-aware vulnerability, and prioritising cooling interventions across Chhatrapati Sambhajinagar.

The system integrates satellite-derived environmental indicators with explainable machine learning to support location-specific urban heat mitigation planning.

## Live Dashboard

Deployed Streamlit application:

https://urban-heat-stress-hotspot-detection-hseepes29gv24nfc28jmgx.streamlit.app/

The dashboard provides interactive views of urban heat hotspots, heat drivers, vulnerability, intervention scenarios, model validation, and priority zones.

## Project Objective

The project addresses urban heat as a planning and decision-support problem rather than only a mapping problem.

It is designed to:

* Predict land surface temperature across the study area using satellite-derived physical indicators.
* Detect and rank urban heat-stress hotspots.
* Identify the dominant environmental and urban drivers of predicted heat.
* Estimate heat vulnerability by combining heat hazard with population exposure.
* Simulate cooling interventions across city zones.
* Recommend the most suitable cooling strategy for each location.
* Provide an interactive dashboard for planners, researchers, and decision-makers.

## Decision-Support Workflow

```text
Satellite Data and Geospatial Layers
                |
                v
Feature Engineering
(NDVI, NDBI, Elevation, Population, Land Cover)
                |
                v
LST Prediction using Machine Learning
                |
                v
Spatial Cross-Validation and Model Selection
                |
                v
SHAP-Based Explainability
                |
                v
Heat Hotspot and Vulnerability Analysis
                |
                v
Scenario-Based Cooling Intervention Simulation
                |
                v
Priority Zone Ranking and Interactive Dashboard
```

## Key Capabilities

Unlike a conventional urban heat map, the framework supports the full workflow from detection to intervention prioritisation.

* Predicts land surface temperature from physical urban and environmental indicators.
* Uses spatial block cross-validation to reduce spatial leakage during model evaluation.
* Uses SHAP analysis to validate whether the model captures meaningful urban-climate relationships.
* Simulates urban greening and cool/permeable-surface scenarios.
* Estimates predicted LST change for each intervention scenario.
* Identifies high-priority heat hotspots.
* Computes a Heat Vulnerability Index using heat hazard and population exposure.
* Produces interactive maps, priority tables, reports, and a deployed decision-support dashboard.

## Study Area

The study focuses on Chhatrapati Sambhajinagar, formerly Aurangabad, Maharashtra, India.

The city experiences increasing urbanisation, built-up expansion, vegetation loss, and heat-stress exposure. These conditions make it suitable for evaluating satellite-driven urban heat mitigation strategies.

## Data Sources and Features

| Parameter                | Dataset                           | Spatial Resolution | Purpose                                             |
| ------------------------ | --------------------------------- | -----------------: | --------------------------------------------------- |
| NDVI                     | Sentinel-2 SR Harmonized          |               10 m | Vegetation density and cooling influence            |
| NDBI                     | Sentinel-2 SR Harmonized          |            10–20 m | Built-up intensity and impervious-surface influence |
| Land Surface Temperature | Landsat 8/9 Collection 2 Level 2  |               30 m | Urban surface heat and hotspot detection            |
| Elevation                | SRTM                              |               30 m | Terrain-related influence on heat distribution      |
| Population               | WorldPop India 2020               |              100 m | Population exposure and vulnerability estimation    |
| Land Cover               | Derived geospatial classification |           Variable | Urban surface characterisation                      |

The working dataset contains approximately 9,900 sampled locations across the study area.

## Methodology

### Feature Engineering

The machine-learning model uses the following physical and urban drivers:

* NDVI
* NDBI
* Elevation
* Population
* Land-cover information

Latitude and longitude are excluded from the model input features. They are used only for spatial grouping, mapping, and visualization.

Excluding coordinates prevents the model from memorising locations instead of learning the physical reasons behind urban heat. This improves the credibility of scenario simulations when land-cover conditions are modified.

### Machine-Learning Models

The project evaluates:

* Linear Regression as a baseline model
* Random Forest Regressor
* XGBoost Regressor

XGBoost is selected as the primary model based on predictive performance and suitability for nonlinear relationships between satellite-derived indicators and land surface temperature.

### Spatial Cross-Validation

Spatial block cross-validation is used instead of a random train-test split.

The study area is divided into spatial blocks, and complete blocks are held out for testing. This reduces the risk of spatial leakage, where nearby observations in training and testing data can produce overly optimistic performance estimates.

### Explainable AI

SHAP analysis is used to interpret model behaviour and evaluate the contribution of each feature to predicted land surface temperature.

The analysis supports the following physical interpretation:

* Higher built-up intensity is associated with increased predicted LST.
* Vegetation-related features contribute to cooling in vegetated areas.
* The model distinguishes between built-up surfaces, sparse vegetation, and cooler surface conditions.
* Feature contributions are used to support transparent planning decisions.

## Cooling Intervention Scenarios

Two scenario-based interventions are simulated across the study area.

### Urban Greening Scenario

This scenario represents an increase in vegetation cover and a corresponding reduction in built-up influence.

The dashboard reports the predicted LST change associated with a simulated increase in green cover.

### Cool and Permeable Surface Scenario

This scenario represents reduced built-up heat influence through interventions such as:

* Cool roofs
* Reflective surfaces
* Permeable pavements
* Low-heat urban materials

Each location is assigned the intervention scenario with the highest predicted cooling benefit.

## Heat Vulnerability Index

The Heat Vulnerability Index combines:

* Predicted heat hazard
* Population exposure

This approach distinguishes between the hottest locations and the locations where heat may affect the greatest number of people.

A moderately hot but densely populated zone may have greater planning priority than an isolated high-temperature zone with low population exposure.

## Key Results

| Output                               | Result                                              |
| ------------------------------------ | --------------------------------------------------- |
| Selected model                       | XGBoost Regressor                                   |
| Validation approach                  | Spatial block cross-validation                      |
| XGBoost performance                  | R² approximately 0.51                               |
| Mean Absolute Error                  | Approximately 1.78 °C                               |
| Root Mean Squared Error              | Approximately 2.26 °C                               |
| Dominant heat driver                 | Built-up intensity represented by NDBI              |
| Maximum zone-level cooling potential | Up to approximately 0.84 °C under targeted greening |
| Hotspot prioritisation               | Top 10 priority zones identified from 96 grid zones |
| Vulnerability finding                | High-risk zones differ from the hottest zones       |

## Decision-Support Interpretation

The project is designed to answer four planning questions:

1. Where are the major urban heat-stress hotspots?
2. Which physical factors are contributing to heat in those locations?
3. Which locations have the highest population-aware heat vulnerability?
4. Which cooling intervention is likely to provide the greatest predicted benefit in each location?

## Generated Outputs

| Output                                      | Description                                                    |
| ------------------------------------------- | -------------------------------------------------------------- |
| `outputs/aurangabad_heat_map.html`          | Interactive gridded LST thermal map with priority-zone markers |
| `outputs/aurangabad_vulnerability_map.html` | Heat Vulnerability Index map                                   |
| `outputs/reports/intervention_priority.csv` | Ranked intervention priority plan                              |
| `outputs/reports/zone_vulnerability.csv`    | Population-aware vulnerability ranking                         |
| `outputs/dashboard_data/`                   | CSV files used by the Streamlit dashboard                      |
| `outputs/plots/`                            | Model and explainability visualisations                        |

## Repository Structure

```text
.
├── data/
│   ├── raw/                         # Source satellite-derived data
│   └── processed/                   # Cleaned and feature-engineered datasets
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
│   ├── 12_vulnerability.ipynb
│   └── 13_dashboard_data_preparation.ipynb
├── outputs/
│   ├── dashboard_data/              # Dashboard-ready CSV files
│   ├── plots/                       # Visualisations
│   ├── reports/                     # Priority and vulnerability reports
│   ├── *.pkl                        # Trained models
│   └── *.html                       # Interactive maps
├── src/                             # Reusable processing and utility modules
├── app.py                           # Streamlit dashboard application
├── requirements.txt
└── README.md
```

## Installation and Local Execution

Clone the repository:

```bash
git clone https://github.com/priyaldeshmukh2005/urban-heat-stress-hotspot-detection.git
cd urban-heat-stress-hotspot-detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the notebook workflow in sequence to reproduce the analysis and generated outputs.

To launch the Streamlit dashboard locally:

```bash
python -m streamlit run app.py
```

## Technology Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* SHAP
* Plotly
* Folium
* Matplotlib
* Streamlit
* Google Earth Engine
* QGIS

## ISRO and Indian Earth-Observation Alignment

The framework is designed to support Indian Earth-observation applications and can be extended using national geospatial and climate datasets.

Potential future integrations include:

* Bhuvan and NRSC Land Use/Land Cover layers for refined land-cover validation.
* NRSC LULC Atlas of India and NICES Essential Climate Variables.
* MOSDAC meteorological datasets for atmospheric and climate context.
* TRISHNA thermal-infrared data for higher-resolution urban thermal monitoring and multi-city deployment.

## Limitations

* Satellite-derived land surface temperature is not identical to near-surface air temperature.
* Population is used as an exposure proxy and does not represent all social vulnerability dimensions.
* Cooling values are model-based scenario estimates and are not guaranteed real-world temperature outcomes.
* Final intervention planning requires field validation, local engineering assessment, land-availability checks, cost analysis, and municipal feasibility review.

## Future Scope

* Integrate Bhuvan and NRSC land-cover datasets for improved land-cover-aware modelling.
* Add socioeconomic vulnerability indicators such as age, income, housing quality, and health-risk proxies.
* Incorporate weather-station observations for additional validation.
* Integrate TRISHNA thermal data for higher-resolution urban heat analysis.
* Extend the framework to additional Indian cities.
* Add intervention cost, feasibility, and implementation-priority scoring.

## Team AstroByte

| Team Member      | Role                                       |
| ---------------- | ------------------------------------------ |
| Srushti Bawaskar | Geospatial and Data Lead                   |
| Priyal Deshmukh  | AI/ML Lead                                 |
| Rishika Deshmukh | Research, Documentation and Dashboard Lead |

## Acknowledgement

Developed by Team AstroByte for the Bharatiya Antariksh Hackathon 2026, Problem Statement PS-01: Optimizing Urban Heat Mitigation and Cooling Strategies via AI/ML.
