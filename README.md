# 🔍 AI Data Quality Detective

A Streamlit web app that automatically audits CSV datasets for data quality problems, scores them out of 100, and gives clear recommendations on what to fix before the data is used for analysis or machine learning.

🔗 **Live Demo:** [ai-data-quality-detective-1442.streamlit.app](https://ai-data-quality-detective-1442.streamlit.app/)

---

## ✨ Features

Upload a CSV and the app runs these analyses:

| # | Analysis | What it checks |
|---|----------|----------------|
| 1 | **Dataset Overview** | Rows, columns, data types, unique values, statistical summary, preview |
| 2 | **Missing Values** | Missing cells and percentages, per column |
| 3 | **Duplicates** | Fully duplicated rows and duplicate identifier columns |
| 4 | **Invalid Values** | Values that break domain or business rules |
| 5 | **Outliers** | Statistically unusual values in numeric columns |
| 6 | **Schema Analysis** | Numbers stored as text, constant columns, high-cardinality (ID-like) columns |
| 7 | **Correlation Analysis** | Strong feature correlations and a correlation matrix |
| 8 | **Target Leakage** | Features that may leak information about the target column |
| 9 | **Overall Data Quality** | A 0–100 quality score, status rating, and prioritized recommendations |

### Highlights
- 🏆 **Data Quality Score (0–100)** with ratings: Excellent / Good / Fair / Poor
- 🎯 **Automatic target column detection** (looks for names like `target`, `label`, `y`, `outcome`, `status`, or falls back to the last numeric column)
- 💡 **Actionable recommendations** based on the issues found
- 🛡️ **Robust error handling**: if one check fails, the rest still run
- 🌙 **Custom dark UI** with a wide-screen layout

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit**: web interface
- **Pandas** and **NumPy**: data handling and analysis

---

## 📂 Project Structure

```
├── app.py                        # Streamlit UI and main application
├── requirements.txt              # Python dependencies
└── src/
    ├── profiler.py               # Dataset profiling
    ├── missing_values.py         # Missing value analysis
    ├── duplicate_checker.py      # Duplicate detection
    ├── invalid_values.py         # Invalid value detection
    ├── outlier_detector.py       # Outlier detection
    ├── schema_detector.py        # Schema / column type issues
    ├── correlation_detector.py   # Correlation analysis
    ├── leakage_detector.py       # Target leakage detection
    └── quality_score.py          # Overall quality score calculation
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/bhanuprakash227/AI-Data-Quality-Detective.git
cd AI-Data-Quality-Detective
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📖 How to Use

1. Open the app and upload a **CSV file** using the uploader at the top right.
2. Pick an analysis from the **Analysis Options** panel on the left.
3. Open **9. Overall Data Quality** for the score, status and recommendations.
4. Fix the flagged issues in your data and re-upload to see the score improve.

---

## 📊 How the Quality Score Works

The score starts at 100 and penalties are applied for issues such as:

- Missing values
- Duplicate rows
- Invalid values
- Outliers
- Constant columns
- High-cardinality columns
- Potential target leakage

| Score | Status |
|-------|--------|
| 90 – 100 | 🟢 Excellent |
| 75 – 89 | 🟢 Good |
| 60 – 74 | 🟡 Fair |
| Below 60 | 🔴 Poor |

---

## ☁️ Deployment

Deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). To deploy your own copy:

1. Fork this repository.
2. Go to Streamlit Community Cloud and click **New app**.
3. Select your fork and set the main file path to `app.py`.
4. Click **Deploy**.

---

## 🗺️ Roadmap

- [ ] Support for Excel, JSON and Parquet files
- [ ] Manual target column selection
- [ ] Download the quality report (PDF / CSV)
- [ ] One-click automated data cleaning
- [ ] LLM-powered natural-language explanations

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a feature branch, and open a pull request.

---

## 👤 Author

**bhanuprakash227**
- GitHub: [@bhanuprakash227](https://github.com/bhanuprakash227)

⭐ If you found this project useful, please give it a star!
