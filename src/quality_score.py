def calculate_quality_score(
    df,
    profile,
    missing_results,
    duplicate_results,
    invalid_results,
    outlier_results,
    schema_results,
    leakage_results=None
):
    """
    Calculate an overall data quality score.

    Score starts at 100 and deductions are applied
    based on detected data-quality problems.

    The score is intended as a practical diagnostic,
    not as a universal statistical standard.
    """

    score = 100

    critical_problems = []
    warnings = []
    details = []

    # ==========================================
    # 1. Missing values
    # ==========================================

    for column, info in missing_results.items():

        percentage = info.get(
            "missing_percentage",
            0
        )

        count = info.get(
            "missing_count",
            0
        )

        if percentage >= 20:

            deduction = 15
            severity = "CRITICAL"

        elif percentage >= 10:

            deduction = 10
            severity = "HIGH"

        elif percentage > 0:

            deduction = 5
            severity = "LOW"

        else:
            continue

        score -= deduction

        message = (
            f"{percentage:.2f}% missing values "
            f"in '{column}' ({count} values)"
        )

        details.append({
            "type": "Missing Values",
            "column": column,
            "severity": severity,
            "deduction": deduction,
            "message": message
        })

        if severity in ["CRITICAL", "HIGH"]:
            critical_problems.append(message)
        else:
            warnings.append(message)

    # ==========================================
    # 2. Duplicate rows
    # ==========================================

    duplicate_rows = duplicate_results.get(
        "duplicate_rows",
        0
    )

    if duplicate_rows > 0:

        deduction = min(
            15,
            duplicate_rows * 5
        )

        score -= deduction

        message = (
            f"{duplicate_rows} duplicate row(s) detected"
        )

        critical_problems.append(message)

        details.append({
            "type": "Duplicate Rows",
            "column": None,
            "severity": "HIGH",
            "deduction": deduction,
            "message": message
        })

    # ==========================================
    # 3. Duplicate identifiers
    # ==========================================

    duplicate_identifiers = (
        duplicate_results.get(
            "duplicate_identifier_columns",
            {}
        )
    )

    for column, info in duplicate_identifiers.items():

        count = info.get(
            "duplicate_count",
            0
        )

        if count > 0:

            deduction = min(
                20,
                count * 10
            )

            score -= deduction

            message = (
                f"Duplicate values detected in "
                f"identifier column '{column}'"
            )

            critical_problems.append(message)

            details.append({
                "type": "Duplicate Identifier",
                "column": column,
                "severity": "CRITICAL",
                "deduction": deduction,
                "message": message
            })

    # ==========================================
    # 4. Invalid values
    # ==========================================

    for column, info in invalid_results.items():

        invalid_count = info.get(
            "invalid_count",
            0
        )

        if invalid_count <= 0:
            continue

        deduction = min(
            20,
            invalid_count * 10
        )

        score -= deduction

        message = (
            f"{invalid_count} invalid value(s) "
            f"detected in '{column}'"
        )

        critical_problems.append(message)

        details.append({
            "type": "Invalid Values",
            "column": column,
            "severity": "HIGH",
            "deduction": deduction,
            "message": message
        })

    # ==========================================
    # 5. Outliers
    # ==========================================

    for column, info in outlier_results.items():

        outlier_count = info.get(
            "outlier_count",
            0
        )

        if outlier_count <= 0:
            continue

        deduction = min(
            10,
            outlier_count * 3
        )

        score -= deduction

        message = (
            f"{outlier_count} statistical outlier(s) "
            f"detected in '{column}'"
        )

        warnings.append(message)

        details.append({
            "type": "Outliers",
            "column": column,
            "severity": "MEDIUM",
            "deduction": deduction,
            "message": message
        })

    # ==========================================
    # 6. Constant columns
    # ==========================================

    constant_columns = schema_results.get(
        "constant_columns",
        {}
    )

    for column in constant_columns:

        deduction = 3

        score -= deduction

        message = (
            f"Constant column '{column}' "
            "contains only one unique value"
        )

        warnings.append(message)

        details.append({
            "type": "Constant Column",
            "column": column,
            "severity": "LOW",
            "deduction": deduction,
            "message": message
        })

    # ==========================================
    # 7. High-cardinality identifiers
    # ==========================================

    high_cardinality = schema_results.get(
        "high_cardinality_columns",
        {}
    )

    for column in high_cardinality:

        deduction = 3

        score -= deduction

        message = (
            f"High-cardinality identifier-like "
            f"column '{column}' detected"
        )

        warnings.append(message)

        details.append({
            "type": "High Cardinality",
            "column": column,
            "severity": "LOW",
            "deduction": deduction,
            "message": message
        })

    # ==========================================
    # 8. Target leakage
    # ==========================================

    if leakage_results:

        potential_leakage = (
            leakage_results.get(
                "potential_leakage",
                []
            )
        )

        for item in potential_leakage:

            severity = item.get(
                "severity",
                "MEDIUM"
            )

            feature = item.get(
                "feature",
                "unknown"
            )

            if severity == "CRITICAL":
                deduction = 20
            elif severity == "HIGH":
                deduction = 15
            else:
                deduction = 5

            score -= deduction

            message = (
                f"Potential target leakage detected "
                f"in '{feature}'"
            )

            if severity in [
                "CRITICAL",
                "HIGH"
            ]:
                critical_problems.append(
                    message
                )
            else:
                warnings.append(message)

            details.append({
                "type": "Target Leakage",
                "column": feature,
                "severity": severity,
                "deduction": deduction,
                "message": message
            })

    # ==========================================
    # Final score
    # ==========================================

    score = max(
        0,
        min(100, score)
    )

    # ==========================================
    # Quality status
    # ==========================================

    if score >= 90:
        status = "EXCELLENT"
    elif score >= 75:
        status = "GOOD"
    elif score >= 60:
        status = "NEEDS ATTENTION"
    elif score >= 40:
        status = "POOR"
    else:
        status = "CRITICAL"

    return {
        "score": score,
        "status": status,
        "critical_problems": critical_problems,
        "warnings": warnings,
        "details": details
    }