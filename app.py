import os
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Urban Heat Mitigation and Cooling Strategy Optimization",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# SUNSET HEATMAP THEME
# ==================================================

st.markdown(
    """
    <style>
        :root {
            --cream: #fffaf4;
            --panel: #fffdf9;
            --line: #f0ddd0;
            --text: #2f1d1a;

            --maroon: #3b080c;
            --maroon-2: #68131a;
            --red: #b82025;
            --orange-red: #e44720;
            --orange: #ff7a1a;
            --gold: #f7b733;

            --green: #4f7d50;
            --green-soft: #edf6e9;
            --blue: #4d83b8;

            --shadow: 0 8px 22px rgba(93, 35, 19, 0.10);
        }

        .stApp {
            background:
                radial-gradient(circle at 88% 4%, rgba(255, 122, 26, 0.10), transparent 18%),
                radial-gradient(circle at 15% 100%, rgba(184, 32, 37, 0.06), transparent 20%),
                var(--cream);
            color: var(--text);
        }

        [data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 85% 90%, rgba(255, 122, 26, 0.38), transparent 22%),
                linear-gradient(180deg, #2c0609 0%, #47090e 50%, #741a1b 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] * {
            color: #fffaf6;
        }

        [data-testid="stSidebar"] .stCaption {
            color: #f2cbc0 !important;
        }

        [data-testid="stSidebar"] .stRadio label {
            color: #fffaf6 !important;
            font-weight: 600;
        }

        h1 {
            color: var(--maroon) !important;
            font-size: 2.15rem !important;
            font-weight: 850 !important;
            letter-spacing: -0.7px;
        }

        h2 {
            color: var(--maroon) !important;
            font-weight: 800 !important;
            border-left: 5px solid var(--orange);
            padding-left: 12px;
        }

        h3 {
            color: var(--maroon-2) !important;
            font-weight: 760 !important;
        }

        p, li, label, .stMarkdown {
            color: #4d3832;
        }

        .top-title {
            padding: 8px 0 15px 0;
        }

        .project-title {
            font-size: 2.35rem;
            font-weight: 900;
            letter-spacing: -1px;
            margin: 0;
            background: linear-gradient(90deg, #94191d 0%, #e44720 55%, #ff8a1c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .project-subtitle {
            color: #5e4c46;
            font-size: 1.05rem;
            margin-top: 5px;
        }

        .top-info-card {
            background: rgba(255, 253, 249, 0.94);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 13px 16px;
            box-shadow: 0 5px 16px rgba(93, 35, 19, 0.07);
            min-height: 70px;
        }

        .top-info-label {
            font-size: 0.78rem;
            font-weight: 800;
            color: #9a2a20;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .top-info-value {
            font-size: 0.98rem;
            font-weight: 700;
            color: #35201b;
            margin-top: 3px;
        }

        .section-panel {
            background: rgba(255, 253, 249, 0.93);
            border: 1px solid var(--line);
            border-radius: 13px;
            padding: 17px 18px;
            box-shadow: var(--shadow);
            margin-bottom: 20px;
        }

        .section-title {
            color: var(--maroon);
            font-size: 1.1rem;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .heat-note {
            background: #fff0e9;
            border: 1px solid #f5d2c5;
            border-left: 5px solid var(--orange-red);
            border-radius: 10px;
            padding: 14px 16px;
            margin: 10px 0 20px 0;
            color: #6b3026;
        }

        .cool-note {
            background: var(--green-soft);
            border: 1px solid #d6e7d0;
            border-left: 5px solid var(--green);
            border-radius: 10px;
            padding: 14px 16px;
            margin: 10px 0 20px 0;
            color: #35573a;
        }

        .info-note {
            background: #fff8e8;
            border: 1px solid #f3e1b8;
            border-left: 5px solid var(--gold);
            border-radius: 10px;
            padding: 14px 16px;
            margin: 10px 0 20px 0;
            color: #6a4a18;
        }

        .risk-note {
            background: #fff0ef;
            border: 1px solid #efd2d2;
            border-left: 5px solid var(--red);
            border-radius: 10px;
            padding: 14px 16px;
            margin: 10px 0 20px 0;
            color: #6b2e33;
        }

        [data-testid="stMetric"] {
            background: rgba(255, 253, 249, 0.96);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 16px;
            box-shadow: var(--shadow);
        }

        [data-testid="stMetricLabel"] {
            color: #8b5d50 !important;
            font-weight: 750;
        }

        [data-testid="stMetricValue"] {
            color: #b82025 !important;
            font-weight: 850;
        }

        [data-testid="stDataFrame"] {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 10px;
            overflow: hidden;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            background: #fffdf9 !important;
            border-color: #e8cfc2 !important;
        }

        .divider {
            height: 1px;
            background: #efdcd1;
            margin: 26px 0;
        }

        .footer-text {
            text-align: center;
            color: #8a6e65;
            padding: 14px;
            font-size: 0.88rem;
        }

        .sidebar-study-card {
            border: 1px solid rgba(255,255,255,0.22);
            border-radius: 11px;
            padding: 14px;
            margin-top: 14px;
            background: rgba(255,255,255,0.06);
        }

        .sidebar-study-title {
            font-size: 0.82rem;
            font-weight: 800;
            color: #ffd9c9;
            margin-bottom: 7px;
        }

        .sidebar-study-value {
            font-size: 0.91rem;
            font-weight: 700;
            color: #fff7f2;
            line-height: 1.45;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DATA LOADING
# ==================================================

DATA_FOLDER = "outputs/dashboard_data"


@st.cache_data
def load_data():
    hotspot_map = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_hotspot_map_v3.csv"))
    scenario_map = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_scenario_map_v3.csv"))
    priority_zones = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_priority_zones_v3.csv"))
    intervention_zones = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_intervention_zones_v3.csv"))
    shap_importance = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_shap_importance_v3.csv"))
    model_comparison = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_model_comparison.csv"))
    scenario_summary = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_scenario_summary_v3.csv"))
    kpis = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_kpis_v3.csv"))
    vulnerability_map = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_vulnerability_map_v3.csv"))
    vulnerability_zones = pd.read_csv(os.path.join(DATA_FOLDER, "dashboard_vulnerability_zones_v3.csv"))

    return (
        hotspot_map,
        scenario_map,
        priority_zones,
        intervention_zones,
        shap_importance,
        model_comparison,
        scenario_summary,
        kpis,
        vulnerability_map,
        vulnerability_zones
    )


try:
    (
        hotspot_map,
        scenario_map,
        priority_zones,
        intervention_zones,
        shap_importance,
        model_comparison,
        scenario_summary,
        kpis,
        vulnerability_map,
        vulnerability_zones
    ) = load_data()

except FileNotFoundError as error:
    st.error("Dashboard data file not found.")
    st.write("Please run Notebook 13 again before running the dashboard.")
    st.code(str(error))
    st.stop()


# ==================================================
# CONSISTENT COLOURS, LEGENDS AND UNITS
# ==================================================

HEAT_COLOR_MAP = {
    "Low": "#f6c64b",
    "Moderate": "#ff9a22",
    "High": "#f0522d",
    "Very High": "#a91f26"
}

VULNERABILITY_COLOR_MAP = {
    "Low": "#f6c64b",
    "Moderate": "#ff9a22",
    "High": "#f0522d",
    "Very High": "#a91f26"
}

INTERVENTION_COLOR_MAP = {
    "Urban greening": "#4f7d50",
    "Cool/permeable surfaces": "#4d83b8"
}

HEAT_CATEGORY_ORDER = ["Low", "Moderate", "High", "Very High"]

MAP_LEGEND_TITLES = {
    "Heat_Category": "Heat Stress Level",
    "Vulnerability_Category": "Vulnerability Level",
    "Recommended_Intervention": "Recommended Strategy"
}


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_kpi_value(kpi_dict, possible_names, default=0):
    for name in possible_names:
        if name in kpi_dict:
            return kpi_dict[name]
    return default


def clean_map_columns(dataframe, columns_to_keep):
    return [column for column in columns_to_keep if column in dataframe.columns]


def format_hover_labels(hover_columns):
    label_map = {
        "Observed_LST_C": "Observed LST (°C)",
        "Predicted_LST_C": "Predicted LST (°C)",
        "Baseline_Predicted_LST_C": "Baseline Predicted LST (°C)",
        "Greening_Cooling_C": "+20% Green Cover Change (°C)",
        "Cool_Surface_Cooling_C": "Cool/Permeable Surface Change (°C)",
        "Best_Cooling_C": "Best Predicted LST Change (°C)",
        "NDVI": "NDVI",
        "NDBI": "NDBI",
        "Population": "Population Exposure",
        "LandCover_Class": "Land Cover",
        "Zone_ID": "Zone ID",
        "Heat_Hazard_Score": "Heat Hazard Score",
        "Population_Exposure_Score": "Population Exposure Score",
        "Heat_Vulnerability_Index": "Heat Vulnerability Index"
    }

    return {
        column: label_map.get(column, column.replace("_", " "))
        for column in hover_columns
    }


def style_map(fig, zoom=11.2):
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            zoom=zoom,
            pitch=0,
            bearing=0
        ),
        margin={"r": 0, "t": 42, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#2f1d1a",
        legend=dict(
            bgcolor="rgba(255,253,249,0.92)",
            bordercolor="#ead6ca",
            borderwidth=1,
            font=dict(size=11),
            x=0.99,
            y=0.98,
            xanchor="right",
            yanchor="top"
        )
    )
    return fig


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#fffdf9",
        font_color="#2f1d1a",
        title_font_color="#4b1617",
        xaxis=dict(gridcolor="#f0e0d7"),
        yaxis=dict(gridcolor="#f0e0d7"),
        legend=dict(
            bgcolor="rgba(255,253,249,0.92)",
            bordercolor="#ead6ca",
            borderwidth=1
        )
    )
    return fig


def make_small_clean_map(
    dataframe,
    color_column,
    hover_columns,
    title,
    color_map,
    height=600
):
    map_data = dataframe.copy()

    # Keeps map readable while tables/KPIs still use the full dataset.
    if len(map_data) > 2500:
        map_data = map_data.sample(n=2500, random_state=42)

    category_order = HEAT_CATEGORY_ORDER if color_column in [
        "Heat_Category",
        "Vulnerability_Category"
    ] else None

    fig = px.scatter_mapbox(
        map_data,
        lat="Latitude",
        lon="Longitude",
        color=color_column,
        hover_data=hover_columns,
        labels=format_hover_labels(hover_columns),
        zoom=11.2,
        height=height,
        title=title,
        color_discrete_map=color_map,
        category_orders={
            color_column: category_order
        } if category_order else None
    )

    # scatter_mapbox does not support marker.line.
    fig.update_traces(
        marker=dict(
            size=6,
            opacity=0.64
        )
    )

    fig.update_layout(
        legend_title_text=MAP_LEGEND_TITLES.get(
            color_column,
            color_column.replace("_", " ")
        )
    )

    return style_map(fig, zoom=11.2)


def get_scenario_display_name(scenario_name):
    scenario_lower = str(scenario_name).lower()

    if "green" in scenario_lower or "vegetation" in scenario_lower:
        return "🌿 +20% Green Cover"

    if "cool" in scenario_lower or "permeable" in scenario_lower:
        return "🏙️ Cool / Permeable Surface"

    return str(scenario_name)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown("## ☀️ UrbanHeat AI")
st.sidebar.caption("AI Cooling Intervention Simulator")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select dashboard section",
    [
        "Project Overview",
        "Urban Heat Hotspots",
        "Heat Drivers",
        "Heat Vulnerability",
        "AI Cooling Intervention Simulator",
        "Model Validation",
        "About Project"
    ]
)

st.sidebar.markdown(
    """
    <div class="sidebar-study-card">
        <div class="sidebar-study-title">📍 STUDY AREA</div>
        <div class="sidebar-study-value">
            Chhatrapati Sambhajinagar<br>
            (Aurangabad), Maharashtra
        </div>
        <br>
        <div class="sidebar-study-value">
            Year: 2025<br>
            Data: Sentinel-2 + Landsat 8/9<br>
            Model: XGBoost
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Team AstroByte")
st.sidebar.markdown(
    """
    **Priyal Deshmukh**  
    AI/ML Lead  

    **Srushti Bawaskar**  
    Geospatial & Data Lead  

    **Rishika Deshmukh**  
    Research, Documentation & Dashboard Lead
    """
)


# ==================================================
# TOP HEADER
# ==================================================

header_left, header_right = st.columns([2.1, 1])

with header_left:
    st.markdown(
        """
        <div class="top-title">
            <div class="project-title">URBANHEAT AI</div>
            <div class="project-subtitle">
                Urban Heat Mitigation and Cooling Strategy Optimization
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    info_1, info_2 = st.columns([1.7, 0.8])

    with info_1:
        st.markdown(
            """
            <div class="top-info-card">
                <div class="top-info-label">📍 Study Area</div>
                <div class="top-info-value">Chhatrapati Sambhajinagar</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with info_2:
        st.markdown(
            """
            <div class="top-info-card">
                <div class="top-info-label">📅 Year</div>
                <div class="top-info-value">2025</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# PROJECT OVERVIEW
# ==================================================

if page == "Project Overview":

    st.markdown(
        """
        <div class="heat-note">
            <b>UrbanHeat AI</b> uses satellite-derived urban indicators and machine learning
            to identify heat-stress hotspots, understand heat drivers, estimate vulnerability,
            and recommend cooling interventions for priority zones.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-panel">
            <div class="section-title">🧭 How to Use This Dashboard</div>
            <ol style="margin-bottom:0; padding-left:22px; line-height:1.85;">
                <li><b>Locate heat stress:</b> use Urban Heat Hotspots to identify High and Very High heat zones.</li>
                <li><b>Prioritize people at risk:</b> open Heat Vulnerability to find areas where heat overlaps with population exposure.</li>
                <li><b>Understand why:</b> review Heat Drivers to see which variables most influence predicted land surface temperature.</li>
                <li><b>Compare interventions:</b> use AI Cooling Intervention Simulator to compare +20% green cover and cool/permeable-surface scenarios..</li>
                <li><b>Verify before implementation:</b> use priority-zone tables for field assessment, cost review, and municipal planning.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    kpi_values = dict(zip(kpis["Metric"], kpis["Value"]))

    r2_value = float(get_kpi_value(
        kpi_values,
        ["Dataset V3 XGBoost R2", "Dataset V3 XGBoost R²"],
        0
    ))

    mae_value = float(get_kpi_value(
        kpi_values,
        ["Dataset V3 XGBoost MAE (C)", "Dataset V3 XGBoost MAE"],
        0
    ))

    total_locations = int(float(get_kpi_value(
        kpi_values,
        ["Total Sampled Locations", "Sampled Locations"],
        0
    )))

    priority_count = int(float(get_kpi_value(
        kpi_values,
        ["High Priority Hotspot Zones", "High-Priority Hotspot Zones"],
        0
    )))

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Model R² Score", f"{r2_value:.3f}")
    col2.metric("MAE (°C)", f"{mae_value:.2f} °C")
    col3.metric("Total Locations", f"{total_locations:,}")
    col4.metric("High Priority Zones", f"{priority_count}")

    if "Heat_Category" in hotspot_map.columns:
        high_heat_share = (
            hotspot_map["Heat_Category"]
            .astype(str)
            .str.contains("High", case=False, na=False)
            .mean() * 100
        )
        col5.metric("High Heat Share", f"{high_heat_share:.1f}%")
    else:
        col5.metric("Heat Stress Level", "High")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1.45, 0.55])

    with left_col:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔥 Urban Heat Hotspots</div>', unsafe_allow_html=True)

        heat_options = [
            category for category in HEAT_CATEGORY_ORDER
            if category in hotspot_map["Heat_Category"].dropna().astype(str).unique()
        ]

        selected_heat = st.multiselect(
            "Filter heat-stress categories",
            options=heat_options,
            default=heat_options,
            key="overview_heat_filter"
        )

        filtered_hotspots = hotspot_map[
            hotspot_map["Heat_Category"].astype(str).isin(selected_heat)
        ].copy()

        if len(filtered_hotspots) > 0:
            hover_columns = clean_map_columns(
                filtered_hotspots,
                [
                    "Observed_LST_C",
                    "Predicted_LST_C",
                    "NDVI",
                    "NDBI",
                    "Population",
                    "LandCover_Class",
                    "Zone_ID"
                ]
            )

            fig = make_small_clean_map(
                dataframe=filtered_hotspots,
                color_column="Heat_Category",
                hover_columns=hover_columns,
                title="Urban Heat Hotspots | Land Surface Temperature (°C)",
                color_map=HEAT_COLOR_MAP,
                height=430
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No locations match the selected heat categories.")

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Heat Stress Distribution</div>', unsafe_allow_html=True)

        if "Heat_Category" in hotspot_map.columns:
            heat_counts = (
                hotspot_map["Heat_Category"]
                .astype(str)
                .value_counts()
                .reindex(HEAT_CATEGORY_ORDER, fill_value=0)
                .reset_index()
            )
            heat_counts.columns = ["Heat Category", "Count"]

            fig = px.pie(
                heat_counts,
                names="Heat Category",
                values="Count",
                hole=0.64,
                color="Heat Category",
                color_discrete_map=HEAT_COLOR_MAP,
                category_orders={"Heat Category": HEAT_CATEGORY_ORDER}
            )

            fig.update_traces(
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
                marker=dict(
                    line=dict(
                        color="#fffaf4",
                        width=2
                    )
                )
            )

            fig.update_layout(
                height=315,
                margin=dict(l=5, r=5, t=10, b=5),
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#2f1d1a",
                showlegend=True,
                legend=dict(
                    title="Heat Stress Level",
                    orientation="v",
                    x=1.02,
                    y=0.5,
                    xanchor="left",
                    yanchor="middle",
                    font=dict(size=11)
                ),
                annotations=[
                    dict(
                        text="<b>Heat Stress</b><br>Distribution",
                        x=0.5,
                        y=0.5,
                        font=dict(size=12, color="#5d2521"),
                        showarrow=False
                    )
                ]
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.05, 0.95])

    with col_a:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Top Heat Drivers (SHAP)</div>', unsafe_allow_html=True)

        shap_plot_data = shap_importance.sort_values(
            by="Mean_Absolute_SHAP",
            ascending=True
        ).copy()

        fig = px.bar(
            shap_plot_data,
            x="Mean_Absolute_SHAP",
            y="Readable_Feature",
            orientation="h",
            color="Mean_Absolute_SHAP",
            color_continuous_scale=["#ffcf5c", "#ff8a1c", "#e44720", "#9b1d22"]
        )

        fig.update_layout(
            coloraxis_showscale=False,
            height=330,
            title="",
            xaxis_title="Mean Absolute SHAP Value"
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">❄️ Scenario-Based Predicted LST Change (°C)</div>',
            unsafe_allow_html=True
        )

        if len(scenario_summary) > 0:
            for _, row in scenario_summary.iterrows():
                scenario_name = str(row["Scenario"])
                cooling_value = float(row["Mean_Cooling_C"])
                display_name = get_scenario_display_name(scenario_name)

                if "green" in scenario_name.lower() or "vegetation" in scenario_name.lower():
                    st.markdown(
                        f"""
                        <div class="cool-note">
                            <b>{display_name}</b><br>
                            <span style="font-size:0.88rem;">
                                Predicted LST change from baseline
                            </span><br>
                            <span style="font-size:1.35rem; font-weight:850;">
                                {cooling_value:.3f} °C
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div style="
                            background:#edf5fd;
                            border:1px solid #d6e5f5;
                            border-left:5px solid #4d83b8;
                            border-radius:10px;
                            padding:14px 16px;
                            margin:10px 0 20px 0;
                            color:#244d7c;
                        ">
                            <b>{display_name}</b><br>
                            <span style="font-size:0.88rem;">
                                Predicted LST change from baseline
                            </span><br>
                            <span style="font-size:1.35rem; font-weight:850;">
                                {cooling_value:.3f} °C
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-note">
            <b>💡 Planning insight:</b> use hotspot intensity, vulnerability level,
            and scenario-based predicted LST change together to prioritize interventions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="risk-note">
            <b>Decision-support disclaimer:</b> predicted LST changes are model-based,
            scenario-specific planning estimates. They support comparison and prioritization,
            but are not guaranteed real-world temperature outcomes. Field verification,
            site feasibility, costs, land availability, and local design conditions must be
            assessed before implementation.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# URBAN HEAT HOTSPOTS
# ==================================================

elif page == "Urban Heat Hotspots":

    st.header("Urban Heat Hotspots")

    st.markdown(
        """
        <div class="heat-note">
            <b>Purpose:</b> identify locations with elevated observed land surface
            temperature (LST, °C) and prioritize concentrated hotspot zones for intervention.
        </div>
        """,
        unsafe_allow_html=True
    )

    heat_options = [
        category for category in HEAT_CATEGORY_ORDER
        if category in hotspot_map["Heat_Category"].dropna().astype(str).unique()
    ]

    selected_heat = st.multiselect(
        "Select heat-stress categories",
        options=heat_options,
        default=heat_options,
        key="hotspot_heat_filter"
    )

    filtered_hotspots = hotspot_map[
        hotspot_map["Heat_Category"].astype(str).isin(selected_heat)
    ].copy()

    if len(filtered_hotspots) > 0:
        hover_columns = clean_map_columns(
            filtered_hotspots,
            [
                "Observed_LST_C",
                "Predicted_LST_C",
                "NDVI",
                "NDBI",
                "Population",
                "LandCover_Class",
                "Zone_ID"
            ]
        )

        fig = make_small_clean_map(
            dataframe=filtered_hotspots,
            color_column="Heat_Category",
            hover_columns=hover_columns,
            title="Urban Heat-Stress Distribution | LST (°C)",
            color_map=HEAT_COLOR_MAP,
            height=610
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected heat categories.")

    st.subheader("Top High-Priority Hotspot Zones")
    st.dataframe(priority_zones, use_container_width=True, hide_index=True)


# ==================================================
# HEAT DRIVERS
# ==================================================

elif page == "Heat Drivers":

    st.header("Heat Drivers and Explainable AI")

    st.markdown(
        """
        <div class="info-note">
            <b>Purpose:</b> understand which environmental and urban features most
            strongly influence predicted land surface temperature (LST, °C) in the XGBoost model.
        </div>
        """,
        unsafe_allow_html=True
    )

    shap_plot_data = shap_importance.sort_values(
        by="Mean_Absolute_SHAP",
        ascending=True
    ).copy()

    fig = px.bar(
        shap_plot_data,
        x="Mean_Absolute_SHAP",
        y="Readable_Feature",
        orientation="h",
        color="Mean_Absolute_SHAP",
        title="Global SHAP Feature Importance",
        color_continuous_scale=["#ffcf5c", "#ff8a1c", "#e44720", "#9b1d22"]
    )

    fig.update_layout(
        coloraxis_showscale=False,
        height=500,
        xaxis_title="Mean Absolute SHAP Value"
    )

    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.markdown(
        """
        <div class="info-note">
            <b>Interpretation:</b> a higher mean absolute SHAP value means that feature
            has a stronger overall influence on model predictions. These results support
            transparency, but do not independently prove causation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        shap_importance[["Readable_Feature", "Mean_Absolute_SHAP"]],
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# HEAT VULNERABILITY
# ==================================================

elif page == "Heat Vulnerability":

    st.header("Heat Vulnerability")

    st.markdown(
        """
        <div class="risk-note">
            <b>Purpose:</b> prioritize areas where predicted heat hazard overlaps with
            higher population exposure. The hottest location is not always the most
            vulnerable location.
        </div>
        """,
        unsafe_allow_html=True
    )

    vulnerability_options = [
        category for category in HEAT_CATEGORY_ORDER
        if category in vulnerability_map["Vulnerability_Category"].dropna().astype(str).unique()
    ]

    selected_vulnerability = st.multiselect(
        "Select vulnerability categories",
        options=vulnerability_options,
        default=vulnerability_options
    )

    filtered_vulnerability = vulnerability_map[
        vulnerability_map["Vulnerability_Category"]
        .astype(str)
        .isin(selected_vulnerability)
    ].copy()

    if len(filtered_vulnerability) > 0:
        hover_columns = clean_map_columns(
            filtered_vulnerability,
            [
                "Baseline_Predicted_LST_C",
                "Population",
                "Heat_Hazard_Score",
                "Population_Exposure_Score",
                "Heat_Vulnerability_Index",
                "Zone_ID"
            ]
        )

        fig = make_small_clean_map(
            dataframe=filtered_vulnerability,
            color_column="Vulnerability_Category",
            hover_columns=hover_columns,
            title="Population-Aware Heat Vulnerability | Predicted LST (°C)",
            color_map=VULNERABILITY_COLOR_MAP,
            height=610
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected vulnerability categories.")

    st.subheader("Top High-Priority Vulnerability Zones")
    st.dataframe(vulnerability_zones, use_container_width=True, hide_index=True)


# ==================================================
# AI Cooling Intervention Simulator
# ==================================================

elif page == "AI Cooling Intervention Simulator":

    st.header("🛰 AI Cooling Intervention Simulator")

    st.markdown(
        """
        <div class="cool-note">
        This simulator performs <b>real-time AI prediction</b> using the trained
        XGBoost model. Instead of applying fixed temperature reductions, it modifies
        urban environmental indicators based on the selected interventions and
        predicts the updated Land Surface Temperature (LST) through model inference.
        </div>
        """,
        unsafe_allow_html=True,
    )

    MODEL_PATH = Path("outputs/models/xgboost_v3_landcover_model.pkl")
    DATA_PATH = Path("data/processed/featured_uhi_v3.csv")

    MODEL_FEATURES = [
        "NDVI",
        "NDBI",
        "Elevation",
        "Population",
        "LandCover_Bare_sparse_vegetation",
        "LandCover_Built-up land",
        "LandCover_Cropland",
        "LandCover_Grassland",
        "LandCover_Permanent_water_bodies",
        "LandCover_Shrubland",
        "LandCover_Tree cover",
    ]

    @st.cache_resource
    def load_ai_model():
        return joblib.load(MODEL_PATH)

    @st.cache_data
    def load_simulation_dataset():
        return pd.read_csv(DATA_PATH)

    model = load_ai_model()

    simulation_df = load_simulation_dataset().copy()
        
    missing_features = [
        feature
        for feature in MODEL_FEATURES
        if feature not in simulation_df.columns
    ]

    if missing_features:

        st.error(
            "Required model features are missing:\n\n"
            + "\n".join(missing_features)
        )

        st.stop()

    st.markdown("---")

    left_col, right_col = st.columns([1, 2])

    with left_col:

        st.subheader("Cooling Interventions")

        green_cover = st.slider(
            "🌿 Green Cover Increase (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
        )

        tree_cover = st.slider(
            "🌳 Tree Plantation (%)",
            min_value=0,
            max_value=100,
            value=25,
            step=1,
        )
        

        cool_roofs = st.slider(
            "🏠 Cool Roof Adoption (%)",
            min_value=0,
            max_value=100,
            value=15,
            step=1,
        )

        permeable_surface = st.slider(
            "🧱 Permeable Surface (%)",
            min_value=0,
            max_value=100,
            value=15,
            step=1,
        )

        builtup_reduction = st.slider(
            "🏢 Built-up Reduction (%)",
            min_value=0,
            max_value=100,
            value=10,
            step=1,
        )

        run_simulation = st.button(
            "🛰 Run AI Simulation",
            use_container_width=True,
            type="primary",
        )

    with right_col:

        st.markdown(
        """
        ### Simulation Workflow

        1. Selected interventions modify environmental indicators.

        2. NDVI increases according to vegetation-related actions.

        3. NDBI decreases according to built-up reduction.

        4. Land-cover proportions are updated.

        5. The trained XGBoost model predicts the new LST.

        6. Results are compared against the original scenario.
        """
        )

        st.markdown("---")

        def clip(series, low=None, high=None):

            if low is not None:
                series = np.maximum(series, low)

            if high is not None:
                series = np.minimum(series, high)

            return series

        def normalize_landcover(df):

            cols = [
                "LandCover_Bare_sparse_vegetation",
                "LandCover_Built-up land",
                "LandCover_Cropland",
                "LandCover_Grassland",
                "LandCover_Permanent_water_bodies",
                "LandCover_Shrubland",
                "LandCover_Tree cover",
            ]

            total = df[cols].sum(axis=1)

            total = total.replace(0, 1)

            df[cols] = df[cols].div(total, axis=0)

            return df
    def apply_interventions(df):

        simulated = df.copy()

        # ==========================================================
        # NDVI MODIFICATION
        # ==========================================================

        ndvi_increase = (
            green_cover * 0.0025
            + tree_cover * 0.0035
            + permeable_surface * 0.0010
        )

        simulated["NDVI"] = clip(
            simulated["NDVI"] + ndvi_increase,
            -1,
            1,
        )

        # ==========================================================
        # NDBI MODIFICATION
        # ==========================================================

        ndbi_decrease = (
            builtup_reduction * 0.0020
            + green_cover * 0.0010
            + tree_cover * 0.0010
        )

        simulated["NDBI"] = clip(
            simulated["NDBI"] - ndbi_decrease,
            -1,
            1,
        )

        # ==========================================================
        # TREE COVER
        # ==========================================================

        simulated["LandCover_Tree cover"] = clip(
            simulated["LandCover_Tree cover"]
            + tree_cover * 0.004
            + green_cover * 0.002,
            0,
            None,
        )

        # ==========================================================
        # BUILT-UP LAND
        # ==========================================================

        simulated["LandCover_Built-up land"] = clip(
            simulated["LandCover_Built-up land"]
            - builtup_reduction * 0.004
            - permeable_surface * 0.002
            - cool_roofs * 0.001,
            0,
            None,
        )

        # ==========================================================
        # CROPLAND
        # ==========================================================

        simulated["LandCover_Cropland"] = clip(
            simulated["LandCover_Cropland"]
            + green_cover * 0.0005,
            0,
            None,
        )

        # ==========================================================
        # GRASSLAND
        # ==========================================================

        simulated["LandCover_Grassland"] = clip(
            simulated["LandCover_Grassland"]
            + green_cover * 0.001
            + permeable_surface * 0.001,
            0,
            None,
        )

        # ==========================================================
        # SHRUBLAND
        # ==========================================================

        simulated["LandCover_Shrubland"] = clip(
            simulated["LandCover_Shrubland"]
            + green_cover * 0.0005,
            0,
            None,
        )

        # ==========================================================
        # BARE / SPARSE VEGETATION
        # ==========================================================

        simulated["LandCover_Bare_sparse_vegetation"] = clip(
            simulated["LandCover_Bare_sparse_vegetation"]
            - green_cover * 0.001,
            0,
            None,
        )

        # ==========================================================
        # WATER BODIES
        # ==========================================================

        simulated["LandCover_Permanent_water_bodies"] = clip(
            simulated["LandCover_Permanent_water_bodies"],
            0,
            None,
        )

        simulated = normalize_landcover(simulated)

        return simulated
    # ==========================================================
    # HOTSPOT CLASSIFICATION
    # ==========================================================

    def classify_hotspot(lst):

        if lst >= 42:
            return "Extreme"

        elif lst >= 38:
            return "Very High"

        elif lst >= 34:
            return "High"

        elif lst >= 30:
            return "Moderate"

        else:
            return "Low"

    # ==========================================================
    # RUN AI SIMULATION
    # ==========================================================

    if run_simulation:

        simulated_df = apply_interventions(simulation_df)

        before_prediction = model.predict(
            simulation_df[MODEL_FEATURES]
        )

        after_prediction = model.predict(
            simulated_df[MODEL_FEATURES]
        )

        simulated_df["LST_Before"] = before_prediction
        simulated_df["LST_After"] = after_prediction

        simulated_df["Temperature_Reduction"] = (
            simulated_df["LST_Before"]
            - simulated_df["LST_After"]
        )

        simulated_df["Hotspot_Before"] = (
            simulated_df["LST_Before"]
            .apply(classify_hotspot)
        )

        simulated_df["Hotspot_After"] = (
            simulated_df["LST_After"]
            .apply(classify_hotspot)
        )

        avg_before = simulated_df["LST_Before"].mean()
        avg_after = simulated_df["LST_After"].mean()

        max_before = simulated_df["LST_Before"].max()
        max_after = simulated_df["LST_After"].max()

        reduction = avg_before - avg_after

        hotspots_before = (
            simulated_df["Hotspot_Before"] != "Low"
        ).sum()

        hotspots_after = (
            simulated_df["Hotspot_After"] != "Low"
        ).sum()

        if hotspots_before == 0:

            improvement = 0

        else:

            improvement = (
                (hotspots_before - hotspots_after)
                / hotspots_before
            ) * 100
        # ==========================================================
        # KPI DASHBOARD
        # ==========================================================

        st.markdown("## 📊 AI Simulation Results")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpi1.metric(
            "Average LST Before",
            f"{avg_before:.2f} °C"
        )

        kpi2.metric(
            "Average LST After",
            f"{avg_after:.2f} °C",
            delta=f"-{reduction:.2f} °C"
        )

        kpi3.metric(
            "Maximum LST Before",
            f"{max_before:.2f} °C"
        )

        kpi4.metric(
            "Maximum LST After",
            f"{max_after:.2f} °C",
            delta=f"-{(max_before-max_after):.2f} °C"
        )

        st.markdown("")

        kpi5, kpi6, kpi7 = st.columns(3)

        kpi5.metric(
            "Hotspots Before",
            int(hotspots_before)
        )

        kpi6.metric(
            "Hotspots After",
            int(hotspots_after)
        )

        kpi7.metric(
            "Overall Improvement",
            f"{improvement:.1f}%"
        )

        st.markdown("---")

        # ==========================================================
        # BEFORE VS AFTER COMPARISON
        # ==========================================================

        st.subheader("📈 Average Land Surface Temperature Comparison")

        comparison_df = pd.DataFrame(
            {
                "Scenario": [
                    "Before Intervention",
                    "After Intervention"
                ],
                "Average LST": [
                    avg_before,
                    avg_after
                ]
            }
        )

        fig = px.bar(
            comparison_df,
            x="Scenario",
            y="Average LST",
            color="Scenario",
            text="Average LST",
            template="plotly_white",
            color_discrete_sequence=[
                "#E4572E",
                "#2E8B57"
            ]
        )

        fig.update_traces(
            texttemplate="%.2f °C",
            textposition="outside"
        )

        fig.update_layout(
            height=470,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Average LST (°C)"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        # ==========================================================
        # TEMPERATURE REDUCTION DISTRIBUTION
        # ==========================================================

        st.subheader("📉 Pixel-wise Temperature Reduction")

        fig = px.histogram(
            simulated_df,
            x="Temperature_Reduction",
            nbins=40,
            template="plotly_white",
            color_discrete_sequence=[
                "#4F7D50"
            ]
        )

        fig.update_layout(
            height=420,
            xaxis_title="Temperature Reduction (°C)",
            yaxis_title="Number of Pixels"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        st.markdown("---")
        # ==========================================================
        # AI HOTSPOT MAP
        # ==========================================================

        st.subheader("🛰 AI Predicted Heat Hotspots")

        hotspot_colors = {
            "Low": "#4F7D50",
            "Moderate": "#F7B733",
            "High": "#FF7A1A",
            "Very High": "#E44720",
            "Extreme": "#8B0000"
        }

        map_df = simulated_df.copy()

        fig = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            color="Hotspot_After",
            hover_name="Hotspot_After",
            hover_data={
                "Latitude":":.4f",
                "Longitude":":.4f",
                "LST_Before":":.2f",
                "LST_After":":.2f",
                "Temperature_Reduction":":.2f"
            },
            color_discrete_map=hotspot_colors,
            zoom=11,
            height=650
        )

        fig.update_traces(
            marker=dict(
                size=7,
                opacity=0.72
            )
        )

        fig.update_layout(
            mapbox_style="carto-positron",
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),
            legend_title="Hotspot Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("---")

        # ==========================================================
        # UPDATED HOTSPOT TABLE
        # ==========================================================

        st.subheader("🔥 Updated Hotspot Classification")

        hotspot_table = (
            simulated_df[
                [
                    "Latitude",
                    "Longitude",
                    "LST_Before",
                    "LST_After",
                    "Temperature_Reduction",
                    "Hotspot_Before",
                    "Hotspot_After"
                ]
            ]
            .sort_values(
                by="LST_After",
                ascending=False
            )
            .reset_index(drop=True)
        )

        hotspot_table.rename(
            columns={
                "LST_Before":"Before (°C)",
                "LST_After":"After (°C)",
                "Temperature_Reduction":"Cooling (°C)",
                "Hotspot_Before":"Category Before",
                "Hotspot_After":"Category After"
            },
            inplace=True
        )

        st.dataframe(
            hotspot_table,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ==========================================================
        # HOTSPOT SUMMARY
        # ==========================================================

        st.subheader("📍 Hotspot Category Summary")

        before_summary = (
            simulated_df["Hotspot_Before"]
            .value_counts()
            .rename("Before")
        )

        after_summary = (
            simulated_df["Hotspot_After"]
            .value_counts()
            .rename("After")
        )

        hotspot_summary = (
            pd.concat(
                [
                    before_summary,
                    after_summary
                ],
                axis=1
            )
            .fillna(0)
            .astype(int)
        )

        hotspot_summary = hotspot_summary.reindex(
            [
                "Extreme",
                "Very High",
                "High",
                "Moderate",
                "Low"
            ],
            fill_value=0
        )

        hotspot_summary = hotspot_summary.reset_index()

        hotspot_summary.columns = [
            "Hotspot Category",
            "Before",
            "After"
        ]

        fig = px.bar(
            hotspot_summary,
            x="Hotspot Category",
            y=[
                "Before",
                "After"
            ],
            barmode="group",
            template="plotly_white",
            color_discrete_sequence=[
                "#E4572E",
                "#4F7D50"
            ]
        )

        fig.update_layout(
            height=430,
            yaxis_title="Number of Pixels"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        st.markdown("---")
        # ==========================================================
        # MUNICIPAL RECOMMENDATION ENGINE
        # ==========================================================

        st.subheader("🏛 AI Municipal Recommendation")

        recommendations = []

        if avg_after >= 40:
            recommendations.append(
                "🔥 Immediate intervention is recommended for high-temperature urban zones."
            )

        if tree_cover < 30:
            recommendations.append(
                "🌳 Increase urban tree plantation to improve canopy density and shading."
            )

        if green_cover < 30:
            recommendations.append(
                "🌿 Develop additional green parks, roadside plantations, and urban forests."
            )

        if cool_roofs < 25:
            recommendations.append(
                "🏠 Promote cool roof technology for public and commercial buildings."
            )

        if permeable_surface < 25:
            recommendations.append(
                "🧱 Replace impervious pavements with permeable materials wherever feasible."
            )

        if builtup_reduction < 20:
            recommendations.append(
                "🏢 Encourage redevelopment strategies that reduce excessive built-up density."
            )

        if reduction >= 2:
            recommendations.append(
                "❄ The selected intervention scenario shows strong cooling potential and should be prioritized."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "✅ The current intervention strategy is balanced. Continue monitoring urban heat conditions periodically."
            )

        st.success("\n\n".join(recommendations))

        st.markdown("---")

        # ==========================================================
        # SIMULATION SUMMARY
        # ==========================================================

        st.subheader("📋 Simulation Summary")

        summary_df = pd.DataFrame(
            {
                "Metric": [
                    "Average LST Before (°C)",
                    "Average LST After (°C)",
                    "Temperature Reduction (°C)",
                    "Maximum LST Before (°C)",
                    "Maximum LST After (°C)",
                    "Hotspots Before",
                    "Hotspots After",
                    "Overall Improvement (%)"
                ],
                "Value": [
                    round(avg_before, 2),
                    round(avg_after, 2),
                    round(reduction, 2),
                    round(max_before, 2),
                    round(max_after, 2),
                    int(hotspots_before),
                    int(hotspots_after),
                    round(improvement, 2)
                ]
            }
        )

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ==========================================================
        # DOWNLOAD RESULTS
        # ==========================================================

        st.subheader("📥 Download AI Simulation Results")

        download_df = simulated_df.copy()

        csv = download_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📄 Download Simulation Results (CSV)",
            data=csv,
            file_name="UrbanHeat_AI_Simulation.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("---")

        # ==========================================================
        # DISCLAIMER
        # ==========================================================

        st.info(
            """
### AI Decision Support Disclaimer

Predictions are AI-based decision-support estimates generated using the
trained XGBoost Urban Heat Prediction model.

Actual cooling performance depends on:

• implementation quality

• environmental conditions

• land availability

• engineering feasibility

• maintenance practices

• climatic variability

The simulator is intended to support municipal planning and urban
heat mitigation decisions and should not replace detailed engineering
or environmental assessments.
"""
        )

    else:

        st.info(
            """
Adjust the intervention sliders and click

### 🛰 Run AI Simulation

to generate a real-time AI prediction using the trained XGBoost model.
"""
        )
            # ==========================================================
        # ADDITIONAL ANALYTICS
        # ==========================================================

        st.markdown("---")

        st.subheader("📈 Intervention Effectiveness")

        effectiveness_df = pd.DataFrame(
            {
                "Intervention": [
                    "Green Cover",
                    "Tree Plantation",
                    "Cool Roof",
                    "Permeable Surface",
                    "Built-up Reduction"
                ],
                "Selected (%)": [
                    green_cover,
                    tree_cover,
                    cool_roofs,
                    permeable_surface,
                    builtup_reduction
                ]
            }
        )

        fig = px.bar(
            effectiveness_df,
            x="Intervention",
            y="Selected (%)",
            color="Selected (%)",
            color_continuous_scale=[
                "#F7B733",
                "#FF7A1A",
                "#E44720",
                "#4F7D50"
            ],
            template="plotly_white"
        )

        fig.update_layout(
            height=420,
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title="Selected Percentage"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

        # ==========================================================
        # AI INSIGHTS
        # ==========================================================

        st.subheader("🤖 AI Insights")

        insight_1 = (
            "Higher NDVI values generally reduce predicted urban heat."
        )

        insight_2 = (
            "Reducing built-up intensity lowers the predicted LST in densely urbanized regions."
        )

        insight_3 = (
            "Tree plantation contributes both through increased NDVI and increased tree-cover proportion."
        )

        insight_4 = (
            "Combining multiple interventions usually produces greater cooling benefits than implementing a single intervention."
        )

        st.markdown(
            f"""
<div class="cool-note">

<b>Key AI Observations</b>

• {insight_1}

• {insight_2}

• {insight_3}

• {insight_4}

</div>
""",
            unsafe_allow_html=True,
        )

    # ==========================================================
    # END OF COOLING STRATEGY
    # ==========================================================
    
# ==================================================
# MODEL VALIDATION
# ==================================================

elif page == "Model Validation":

    st.header("Model Validation")

    st.markdown(
        """
        <div class="info-note">
            <b>Validation approach:</b> Dataset V2 and Dataset V3 are evaluated using
            spatial block cross-validation to reduce spatial leakage and provide a more
            realistic estimate of model performance in unseen locations.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(model_comparison, use_container_width=True, hide_index=True)

    metric_options = [
        column for column in model_comparison.columns
        if column not in ["Dataset", "Model"]
        and pd.api.types.is_numeric_dtype(model_comparison[column])
    ]

    if metric_options:
        selected_metric = st.selectbox(
            "Select performance metric",
            metric_options
        )

        fig = px.bar(
            model_comparison,
            x="Dataset",
            y=selected_metric,
            color="Dataset",
            text_auto=".3f",
            title=f"Dataset V2 vs Dataset V3: {selected_metric}",
            color_discrete_sequence=[
                "#b82025",
                "#ff7a1a",
                "#4f7d50"
            ]
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    st.info(
        "Latitude and Longitude are used only for mapping and spatial grouping. "
        "They are excluded from model features to prevent target leakage and spatial leakage."
    )
        
#===================================================
# ABOUT PROJECT
# ==================================================
elif page == "About Project":

    st.header("About the Project")

    st.markdown(
        """
        <div class="section-panel">
            <div class="section-title">Urban Heat Mitigation and Cooling Strategy Optimization</div>
            This project develops an AI/ML-powered geospatial decision-support system for
            Chhatrapati Sambhajinagar. It integrates satellite-derived NDVI, NDBI, LST,
            elevation, population, and land-cover information to detect heat-stress hotspots,
            predict urban heat, explain model drivers, identify vulnerable zones, and simulate
            cooling interventions.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Key Inputs")
        st.markdown(
            """
            - Sentinel-2 SR Harmonized  
            - Landsat 8/9 Collection 2 Level 2  
            - SRTM Elevation  
            - WorldPop India 2020  
            - Google Earth Engine  
            """
        )

    with col2:
        st.subheader("Key Outputs")
        st.markdown(
            """
            - Urban heat hotspot map  
            - XGBoost LST prediction model  
            - Spatial cross-validation results  
            - SHAP feature importance  
            - Cooling intervention comparison  
            - Heat vulnerability priority zones  
            """
        )

    st.markdown(
        """
        <div class="risk-note">
            <b>Limitations:</b> satellite-derived LST is not the same as near-surface air
            temperature. Population is used as an exposure proxy, and scenario outputs are
            decision-support estimates. Field validation and local feasibility assessment are
            required before implementation.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Team AstroByte")
    st.markdown(
        """
        - **Priyal Deshmukh** — AI/ML Lead  
        - **Srushti Bawaskar** — Geospatial & Data Lead  
        - **Rishika Deshmukh** — Research, Documentation & Dashboard Lead  
        """
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer-text">
        Team AstroByte | Bharatiya Antariksh Hackathon 2026 |
        Urban Heat Mitigation and Cooling Strategy Optimization
    </div>
    """,
    unsafe_allow_html=True
)