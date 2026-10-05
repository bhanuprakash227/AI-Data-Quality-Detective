import pandas as pd
import numpy as np


def analyze_correlations(df, threshold=0.7):

    results = {
        "strong_correlations": [],
        "correlation_matrix": {}
    }

    # Select numeric columns
    numeric_df = df.select_dtypes(
        include=np.number
    ).copy()

    # Exclude identifiers
    id_columns = [
        col for col in numeric_df.columns
        if str(col).lower().endswith(
            ("_id", "_key", "_code")
        )
        or str(col).lower() in ("id", "uuid")
    ]

    numeric_df = numeric_df.drop(
        columns=id_columns
    )

    # Remove constant columns
    numeric_df = numeric_df.loc[
        :,
        numeric_df.nunique() > 1
    ]

    if numeric_df.shape[1] < 2:
        return results

    # Pearson correlation
    corr_matrix = numeric_df.corr()

    results["correlation_matrix"] = (
        corr_matrix.round(3).to_dict()
    )

    columns = corr_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            col1 = columns[i]
            col2 = columns[j]

            correlation = corr_matrix.loc[
                col1, col2
            ]

            if pd.isna(correlation):
                continue

            strength = abs(correlation)

            if strength >= threshold:

                if strength >= 0.90:
                    level = "VERY STRONG"
                else:
                    level = "STRONG"

                results[
                    "strong_correlations"
                ].append({
                    "feature_1": col1,
                    "feature_2": col2,
                    "correlation": round(
                        float(correlation), 3
                    ),
                    "strength": level,
                    "recommendation": (
                        "Investigate whether these "
                        "features contain redundant "
                        "information. High correlation "
                        "does not automatically mean "
                        "one must be removed."
                    )
                })

    return results