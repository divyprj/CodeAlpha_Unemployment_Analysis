# 📈 Unemployment Analysis with Python

An interactive **Streamlit dashboard** that performs comprehensive analysis of unemployment trends in India during the **2019–2020 period**, with a special focus on the economic impact of the **COVID-19 lockdowns**.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.15+-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Features

- **🧹 Automated Data Pipeline** - Downloads, cleans, and processes the CMIE unemployment datasets automatically
- **📊 Interactive Dashboard** - Premium dark-themed UI with glassmorphism styling and smooth animations
- **📈 National Trends** - Track employment rate, labour participation, and employed population over time
- **🗺️ State-wise Breakdown** - Compare unemployment across Indian states with interactive filters
- **🦠 COVID-19 Impact Analysis** - Quantify the lockdown shock with pre vs. post-lockdown statistics
- **🏢 Rural vs Urban Dynamics** - Analyze disparities between rural and urban employment patterns
- **💡 Policy Insights** - Data-driven policy recommendations for economic resilience

## 🖼️ Dashboard Sections

| Section | Description |
|---------|-------------|
| **Dashboard Overview** | Key statistics, data preview, and KPI cards |
| **National Trends** | Time-series charts of unemployment rate, employment, and labour participation |
| **State Breakdown** | Multi-select state comparison and lockdown-period state rankings |
| **COVID-19 Impact** | Pre-lockdown vs. lockdown KPIs, period summary table, state-by-state spike chart |
| **Rural vs Urban** | Area-wise trend lines, summary statistics, and donut chart breakdown |
| **Policy Insights** | Economic recommendations based on data findings |

## 🚀 Quick Start

### Using Batch Files (Windows)

```bash
# 1. Install dependencies (creates virtual environment)
install.bat

# 2. Run the dashboard
run.bat

# 3. Uninstall (removes virtual environment)
uninstall.bat
```

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate    # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**

## 📁 Project Structure

```
Unemployment Analysis with Python/
├── .streamlit/
│   └── config.toml          # Streamlit dark theme configuration
├── data/                     # Auto-downloaded CSV datasets (gitignored)
├── app.py                    # Main Streamlit dashboard application
├── analysis.py               # Data cleaning, loading, and statistical analysis
├── download_data.py          # Dataset downloader with fallback URLs
├── requirements.txt          # Python dependencies
├── install.bat               # Windows: create venv + install dependencies
├── run.bat                   # Windows: launch the Streamlit dashboard
├── uninstall.bat             # Windows: remove virtual environment
├── .gitignore
└── README.md
```

## 📊 Dataset

The datasets are sourced from the [Unemployment in India](https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india) Kaggle dataset compiled by the **Centre for Monitoring Indian Economy (CMIE)**:

| File | Description |
|------|-------------|
| `Unemployment in India.csv` | State-level unemployment data split by **Rural/Urban** areas |
| `Unemployment_Rate_upto_11_2020.csv` | Regional unemployment data with **geographic coordinates** |

**Key columns:** Region, Date, Estimated Unemployment Rate (%), Estimated Employed, Estimated Labour Participation Rate (%)

## 🛠️ Tech Stack

- **Python 3.10+** - Core language
- **Streamlit** - Web dashboard framework
- **Plotly** - Interactive charts and visualizations
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Requests** - HTTP dataset downloads

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

> Built as part of **CodeAlpha Python Programming Internship**
