# scripts/simulate_kpis.py
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# ... (CONFIG and DEFINITIONS are unchanged) ...
NUM_SITES = 10
KPI_RECORDS_PER_SITE = 96
OUTPUT_DIR = Path("data/raw")
TODAY = datetime.now().date()
sites = [f"S{101 + i}" for i in range(NUM_SITES)]

def generate_kpi_data(faults_map: dict):
    """Generates simulated KPI data, adjusting values based on active faults."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"kpi_logs_{TODAY}.csv"
    
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Site_ID", "Call_Drop_Rate", "Traffic_MB", "Latency_ms"])
        
        for site in sites:
            current_time = datetime.combine(TODAY, datetime.min.time())
            site_faults = faults_map.get(site, []) # Get list of faults for the site
            
            for _ in range(KPI_RECORDS_PER_SITE):
                call_drop_rate = random.uniform(0.1, 1.5)
                traffic = random.randint(50, 800)
                latency = random.randint(30, 150)
                
                # --- NEW, ROBUST CORRELATION LOGIC ---
                is_call_drop_fault_active = False
                # Define the time window we care about: the last 30 minutes
                window_start = current_time - timedelta(minutes=30)
                
                # Check if any A109 fault occurred within this window
                for fault_time, alarm_code in site_faults:
                    if alarm_code == "A109" and window_start <= fault_time <= current_time:
                        is_call_drop_fault_active = True
                        break # Found one, no need to check further

                if is_call_drop_fault_active:
                    call_drop_rate = random.uniform(5.0, 15.0) # Spike the rate!
                # --- END CORRELATION LOGIC ---

                writer.writerow([
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    site, f"{call_drop_rate:.2f}%", traffic, latency
                ])
                current_time += timedelta(minutes=15)

    print(f"✅ Simulated KPI data (with correlation) written to: {output_file}")

if __name__ == "__main__":
    print("This script is intended to be run from main.py.")