import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import fastf1


# -----------------------------
# Basic App Setup
# -----------------------------
st.set_page_config(
    page_title="ApexRace AI",
    page_icon="🏎️",
    layout="wide"
)

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(239, 68, 68, 0.18), transparent 30%),
            radial-gradient(circle at top right, rgba(59, 130, 246, 0.14), transparent 30%),
            linear-gradient(135deg, #050816 0%, #0b1020 45%, #050816 100%);
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #020617 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] label {
        color: #e5e7eb !important;
        font-weight: 600;
    }

    .hero-card {
        position: relative;
        overflow: hidden;
        padding: 36px 34px;
        border-radius: 28px;
        background:
            linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(59, 130, 246, 0.12)),
            rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 24px 70px rgba(0,0,0,0.40);
        margin-bottom: 26px;
        animation: fadeUp 0.75s ease both;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        background: rgba(239, 68, 68, 0.30);
        top: -120px;
        right: -80px;
        filter: blur(18px);
        animation: floatGlow 5s ease-in-out infinite alternate;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        color: #fecaca;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 50px;
        line-height: 1.05;
        font-weight: 850;
        margin: 0;
        letter-spacing: -0.04em;
        color: #ffffff;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 18px;
        max-width: 900px;
        margin-top: 16px;
        line-height: 1.65;
    }

    .hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 24px;
    }

    .tag {
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255,255,255,0.12);
        color: #e5e7eb;
        font-size: 13px;
        font-weight: 600;
    }

    .section-title {
        font-size: 30px;
        font-weight: 800;
        margin: 34px 0 16px 0;
        letter-spacing: -0.03em;
        color: #f8fafc;
    }

    .section-caption {
        color: #94a3b8;
        font-size: 15px;
        margin-top: -6px;
        margin-bottom: 18px;
    }

    .metric-card {
        padding: 22px 20px;
        border-radius: 22px;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 18px 40px rgba(0,0,0,0.24);
        min-height: 132px;
        transition: all 0.25s ease;
        animation: fadeUp 0.7s ease both;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(248, 113, 113, 0.45);
        box-shadow: 0 22px 55px rgba(239, 68, 68, 0.14);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 850;
        letter-spacing: -0.04em;
    }

    .metric-help {
        color: #cbd5e1;
        font-size: 13px;
        margin-top: 8px;
        line-height: 1.45;
    }

    .score-card {
        padding: 26px 22px;
        border-radius: 24px;
        background:
            linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(30, 41, 59, 0.90)),
            rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(248, 113, 113, 0.22);
        box-shadow: 0 24px 70px rgba(0,0,0,0.32);
        min-height: 150px;
        transition: 0.25s ease;
        animation: fadeUp 0.8s ease both;
    }

    .score-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 24px 70px rgba(239, 68, 68, 0.18);
    }

    .score-value {
        font-size: 42px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1;
        margin-top: 10px;
    }

    .status-good {
        color: #86efac;
    }

    .status-medium {
        color: #fde68a;
    }

    .status-risk {
        color: #fca5a5;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.10);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.10);
    }

    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(248, 113, 113, 0.35);
        background: linear-gradient(135deg, #ef4444, #991b1b);
        color: white;
        font-weight: 800;
        padding: 0.75rem 1rem;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 34px rgba(239, 68, 68, 0.28);
        border: 1px solid rgba(248, 113, 113, 0.70);
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(18px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes floatGlow {
        from {
            transform: translateY(0px) scale(1);
        }
        to {
            transform: translateY(20px) scale(1.08);
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Hero Section
# -----------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-kicker">🏁 Race Strategy Intelligence</div>
        <h1 class="hero-title">🏎️ ApexRace AI</h1>
        <div class="hero-subtitle">
            Formula 1 race analytics dashboard that explains whether a driver's race result was shaped by
            tire degradation, pit-stop timing, or race pace consistency.
        </div>
        <div class="hero-tags">
            <div class="tag">Tire Degradation</div>
            <div class="tag">Pit Strategy</div>
            <div class="tag">Race Pace</div>
            <div class="tag">Driver Comparison</div>
            <div class="tag">Strategy Score</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# FastF1 Cache Setup
# -----------------------------
cache_folder = "data/cache"
os.makedirs(cache_folder, exist_ok=True)
fastf1.Cache.enable_cache(cache_folder)


# -----------------------------
# Manual Driver Name Map
# This avoids Streamlit Cloud errors from session.results.
# -----------------------------
DRIVER_FULL_NAMES = {
    "VER": "Max Verstappen (VER)",
    "PER": "Sergio Perez (PER)",
    "LAW": "Liam Lawson (LAW)",
    "TSU": "Yuki Tsunoda (TSU)",
    "LEC": "Charles Leclerc (LEC)",
    "SAI": "Carlos Sainz (SAI)",
    "HAM": "Lewis Hamilton (HAM)",
    "RUS": "George Russell (RUS)",
    "ANT": "Andrea Kimi Antonelli (ANT)",
    "NOR": "Lando Norris (NOR)",
    "PIA": "Oscar Piastri (PIA)",
    "ALO": "Fernando Alonso (ALO)",
    "STR": "Lance Stroll (STR)",
    "GAS": "Pierre Gasly (GAS)",
    "OCO": "Esteban Ocon (OCO)",
    "DOO": "Jack Doohan (DOO)",
    "COL": "Franco Colapinto (COL)",
    "ALB": "Alexander Albon (ALB)",
    "SAR": "Logan Sargeant (SAR)",
    "BEA": "Oliver Bearman (BEA)",
    "HUL": "Nico Hulkenberg (HUL)",
    "MAG": "Kevin Magnussen (MAG)",
    "BOT": "Valtteri Bottas (BOT)",
    "ZHO": "Zhou Guanyu (ZHO)",
    "BOR": "Gabriel Bortoleto (BOR)",
    "RIC": "Daniel Ricciardo (RIC)",
    "HAD": "Isack Hadjar (HAD)",
}


# -----------------------------
# Schedule Loader
# -----------------------------
@st.cache_data(show_spinner=True)
def get_race_schedule(year):
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    schedule = schedule[schedule["RoundNumber"] > 0].copy()
    schedule = schedule.sort_values("RoundNumber")

    races = []

    for _, row in schedule.iterrows():
        round_number = int(row["RoundNumber"])
        event_name = str(row["EventName"])

        races.append({
            "round": round_number,
            "event_name": event_name,
            "label": f"Round {round_number} - {event_name}"
        })

    return races


# -----------------------------
# Race Data Loader
# -----------------------------
@st.cache_data(show_spinner=True)
def load_race_data(year, race_round):
    session = fastf1.get_session(year, race_round, "R")

    session.load(
        laps=True,
        telemetry=False,
        weather=False,
        messages=False
    )

    laps = session.laps.copy()

    if laps.empty:
        raise ValueError("No lap data found for this race. Try another completed race.")

    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()
    laps = laps.dropna(subset=["LapTimeSeconds"])

    driver_name_map = {}

    for code in laps["Driver"].dropna().unique():
        code = str(code)
        driver_name_map[code] = DRIVER_FULL_NAMES.get(code, code)

    return laps, driver_name_map


# -----------------------------
# Helper Functions
# -----------------------------
def get_clean_laps(driver_laps):
    clean_laps = driver_laps.copy()
    clean_laps = clean_laps.dropna(subset=["LapTimeSeconds", "Compound"])

    if "PitOutTime" in clean_laps.columns:
        clean_laps = clean_laps[clean_laps["PitOutTime"].isna()]

    if "PitInTime" in clean_laps.columns:
        clean_laps = clean_laps[clean_laps["PitInTime"].isna()]

    if "IsAccurate" in clean_laps.columns:
        accurate_laps = clean_laps[clean_laps["IsAccurate"] == True]
        if len(accurate_laps) >= 5:
            clean_laps = accurate_laps

    if clean_laps.empty:
        return clean_laps

    median_lap = clean_laps["LapTimeSeconds"].median()

    clean_laps = clean_laps[
        (clean_laps["LapTimeSeconds"] >= median_lap - 5) &
        (clean_laps["LapTimeSeconds"] <= median_lap + 12)
    ]

    return clean_laps


def add_rolling_pace(clean_laps):
    pace_laps = clean_laps.copy()
    pace_laps = pace_laps.sort_values("LapNumber")

    if pace_laps.empty:
        return pace_laps

    pace_laps["PaceTrend"] = (
        pace_laps
        .groupby("Stint")["LapTimeSeconds"]
        .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
    )

    return pace_laps


def calculate_consistency_score(clean_laps):
    if clean_laps.empty:
        return 0

    lap_std = clean_laps["LapTimeSeconds"].std()

    if pd.isna(lap_std):
        return 0

    score = max(0, 100 - (lap_std * 10))
    return round(score, 2)


def build_tire_degradation_table(clean_laps):
    tire_laps = clean_laps.dropna(
        subset=["TyreLife", "LapTimeSeconds", "Compound"]
    ).copy()

    if tire_laps.empty:
        return tire_laps

    tire_summary = tire_laps.groupby(
        ["Compound", "TyreLife"],
        as_index=False
    ).agg(
        AvgLapTime=("LapTimeSeconds", "mean"),
        LapCount=("LapTimeSeconds", "count")
    )

    tire_summary["AvgLapTime"] = tire_summary["AvgLapTime"].round(3)

    return tire_summary


def calculate_tire_risk(clean_laps):
    tire_laps = clean_laps.dropna(
        subset=["TyreLife", "LapTimeSeconds", "Compound", "Stint"]
    ).copy()

    if tire_laps.empty:
        return {
            "risk": "Unknown",
            "slope": 0,
            "message": "Not enough tire data available."
        }

    slopes = []

    for _, stint_data in tire_laps.groupby("Stint"):
        stint_data = stint_data.sort_values("TyreLife")

        if len(stint_data) >= 5 and stint_data["TyreLife"].nunique() >= 3:
            x = stint_data["TyreLife"].astype(float)
            y = stint_data["LapTimeSeconds"].astype(float)

            try:
                slope = np.polyfit(x, y, 1)[0]
                slopes.append(slope)
            except Exception:
                pass

    if not slopes:
        return {
            "risk": "Unknown",
            "slope": 0,
            "message": "Not enough clean stint data to estimate tire risk."
        }

    max_slope = max(slopes)

    if max_slope > 0.18:
        risk = "High"
        message = "Lap times increased strongly as tire age increased."
    elif max_slope > 0.08:
        risk = "Medium"
        message = "Lap times showed moderate tire degradation."
    else:
        risk = "Low"
        message = "Lap times stayed mostly stable as tires aged."

    return {
        "risk": risk,
        "slope": round(max_slope, 3),
        "message": message
    }


def detect_tire_drop_window(clean_laps):
    tire_laps = clean_laps.dropna(
        subset=["LapNumber", "TyreLife", "LapTimeSeconds", "Stint"]
    ).copy()

    if tire_laps.empty:
        return {
            "text": "No clear tire drop detected",
            "start": None,
            "end": None,
            "drop_lap": None
        }

    drop_laps = []

    for _, stint_data in tire_laps.groupby("Stint"):
        stint_data = stint_data.sort_values("LapNumber")

        if len(stint_data) < 5:
            continue

        baseline = stint_data["LapTimeSeconds"].quantile(0.30)

        possible_drop = stint_data[
            (stint_data["TyreLife"] >= 5) &
            (stint_data["LapTimeSeconds"] > baseline + 1.0)
        ]

        if not possible_drop.empty:
            drop_lap = int(possible_drop["LapNumber"].iloc[0])
            drop_laps.append(drop_lap)

    if not drop_laps:
        return {
            "text": "No clear tire drop detected",
            "start": None,
            "end": None,
            "drop_lap": None
        }

    first_drop_lap = min(drop_laps)
    start_window = max(1, first_drop_lap - 2)
    end_window = first_drop_lap + 2

    return {
        "text": f"Laps {start_window} - {end_window}",
        "start": start_window,
        "end": end_window,
        "drop_lap": first_drop_lap
    }


def get_actual_pit_laps(driver_laps):
    if driver_laps.empty or "Stint" not in driver_laps.columns:
        return []

    stint_table = driver_laps.groupby("Stint").agg(
        Start_Lap=("LapNumber", "min"),
        End_Lap=("LapNumber", "max")
    ).reset_index()

    stint_table = stint_table.sort_values("Stint")

    if len(stint_table) <= 1:
        return []

    pit_laps = []

    for i in range(len(stint_table) - 1):
        pit_lap = int(stint_table.iloc[i]["End_Lap"])
        pit_laps.append(pit_lap)

    return pit_laps


def evaluate_pit_timing(actual_pit_laps, pit_window):
    if pit_window["start"] is None:
        return {
            "rating": "No Clear Drop",
            "message": "No strong tire drop window was detected."
        }

    if not actual_pit_laps:
        return {
            "rating": "No Pit Stop",
            "message": "No pit stop was detected even though tire drop was estimated."
        }

    start = pit_window["start"]
    end = pit_window["end"]
    drop_lap = pit_window["drop_lap"]

    closest_pit = min(actual_pit_laps, key=lambda lap: abs(lap - drop_lap))

    if start <= closest_pit <= end:
        rating = "Good"
        message = f"Pit stop around lap {closest_pit} was close to the suggested window."
    elif closest_pit < start:
        rating = "Early"
        message = f"Pit stop around lap {closest_pit} may have been early."
    else:
        rating = "Late"
        message = f"Pit stop around lap {closest_pit} may have been late."

    return {
        "rating": rating,
        "message": message
    }


def calculate_strategy_score(consistency_score, tire_risk, pit_rating):
    score = 100

    if consistency_score < 50:
        score -= 25
    elif consistency_score < 70:
        score -= 15
    elif consistency_score < 85:
        score -= 5

    if tire_risk == "High":
        score -= 25
    elif tire_risk == "Medium":
        score -= 12
    elif tire_risk == "Unknown":
        score -= 5

    if pit_rating == "Late":
        score -= 15
    elif pit_rating == "Early":
        score -= 10
    elif pit_rating == "No Pit Stop":
        score -= 20

    score = max(0, min(100, score))

    if score >= 85:
        status = "Excellent Strategy"
    elif score >= 70:
        status = "Good Strategy"
    elif score >= 55:
        status = "Strategy Review Needed"
    else:
        status = "High Strategy Risk"

    return score, status


def get_status_class(status_text):
    if "Excellent" in status_text or "Good" in status_text:
        return "status-good"
    if "Review" in status_text or "Medium" in status_text:
        return "status-medium"
    return "status-risk"


def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.25)",
        font=dict(color="#e5e7eb"),
        title_font=dict(size=20, color="#ffffff"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(255,255,255,0.10)",
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=60, b=35)
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.08)"
    )

    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.08)"
    )

    return fig


def metric_card(label, value, help_text=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """


def score_card(label, value, help_text="", status_class=""):
    return f"""
    <div class="score-card">
        <div class="metric-label">{label}</div>
        <div class="score-value {status_class}">{value}</div>
        <div class="metric-help">{help_text}</div>
    </div>
    """


# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Race Selection")

year = st.sidebar.selectbox(
    "Select Season",
    [2026, 2025, 2024, 2023, 2022, 2021],
    index=1
)

try:
    race_options = get_race_schedule(year)
except Exception as e:
    st.error("Could not load race schedule for this season.")
    st.code(str(e))
    st.stop()

if not race_options:
    st.warning("No race schedule found for this season.")
    st.stop()

race_labels = [race["label"] for race in race_options]

selected_race_label = st.sidebar.selectbox(
    "Select Race",
    race_labels
)

selected_race = next(
    race for race in race_options
    if race["label"] == selected_race_label
)

race_round = selected_race["round"]
race_name = selected_race["event_name"]

load_button = st.sidebar.button("Load Race Data")


# -----------------------------
# Load Button Logic
# -----------------------------
if load_button:
    try:
        with st.spinner("Loading F1 race data... Please wait."):
            laps, driver_name_map = load_race_data(year, race_round)

        st.session_state["laps"] = laps
        st.session_state["driver_name_map"] = driver_name_map
        st.session_state["loaded_year"] = year
        st.session_state["loaded_race"] = race_name
        st.session_state["loaded_round"] = race_round

        st.success("Race data loaded successfully!")

    except Exception as e:
        st.error("Something went wrong while loading the race data.")
        st.write("Try another completed race or season.")
        st.warning("Future 2026 races may not load until FastF1 race data is available.")
        st.code(str(e))


# -----------------------------
# Dashboard Display
# -----------------------------
if "laps" in st.session_state:
    laps = st.session_state["laps"]
    driver_name_map = st.session_state["driver_name_map"]

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Loaded Race</div>
            <div class="metric-value">
                {st.session_state['loaded_year']} {st.session_state['loaded_race']}
            </div>
            <div class="metric-help">Round {st.session_state['loaded_round']} • Race session data loaded successfully</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    drivers = sorted(laps["Driver"].dropna().unique())

    driver_display_options = [
        driver_name_map.get(driver, driver)
        for driver in drivers
    ]

    display_to_code = {
        driver_name_map.get(driver, driver): driver
        for driver in drivers
    }

    selected_driver_display = st.sidebar.selectbox(
        "Select Driver",
        driver_display_options
    )

    selected_driver = display_to_code[selected_driver_display]

    compare_display_options = [
        option for option in driver_display_options
        if option != selected_driver_display
    ]

    if compare_display_options:
        compare_driver_display = st.sidebar.selectbox(
            "Compare With Driver",
            compare_display_options
        )
        compare_driver = display_to_code[compare_driver_display]
    else:
        compare_driver_display = None
        compare_driver = None

    driver_laps = laps[laps["Driver"] == selected_driver].copy()
    clean_driver_laps = get_clean_laps(driver_laps)
    pace_driver_laps = add_rolling_pace(clean_driver_laps)

    if driver_laps.empty:
        st.error("No lap data found for this driver.")

    else:
        total_laps = int(driver_laps["LapNumber"].max())

        if clean_driver_laps.empty:
            best_lap = round(driver_laps["LapTimeSeconds"].min(), 3)
            avg_lap = round(driver_laps["LapTimeSeconds"].mean(), 3)
        else:
            best_lap = round(clean_driver_laps["LapTimeSeconds"].min(), 3)
            avg_lap = round(clean_driver_laps["LapTimeSeconds"].mean(), 3)

        pit_stops = max(0, driver_laps["Stint"].nunique() - 1)
        actual_pit_laps = get_actual_pit_laps(driver_laps)

        consistency_score = calculate_consistency_score(clean_driver_laps)
        tire_info = calculate_tire_risk(clean_driver_laps)
        pit_window = detect_tire_drop_window(clean_driver_laps)
        pit_timing = evaluate_pit_timing(actual_pit_laps, pit_window)

        strategy_score, strategy_status = calculate_strategy_score(
            consistency_score,
            tire_info["risk"],
            pit_timing["rating"]
        )

        status_class = get_status_class(strategy_status)

        # -----------------------------
        # Race Overview
        # -----------------------------
        st.markdown('<div class="section-title">Race Overview</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Clean race metrics after removing pit laps and unusual outlier laps.</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.markdown(metric_card("Total Laps", total_laps, "Race distance completed"), unsafe_allow_html=True)
        col2.markdown(metric_card("Best Clean Lap", f"{best_lap}s", "Fastest stable lap"), unsafe_allow_html=True)
        col3.markdown(metric_card("Avg Clean Lap", f"{avg_lap}s", "Average race pace"), unsafe_allow_html=True)
        col4.markdown(metric_card("Pit Stops", pit_stops, "Detected stint changes"), unsafe_allow_html=True)
        col5.markdown(metric_card("Consistency", f"{consistency_score}/100", "Higher means steadier pace"), unsafe_allow_html=True)

        # -----------------------------
        # Strategy Scorecard
        # -----------------------------
        st.markdown('<div class="section-title">Strategy Scorecard</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">A single strategy rating based on tire degradation, pit timing, and driver consistency.</div>',
            unsafe_allow_html=True
        )

        score_col1, score_col2, score_col3, score_col4 = st.columns(4)

        score_col1.markdown(
            score_card("Strategy Score", f"{strategy_score}/100", "Overall strategy quality", status_class),
            unsafe_allow_html=True
        )

        score_col2.markdown(
            score_card("Tire Risk", tire_info["risk"], tire_info["message"]),
            unsafe_allow_html=True
        )

        score_col3.markdown(
            score_card("Pit Timing", pit_timing["rating"], pit_timing["message"]),
            unsafe_allow_html=True
        )

        score_col4.markdown(
            score_card("Final Status", strategy_status, "Main race strategy conclusion", status_class),
            unsafe_allow_html=True
        )

        with st.expander("How this score works"):
            st.write(
                "The score uses three simple analytics signals: tire degradation risk, "
                "pit-stop timing, and lap-time consistency. Higher score means the driver's "
                "race strategy looked stronger based on clean race pace."
            )

        # -----------------------------
        # 1. Clean Race Pace Chart
        # -----------------------------
        st.markdown('<div class="section-title">1. Clean Race Pace Trend</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">This chart removes pit laps and unusual slow laps, then uses a 3-lap rolling average.</div>',
            unsafe_allow_html=True
        )

        if pace_driver_laps.empty:
            st.warning("No clean laps available for this driver.")
        else:
            fig_lap = px.line(
                pace_driver_laps,
                x="LapNumber",
                y="PaceTrend",
                color="Compound",
                markers=True,
                title=f"{selected_driver_display} Clean Race Pace Trend",
                labels={
                    "LapNumber": "Lap Number",
                    "PaceTrend": "Clean Lap Time Trend (seconds)",
                    "Compound": "Tire Compound"
                }
            )

            fig_lap.update_traces(line=dict(width=3), marker=dict(size=6))
            fig_lap = style_chart(fig_lap)

            st.plotly_chart(fig_lap, use_container_width=True)

        # -----------------------------
        # 2. Tire Degradation Chart
        # -----------------------------
        st.markdown('<div class="section-title">2. Tire Degradation Analysis</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">A rising line usually means the tire is losing performance as it gets older.</div>',
            unsafe_allow_html=True
        )

        tire_summary = build_tire_degradation_table(clean_driver_laps)

        if tire_summary.empty:
            st.warning("Not enough tire data available.")
        else:
            fig_tire = px.line(
                tire_summary,
                x="TyreLife",
                y="AvgLapTime",
                color="Compound",
                markers=True,
                title=f"{selected_driver_display} Tire Degradation Trend",
                labels={
                    "TyreLife": "Tire Age / Laps Used",
                    "AvgLapTime": "Average Lap Time (seconds)",
                    "Compound": "Tire Compound"
                }
            )

            fig_tire.update_traces(line=dict(width=3), marker=dict(size=7))
            fig_tire = style_chart(fig_tire)

            st.plotly_chart(fig_tire, use_container_width=True)

            with st.expander("View tire degradation table"):
                st.dataframe(tire_summary, use_container_width=True)

        # -----------------------------
        # 3. Pit Strategy
        # -----------------------------
        st.markdown('<div class="section-title">3. Pit Stop Strategy</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">This table shows each stint, tire compound, stint length, and average lap time.</div>',
            unsafe_allow_html=True
        )

        stint_table = driver_laps.groupby("Stint").agg(
            Start_Lap=("LapNumber", "min"),
            End_Lap=("LapNumber", "max"),
            Tire_Compound=("Compound", "first"),
            Average_Lap_Time=("LapTimeSeconds", "mean")
        ).reset_index()

        stint_table["Average_Lap_Time"] = stint_table["Average_Lap_Time"].round(3)

        st.dataframe(stint_table, use_container_width=True)

        st.info(f"Suggested pit window based on tire drop: **{pit_window['text']}**")

        if actual_pit_laps:
            st.write(f"Actual pit lap(s): **{actual_pit_laps}**")
        else:
            st.write("Actual pit lap(s): **No pit stop detected**")

        # -----------------------------
        # 4. Driver Comparison
        # -----------------------------
        st.markdown('<div class="section-title">4. Driver Comparison</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-caption">Compare clean race pace, best lap, consistency, and pit-stop count.</div>',
            unsafe_allow_html=True
        )

        if compare_driver is not None:
            compare_laps = laps[laps["Driver"] == compare_driver].copy()
            clean_compare_laps = get_clean_laps(compare_laps)
            pace_compare_laps = add_rolling_pace(clean_compare_laps)

            if not compare_laps.empty and not clean_compare_laps.empty:
                selected_avg = round(clean_driver_laps["LapTimeSeconds"].mean(), 3)
                compare_avg = round(clean_compare_laps["LapTimeSeconds"].mean(), 3)

                selected_best = round(clean_driver_laps["LapTimeSeconds"].min(), 3)
                compare_best = round(clean_compare_laps["LapTimeSeconds"].min(), 3)

                selected_consistency = calculate_consistency_score(clean_driver_laps)
                compare_consistency = calculate_consistency_score(clean_compare_laps)

                selected_pits = max(0, driver_laps["Stint"].nunique() - 1)
                compare_pits = max(0, compare_laps["Stint"].nunique() - 1)

                comparison_table = pd.DataFrame({
                    "Metric": [
                        "Average Clean Lap Time",
                        "Best Clean Lap Time",
                        "Consistency Score",
                        "Pit Stops"
                    ],
                    selected_driver_display: [
                        f"{selected_avg}s",
                        f"{selected_best}s",
                        f"{selected_consistency}/100",
                        selected_pits
                    ],
                    compare_driver_display: [
                        f"{compare_avg}s",
                        f"{compare_best}s",
                        f"{compare_consistency}/100",
                        compare_pits
                    ]
                })

                st.dataframe(comparison_table, use_container_width=True)

                combined_laps = pd.concat([
                    pace_driver_laps.assign(SelectedDriver=selected_driver_display),
                    pace_compare_laps.assign(SelectedDriver=compare_driver_display)
                ])

                fig_compare = px.line(
                    combined_laps,
                    x="LapNumber",
                    y="PaceTrend",
                    color="SelectedDriver",
                    title=f"{selected_driver_display} vs {compare_driver_display} Clean Race Pace",
                    labels={
                        "LapNumber": "Lap Number",
                        "PaceTrend": "Clean Lap Time Trend (seconds)",
                        "SelectedDriver": "Driver"
                    }
                )

                fig_compare.update_traces(line=dict(width=3))
                fig_compare = style_chart(fig_compare)

                st.plotly_chart(fig_compare, use_container_width=True)

                if selected_avg < compare_avg:
                    st.success(
                        f"{selected_driver_display} had better average clean race pace than "
                        f"{compare_driver_display}."
                    )
                elif selected_avg > compare_avg:
                    st.success(
                        f"{compare_driver_display} had better average clean race pace than "
                        f"{selected_driver_display}."
                    )
                else:
                    st.info("Both drivers had almost the same average clean race pace.")

        # -----------------------------
        # 5. Race Insight Summary
        # -----------------------------
        st.markdown('<div class="section-title">5. Race Insight Summary</div>', unsafe_allow_html=True)

        if consistency_score >= 85:
            consistency_text = "The driver showed strong race pace consistency."
        elif consistency_score >= 70:
            consistency_text = "The driver had decent consistency with some lap-time variation."
        else:
            consistency_text = "The driver had low consistency, meaning lap times changed a lot during the race."

        with st.container(border=True):
            st.markdown(f"### Driver Analyzed: {selected_driver_display}")

            st.markdown(f"""
**Race:** {st.session_state['loaded_year']} {st.session_state['loaded_race']}

**Strategy Score:** {strategy_score}/100

**Final Status:** {strategy_status}

**Key Finding:** {selected_driver_display}'s best clean lap was **{best_lap}s**, with an average clean lap of **{avg_lap}s**.

**Tire Risk:** {tire_info['risk']} — {tire_info['message']}

**Pit Strategy:** Suggested pit window was **{pit_window['text']}**. {pit_timing['message']}

**Pit Stops:** {selected_driver_display} completed **{pit_stops}** pit stop(s).

**Consistency:** {consistency_text}

**Actionable Impact:** This helps explain whether the driver's race result was more affected by tire degradation, pit-stop timing, or race pace consistency.
""")

else:
    st.info("Select season and race from dropdown, then click **Load Race Data**.")