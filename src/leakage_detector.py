import pandas as pd


def analyze_leakage(
    df,
    target_column,
    correlation_threshold=0.70
):
    """
    Detect potential target leakage in a dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    target_column : str
        Target variable used for prediction.

    correlation_threshold : float
        Correlation threshold for detecting potentially
        suspicious numeric features.

    Returns
    -------
    dict
        Leakage analysis results.
    """

    results = {
        "target": target_column,
        "potential_leakage": []
    }

    # --------------------------------------------------
    # Validate target column
    # --------------------------------------------------

    if target_column not in df.columns:

        results["error"] = (
            f"Target column '{target_column}' "
            "was not found in the dataset."
        )

        return results

    # --------------------------------------------------
    # Get numeric columns
    # --------------------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # --------------------------------------------------
    # Target must be numeric for correlation analysis
    # --------------------------------------------------

    if target_column not in numeric_columns:

        results["message"] = (
            f"Target column '{target_column}' "
            "is not numeric. Correlation-based "
            "leakage detection was skipped."
        )

        return results

    # --------------------------------------------------
    # Calculate correlations with target
    # --------------------------------------------------

    correlations = df[numeric_columns].corr(
        method="pearson"
    )[target_column]

    # --------------------------------------------------
    # Check every feature
    # --------------------------------------------------

    for feature in numeric_columns:

        # Never compare target with itself
        if feature == target_column:
            continue

        correlation = correlations.get(feature)

        if pd.isna(correlation):
            continue

        absolute_correlation = abs(
            float(correlation)
        )

        reasons = []

        # --------------------------------------------------
        # Reason 1: High correlation
        # --------------------------------------------------

        if absolute_correlation >= 0.90:

            reasons.append(
                "Feature has extremely high correlation "
                "with the target."
            )

        elif absolute_correlation >= correlation_threshold:

            reasons.append(
                "Feature has strong correlation "
                "with the target."
            )

        # --------------------------------------------------
        # Reason 2: Target-derived naming
        # --------------------------------------------------

        feature_name = feature.lower()

        leakage_keywords = [
            "post",
            "after",
            "result",
            "outcome",
            "approved",
            "approval",
            "final",
            "decision",
            "target",
            "label",
            "future"
        ]

        target_derived_name = any(
            keyword in feature_name
            for keyword in leakage_keywords
        )

        if target_derived_name:

            reasons.append(
                "Feature name suggests post-outcome "
                "or target-derived information."
            )

        # --------------------------------------------------
        # Add potential leakage
        # --------------------------------------------------

        if reasons:

            if (
                target_derived_name
                and absolute_correlation >= 0.90
            ):

                severity = "CRITICAL"

            elif target_derived_name:

                severity = "HIGH"

            elif absolute_correlation >= 0.90:

                severity = "HIGH"

            else:

                severity = "MEDIUM"

            recommendation = (
                f"Investigate '{feature}' before using "
                "it for prediction. Confirm that this "
                "feature is available at prediction time "
                "and was not created using the target or "
                "future information."
            )

            results["potential_leakage"].append(
                {
                    "feature": feature,
                    "correlation": round(
                        float(correlation),
                        3
                    ),
                    "severity": severity,
                    "reasons": reasons,
                    "recommendation": recommendation
                }
            )

    return results