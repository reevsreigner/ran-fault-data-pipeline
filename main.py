# main.py (in the root folder)
from scripts.simulate_faults import generate_fault_data
from scripts.simulate_kpis import generate_kpi_data
from scripts.load_to_sqlite import load_all_data

def run_pipeline():
    """Executes the entire data pipeline from generation to loading."""
    print("--- (1/3) Starting Fault Data Generation ---")
    faults_data_map = generate_fault_data()
    
    print("\n--- (2/3) Starting KPI Data Generation (with Correlation) ---")
    generate_kpi_data(faults_data_map)
    
    print("\n--- (3/3) Loading All Data into SQLite ---")
    load_all_data()

    print("\n✅ Pipeline execution complete.")

if __name__ == "__main__":
    run_pipeline()