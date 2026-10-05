import pandas as pd


def analyze_missing_values(df):
    """
    Analyze missing values in each column.

    Returns:
        Dictionary containing missing count,
        missing percentage, severity, and recommendation.
    """

    results = {}

    total_rows = len(df)

    if total_rows == 0:
        return results

    for column in df.columns:

        missing_count = int(df[column].isna().sum())

        if missing_count == 0:
            continue

        missing_percentage = (
            missing_count / total_rows
        ) * 100

        if missing_percentage >= 30:
            severity = "CRITICAL"
            recommendation = (
                "Investigate the reason for the missing values. "
                "Consider whether the column should be retained."
            )

        elif missing_percentage >= 10:
            severity = "HIGH"
            recommendation = (
                "Investigate the missing-value pattern. "
                "Consider an appropriate imputation strategy."
            )

        elif missing_percentage >= 5:
            severity = "MEDIUM"
            recommendation = (
                "Review the missing records and consider "
                "appropriate imputation."
            )

        else:
            severity = "LOW"
            recommendation = (
                "Small amount of missing data. "
                "Review before deciding whether to impute or remove."
            )

        results[column] = {
            "missing_count": missing_count,
            "missing_percentage": round(
                missing_percentage, 2
            ),
            "severity": severity,
            "recommendation": recommendation
        }

    return results