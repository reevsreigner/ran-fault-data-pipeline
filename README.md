# 📡 RAN Fault & KPI Dashboard

A fully simulated telecom monitoring pipeline that models **Radio Access Network (RAN)** fault logs and KPI metrics, correlates them intelligently, and visualizes site-level performance using a live dashboard.

> 🚀 **[Live Dashboard Here] - https://ran-fault-data-pipeline-9ihr5nisn7fmjkkljlppa4.streamlit.app/

---

## 🧰 Tech Stack

- **Python 3.12**
- **Pandas**, **SQLAlchemy**
- **SQLite** for temporary storage
- **Streamlit** for interactive dashboard

---

## 📊 Features

- Simulates telecom network faults across 10 sites (S101–S110)
- Generates performance KPIs (Call Drop Rate, Latency, Traffic)
- Correlates specific alarms (e.g., `A109 - Abnormal Call Drop`) with KPI spikes
- Interactive dashboard with:
  - Site filter
  - KPI time-series charts
  - Severity-colored fault logs

---

## 📦 Project Structure

├── main.py                  # Orchestrates the pipeline
├── dashboard.py             # Streamlit dashboard app
├── telecom_data.db          # Auto-generated SQLite database
├── scripts/
│   ├── simulate_faults.py   # Fault log generator
│   ├── simulate_kpis.py     # KPI generator with correlation logic
│   └── load_to_sqlite.py    # Loads generated CSVs into DB
├── data/raw/                # Stores simulated CSVs (auto-ignored)
├── requirements.txt         # Dependencies for deployment
└── .gitignore

**Run Locally**
**1. Set up environment**
python -m venv venv
venv\Scripts\activate          # On Windows
pip install -r requirements.txt


2. Generate Data
python main.py


3. Launch Dashboard
streamlit run dashboard.py


<img width="1691" height="769" alt="image" src="https://github.com/user-attachments/assets/df929bb5-26ea-487c-9f0b-8f8594e5c893" />

<img width="305" height="557" alt="image" src="https://github.com/user-attachments/assets/8352be41-bb66-4a65-94b5-a2a04601dd67" />

<img width="1863" height="744" alt="image" src="https://github.com/user-attachments/assets/304db48f-c31e-4f7e-bb3a-d909042f1f0d" />

<img width="1519" height="564" alt="image" src="https://github.com/user-attachments/assets/a3edf1ed-2095-4e7a-be6c-566c2423d865" />

<img width="1781" height="653" alt="image" src="https://github.com/user-attachments/assets/00b0a53d-f76c-4c4b-a4f2-4b32b0075cc4" />




