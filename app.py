import os
import pandas as pd
import plotly.express as px
import streamlit as st


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
# HELPER FUNCTIONS
# ==================================================

def get_kpi_value(kpi_dict, possible_names, default=0):
    for name in possible_names:
        if name in kpi_dict:
            return kpi_dict[name]
    return default


def clean_map_columns(dataframe, columns_to_keep):
    return [column for column in columns_to_keep if column in dataframe.columns]


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
            title="",
            bgcolor="rgba(255,253,249,0.88)",
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
    color_sequence=None,
    color_map=None,
    height=600
):
    fig = px.scatter_mapbox(
        dataframe,
        lat="Latitude",
        lon="Longitude",
        color=color_column,
        hover_data=hover_columns,
        zoom=11.2,
        height=height,
        title=title,
        color_discrete_sequence=color_sequence,
        color_discrete_map=color_map
    )

    # IMPORTANT:
    # scatter_mapbox marker does NOT support marker.line.
    fig.update_traces(
        marker=dict(
            size=7,
            opacity=0.68
        )
    )

    return style_map(fig, zoom=11.2)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown("## ☀️ UrbanHeat AI")
st.sidebar.caption("Heat to Cool Strategy")

st.sidebar.markdown("---")
st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Select dashboard section",
    [
        "Project Overview",
        "Urban Heat Hotspots",
        "Heat Drivers",
        "Heat Vulnerability",
        "Cooling Strategy",
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

        heat_options = sorted(hotspot_map["Heat_Category"].dropna().astype(str).unique())

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
                title="Urban Heat Hotspots",
                color_sequence=["#f6c64b", "#ff9a22", "#f0522d", "#a91f26"],
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
                .reset_index()
            )
            heat_counts.columns = ["Heat Category", "Count"]

            fig = px.pie(
                heat_counts,
                names="Heat Category",
                values="Count",
                hole=0.64,
                color="Heat Category",
                color_discrete_sequence=[
                    "#f6c64b",
                    "#ff9a22",
                    "#f0522d",
                    "#a91f26"
                ]
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
                    title="",
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
            title=""
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="section-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">❄️ Cooling Potential (°C)</div>', unsafe_allow_html=True)

        if len(scenario_summary) > 0:
            for _, row in scenario_summary.iterrows():
                scenario_name = str(row["Scenario"])
                cooling_value = float(row["Mean_Cooling_C"])

                if "Green" in scenario_name or "Vegetation" in scenario_name:
                    st.markdown(
                        f"""
                        <div class="cool-note">
                            <b>🌿 {scenario_name}</b><br>
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
                            <b>🏙️ {scenario_name}</b><br>
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
            and scenario cooling potential together to prioritize interventions.
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
            temperature and prioritize concentrated hotspot zones for intervention.
        </div>
        """,
        unsafe_allow_html=True
    )

    heat_options = sorted(hotspot_map["Heat_Category"].dropna().astype(str).unique())

    selected_heat = st.multiselect(
        "Select heat categories",
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
            title="Urban Heat-Stress Distribution",
            color_sequence=["#f6c64b", "#ff9a22", "#f0522d", "#a91f26"],
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
            strongly influence predicted land surface temperature in the XGBoost model.
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
        height=500
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

    vulnerability_options = sorted(
        vulnerability_map["Vulnerability_Category"].dropna().astype(str).unique()
    )

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
            title="Population-Aware Heat Vulnerability",
            color_sequence=["#f6c64b", "#ffad4d", "#ed7358", "#a91f26"],
            height=610
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected vulnerability categories.")

    st.subheader("Top High-Priority Vulnerability Zones")
    st.dataframe(vulnerability_zones, use_container_width=True, hide_index=True)


# ==================================================
# COOLING STRATEGY
# ==================================================

elif page == "Cooling Strategy":

    st.header("Cooling Strategy Planning")

    st.markdown(
        """
        <div class="cool-note">
            <b>Purpose:</b> compare predicted cooling effects from intervention scenarios
            and identify the best cooling strategy for each location.
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = px.bar(
        scenario_summary,
        x="Scenario",
        y="Mean_Cooling_C",
        text="Mean_Cooling_C",
        title="Cooling Potential by Strategy",
        color="Scenario",
        color_discrete_map={
            "Urban greening": "#4f7d50",
            "Cool/permeable surfaces": "#4d83b8"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f} °C",
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        showlegend=False,
        height=380,
        yaxis_title="Predicted Cooling (°C)",
        xaxis_title=""
    )

    st.plotly_chart(style_chart(fig), use_container_width=True)

    intervention_options = sorted(
        scenario_map["Recommended_Intervention"].dropna().astype(str).unique()
    )

    selected_intervention = st.selectbox(
        "Filter map by recommended intervention",
        options=["All"] + intervention_options
    )

    if selected_intervention == "All":
        filtered_scenarios = scenario_map.copy()
    else:
        filtered_scenarios = scenario_map[
            scenario_map["Recommended_Intervention"].astype(str)
            == selected_intervention
        ].copy()

    if len(filtered_scenarios) > 0:
        hover_columns = clean_map_columns(
            filtered_scenarios,
            [
                "Baseline_Predicted_LST_C",
                "Greening_Cooling_C",
                "Cool_Surface_Cooling_C",
                "Best_Cooling_C",
                "Population",
                "Zone_ID"
            ]
        )

        fig = make_small_clean_map(
            dataframe=filtered_scenarios,
            color_column="Recommended_Intervention",
            hover_columns=hover_columns,
            title="Recommended Cooling Intervention by Location",
            color_map={
                "Urban greening": "#4f7d50",
                "Cool/permeable surfaces": "#4d83b8"
            },
            height=610
        )

        # Smaller and more transparent cooling points
        fig.update_traces(
            marker=dict(
                size=6,
                opacity=0.56
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No locations match the selected intervention.")

    st.subheader("Top Zones by Cooling Potential")
    st.dataframe(intervention_zones, use_container_width=True, hide_index=True)

    st.warning(
        "Cooling values are model-based comparative estimates. Final intervention "
        "selection should also consider cost, land availability, feasibility, and field validation."
    )


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
        selected_metric = st.selectbox("Select performance metric", metric_options)

        fig = px.bar(
            model_comparison,
            x="Dataset",
            y=selected_metric,
            color="Dataset",
            text_auto=".3f",
            title=f"Dataset V2 vs Dataset V3: {selected_metric}",
            color_discrete_sequence=["#b82025", "#ff7a1a", "#4f7d50"]
        )

        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.info(
        "Latitude and Longitude are used only for mapping and spatial grouping. "
        "They are excluded from model features to prevent target leakage and spatial leakage."
    )


# ==================================================
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