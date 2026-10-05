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

income
"45000"
"52000"
"61000"

## 7. 🔗 Correlation Analysis

Analyzes relationships between numerical features in the dataset.

Correlation analysis helps identify whether two numerical variables contain similar or strongly related information.

### Detects:

#### Strong Correlations

The application identifies pairs of numerical features with a correlation strength of **0.70 or higher**.

Examples:

income ↔ credit_score
age ↔ income
feature_1 ↔ feature_2

## 8. 🔐 Target Leakage Analysis

Identifies features that may contain information derived from the target variable or information that would not be available at prediction time.

Target leakage can cause a Machine Learning model to achieve unrealistically high performance during training and testing but perform poorly on real-world data.

### Detects:

#### High Target Correlation

The application checks numerical features for strong correlation with the selected target column.

Features with an absolute correlation of **0.70 or higher** are flagged for investigation.

### Leakage-Based Feature Names

The application also checks feature names for keywords that may indicate target-derived or post-outcome information.

Examples include:

- `post`
- `after`
- `result`
- `outcome`
- `approved`
- `approval`
- `final`
- `decision`
- `target`
- `label`
- `future`

### Example

loan_approved
post_approval_score
income
credit_score

## 8. 🔐 Target Leakage Analysis

Identifies features that may contain information derived from the target variable or information that would not be available at prediction time.

Target leakage can cause a Machine Learning model to achieve unrealistically high performance during training and testing but perform poorly on real-world data.

### Detects:

#### High Target Correlation

The application checks numerical features for strong correlation with the selected target column.

Features with an absolute correlation of **0.70 or higher** are flagged for investigation.

### Leakage-Based Feature Names

The application also checks feature names for keywords that may indicate target-derived or post-outcome information.

Examples include:

- `post`
- `after`
- `result`
- `outcome`
- `approved`
- `approval`
- `final`
- `decision`
- `target`
- `label`
- `future`

### Example

loan_approved
post_approval_score
income
credit_score

## 9. 🎯 Overall Data Quality

Provides an overall assessment of the uploaded dataset by combining the results from the different data quality checks.

The application calculates a **Data Quality Score** based on detected data quality issues.

### The Overall Analysis Considers:

- Missing values
- Duplicate rows
- Duplicate identifier values
- Invalid values
- Outliers
- Constant columns
- High-cardinality identifier columns
- Potential target leakage

### Data Quality Score

The score starts from a maximum of **100** and deductions are applied based on the severity and presence of detected data quality problems.

A higher score indicates better overall dataset quality.

### Quality Levels

| Score | Status |
|---|---|
| 90 – 100 | Excellent |
| 75 – 89 | Good |
| 60 – 74 | Fair |
| Below 60 | Poor |

### Results Include:

- Overall Data Quality Score
- Quality status
- Critical problems
- Warnings
- Detailed issue information
- Recommendations for improving dataset quality

### Example

A dataset with:

- Few missing values
- No duplicate records
- No invalid values
- No significant outliers
- No suspicious schema issues
- No potential target leakage

will generally receive a higher quality score.

A dataset containing multiple serious quality problems will receive a lower score.

### Recommendations

The application provides actionable recommendations based on the detected issues so that users can investigate and improve the dataset before using it for:

- Data Science
- Machine Learning
- Statistical Analysis
- Data Visualization
- Business Analytics
- Predictive Modeling

## 📊 Data Quality Score

The **Data Quality Score** provides a single numerical measure of the overall health of the uploaded dataset.

The score ranges from **0 to 100**.

A score closer to **100** indicates that the dataset has fewer detected quality problems.

### Quality Levels

| Score | Status | Meaning |
|---|---|---|
| 90 – 100 | Excellent | Dataset has very few or no significant quality issues |
| 75 – 89 | Good | Dataset is generally usable but has some issues to review |
| 60 – 74 | Fair | Dataset contains several quality issues that should be investigated |
| Below 60 | Poor | Dataset contains significant quality problems |

### Score Components

The score considers multiple dimensions of data quality:

- **Missing Values** — checks for incomplete data
- **Duplicate Rows** — checks for repeated records
- **Duplicate Identifiers** — checks identifier uniqueness
- **Invalid Values** — checks for potentially incorrect values
- **Outliers** — checks for unusual numerical observations
- **Constant Columns** — identifies columns with no meaningful variation
- **High-Cardinality Columns** — identifies identifier-like columns
- **Target Leakage** — identifies potentially leaked information

### Score Interpretation

A high score does not guarantee that a dataset is perfect.

Similarly, a low score does not necessarily mean that every detected issue must be removed.

The score is intended to provide an initial assessment of dataset health and help users identify areas that require further investigation.

### Important

Data quality decisions should be based on business context and domain knowledge.

For example, an outlier may be:

- A genuine observation
- A rare but valid event
- A measurement error
- A data entry error

Therefore, the application provides **recommendations for investigation rather than automatically deleting data**.

## ⚙️ How It Works

The application follows a structured data-quality analysis workflow.

### Step 1 — Upload Dataset

The user uploads a CSV file through the Streamlit interface.

The application reads the uploaded file using Pandas.

### Step 2 — Dataset Profiling

The application examines the basic structure of the dataset, including:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Unique values
- Numeric columns
- Categorical columns
- Statistical information

### Step 3 — Data Quality Analysis

The dataset is passed through multiple specialized analysis modules.

Uploaded CSV
     ↓
Dataset Profiler
     ↓
┌─────────────────────────────┐
│ Missing Value Analysis      │
│ Duplicate Analysis          │
│ Invalid Value Analysis      │
│ Outlier Analysis            │
│ Schema Analysis             │
│ Correlation Analysis        │
│ Target Leakage Analysis     │
└─────────────────────────────┘
     ↓
Quality Score Calculation
     ↓
Results & Recommendations

## 🏗️ System Architecture

The application follows a modular architecture where each data-quality check is implemented as a separate Python module.

### Architecture Overview

``
                    User
                      │
                      ▼
              Streamlit Interface
                      │
                      ▼
                 CSV Upload
                      │
                      ▼
               Dataset (Pandas)
                      │
                      ▼
              Dataset Profiler
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   Missing Value   Duplicate     Invalid Value
     Detector      Checker        Detector
        │             │             │
        └─────────────┼─────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
     Outlier       Schema       Correlation
     Detector      Detector       Detector
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
             Leakage Detector
                      │
                      ▼
             Quality Score Engine
                      │
                      ▼
             Analysis Results
                      │
                      ▼
              Recommendations
                      │
                      ▼
                   User


## 🔄 Project Workflow

The project follows a step-by-step workflow from dataset upload to final data-quality recommendations.

### Complete Workflow

1. User opens the application
              ↓
2. User uploads a CSV dataset
              ↓
3. Application reads the dataset
              ↓
4. Dataset profiling
              ↓
5. Missing value analysis
              ↓
6. Duplicate analysis
              ↓
7. Invalid value analysis
              ↓
8. Outlier analysis
              ↓
9. Schema analysis
              ↓
10. Correlation analysis
              ↓
11. Target leakage analysis
              ↓
12. Overall quality score calculation
              ↓
13. Results and recommendations
              ↓
14. User investigates and improves the dataset


## 🛠️ Technology Stack

The project uses Python-based data analysis tools together with Streamlit to provide an interactive web application.

### Python

Python is the primary programming language used to build the application.

It is used for:

- Data processing
- Data-quality analysis
- Statistical calculations
- Issue detection
- Quality score calculation
- Application logic

### Pandas

Pandas is used for working with tabular datasets.

It is mainly used for:

- Reading CSV files
- Creating DataFrames
- Inspecting dataset structure
- Detecting missing values
- Detecting duplicate records
- Data type analysis
- Statistical analysis
- Data filtering and processing

### NumPy

NumPy is used for numerical operations and numerical data processing.

It supports:

- Numerical calculations
- Array operations
- Numerical data type detection
- Correlation analysis
- Statistical computations

### Scikit-learn

Scikit-learn is included in the project environment for future Machine Learning extensions and advanced data-quality capabilities.

Potential future applications include:

- Machine Learning-based anomaly detection
- Automated feature analysis
- Predictive data-quality checks
- Advanced classification techniques

### Streamlit

Streamlit is used to build the interactive web interface.

It provides:

- CSV file upload
- Analysis selection
- Interactive results
- Data tables
- Metrics
- Quality score visualization
- Recommendations

### Development Tools

The project is developed using:

- Visual Studio Code
- Python Virtual Environment
- Git
- GitHub
- GitHub CLI

### Testing

Python testing tools are used to verify individual project modules and ensure that the analysis functions work correctly.

### Deployment

The application is deployed using **Streamlit Community Cloud**.

Live application:

https://ai-data-quality-detective-1442.streamlit.app/

Source code:

https://github.com/bhanuprakash227/AI-Data-Quality-Detective

## 📁 Project Structure

The project is organized into separate modules so that each data-quality function has a clear responsibility.

AI-Data-Quality-Detective/
│
├── data/
│   └── sample.csv
│
├── src/
│   ├── __init__.py
│   ├── profiler.py
│   ├── missing_values.py
│   ├── duplicate_checker.py
│   ├── invalid_values.py
│   ├── outlier_detector.py
│   ├── schema_detector.py
│   ├── correlation_detector.py
│   ├── leakage_detector.py
│   └── quality_score.py
│
├── tests/
│   ├── __init__.py
│   └── test_profiler.py
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore

## ⚙️ Installation

Follow the steps below to set up and run the AI Data Quality Detective locally.

### Prerequisites

Before installing the project, make sure the following are installed:

- Python 3.9 or higher
- Git
- Visual Studio Code
- Internet connection

### 1. Clone the Repository

Open a terminal and run:


git clone https://github.com/bhanuprakash227/AI-Data-Quality-Detective.git

## 🖥️ How to Use

Follow these steps to analyze a dataset using AI Data Quality Detective.

### Step 1 — Open the Application

Open the deployed application:

https://ai-data-quality-detective-1442.streamlit.app/

You can also run the application locally using:


streamlit run app.py


## 🧪 Testing

Testing is used to verify that the individual components of the application work correctly.

### Testing Objectives

The testing process helps ensure that:

- Dataset profiling works correctly
- Data is processed correctly
- Quality checks return expected results
- Empty datasets are handled safely
- Analysis modules produce valid outputs
- The application remains stable when processing datasets

### Test Directory

The project contains a dedicated testing directory:


tests/
├── __init__.py
└── test_profiler.py

## 💼 Use Cases

AI Data Quality Detective can be useful in different stages of data preparation and analysis.

### 👨‍💻 Data Scientists

Data Scientists can use the application to perform an initial quality assessment before starting:

- Exploratory Data Analysis
- Feature engineering
- Statistical analysis
- Machine Learning modeling
- Predictive analytics

It helps identify potential data-quality problems before they affect downstream analysis.

### 🤖 Machine Learning Engineers

Machine Learning Engineers can use the platform to investigate issues that may affect model development.

Useful checks include:

- Missing values
- Duplicate records
- Outliers
- Data-type inconsistencies
- Strong feature correlations
- Potential target leakage

This can help improve the reliability of Machine Learning pipelines.

### 📊 Data Analysts

Data Analysts can use the application to quickly understand the quality and structure of CSV datasets before creating reports or performing analysis.

The platform provides:

- Dataset profiling
- Missing-value statistics
- Duplicate detection
- Schema analysis
- Statistical information
- Data-quality recommendations

### 📈 Business Intelligence

Business Intelligence teams can use the application as an initial data-quality check before using datasets for:

- Dashboards
- Reports
- Business metrics
- Trend analysis
- Decision-making

Better-quality input data can help reduce the risk of incorrect conclusions.

### 🎓 Students

Students learning:

- Python
- Pandas
- NumPy
- Data Science
- Machine Learning
- Data Analytics

can use the project to understand practical data-quality concepts through an interactive application.

### 🏢 Data Teams

Data teams can use the project as a starting point for building more advanced data-quality workflows and automated validation systems.

It can be extended with:

- Custom validation rules
- Database connectivity
- Automated reports
- Data-quality monitoring
- Machine Learning-based anomaly detection
- Automated data-cleaning pipelines

## 🔒 Data Privacy

AI Data Quality Detective is designed to analyze datasets provided by the user and display data-quality results.

### Local Analysis

When running the application locally, the uploaded CSV is processed by the application running on the user's machine.

The project does not require the dataset to be permanently stored by the application.

### Deployed Application

When using the deployed Streamlit application, users should avoid uploading confidential, sensitive, or personally identifiable information unless they understand and accept the hosting environment's data-handling policies.

### Recommended Practices

Users should:

- Avoid uploading sensitive personal information
- Remove unnecessary personally identifiable information
- Anonymize confidential datasets when possible
- Use sample or synthetic data for demonstrations
- Review organizational data-security policies before uploading business data

### Sensitive Information

Do not upload datasets containing sensitive information such as:

- Passwords
- API keys
- Authentication credentials
- Financial account credentials
- Private medical records
- Confidential business information
- Unnecessary personally identifiable information

### Original Dataset

The application is designed to analyze the uploaded dataset rather than automatically modify the original data.

Users should maintain their own backup of important datasets before performing any data-cleaning operations outside the application.

### Important

AI Data Quality Detective is a data-quality analysis tool and should not be considered a replacement for an organization's formal data-security, privacy, governance, or compliance procedures.

## 👨‍💻 Author

### Ravula Bhanu Prakash

Computer Science Graduate from **SR University, Warangal**, with an interest in:

- Python
- SQL
- Data Science
- Machine Learning
- Artificial Intelligence
- Web Development
