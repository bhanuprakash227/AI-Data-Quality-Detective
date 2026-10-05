import pandas as pd

from src.duplicate_checker import analyze_duplicates
from src.missing_values import analyze_missing_values
from src.profiler import profile_dataset
from src.invalid_values import analyze_invalid_values
from src.outlier_detector import detect_outliers
from src.schema_detector import analyze_schema
from src.correlation_detector import analyze_correlations
from src.leakage_detector import analyze_leakage
from src.quality_score import calculate_quality_score


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("data/sample.csv")


# ==========================================
# 1. DATASET PROFILE
# ==========================================

profile = profile_dataset(df)

print("\n===== DATASET PROFILE =====")

print("Rows:", profile["rows"])
print("Columns:", profile["columns"])

print("\nColumn Names:")
print(profile["column_names"])

print("\nData Types:")
print(profile["data_types"])

print("\nNumeric Columns:")
print(profile["numeric_columns"])

print("\nCategorical Columns:")
print(profile["categorical_columns"])

print("\nMissing Values:")
print(profile["missing_values"])

print("\nDuplicate Rows:")
print(profile["duplicate_rows"])

print("\nUnique Values:")
print(profile["unique_values"])

print("\nStatistics:")
print(profile["statistics"])


# ==========================================
# 2. MISSING VALUE ANALYSIS
# ==========================================

missing_results = analyze_missing_values(df)

print("\n===== MISSING VALUE ANALYSIS =====")

for column, result in missing_results.items():

    print("\nColumn:", column)
    print("Missing Count:", result["missing_count"])
    print(
        "Missing Percentage:",
        f'{result["missing_percentage"]:.2f}%'
    )
    print("Severity:", result["severity"])
    print("Recommendation:", result["recommendation"])


# ==========================================
# 3. DUPLICATE ANALYSIS
# ==========================================

duplicate_results = analyze_duplicates(df)

print("\n===== DUPLICATE ANALYSIS =====")

print(
    "Duplicate Rows:",
    duplicate_results["duplicate_rows"]
)

print(
    "Duplicate Row Percentage:",
    f'{duplicate_results["duplicate_row_percentage"]:.2f}%'
)

print("\nDuplicate Identifier Columns:")

for column, result in duplicate_results[
    "duplicate_identifier_columns"
].items():

    print("\nColumn:", column)
    print("Duplicate Count:", result["duplicate_count"])
    print("Unique Count:", result["unique_count"])
    print("Severity:", result["severity"])
    print("Recommendation:", result["recommendation"])


# ==========================================
# 4. INVALID VALUE ANALYSIS
# ==========================================

invalid_results = analyze_invalid_values(df)

print("\n===== INVALID VALUE ANALYSIS =====")

for column, result in invalid_results.items():

    if result["invalid_count"] == 0:
        continue

    print("\nColumn:", column)
    print("Invalid Count:", result["invalid_count"])
    print("Invalid Values:", result["invalid_values"])
    print("Severity:", result["severity"])
    print("Rule:", result["rule"])
    print("Recommendation:", result["recommendation"])


# ==========================================
# 5. OUTLIER ANALYSIS
# ==========================================

outlier_results = detect_outliers(df)

print("\n===== OUTLIER ANALYSIS =====")

for column, result in outlier_results.items():

    if result["outlier_count"] == 0:
        continue

    print("\nColumn:", column)
    print("Outlier Count:", result["outlier_count"])
    print(
        "Outlier Percentage:",
        f'{result["outlier_percentage"]:.2f}%'
    )
    print("Q1:", result["q1"])
    print("Q3:", result["q3"])
    print("IQR:", result["iqr"])
    print("Lower Bound:", result["lower_bound"])
    print("Upper Bound:", result["upper_bound"])
    print("Outlier Values:", result["outlier_values"])
    print("Severity:", result["severity"])
    print("Method:", result["method"])
    print("Recommendation:", result["recommendation"])


# ==========================================
# 6. SCHEMA ANALYSIS
# ==========================================

schema_results = analyze_schema(df)

print("\n===== SCHEMA ANALYSIS =====")

print("\nSuspicious Numeric Columns:")

for column, result in schema_results[
    "suspicious_numeric_columns"
].items():

    print("\nColumn:", column)
    print("Reason:", result["reason"])
    print("Recommendation:", result["recommendation"])


print("\nConstant Columns:")

for column, result in schema_results[
    "constant_columns"
].items():

    print("\nColumn:", column)
    print("Unique Values:", result["unique_count"])
    print("Recommendation:", result["recommendation"])


print("\nHigh Cardinality Columns:")

for column, result in schema_results[
    "high_cardinality_columns"
].items():

    print("\nColumn:", column)
    print("Unique Values:", result["unique_count"])
    print(
        "Cardinality:",
        f'{result["cardinality_percentage"]:.2f}%'
    )
    print("Recommendation:", result["recommendation"])


# ==========================================
# 7. CORRELATION ANALYSIS
# ==========================================

correlation_results = analyze_correlations(df)

print("\n===== CORRELATION ANALYSIS =====")

print("\nStrong Correlations:")

for result in correlation_results[
    "strong_correlations"
]:

    print("\nFeature 1:", result["feature_1"])
    print("Feature 2:", result["feature_2"])
    print("Correlation:", result["correlation"])
    print("Strength:", result["strength"])
    print("Recommendation:", result["recommendation"])


# ==========================================
# 8. TARGET LEAKAGE ANALYSIS
# ==========================================

target_column = "loan_approved"

leakage_results = analyze_leakage(
    df,
    target_column
)

print("\n===== TARGET LEAKAGE ANALYSIS =====")

print("\nTarget:", target_column)

print("\nPotential Leakage:")

for result in leakage_results[
    "potential_leakage"
]:

    print("\nFeature:", result["feature"])
    print(
        "Correlation with Target:",
        result["correlation"]
    )
    print("Severity:", result["severity"])

    print("Reasons:")

    for reason in result["reasons"]:
        print("-", reason)

    print(
        "Recommendation:",
        result["recommendation"]
    )


# ==========================================
# 9. OVERALL DATA QUALITY SCORE
# ==========================================

quality_result = calculate_quality_score(
    df=df,
    profile=profile,
    missing_results=missing_results,
    duplicate_results=duplicate_results,
    invalid_results=invalid_results,
    outlier_results=outlier_results,
    schema_results=schema_results,
    leakage_results=leakage_results
)


# ==========================================
# 10. DISPLAY QUALITY SCORE
# ==========================================

print("\n")
print("=" * 50)
print("           DATA QUALITY SCORE")
print("=" * 50)

print(
    f'\nScore: {quality_result["score"]}/100'
)

print(
    f'Status: {quality_result["status"]}'
)


# ==========================================
# 11. CRITICAL PROBLEMS
# ==========================================

print("\n===== CRITICAL PROBLEMS =====")

if quality_result["critical_problems"]:

    for problem in quality_result[
        "critical_problems"
    ]:
        print("🔴", problem)

else:

    print("No critical problems detected.")


# ==========================================
# 12. WARNINGS
# ==========================================

print("\n===== WARNINGS =====")

if quality_result["warnings"]:

    for warning in quality_result["warnings"]:
        print("🟡", warning)

else:

    print("No major warnings detected.")


# ==========================================
# 13. DETAILED SCORE BREAKDOWN
# ==========================================

print("\n===== SCORE BREAKDOWN =====")

for detail in quality_result["details"]:

    print(
        f'\n{detail["type"]}'
    )

    if detail["column"]:

        print(
            "Column:",
            detail["column"]
        )

    print(
        "Severity:",
        detail["severity"]
    )

    print(
        "Deduction:",
        detail["deduction"]
    )

    print(
        "Message:",
        detail["message"]
    )


print("\n" + "=" * 50)
print("       ANALYSIS COMPLETED")
print("=" * 50)