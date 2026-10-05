# 🔍 AI Data Quality Detective

> An intelligent data quality analysis platform that automatically detects data quality issues in CSV datasets, evaluates overall dataset health, and provides actionable recommendations.

🌐 **Live Demo:**  
https://ai-data-quality-detective-1442.streamlit.app/

📂 **GitHub Repository:**  
https://github.com/bhanuprakash227/AI-Data-Quality-Detective

---

## 📌 Overview

**AI Data Quality Detective** is a Python and Streamlit-based platform for automatically analyzing the quality of CSV datasets.

Before using a dataset for Data Science, Machine Learning, analytics, or business decision-making, it is important to understand whether the data is reliable, consistent, and suitable for further processing.

This application automates the initial data-quality investigation by analyzing a dataset across multiple dimensions and generating an overall **Data Quality Score** with recommendations.

Users simply upload a CSV dataset and the application performs the analysis.

---

## 🎯 Problem Statement

Real-world datasets often contain hidden quality problems such as:

- Missing values
- Duplicate records
- Invalid values
- Outliers
- Incorrect data types
- Constant columns
- High-cardinality identifier columns
- Strongly correlated features
- Potential target leakage
- Schema inconsistencies

These problems can negatively affect:

- Machine Learning models
- Statistical analysis
- Data visualization
- Business intelligence
- Predictive analytics
- Decision-making

**AI Data Quality Detective** is designed to detect these issues before the dataset is used for further analysis or Machine Learning.

---

# 🚀 Features

## 1. 📊 Dataset Overview

Provides a complete profile of the uploaded dataset.

### Includes:

- Number of rows
- Number of columns
- Total cells
- Missing cells
- Duplicate rows
- Column names
- Data types
- Numeric columns
- Categorical columns
- Unique values
- Statistical summary
- Dataset preview

---

## 2. ⚠️ Missing Value Analysis

Detects missing values across all columns.

### Provides:

- Missing value count
- Missing percentage
- Columns containing missing values
- Recommendations for handling missing data

Possible approaches include:

- Imputation
- Record removal
- Business-rule based handling
- Investigation of the source of missing data

---

## 3. 🔁 Duplicate Analysis

Detects duplicate records and potentially duplicated identifier values.

### Checks:

- Exact duplicate rows
- Duplicate row percentage
- Duplicate identifier values
- Identifier uniqueness

This helps identify repeated records and potential data integrity issues.

---

## 4. ❌ Invalid Value Analysis

Identifies potentially invalid values according to validation rules.

Examples include:

- Impossible numerical values
- Values outside expected ranges
- Invalid categorical values
- Data inconsistencies

The application provides recommendations for investigating and correcting invalid values.

---

## 5. 📈 Outlier Analysis

Detects unusual numerical observations.

Outliers may represent:

- Data entry errors
- Measurement errors
- Exceptional business cases
- Genuine extreme observations

The application identifies potential outliers so they can be investigated before being removed or transformed.

---

## 6. 🧬 Schema Analysis

Analyzes the structure and schema of the dataset.

### Detects:

#### Suspicious Numeric Columns

Identifies columns where numerical values are stored as text.

Example:

```text
income
"45000"
"52000"
"61000"
