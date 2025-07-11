# dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RAN Fault & KPI Dashboard",
    page_icon="📡",
    layout="wide"
)

# --- DATABASE CONNECTION ---
DB_PATH = Path("telecom_data.db")
if not DB_PATH.exists():
    st.error("Database not found! Please run `main.py` to generate the data.")
    st.stop()

engine = create_engine(f"sqlite:///{DB_PATH}")


# --- DATA LOADING FUNCTIONS (with Caching) ---
# The @st.cache_data decorator caches the output of this function.
# Streamlit will only rerun it if the input arguments change.
@st.cache_data
def load_kpi_data():
    """Load all KPI data from the database."""
    query = "SELECT * FROM kpi_metrics"
    df = pd.read_sql(query, engine, parse_dates=["Timestamp"])
    return df

@st.cache_data
def load_fault_data():
    """Load all fault data from the database."""
    query = "SELECT * FROM fault_logs"
    df = pd.read_sql(query, engine, parse_dates=["Timestamp"])
    return df

# Load the data once
kpi_df = load_kpi_data()
fault_df = load_fault_data()
site_list = sorted(kpi_df['Site_ID'].unique())


# --- SIDEBAR / FILTERS ---
st.sidebar.title("Filters")
selected_site = st.sidebar.selectbox(
    "Select a Site:",
    options=site_list,
    index=0 # Default to the first site in the list
)

st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard visualizes simulated telecom data. "
    "Use the filter above to inspect the performance and faults of a specific site."
)


# --- MAIN PAGE LAYOUT ---
st.title(f"📡 RAN Performance Dashboard: {selected_site}")

# Filter dataframes based on the selected site
site_kpi_df = kpi_df[kpi_df['Site_ID'] == selected_site]
site_fault_df = fault_df[fault_df['Site_ID'] == selected_site]


# --- KPI VISUALIZATIONS ---
st.header("Key Performance Indicators (KPIs)")

# Create two columns for our charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Drop Rate (%)")
    st.line_chart(site_kpi_df, x="Timestamp", y="Call_Drop_Rate", color="#FF4B4B") # Red color for drops

with col2:
    st.subheader("Network Latency (ms)")
    st.line_chart(site_kpi_df, x="Timestamp", y="Latency_ms", color="#0068C9")

st.subheader("Data Traffic (MB)")
st.area_chart(site_kpi_df, x="Timestamp", y="Traffic_MB")


# --- FAULT LOGS DISPLAY ---
st.header("Recent Faults")

# Style the severity column for better readability
def style_severity(s):
    color = "black"
    if s == "Critical":
        color = "red"
    elif s == "Major":
        color = "orange"
    elif s == "Minor":
        color = "blue"
    return f'color: {color}'

st.dataframe(
    site_fault_df.sort_values("Timestamp", ascending=False).style.applymap(style_severity, subset=['Severity']),
    use_container_width=True
)