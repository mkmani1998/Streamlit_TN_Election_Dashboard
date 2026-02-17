# 🗳️ Tamil Nadu Election Results — Streamlit Dashboard

An interactive data visualisation app for exploring Tamil Nadu election results, built with Streamlit and Plotly.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## 📸 Features

| Page | Description |
|------|-------------|
| **Overview** | KPI metrics, top parties by vote share, turnout distribution |
| **Party Analysis** | Vote share pie, candidates fielded vs votes scatter, avg votes per candidate |
| **Constituency Deep Dive** | Per-constituency candidate breakdown, general vs postal vote split |
| **Candidate Explorer** | Search candidates, age/gender distribution, sortable table |
| **Voter Demographics** | Turnout heatmap, high/low turnout constituencies, category-wise analysis |

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/your-username/tn-election-dashboard.git
cd tn-election-dashboard
```

### 2. Add the data file

Place `Election_Results_Clean.csv` in the root of the project directory.

> The CSV should have these columns:  
> `STATE_UT_NAME, AC_NO, AC_NAME, CANDIDATE_NAME, SEX, AGE, CATEGORY, PARTY, SYMBOL, GENERAL_VOTES, POSTAL_VOTES, TOTAL_VOTES, VOTES_POLLED_PCT, TOTAL_ELECTORS`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
tn-election-dashboard/
│
├── app.py                      # Main Streamlit application
├── Election_Results_Clean.csv  # Dataset (add this yourself)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub (make sure the CSV is included)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set `app.py` as the main file
4. Click **Deploy**

## 📊 Data Source

Election Results data from the Election Commission of India (Tamil Nadu Assembly Elections).

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io) — App framework
- [Plotly](https://plotly.com/python/) — Interactive charts
- [Pandas](https://pandas.pydata.org) — Data manipulation

## 📄 License

MIT License — free to use and modify.
