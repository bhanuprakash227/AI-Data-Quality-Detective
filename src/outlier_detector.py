import pandas as pd
import numpy as np


def analyze_outliers(df):
    """
    Detect outliers in numeric columns using the IQR method.

    IQR = Q3 - Q1
    Lower Bound = Q1 - 1.5 * IQR
    Upper Bound = Q3 + 1.5 * IQR
    """

    results = {
        "outliers": {},
        "total_outliers": 0,
        "outlier_count": 0,
        "columns_with_outliers": [],
        "summary": []
    }

    if df.empty:
        return results

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    # Remove identifier-like numeric columns
    filtered_columns = []

    for column in numeric_columns:

        column_name = str(column).lower()

        if (
            column_name == "id"
            or column_name.endswith("_id")
            or column_name.endswith("_key")
            or column_name.endswith("_code")
            or column_name == "uuid"
        ):
            continue

        filtered_columns.append(column)

    for column in filtered_columns:

        series = df[column].dropna()

        # Need enough values for meaningful IQR calculation
        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        # Constant columns cannot have meaningful IQR outliers
        if iqr == 0:
            continue

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        outlier_mask = outlier_mask.fillna(False)

        outlier_count = int(outlier_mask.sum())

        if outlier_count > 0:

            outlier_indices = df.index[
                outlier_mask
            ].tolist()

            outlier_values = df.loc[
                outlier_mask,
                column
            ].tolist()

            # Convert NumPy values to normal Python values
            clean_values = []

            for value in outlier_values:

                if pd.isna(value):
                    clean_values.append(None)

                elif isinstance(
                    value,
                    (np.integer, np.floating)
                ):
                    clean_values.append(
                        float(value)
                    )

                else:
                    clean_values.append(value)

            results["outliers"][column] = {
                "count": outlier_count,
                "percentage": round(
                    (outlier_count / len(series)) * 100,
                    2
                ),
                "q1": round(float(q1), 3),
                "q3": round(float(q3), 3),
                "iqr": round(float(iqr), 3),
                "lower_bound": round(
                    float(lower_bound),
                    3
                ),
                "upper_bound": round(
                    float(upper_bound),
                    3
                ),
                "outlier_indices": outlier_indices,
                "outlier_values": clean_values,
                "severity": (
                    "HIGH"
                    if outlier_count >= 3
                    else "MEDIUM"
                ),
                "recommendation": (
                    f"Investigate {outlier_count} outlier(s) "
                    f"in '{column}'. Determine whether they "
                    "are genuine observations or data errors "
                    "before removing or transforming them."
                )
            }

            results["columns_with_outliers"].append(
                column
            )

            results["summary"].append(
                {
                    "column": column,
                    "outlier_count": outlier_count,
                    "outlier_percentage": round(
                        (outlier_count / len(series)) * 100,
                        2
                    ),
                    "lower_bound": round(
                        float(lower_bound),
                        3
                    ),
                    "upper_bound": round(
                        float(upper_bound),
                        3
                    )
                }
            )

            results["total_outliers"] += outlier_count

    # Keep both names for compatibility
    results["outlier_count"] = results["total_outliers"]

    return results