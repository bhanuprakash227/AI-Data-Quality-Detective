import pandas as pd


def analyze_duplicates(df):
    """
    Analyze duplicate rows and duplicate values in
    identifier-like columns.
    """

    total_rows = len(df)

    # --------------------------------------------------
    # Duplicate rows
    # --------------------------------------------------

    duplicate_rows = int(df.duplicated().sum())

    if total_rows > 0:
        duplicate_row_percentage = (
            duplicate_rows / total_rows
        ) * 100
    else:
        duplicate_row_percentage = 0.0

    # --------------------------------------------------
    # Detect identifier-like columns
    # --------------------------------------------------

    identifier_keywords = [
        "id",
        "identifier",
        "code",
        "uuid",
        "key"
    ]

    identifier_columns = []

    for column in df.columns:

        column_name = str(column).lower()

        if any(
            keyword in column_name
            for keyword in identifier_keywords
        ):
            identifier_columns.append(column)

    # --------------------------------------------------
    # Analyze duplicate values in identifier columns
    # --------------------------------------------------

    duplicate_identifier_columns = {}

    for column in identifier_columns:

        duplicate_count = int(
            df[column].duplicated().sum()
        )

        unique_count = int(
            df[column].nunique(dropna=True)
        )

        if duplicate_count > 0:

            duplicate_identifier_columns[column] = {
                "duplicate_count": duplicate_count,
                "unique_count": unique_count,
                "severity": "HIGH",
                "recommendation": (
                    f"Investigate duplicate values in "
                    f"identifier column '{column}'. "
                    "Identifiers are normally expected "
                    "to be unique."
                )
            }

    # --------------------------------------------------
    # Return complete result
    # --------------------------------------------------

    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_row_percentage": round(
            duplicate_row_percentage,
            2
        ),
        "duplicate_identifier_columns":
            duplicate_identifier_columns
    }