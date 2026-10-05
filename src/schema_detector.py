import pandas as pd


def analyze_schema(df):
    """
    Analyze the schema of a dataset and detect
    potential data-type and structural problems.

    Checks:
    1. Suspicious numeric columns stored as text
    2. Constant columns
    3. High-cardinality identifier-like columns
    """

    results = {
        "suspicious_numeric_columns": {},
        "constant_columns": {},
        "high_cardinality_columns": {}
    }

    # Handle empty dataset
    if df.empty:
        return results

    total_rows = len(df)

    for column in df.columns:

        series = df[column]

        column_name = str(column).lower().strip()

        # ==========================================
        # 1. Suspicious numeric columns
        # ==========================================

        if series.dtype == "object":

            non_null = series.dropna()

            if len(non_null) > 0:

                converted = pd.to_numeric(
                    non_null,
                    errors="coerce"
                )

                numeric_ratio = (
                    converted.notna().mean() * 100
                )

                # If at least 80% of the values
                # look numeric, flag the column.
                if numeric_ratio >= 80:

                    results[
                        "suspicious_numeric_columns"
                    ][column] = {

                        "current_dtype": str(
                            series.dtype
                        ),

                        "numeric_ratio": round(
                            numeric_ratio,
                            2
                        ),

                        "recommendation": (
                            f"Column '{column}' appears "
                            "mostly numeric but is stored "
                            "as text. Review non-numeric "
                            "values and consider converting "
                            "the column to a numeric type."
                        )
                    }

        # ==========================================
        # 2. Constant columns
        # ==========================================

        unique_count = series.nunique(
            dropna=False
        )

        if unique_count <= 1:

            results[
                "constant_columns"
            ][column] = {

                "unique_count": int(
                    unique_count
                ),

                "recommendation": (
                    f"Column '{column}' contains "
                    "only one unique value. It provides "
                    "little or no predictive information "
                    "and may be removed."
                )
            }

        # ==========================================
        # 3. High-cardinality columns
        # ==========================================

        cardinality_ratio = (
            unique_count / total_rows
        ) * 100

        # Determine whether the column name
        # looks like an identifier.
        is_identifier_like = (
            "id" in column_name
            or "code" in column_name
            or "key" in column_name
            or "uuid" in column_name
        )

        # Conservative rule:
        # - at least 95% unique
        # - at least 20 rows
        # - identifier-like column name
        if (
            cardinality_ratio >= 95
            and total_rows >= 20
            and is_identifier_like
        ):

            results[
                "high_cardinality_columns"
            ][column] = {

                "unique_count": int(
                    unique_count
                ),

                "cardinality_percentage": round(
                    cardinality_ratio,
                    2
                ),

                "recommendation": (
                    f"Column '{column}' has very high "
                    "cardinality and appears to be an "
                    "identifier-like field. Check whether "
                    "it should be used as a predictive "
                    "feature."
                )
            }

    return results