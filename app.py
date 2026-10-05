import streamlit as st
import pandas as pd
import numpy as np

from src.profiler import profile_dataset
from src.missing_values import analyze_missing_values
from src.duplicate_checker import analyze_duplicates
from src.invalid_values import analyze_invalid_values
from src.outlier_detector import analyze_outliers
from src.schema_detector import analyze_schema
from src.correlation_detector import analyze_correlations
from src.leakage_detector import analyze_leakage
from src.quality_score import calculate_quality_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Data Quality Detective",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #0f1016;
}

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2rem;
    max-width: 100%;
}

.main-title {
    font-size: 34px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 16px;
    color: #a9abb5;
    line-height: 1.5;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 5px;
    margin-bottom: 20px;
}

.recommendation {
    background-color: #192235;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    color: #f2f2f2;
    font-size: 16px;
}

.metric-card {
    background-color: #181b24;
    border: 1px solid #2b2e39;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 15px;
}

[data-testid="stFileUploader"] {
    background-color: #181b24;
    border-radius: 12px;
    padding: 10px;
}

div[role="radiogroup"] label {
    padding: 7px 0px;
    font-size: 15px;
}

hr {
    border-color: #30323c;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns(
    [7, 3],
    gap="medium"
)


with header_left:

    st.markdown(
        '<div class="main-title">🔍 AI Data Quality Detective</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'An AI-powered platform for detecting data quality problems, '
        'analyzing datasets, and generating intelligent recommendations.'
        '</div>',
        unsafe_allow_html=True
    )


with header_right:

    uploaded_file = st.file_uploader(
        "📂 Upload CSV Dataset",
        type=["csv"]
    )


st.markdown("<hr>", unsafe_allow_html=True)


# ============================================================
# NO FILE UPLOADED
# ============================================================

if uploaded_file is None:

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.markdown(
            "<h1 style='text-align:center;'>🔍</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h2 style='text-align:center;'>"
            "Welcome to AI Data Quality Detective"
            "</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align:center; "
            "color:#a9abb5; "
            "font-size:17px;'>"
            "Upload a CSV dataset to automatically analyze "
            "missing values, duplicates, invalid values, "
            "outliers, schema problems, correlations, "
            "target leakage, and overall data quality."
            "</p>",
            unsafe_allow_html=True
        )

        st.write("")

        st.info(
            "📂 Upload a CSV file using the upload box above "
            "to get started."
        )

    st.stop()


# ============================================================
# LOAD UPLOADED DATASET
# ============================================================

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(
        f"❌ Unable to read the uploaded CSV file: {e}"
    )

    st.stop()


# ============================================================
# EMPTY DATASET CHECK
# ============================================================

if df.empty:

    st.error(
        "❌ The uploaded CSV file is empty."
    )

    st.stop()


# ============================================================
# DATASET PROFILE
# ============================================================

try:

    profile = profile_dataset(df)

except Exception:

    profile = {}


# ============================================================
# RUN ANALYSIS
# ============================================================

try:

    missing_result = analyze_missing_values(df)

except Exception as e:

    missing_result = {
        "error": str(e)
    }


try:

    duplicate_result = analyze_duplicates(df)

except Exception as e:

    duplicate_result = {
        "error": str(e)
    }


try:

    invalid_result = analyze_invalid_values(df)

except Exception as e:

    invalid_result = {
        "error": str(e)
    }


try:

    outlier_result = analyze_outliers(df)

except Exception as e:

    outlier_result = {
        "error": str(e)
    }


try:

    schema_result = analyze_schema(df)

except Exception as e:

    schema_result = {
        "error": str(e)
    }


try:

    correlation_result = analyze_correlations(df)

except Exception as e:

    correlation_result = {
        "error": str(e)
    }


# ============================================================
# COMMON ANALYSIS VARIABLES
# ============================================================

strong_correlations = correlation_result.get(
    "strong_correlations",
    []
)

constant_columns = schema_result.get(
    "constant_columns",
    {}
)

high_cardinality = schema_result.get(
    "high_cardinality_columns",
    {}
)

suspicious_numeric = schema_result.get(
    "suspicious_numeric_columns",
    {}
)


# ============================================================
# TARGET COLUMN DETECTION
# ============================================================

target_column = None

possible_targets = [
    "target",
    "label",
    "y",
    "loan_approved",
    "approved",
    "outcome",
    "status"
]

for column in possible_targets:

    if column in df.columns:

        target_column = column

        break


if target_column is None:

    numeric_target_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if numeric_target_columns:

        target_column = numeric_target_columns[-1]


# ============================================================
# TARGET LEAKAGE
# ============================================================

if target_column is not None:

    try:

        leakage_result = analyze_leakage(
            df,
            target_column
        )

    except Exception as e:

        leakage_result = {
            "error": str(e),
            "potential_leakage": []
        }

else:

    leakage_result = {
        "message": "No suitable target column was detected.",
        "potential_leakage": []
    }


potential_leakage = leakage_result.get(
    "potential_leakage",
    []
)


# ============================================================
# BASIC DATASET METRICS
# ============================================================

rows = len(df)

columns = len(df.columns)

total_cells = rows * columns

missing_cells = int(
    df.isnull().sum().sum()
)

duplicate_rows = int(
    df.duplicated().sum()
)

if total_cells > 0:

    missing_percentage = (
        missing_cells / total_cells
    ) * 100

else:

    missing_percentage = 0


numeric_columns = df.select_dtypes(
    include=np.number
).columns.tolist()

categorical_columns = df.select_dtypes(
    exclude=np.number
).columns.tolist()


# ============================================================
# INVALID VALUE COUNT
# ============================================================

invalid_count = 0

for key in [
    "invalid_count",
    "total_invalid_values"
]:

    value = invalid_result.get(key)

    if isinstance(
        value,
        (int, float)
    ):

        invalid_count = int(value)

        break


# ============================================================
# OUTLIER COUNT
# ============================================================

outlier_count = 0

for key in [
    "total_outliers",
    "outlier_count"
]:

    value = outlier_result.get(key)

    if isinstance(
        value,
        (int, float)
    ):

        outlier_count = int(value)

        break


# ============================================================
# QUALITY SCORE
# ============================================================

try:

    quality_result = calculate_quality_score(
        df=df,
        missing_result=missing_result,
        duplicate_result=duplicate_result,
        invalid_result=invalid_result,
        outlier_result=outlier_result,
        schema_result=schema_result,
        leakage_result=leakage_result
    )

except Exception:

    score = 100.0

    if total_cells > 0:

        score -= min(
            missing_percentage * 0.5,
            20
        )

    if rows > 0:

        duplicate_percentage = (
            duplicate_rows / rows
        ) * 100

        score -= min(
            duplicate_percentage * 0.5,
            15
        )

    score -= min(
        invalid_count * 2,
        15
    )

    score -= min(
        outlier_count,
        10
    )

    score -= min(
        len(constant_columns) * 3,
        10
    )

    score -= min(
        len(high_cardinality) * 3,
        10
    )

    score -= min(
        len(potential_leakage) * 5,
        20
    )

    score = max(
        0,
        min(
            100,
            score
        )
    )

    if score >= 90:

        status = "Excellent"

    elif score >= 75:

        status = "Good"

    elif score >= 60:

        status = "Fair"

    else:

        status = "Poor"

    quality_result = {
        "score": round(score, 2),
        "status": status,
        "critical_problems": [],
        "warnings": [],
        "details": {}
    }


# ============================================================
# EXTRACT SCORE
# ============================================================

score = quality_result.get(
    "score",
    quality_result.get(
        "quality_score",
        0
    )
)

status = quality_result.get(
    "status",
    "Unknown"
)

try:

    score = float(score)

except Exception:

    score = 0.0


# ============================================================
# MAIN LAYOUT
# ============================================================

left_column, right_column = st.columns(
    [1, 3],
    gap="large"
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left_column:

    st.markdown(
        '<div class="section-title">📋 Analysis Options</div>',
        unsafe_allow_html=True
    )

    options = [
        "1. Dataset Overview",
        "2. Missing Value Analysis",
        "3. Duplicate Analysis",
        "4. Invalid Value Analysis",
        "5. Outlier Analysis",
        "6. Schema Analysis",
        "7. Correlation Analysis",
        "8. Target Leakage Analysis",
        "9. Overall Data Quality"
    ]

    selected_option = st.radio(
        "Analysis",
        options,
        index=8,
        label_visibility="collapsed"
    )


# ============================================================
# RIGHT COLUMN
# ============================================================

with right_column:


    # ========================================================
    # 1. DATASET OVERVIEW
    # ========================================================

    if selected_option == "1. Dataset Overview":

        st.markdown(
            "## 📊 Dataset Profile"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Rows",
                rows
            )

        with c2:

            st.metric(
                "Columns",
                columns
            )

        with c3:

            st.metric(
                "Missing Cells",
                missing_cells
            )

        with c4:

            st.metric(
                "Duplicate Rows",
                duplicate_rows
            )


        st.markdown(
            "### 📌 Basic Information"
        )

        basic_info = pd.DataFrame(
            {
                "Property": [
                    "Rows",
                    "Columns",
                    "Total Cells",
                    "Missing Cells",
                    "Missing Percentage",
                    "Duplicate Rows",
                    "Numeric Columns",
                    "Categorical Columns"
                ],

                "Value": [
                    rows,
                    columns,
                    total_cells,
                    missing_cells,
                    f"{missing_percentage:.2f}%",
                    duplicate_rows,
                    len(numeric_columns),
                    len(categorical_columns)
                ]
            }
        )

        st.dataframe(
            basic_info,
            use_container_width=True,
            hide_index=True
        )


        st.markdown(
            "### 🏷️ Column Information"
        )

        column_info = pd.DataFrame(
            {
                "Column": df.columns,

                "Data Type": [
                    str(df[col].dtype)
                    for col in df.columns
                ],

                "Non-Null": [
                    int(
                        df[col].notna().sum()
                    )
                    for col in df.columns
                ],

                "Unique Values": [
                    int(
                        df[col].nunique(
                            dropna=False
                        )
                    )
                    for col in df.columns
                ]
            }
        )

        st.dataframe(
            column_info,
            use_container_width=True,
            hide_index=True
        )


        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### 🔢 Numeric Columns"
            )

            if numeric_columns:

                for column in numeric_columns:

                    st.write(
                        f"• `{column}`"
                    )

            else:

                st.info(
                    "No numeric columns."
                )


        with col2:

            st.markdown(
                "### 🔤 Categorical Columns"
            )

            if categorical_columns:

                for column in categorical_columns:

                    st.write(
                        f"• `{column}`"
                    )

            else:

                st.info(
                    "No categorical columns."
                )


        st.markdown(
            "### ⚠️ Missing Values"
        )

        missing_table = pd.DataFrame(
            {
                "Column": df.columns,

                "Missing Count": [
                    int(
                        df[col].isnull().sum()
                    )
                    for col in df.columns
                ],

                "Missing %": [
                    round(
                        df[col].isnull().mean() * 100,
                        2
                    )
                    for col in df.columns
                ]
            }
        )

        missing_table = missing_table[
            missing_table["Missing Count"] > 0
        ]

        if not missing_table.empty:

            st.dataframe(
                missing_table,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No missing values."
            )


        st.markdown(
            "### 🔑 Unique Values"
        )

        unique_table = pd.DataFrame(
            {
                "Column": df.columns,

                "Unique Values": [
                    int(
                        df[col].nunique(
                            dropna=False
                        )
                    )
                    for col in df.columns
                ]
            }
        )

        st.dataframe(
            unique_table,
            use_container_width=True,
            hide_index=True
        )


        st.markdown(
            "### 📈 Statistical Summary"
        )

        if numeric_columns:

            st.dataframe(
                df[numeric_columns].describe().T,
                use_container_width=True
            )

        else:

            st.info(
                "No numeric columns available."
            )


        st.markdown(
            "### 👀 Dataset Preview"
        )

        st.dataframe(
            df.head(10),
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # 2. MISSING VALUE ANALYSIS
    # ========================================================

    elif selected_option == "2. Missing Value Analysis":

        st.markdown(
            "## ⚠️ Missing Value Analysis"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Missing Cells",
                missing_cells
            )

        with c2:

            st.metric(
                "Missing Percentage",
                f"{missing_percentage:.2f}%"
            )


        if missing_cells == 0:

            st.success(
                "✅ No missing values detected."
            )

        else:

            missing_table = pd.DataFrame(
                {
                    "Column": df.columns,

                    "Missing Count": [
                        int(
                            df[col].isnull().sum()
                        )
                        for col in df.columns
                    ],

                    "Missing %": [
                        round(
                            df[col].isnull().mean() * 100,
                            2
                        )
                        for col in df.columns
                    ]
                }
            )

            missing_table = missing_table[
                missing_table["Missing Count"] > 0
            ]

            st.dataframe(
                missing_table,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "💡 Handle missing values using appropriate "
                "imputation, removal, or business rules."
            )


    # ========================================================
    # 3. DUPLICATE ANALYSIS
    # ========================================================

    elif selected_option == "3. Duplicate Analysis":

        st.markdown(
            "## 🔁 Duplicate Analysis"
        )

        duplicate_percentage = (
            duplicate_rows / rows * 100
            if rows > 0
            else 0
        )

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Duplicate Rows",
                duplicate_rows
            )

        with c2:

            st.metric(
                "Duplicate Percentage",
                f"{duplicate_percentage:.2f}%"
            )


        if duplicate_rows > 0:

            st.warning(
                "⚠️ Duplicate records detected."
            )

            duplicate_data = df[
                df.duplicated(
                    keep=False
                )
            ]

            st.dataframe(
                duplicate_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No duplicate rows detected."
            )


        duplicate_identifiers = duplicate_result.get(
            "duplicate_identifier_columns",
            {}
        )

        if duplicate_identifiers:

            st.markdown(
                "### 🆔 Duplicate Identifiers"
            )

            for column, details in duplicate_identifiers.items():

                st.warning(
                    f"⚠️ `{column}` contains duplicate values."
                )

                st.write(
                    details.get(
                        "recommendation",
                        ""
                    )
                )


    # ========================================================
    # 4. INVALID VALUE ANALYSIS
    # ========================================================

    elif selected_option == "4. Invalid Value Analysis":

        st.markdown(
            "## ❌ Invalid Value Analysis"
        )

        if invalid_result.get("error"):

            st.error(
                invalid_result["error"]
            )

        else:

            st.json(
                invalid_result
            )

            st.info(
                "💡 Review invalid values according to "
                "domain and business rules."
            )


    # ========================================================
    # 5. OUTLIER ANALYSIS
    # ========================================================

    elif selected_option == "5. Outlier Analysis":

        st.markdown(
            "## 📊 Outlier Analysis"
        )

        st.metric(
            "Total Outliers",
            outlier_count
        )


        if outlier_count > 0:

            outlier_summary = outlier_result.get(
                "summary",
                []
            )

            if outlier_summary:

                st.dataframe(
                    pd.DataFrame(
                        outlier_summary
                    ),
                    use_container_width=True,
                    hide_index=True
                )

            st.warning(
                "⚠️ Outliers detected. Investigate them "
                "before removing or transforming values."
            )

        else:

            st.success(
                "✅ No outliers detected."
            )


    # ========================================================
    # 6. SCHEMA ANALYSIS
    # ========================================================

    elif selected_option == "6. Schema Analysis":

        st.markdown(
            "## 🧬 Schema Analysis"
        )


        st.markdown(
            "### 🔢 Suspicious Numeric Columns"
        )

        if suspicious_numeric:

            schema_rows = []

            for column, details in suspicious_numeric.items():

                schema_rows.append(
                    {
                        "Column": column,

                        "Current Type": details.get(
                            "current_dtype",
                            ""
                        ),

                        "Numeric Ratio": (
                            f"{details.get('numeric_ratio', 0)}%"
                        ),

                        "Recommendation": details.get(
                            "recommendation",
                            ""
                        )
                    }
                )

            st.dataframe(
                pd.DataFrame(
                    schema_rows
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No suspicious numeric columns."
            )


        st.markdown(
            "### 📌 Constant Columns"
        )

        if constant_columns:

            for column, details in constant_columns.items():

                st.warning(
                    f"⚠️ `{column}` is a constant column."
                )

                st.write(
                    details.get(
                        "recommendation",
                        ""
                    )
                )

        else:

            st.success(
                "✅ No constant columns."
            )


        st.markdown(
            "### 🆔 High Cardinality Columns"
        )

        if high_cardinality:

            high_rows = []

            for column, details in high_cardinality.items():

                high_rows.append(
                    {
                        "Column": column,

                        "Unique Values": details.get(
                            "unique_count",
                            0
                        ),

                        "Cardinality %": (
                            f"{details.get('cardinality_percentage', 0)}%"
                        ),

                        "Recommendation": details.get(
                            "recommendation",
                            ""
                        )
                    }
                )

            st.dataframe(
                pd.DataFrame(
                    high_rows
                ),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "✅ No suspicious high-cardinality identifiers."
            )


    # ========================================================
    # 7. CORRELATION ANALYSIS
    # ========================================================

    elif selected_option == "7. Correlation Analysis":

        st.markdown(
            "## 🔗 Correlation Analysis"
        )

        if strong_correlations:

            correlation_table = pd.DataFrame(
                strong_correlations
            )

            st.dataframe(
                correlation_table,
                use_container_width=True,
                hide_index=True
            )

            st.info(
                "💡 Highly correlated features may contain "
                "redundant information."
            )

        else:

            st.success(
                "✅ No strong correlations detected."
            )


        correlation_matrix = correlation_result.get(
            "correlation_matrix",
            {}
        )

        if correlation_matrix:

            st.markdown(
                "### 📈 Correlation Matrix"
            )

            corr_df = pd.DataFrame(
                correlation_matrix
            )

            st.dataframe(
                corr_df,
                use_container_width=True
            )


    # ========================================================
    # 8. TARGET LEAKAGE ANALYSIS
    # ========================================================

    elif selected_option == "8. Target Leakage Analysis":

        st.markdown(
            "## 🚨 Target Leakage Analysis"
        )

        if target_column:

            st.info(
                f"Target column: `{target_column}`"
            )

        else:

            st.warning(
                "No suitable target column detected."
            )


        if potential_leakage:

            leakage_rows = []

            for item in potential_leakage:

                leakage_rows.append(
                    {
                        "Feature": item.get(
                            "feature",
                            ""
                        ),

                        "Correlation": item.get(
                            "correlation",
                            ""
                        ),

                        "Severity": item.get(
                            "severity",
                            ""
                        ),

                        "Reason": "; ".join(
                            item.get(
                                "reasons",
                                []
                            )
                        )
                    }
                )

            st.dataframe(
                pd.DataFrame(
                    leakage_rows
                ),
                use_container_width=True,
                hide_index=True
            )

            st.warning(
                "⚠️ Potential target leakage detected."
            )

        else:

            st.success(
                "✅ No potential target leakage detected."
            )


    # ========================================================
    # 9. OVERALL DATA QUALITY
    # ========================================================

    elif selected_option == "9. Overall Data Quality":

        st.markdown(
            "## 🏆 Overall Data Quality"
        )


        if status.lower() == "excellent":

            icon = "🟢"

        elif status.lower() == "good":

            icon = "🟢"

        elif status.lower() == "fair":

            icon = "🟡"

        else:

            icon = "🔴"


        score_col1, score_col2, score_col3 = st.columns(
            [1, 2, 1]
        )

        with score_col2:

            st.metric(
                "Data Quality Score",
                f"{score:.2f}/100"
            )

            st.markdown(
                f"<p style='text-align:center; "
                f"font-size:21px; "
                f"font-weight:600; "
                f"color:white;'>"
                f"{status} {icon}"
                f"</p>",
                unsafe_allow_html=True
            )


        if score >= 90:

            st.success(
                "Excellent dataset quality. "
                "Only minor improvements may be required."
            )

        elif score >= 75:

            st.info(
                "Good dataset quality, but some issues "
                "should be addressed before production use."
            )

        elif score >= 60:

            st.warning(
                "Fair dataset quality. Several issues "
                "should be investigated and corrected."
            )

        else:

            st.error(
                "Poor dataset quality. Significant "
                "data cleaning is recommended."
            )


        st.markdown(
            "## 💡 Recommendations"
        )


        recommendations = []


        if missing_cells > 0:

            recommendations.append(
                "Handle missing values using appropriate "
                "imputation or removal."
            )


        if duplicate_rows > 0:

            recommendations.append(
                "Investigate and remove duplicate records "
                "where appropriate."
            )


        if invalid_count > 0:

            recommendations.append(
                "Review and correct invalid values "
                "according to business rules."
            )


        if outlier_count > 0:

            recommendations.append(
                "Review detected outliers and determine "
                "whether they are errors or valid observations."
            )


        if constant_columns:

            recommendations.append(
                "Review constant columns because they "
                "provide little predictive information."
            )


        if high_cardinality:

            recommendations.append(
                "Review high-cardinality identifier-like "
                "columns before using them as model features."
            )


        if suspicious_numeric:

            recommendations.append(
                "Review columns containing numeric values "
                "stored as text."
            )


        if strong_correlations:

            recommendations.append(
                "Investigate highly correlated features "
                "for possible redundant information."
            )


        if potential_leakage:

            recommendations.append(
                "Investigate potential target leakage and "
                "ensure features are available at prediction time."
            )


        if not recommendations:

            recommendations.append(
                "Dataset quality looks good. Continue monitoring "
                "data quality during future data ingestion."
            )


        for recommendation in recommendations:

            st.markdown(
                f"""
<div class="recommendation">
    ✅ {recommendation}
</div>
""",
                unsafe_allow_html=True
            )


        st.markdown(
            "## 📋 Quality Summary"
        )


        summary_data = pd.DataFrame(
            {
                "Quality Check": [
                    "Missing Values",
                    "Duplicate Rows",
                    "Invalid Values",
                    "Outliers",
                    "Constant Columns",
                    "High Cardinality",
                    "Strong Correlations",
                    "Potential Leakage"
                ],

                "Detected": [
                    "Yes" if missing_cells > 0 else "No",
                    "Yes" if duplicate_rows > 0 else "No",
                    "Yes" if invalid_count > 0 else "No",
                    "Yes" if outlier_count > 0 else "No",
                    "Yes" if constant_columns else "No",
                    "Yes" if high_cardinality else "No",
                    "Yes" if strong_correlations else "No",
                    "Yes" if potential_leakage else "No"
                ]
            }
        )

        st.dataframe(
            summary_data,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; "
    "color:#777b87; "
    "font-size:14px;'>"
    "🔍 AI Data Quality Detective "
    "&nbsp; | &nbsp; "
    "Intelligent Data Quality Analysis"
    "</p>",
    unsafe_allow_html=True
)