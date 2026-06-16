# 🌡️ Urban Heat Stress Hotspot Detection

> 🌍 **An AI-powered geospatial intelligence system for detecting, predicting, and mitigating urban heat stress hotspots using satellite imagery, environmental indicators, and machine learning.**

Developed as part of **Bharatiya Antariksha Hackathon 2026**, this project combines Remote Sensing, GIS, Artificial Intelligence, and Data Analytics to support climate-resilient urban planning and sustainable city development.

---

## 🚀 Project Overview

Rapid urbanization has intensified the **Urban Heat Island (UHI)** effect, causing cities to experience significantly higher temperatures than surrounding regions. These elevated temperatures impact public health, energy consumption, infrastructure, and overall quality of life.

This project aims to build an end-to-end geospatial AI system capable of:

* 🔍 Detecting Urban Heat Stress Hotspots
* 📊 Identifying the key drivers of urban heating
* 🤖 Predicting heat stress levels using Machine Learning
* 🌱 Recommending mitigation strategies
* 🔄 Simulating "what-if" urban planning scenarios

By integrating satellite-derived indicators with environmental and socio-economic factors, the system provides actionable insights for urban planners and decision-makers.

---

## 🎯 Objectives

### Primary Goals

✅ Detect Urban Heat Stress Hotspots

✅ Analyze environmental and urban factors contributing to heat accumulation

✅ Predict Land Surface Temperature (LST) and Heat Stress Levels

✅ Explain model predictions using Explainable AI techniques

✅ Evaluate mitigation strategies through scenario-based simulations

---

## 🌍 Key Features

### Geospatial Analysis

* NDVI (Vegetation Analysis)
* NDBI (Built-up Area Analysis)
* Land Surface Temperature Mapping
* Satellite Data Processing

### Artificial Intelligence

* Data Cleaning & Preprocessing
* Exploratory Data Analysis (EDA)
* Feature Engineering
* Random Forest Modeling
* XGBoost Modeling (Planned)
* Explainable AI using SHAP

### Decision Support

* Heat Stress Prediction
* Hotspot Identification
* Driver Analysis
* Scenario-Based Mitigation Planning

---

## 📊 Data Sources

The project utilizes a combination of:

### Satellite-Derived Features

* 🌿 NDVI (Normalized Difference Vegetation Index)
* 🏙️ NDBI (Normalized Difference Built-up Index)
* 🌡️ Land Surface Temperature (LST)

### Environmental Features

* 💧 Humidity
* 🌬️ Wind Speed
* ☀️ Solar Radiation

### Urban Features

* 👥 Population Density
* 🏢 Building Density
* 🛣️ Road Density

---

## 🛠️ Technology Stack

### Programming & Data Science

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* Random Forest
* XGBoost (Planned)
* SHAP (Planned)

### Geospatial Technologies

* QGIS
* Google Earth Engine
* Remote Sensing Datasets

### Visualization & Dashboard

* Matplotlib
* Streamlit

### Development Tools

* Git
* GitHub
* Jupyter Notebook
* VS Code

---

## 📂 Project Structure

```text
UrbanHeatStress/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_baseline.ipynb
│   ├── 06_hotspot_detection.ipynb
│   ├── 07_explainable_ai.ipynb
│   └── 08_scenario_simulation.ipynb
│
├── outputs/
│   ├── plots/
│   └── reports/
│
├── src/
│   ├── cleaning.py
│   ├── eda.py
│   ├── features.py
│   └── utils.py
│
├── README.md
└── requirements.txt
```

---

## 🔄 Project Workflow

```text
Satellite Data Collection
            ↓
GIS Processing
            ↓
NDVI / NDBI / LST Extraction
            ↓
Dataset Preparation
            ↓
Data Cleaning
            ↓
Exploratory Data Analysis
            ↓
Feature Engineering
            ↓
Machine Learning Model
            ↓
Heat Stress Prediction
            ↓
Hotspot Detection
            ↓
Explainable AI
            ↓
Scenario Simulation
            ↓
Dashboard & Visualization
```

---

## 📓 Notebook Pipeline

| Notebook                     | Description                                 |
| ---------------------------- | ------------------------------------------- |
| 01_data_audit.ipynb          | Data inspection and quality assessment      |
| 02_data_cleaning.ipynb       | Data preprocessing and cleaning             |
| 03_eda.ipynb                 | Exploratory Data Analysis                   |
| 04_feature_engineering.ipynb | Feature creation and transformation         |
| 05_model_baseline.ipynb      | Baseline machine learning model             |
| 06_hotspot_detection.ipynb   | Heat hotspot identification                 |
| 07_explainable_ai.ipynb      | Feature importance and model interpretation |
| 08_scenario_simulation.ipynb | Urban heat mitigation simulations           |

---

## 👥 Team

This project is being developed by a multidisciplinary team participating in **Bharatiya Antariksha Hackathon 2026**.

### 🌍 Srushti Bawaskar

**Geospatial & Data Lead**

### 👩‍💻 Priyal Deshmukh

**AI/ML Lead**

### 📊 Rishika Deshmukh

**Research, Dashboard & Documentation Lead**

---

## 🌱 Expected Impact

The proposed system can support:

* Climate-Resilient Urban Planning
* Smart City Development
* Heat Risk Assessment
* Sustainable Infrastructure Planning
* Environmental Decision Support Systems

By identifying vulnerable heat-stress regions and evaluating mitigation strategies, the project contributes toward creating safer and more sustainable urban environments.

---

## 🔮 Future Enhancements

* Real-Time Satellite Data Integration
* Interactive GIS-Based Heat Maps
* Advanced Deep Learning Models
* Automated Mitigation Recommendations
* Climate Risk Forecasting Dashboard
* Multi-City Comparative Analysis

---

## 🏆 Bharatiya Antariksha Hackathon 2026

This project represents an interdisciplinary approach that combines **Remote Sensing**, **Geospatial Analytics**, **Artificial Intelligence**, and **Climate Science** to address one of the most critical urban sustainability challenges of our time.

---

## ⭐ Vision

**"Building climate-resilient cities through geospatial intelligence, machine learning, and data-driven decision making."** 🌍🚀🌱
