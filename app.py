import html
from pathlib import Path

import streamlit as st
from streamlit_folium import st_folium

from map_module import create_antarctic_map
from preprocessing import prepare_data_for_ai
from sea_ice_prediction import generate_sea_ice_forecast

from iceberg.loader import (
    load_antarctic_icebergs,
    prepare_iceberg_data,
    get_nearby_icebergs_with_distance,
)

from risk_module import (
    calculate_sea_ice_risk,
    calculate_iceberg_risk,
    calculate_weather_risk,
    calculate_iceberg_trajectory_risk,
    generate_risk_assessment,
)

from route_module import (
    generate_candidate_routes,
    recommend_best_route,
    dynamic_reroute,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ANTARCTIC AI",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# M2 - SEA-ICE FORECAST
# =========================================================

m2_forecast_result = generate_sea_ice_forecast()

m2_forecast_value = m2_forecast_result.get("forecast")

if m2_forecast_value is None:
    m2_forecast_value = 93.0

m2_category = m2_forecast_result.get(
    "category",
    "UNKNOWN"
)


# =========================================================
# REAL ICEBERG DATA
# =========================================================

ICEBERG_FILE = Path(
    "data/AntarcticIcebergs_20260910.csv"
)

# Current vessel coordinate used by the existing
# Antarctic Folium map.
VESSEL_LATITUDE = -69.0
VESSEL_LONGITUDE = 39.0

iceberg_data_ready = False
iceberg_data = None
iceberg_records = []
nearest_iceberg = None

try:

    raw_iceberg_data = load_antarctic_icebergs(
        ICEBERG_FILE
    )

    iceberg_data = prepare_iceberg_data(
        raw_iceberg_data
    )

    iceberg_records = get_nearby_icebergs_with_distance(
        iceberg_data,
        VESSEL_LATITUDE,
        VESSEL_LONGITUDE,
        max_distance_km=10000,
    )

    if iceberg_records:

        nearest_iceberg = min(
            iceberg_records,
            key=lambda item: item["distance_km"]
        )

    iceberg_data_ready = True

except Exception as error:

    iceberg_data_ready = False
    iceberg_data = None
    iceberg_records = []
    nearest_iceberg = None
    iceberg_error = str(error)


# =========================================================
# REAL ICEBERG VALUES
# =========================================================

if nearest_iceberg:

    real_iceberg_distance = float(
        nearest_iceberg["distance_km"]
    )

    nearest_iceberg_name = str(
        nearest_iceberg["iceberg"]
    )

else:

    real_iceberg_distance = 40.0
    nearest_iceberg_name = "UNAVAILABLE"


if iceberg_data_ready and iceberg_data is not None:

    total_icebergs = len(iceberg_data)

else:

    total_icebergs = 0


# =========================================================
# COMMAND CENTER THEME
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       GLOBAL APPLICATION
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #12334a 0%,
                #081827 32%,
                #030911 72%,
                #02060b 100%
            );
        color: #eaf6ff;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    /* =====================================================
       HEADER
       ===================================================== */

    .command-header {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                rgba(12, 38, 58, 0.98),
                rgba(4, 14, 25, 0.99)
            );

        border: 1px solid #28536d;
        border-radius: 16px;

        padding: 22px 26px;
        margin-bottom: 16px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }

    .command-header::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent,
            #36d7a1,
            #4aaee8,
            transparent
        );
        opacity: 0.75;
    }

    .header-grid {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
    }

    .command-title {
        font-size: 30px;
        font-weight: 900;
        letter-spacing: 2.5px;
        color: #f4fbff;
        margin: 0;
    }

    .command-subtitle {
        font-size: 12px;
        color: #82a9bf;
        letter-spacing: 2.4px;
        margin-top: 6px;
    }

    .header-status {
        text-align: right;
        min-width: 250px;
    }

    .online {
        color: #55e0a7;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.2px;
    }

    .status-sub {
        color: #7896aa;
        font-size: 10px;
        margin-top: 6px;
        letter-spacing: 0.7px;
    }

    /* =====================================================
       SECTION HEADINGS
       ===================================================== */

    .section-title {
        color: #eaf6ff;
        font-size: 15px;
        font-weight: 850;
        letter-spacing: 1.5px;
        margin-top: 20px;
        margin-bottom: 8px;
        padding-left: 2px;
    }

    .section-title::before {
        content: "▌";
        color: #45d8a4;
        margin-right: 7px;
    }

    .section-caption {
        color: #6f8fa3;
        font-size: 10px;
        margin-top: -3px;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
    }

    /* =====================================================
       INFORMATION CARDS
       ===================================================== */

    .info-card {
        position: relative;
        overflow: hidden;

        background:
            linear-gradient(
                145deg,
                rgba(14, 36, 53, 0.98),
                rgba(6, 17, 29, 0.98)
            );

        border: 1px solid #234b63;
        border-radius: 12px;

        padding: 15px 16px;
        min-height: 105px;

        box-shadow:
            0 7px 20px rgba(0, 0, 0, 0.16),
            inset 0 1px 0 rgba(255,255,255,0.025);
    }

    .info-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: #39c996;
        opacity: 0.75;
    }

    .card-label {
        color: #7598ac;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 1.25px;
    }

    .card-value {
        color: #f0f8fd;
        font-size: 21px;
        font-weight: 850;
        margin-top: 8px;
        line-height: 1.15;
    }

    .card-small {
        color: #6f91a6;
        font-size: 9px;
        margin-top: 7px;
        letter-spacing: 0.3px;
    }

    /* =====================================================
       MAP CONTAINER
       ===================================================== */

    .map-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        background:
            linear-gradient(
                145deg,
                rgba(10, 28, 43, 0.98),
                rgba(4, 13, 23, 0.98)
            );

        border: 1px solid #234b64;
        border-bottom: none;

        border-radius: 13px 13px 0 0;

        padding: 11px 15px;
        margin-top: 3px;
    }

    .map-header-title {
        color: #eaf7ff;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .map-header-status {
        color: #55dda7;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.8px;
    }

    .map-shell {
        background: #04101a;
        border: 1px solid #234b64;
        border-radius: 0 0 13px 13px;
        padding: 6px;

        box-shadow:
            0 12px 38px rgba(0, 0, 0, 0.38),
            inset 0 1px 0 rgba(255,255,255,0.025);
    }

    /* =====================================================
       PANELS
       ===================================================== */

    .panel {
        background:
            linear-gradient(
                145deg,
                rgba(11, 29, 44, 0.99),
                rgba(4, 14, 24, 0.99)
            );

        border: 1px solid #21475f;
        border-radius: 12px;

        padding: 16px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.18);
    }

    .panel-heading {
        color: #eaf7ff;
        font-size: 13px;
        font-weight: 850;
        letter-spacing: 1px;
        margin-bottom: 9px;
    }

    .panel-line {
        height: 1px;
        background: #18384b;
        margin: 10px 0;
    }

    .risk-level {
        color: #f0f8fd;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: 0.5px;
    }

    .risk-score {
        color: #7895a7;
        font-size: 10px;
        margin-top: 5px;
    }

    /* =====================================================
       ROUTE CARDS
       ===================================================== */

    .route-card {
        background:
            linear-gradient(
                145deg,
                rgba(12, 31, 46, 0.99),
                rgba(6, 17, 28, 0.99)
            );

        border: 1px solid #21465d;
        border-radius: 10px;

        padding: 13px 14px;
        margin-bottom: 9px;

        transition: 0.2s ease;
    }

    .route-card.recommended {
        border: 1px solid #39c996;

        box-shadow:
            0 0 16px rgba(57, 201, 150, 0.10),
            inset 3px 0 0 #39c996;
    }

    .route-name {
        color: #edf8ff;
        font-size: 14px;
        font-weight: 850;
    }

    .route-data {
        color: #8ba8b8;
        font-size: 10px;
        margin-top: 6px;
    }

    .recommended-label {
        color: #50dda7;
        font-size: 8px;
        font-weight: 900;
        letter-spacing: 1.3px;
        margin-bottom: 5px;
    }

    /* =====================================================
       REROUTE
       ===================================================== */

    .reroute-panel {
        background:
            linear-gradient(
                145deg,
                rgba(11, 31, 45, 0.99),
                rgba(5, 16, 27, 0.99)
            );

        border: 1px solid #21475e;
        border-radius: 12px;
        padding: 14px;

        box-shadow:
            0 7px 22px rgba(0, 0, 0, 0.16);
    }

    /* =====================================================
       WORKFLOW
       ===================================================== */

    .workflow {
        background:
            linear-gradient(
                90deg,
                rgba(6, 18, 29, 0.99),
                rgba(10, 29, 44, 0.99)
            );

        border: 1px solid #21465d;
        border-radius: 12px;

        padding: 17px 13px;

        text-align: center;
        line-height: 2.2;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .workflow-active {
        color: #59dca9;
        font-weight: 800;
        font-size: 10px;
        letter-spacing: 0.3px;
    }

    .workflow-arrow {
        color: #526f82;
        font-size: 10px;
        margin: 0 2px;
    }

    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(9, 25, 39, 0.92),
                rgba(5, 15, 25, 0.92)
            );

        border: 1px solid #1b4057;
        border-radius: 9px;

        padding: 9px 10px;

        min-height: 72px;
    }

    [data-testid="stMetricLabel"] {
        color: #7896a8 !important;
        font-size: 9px !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #e8f5fd !important;
        font-size: 17px !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        display: none;
    }

    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071827 0%,
                #04101b 100%
            );

        border-right: 1px solid #21465d;
    }

    [data-testid="stSidebar"] h2 {
        color: #eaf7ff;
        letter-spacing: 1px;
    }

    [data-testid="stSidebar"] h3 {
        color: #8fb3c7;
        font-size: 13px;
        letter-spacing: 0.8px;
    }

    [data-testid="stSidebar"] label {
        color: #a8c0ce !important;
        font-size: 11px !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: #091d2c;
        border-color: #28516a;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #e4f1f8;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        color: #e4f1f8;
    }

    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 9px;
        border-width: 1px;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-bar {
        background:
            linear-gradient(
                90deg,
                rgba(5, 15, 25, 0.98),
                rgba(8, 24, 37, 0.98),
                rgba(5, 15, 25, 0.98)
            );

        border: 1px solid #1b3b50;
        border-radius: 10px;

        padding: 12px;
        margin-top: 20px;

        color: #66869a;
        font-size: 9px;
        text-align: center;
        letter-spacing: 0.8px;
    }

    </style>
    """
)


# =========================================================
# HEADER
# =========================================================

st.html(
    """
    <div class="command-header">
        <div class="header-grid">

            <div>
                <div class="command-title">
                    ❄️ ANTARCTIC AI
                </div>

                <div class="command-subtitle">
                    RESEARCH VESSEL COMMAND CENTER
                </div>
            </div>

            <div class="header-status">
                <div class="online">
                    ● SYSTEM ONLINE
                </div>

                <div class="status-sub">
                    AI NAVIGATION ACTIVE &nbsp; | &nbsp;
                    DECISION SUPPORT READY
                </div>
            </div>

        </div>
    </div>
    """
)


# =========================================================
# SIDEBAR - OPERATOR CONTROLS
# =========================================================

with st.sidebar:

    st.markdown("## 🚢 OPERATOR CONTROL")

    st.caption(
        "Mission configuration and environmental inputs"
    )

    start_location = st.selectbox(
        "Vessel Location",
        [
            "Research Vessel",
            "McMurdo",
            "Palmer",
            "Rothera",
            "Casey",
            "Davis",
            "Mawson",
            "Halley",
        ],
    )

    destination = st.selectbox(
        "Destination Station",
        [
            "McMurdo",
            "Palmer",
            "Rothera",
            "Amundsen-Scott",
            "Casey",
            "Davis",
            "Mawson",
            "Halley",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### 🌊 Environmental Input")

    sea_ice = st.number_input(
        "Sea-Ice Concentration (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(m2_forecast_value),
        step=1.0,
    )

    st.caption(
        f"M2 NOAA Forecast: {m2_forecast_value:.1f}% "
        f"({m2_category})"
    )

    # =====================================================
    # REAL ICEBERG DATA DISPLAY
    # =====================================================

    if iceberg_data_ready and nearest_iceberg:

        st.number_input(
            "Nearest Iceberg (km)",
            min_value=0.1,
            value=real_iceberg_distance,
            step=1.0,
            disabled=True,
        )

        st.caption(
            f"Real USNIC data: {nearest_iceberg_name} "
            f"({real_iceberg_distance:.1f} km)"
        )

    else:

        st.number_input(
            "Nearest Iceberg (km)",
            min_value=0.1,
            value=40.0,
            step=1.0,
            disabled=True,
        )

        st.caption(
            "Real iceberg data unavailable."
        )

    wind_speed = st.number_input(
        "Wind Speed (knots)",
        min_value=0.0,
        value=20.0,
        step=1.0,
    )

    wave_height = st.number_input(
        "Wave Height (m)",
        min_value=0.0,
        value=2.0,
        step=0.1,
    )

    # =====================================================
    # TRAJECTORY DEMO INPUT
    # =====================================================

    future_iceberg_distance = st.number_input(
        "Future Iceberg Distance (km)",
        min_value=0.1,
        value=35.0,
        step=1.0,
    )

    st.caption(
        "Trajectory value is currently simulation/demo data; "
        "the current USNIC CSV provides a single observation date."
    )

    st.divider()

    st.caption(
        "AI engine continuously evaluates the configured "
        "environment before route recommendation."
    )


# =========================================================
# M3 - PREPROCESSING
# =========================================================

raw_environment = {
    "sea_ice_concentration": sea_ice,
    "iceberg_distance": real_iceberg_distance,
    "wind_speed": wind_speed,
    "wave_height": wave_height,
}

preprocessed = prepare_data_for_ai(
    raw_environment
)


# =========================================================
# M4 - RISK INTELLIGENCE
# =========================================================

risk_assessment = None

sea_ice_risk = None
iceberg_risk = None
weather_risk = None
trajectory_risk = None

if preprocessed["status"] == "READY":

    processed_data = preprocessed["data"]

    sea_ice_risk = calculate_sea_ice_risk(
        processed_data["sea_ice_concentration"]
    )

    iceberg_risk = calculate_iceberg_risk(
        processed_data["iceberg_distance"]
    )

    weather_risk = calculate_weather_risk(
        processed_data["wind_speed"],
        processed_data["wave_height"],
    )

    trajectory_risk = calculate_iceberg_trajectory_risk(
        processed_data["iceberg_distance"],
        future_iceberg_distance,
    )

    risk_assessment = generate_risk_assessment(
        sea_ice_risk,
        iceberg_risk,
        weather_risk,
        trajectory_risk,
    )


# =========================================================
# M5 - ROUTE OPTIMIZATION
# =========================================================

routes = generate_candidate_routes(
    start=start_location,
    destination=destination,
)

recommended_route = recommend_best_route(
    routes
)

current_route_name = recommended_route["name"]

reroute_result = dynamic_reroute(
    routes,
    current_route_name,
)


# =========================================================
# SAFE RISK VALUES
# =========================================================

if risk_assessment:

    overall_risk_level = risk_assessment.get(
        "risk_level",
        risk_assessment.get(
            "level",
            "UNKNOWN"
        ),
    )

    overall_risk_score = risk_assessment.get(
        "risk_score",
        risk_assessment.get(
            "score",
            "N/A"
        ),
    )

else:

    overall_risk_level = "UNKNOWN"
    overall_risk_score = "N/A"


def get_risk_level(risk_data):

    if isinstance(risk_data, dict):

        return risk_data.get(
            "risk_level",
            risk_data.get(
                "level",
                "UNKNOWN"
            ),
        )

    return "UNKNOWN"


# =========================================================
# MISSION OVERVIEW
# =========================================================

st.html(
    """
    <div class="section-title">
        MISSION OVERVIEW
    </div>
    """
)

mission_col1, mission_col2, mission_col3, mission_col4 = st.columns(4)


with mission_col1:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">VESSEL LOCATION</div>
            <div class="card-value">
                {html.escape(str(start_location))}
            </div>
            <div class="card-small">
                NAVIGATION SOURCE: ACTIVE
            </div>
        </div>
        """
    )


with mission_col2:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">DESTINATION</div>
            <div class="card-value">
                {html.escape(str(destination))}
            </div>
            <div class="card-small">
                MISSION TARGET
            </div>
        </div>
        """
    )


with mission_col3:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">OVERALL RISK</div>
            <div class="card-value">
                {html.escape(str(overall_risk_level))}
            </div>
            <div class="card-small">
                SAFETY SCORE: {html.escape(str(overall_risk_score))}
            </div>
        </div>
        """
    )


with mission_col4:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">AI ROUTE OUTPUT</div>
            <div class="card-value">
                {html.escape(str(recommended_route["name"]))}
            </div>
            <div class="card-small">
                ROUTE ENGINE RECOMMENDATION
            </div>
        </div>
        """
    )


# =========================================================
# AI NAVIGATION INTELLIGENCE
# =========================================================

st.html(
    """
    <div class="section-title">
        AI NAVIGATION INTELLIGENCE
    </div>
    """
)

st.html(
    """
    <div class="section-caption">
        Environmental intelligence generated from real iceberg
        observations, NOAA sea-ice data and current mission inputs.
    </div>
    """
)

intel_col1, intel_col2, intel_col3, intel_col4 = st.columns(4)


with intel_col1:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">
                SEA-ICE CONCENTRATION
            </div>

            <div class="card-value">
                {sea_ice:.1f}%
            </div>

            <div class="card-small">
                FORECAST: {html.escape(str(m2_category))}
            </div>
        </div>
        """
    )


with intel_col2:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">
                ICEBERGS IN DATA
            </div>

            <div class="card-value">
                {total_icebergs:02d}
            </div>

            <div class="card-small">
                REAL USNIC OBSERVATIONS
            </div>
        </div>
        """
    )


with intel_col3:

    if nearest_iceberg:

        st.html(
            f"""
            <div class="info-card">
                <div class="card-label">
                    NEAREST ICEBERG
                </div>

                <div class="card-value">
                    {real_iceberg_distance:.1f} km
                </div>

                <div class="card-small">
                    {html.escape(nearest_iceberg_name)}
                    &nbsp; | &nbsp;
                    REAL OBSERVATION
                </div>
            </div>
            """
        )

    else:

        st.html(
            """
            <div class="info-card">
                <div class="card-label">
                    NEAREST ICEBERG
                </div>

                <div class="card-value">
                    N/A
                </div>

                <div class="card-small">
                    REAL DATA UNAVAILABLE
                </div>
            </div>
            """
        )


with intel_col4:

    st.html(
        f"""
        <div class="info-card">
            <div class="card-label">
                WEATHER CONDITIONS
            </div>

            <div class="card-value">
                {wind_speed:.0f} kn
            </div>

            <div class="card-small">
                WAVE HEIGHT: {wave_height:.1f} m
            </div>
        </div>
        """
    )


# =========================================================
# REAL ICEBERG DATA STATUS
# =========================================================

if iceberg_data_ready and nearest_iceberg:

    st.caption(
        f"🛰️ Real iceberg data loaded: {total_icebergs} valid "
        f"USNIC observations | Nearest: {nearest_iceberg_name} "
        f"at {real_iceberg_distance:.1f} km from the configured "
        f"vessel coordinate."
    )

else:

    st.warning(
        "Real iceberg dataset could not be loaded. "
        "Iceberg risk is using fallback values."
    )


# =========================================================
# ANTARCTIC NAVIGATION MAP
# =========================================================

st.html(
    """
    <div class="section-title">
        ANTARCTIC NAVIGATION MAP
    </div>

    <div class="section-caption">
        Geographic navigation view with vessel, destination,
        route and Antarctic operational context.
    </div>

    <div class="map-header">
        <div class="map-header-title">
            🧭 LIVE NAVIGATION DISPLAY
        </div>

        <div class="map-header-status">
            ● FOLIUM MAP ACTIVE
        </div>
    </div>

    <div class="map-shell">
    """
)

antarctic_map = create_antarctic_map()

st_folium(
    antarctic_map,
    width="stretch",
    height=700,
    key="titanshield_antarctic_map",
    returned_objects=[],
)


st.html(
    """
    </div>
    """
)


# =========================================================
# RISK + ROUTE COMMAND PANELS
# =========================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# LEFT - RISK INTELLIGENCE
# =========================================================

with left_col:

    st.html(
        """
        <div class="section-title">
            AI RISK INTELLIGENCE
        </div>
        """
    )

    if risk_assessment:

        st.html(
            f"""
            <div class="panel">

                <div class="panel-heading">
                    OVERALL NAVIGATION ASSESSMENT
                </div>

                <div class="panel-line"></div>

                <div class="risk-level">
                    {html.escape(str(overall_risk_level))}
                </div>

                <div class="risk-score">
                    Safety Score:
                    {html.escape(str(overall_risk_score))}
                </div>

            </div>
            """
        )

        st.write("")

        risk_col1, risk_col2 = st.columns(2)

        with risk_col1:

            st.metric(
                "Sea-Ice Risk",
                get_risk_level(sea_ice_risk),
            )

            st.metric(
                "Iceberg Risk",
                get_risk_level(iceberg_risk),
            )

        with risk_col2:

            st.metric(
                "Weather Risk",
                get_risk_level(weather_risk),
            )

            st.metric(
                "Trajectory Risk",
                get_risk_level(trajectory_risk),
            )

        hazards = risk_assessment.get(
            "hazards",
            []
        )

        if hazards:

            st.markdown(
                "**⚠️ DETECTED HAZARDS**"
            )

            for hazard in hazards:

                st.warning(hazard)

        else:

            st.success(
                "No major navigation hazards detected."
            )

    else:

        st.error(
            "Environmental data is not ready for AI analysis."
        )


# =========================================================
# RIGHT - ROUTE OPTIONS
# =========================================================

with right_col:

    st.html(
        """
        <div class="section-title">
            ROUTE OPTIONS
        </div>
        """
    )

    st.html(
        """
        <div class="section-caption">
            Candidate navigation routes evaluated by the route engine.
        </div>
        """
    )

    for route in routes:

        is_recommended = (
            route["name"]
            == recommended_route["name"]
        )

        route_class = (
            "route-card recommended"
            if is_recommended
            else "route-card"
        )

        recommended_label = (
            '<div class="recommended-label">'
            '● AI RECOMMENDED ROUTE'
            '</div>'
            if is_recommended
            else ""
        )

        st.html(
            f"""
            <div class="{route_class}">

                {recommended_label}

                <div class="route-name">
                    {html.escape(str(route["name"]))}
                    &nbsp; — &nbsp;
                    {html.escape(str(route["risk_level"]))}
                </div>

                <div class="route-data">
                    Distance: {route["distance_km"]:,} km
                    &nbsp; | &nbsp;
                    Fuel Cost: ₹{route["fuel_cost"]:,}
                </div>

                <div class="route-data">
                    Travel Time:
                    {route["travel_time_hours"]} hrs
                    &nbsp; | &nbsp;
                    Route Score:
                    {route.get("score", "-")}
                </div>

            </div>
            """
        )

    st.caption(
        f"Route engine recommendation: "
        f"{recommended_route['name']} "
        f"based on the configured route scoring model."
    )


# =========================================================
# DYNAMIC ROUTE REASSESSMENT
# =========================================================

st.html(
    """
    <div class="section-title">
        DYNAMIC ROUTE REASSESSMENT
    </div>

    <div class="section-caption">
        Continuous monitoring enables route reassessment when
        environmental risk conditions change.
    </div>
    """
)

reroute_col1, reroute_col2 = st.columns(
    [1, 2],
    gap="large"
)


with reroute_col1:

    st.html(
        f"""
        <div class="reroute-panel">

            <div class="card-label">
                CURRENT ACTIVE ROUTE
            </div>

            <div class="card-value">
                {html.escape(str(current_route_name))}
            </div>

            <div class="card-small">
                ● CONTINUOUS RISK MONITORING ACTIVE
            </div>

        </div>
        """
    )


with reroute_col2:

    if reroute_result:

        if reroute_result["name"] != current_route_name:

            st.warning(
                f"Route reassessment triggered: "
                f"{current_route_name} → "
                f"{reroute_result['name']}"
            )

        else:

            st.success(
                f"Current route remains "
                f"{current_route_name} "
                f"after risk reassessment."
            )

        st.caption(
            "The route engine evaluates safer alternatives when "
            "the current route reaches HIGH or CRITICAL risk."
        )


# =========================================================
# AI NAVIGATION WORKFLOW
# =========================================================

st.html(
    """
    <div class="section-title">
        AI NAVIGATION WORKFLOW
    </div>
    """
)

st.html(
    """
    <div class="workflow">

        <span class="workflow-active">DATA</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">PREPROCESSING</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">SEA-ICE ANALYSIS</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">ICEBERG DETECTION</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">TRAJECTORY PREDICTION</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">RISK ANALYSIS</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">ROUTE GENERATION</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">AI RECOMMENDATION</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">LIVE MONITORING</span>
        <span class="workflow-arrow"> → </span>

        <span class="workflow-active">DYNAMIC REROUTING</span>

    </div>
    """
)


# =========================================================
# SYSTEM STATUS
# =========================================================

st.html(
    """
    <div class="section-title">
        SYSTEM STATUS
    </div>
    """
)

s1, s2, s3, s4, s5, s6 = st.columns(6)


with s1:

    st.metric(
        "Vessel GPS",
        "ACTIVE",
    )


with s2:

    st.metric(
        "Destination",
        destination,
    )


with s3:

    st.metric(
        "Data",
        "CONNECTED",
    )


with s4:

    st.metric(
        "Satellite",
        "AVAILABLE",
    )


with s5:

    st.metric(
        "AI Model",
        "ONLINE",
    )


with s6:

    st.metric(
        "System",
        "OPERATIONAL",
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="footer-bar">
        TITANSHIELD • ANTARCTIC AI NAVIGATION SYSTEM
        &nbsp; | &nbsp;
        AI-ENABLED RESEARCH VESSEL DECISION SUPPORT
        &nbsp; | &nbsp;
        SIH26059
    </div>
    """
)
