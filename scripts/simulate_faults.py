# scripts/simulate_faults.py
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# ... (CONFIG and DEFINITIONS are unchanged) ...
NUM_SITES = 10
ALARMS_PER_SITE = 48
OUTPUT_DIR = Path("data/raw")
TODAY = datetime.now().date()
sites = [f"S{101 + i}" for i in range(NUM_SITES)]
alarm_types = {
    "A101": "TX Path Loss", "A102": "VSWR High", "A103": "Power Supply Failure",
    "A104": "Cooling System Alert", "A105": "Battery Backup Low", "A106": "Over Temperature",
    "A107": "Node Unreachable", "A108": "Clock Sync Error", "A109": "Abnormal Call Drop",
    "A110": "Excessive Retransmissions"
}
severity_levels = ["Critical", "Major", "Minor", "Warning"]

def generate_fault_data():
    """
    Generates simulated fault data, writes it to a CSV, 
    and returns it as a map of {site: [(datetime, alarm_code), ...]}
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"fault_logs_{TODAY}.csv"
    
    # Store faults as a list of tuples: (datetime_object, alarm_code)
    faults_map = {site: [] for site in sites}
    
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Site_ID", "Alarm_Code", "Severity", "Description"])
        
        for site in sites:
            # Start each site's simulation at a random time in the first 15 mins
            current_time = datetime.combine(TODAY, datetime.min.time()) + timedelta(minutes=random.randint(0, 14))
            for _ in range(ALARMS_PER_SITE):
                alarm_code = random.choice(list(alarm_types.keys()))
                
                writer.writerow([
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    site, alarm_code,
                    random.choices(severity_levels, weights=[0.2, 0.3, 0.3, 0.2])[0],
                    alarm_types[alarm_code]
                ])
                
                # Append the actual datetime object to our map
                faults_map[site].append((current_time, alarm_code))
                
                current_time += timedelta(minutes=random.randint(15, 30), seconds=random.randint(0, 59))

    print(f"✅ Simulated fault data written to: {output_file}")
    return faults_map

if __name__ == "__main__":
    generate_fault_data()