# scripts/load_to_sqlite.py
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# Config now points to the parent directory, assuming this is called from main.py
RAW_DIR = Path("data/raw")
DB_PATH = Path("telecom_data.db")

def load_all_data():
    """Finds the MOST RECENT generated CSVs, cleans them, and loads them."""
    try:
        # Get all matching files, sort them by name (newest first), and pick the first one.
        fault_file = sorted(RAW_DIR.glob("fault_logs_*.csv"), reverse=True)[0]
        kpi_file = sorted(RAW_DIR.glob("kpi_logs_*.csv"), reverse=True)[0]
        print(f"Found latest data files: {fault_file.name}, {kpi_file.name}")
    except IndexError:
        print("❌ ERROR: Data files not found. Please run the simulation first.")
        return

    # === LOAD & TRANSFORM DATA ===
    fault_df = pd.read_csv(fault_file, parse_dates=["Timestamp"])
    kpi_df = pd.read_csv(kpi_file, parse_dates=["Timestamp"])

    # --- Data Cleaning Step ---
    kpi_df['Call_Drop_Rate'] = kpi_df['Call_Drop_Rate'].str.replace('%', '', regex=False).astype(float)
    print("Cleaned 'Call_Drop_Rate' column.")

    # === LOAD TO DATABASE ===
    engine = create_engine(f"sqlite:///{DB_PATH}")
    fault_df.to_sql("fault_logs", con=engine, if_exists="replace", index=False)
    print("Loaded 'fault_logs' table.")
    kpi_df.to_sql("kpi_metrics", con=engine, if_exists="replace", index=False)
    print("Loaded 'kpi_metrics' table.")
    print("✅ Data loading process completed successfully.")

if __name__ == "__main__":
    # If run standalone, adjust paths to be relative to the scripts folder
    RAW_DIR = Path("../data/raw")
    DB_PATH = Path("../telecom_data.db")
    load_all_data()