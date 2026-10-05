import pandas as pd


def profile_dataset(df):
    """
    Generate a basic profile of the given dataset.
    """

    if df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "column_names": [],
            "data_types": {},
            "numeric_columns": [],
            "categorical_columns": [],
            "missing_values": {},
            "duplicate_rows": 0,
            "unique_values": {},
            "statistics": {}
        }

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    missing_values = df.isnull().sum()
    missing_values = missing_values[
        missing_values > 0
    ].to_dict()

    unique_values = df.nunique(
        dropna=False
    ).to_dict()

    statistics = {}

    if numeric_columns:
        statistics = (
            df[numeric_columns]
            .describe()
            .round(2)
            .to_dict()
        )

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_values": missing_values,
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_values": unique_values,
        "statistics": statistics
    }

    return profile