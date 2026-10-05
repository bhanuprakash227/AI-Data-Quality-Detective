import pandas as pd


def analyze_invalid_values(df):
    """
    Detect logically invalid or suspicious values
    using common column-name rules.
    """

    results = {}

    for column in df.columns:

        column_name = column.lower().strip()

        invalid_mask = pd.Series(
            False,
            index=df.index
        )

        rule = None

        # -----------------------------------
        # Age validation
        # -----------------------------------

        if "age" in column_name:

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = (
                    (df[column] < 0)
                    | (df[column] > 120)
                )

                rule = "Age should normally be between 0 and 120."

        # -----------------------------------
        # Percentage validation
        # -----------------------------------

        elif (
            "percentage" in column_name
            or "percent" in column_name
            or column_name.endswith("_pct")
        ):

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = (
                    (df[column] < 0)
                    | (df[column] > 100)
                )

                rule = (
                    "Percentage values should normally "
                    "be between 0 and 100."
                )

        # -----------------------------------
        # Rating validation
        # -----------------------------------

        elif "rating" in column_name:

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = (
                    (df[column] < 0)
                    | (df[column] > 5)
                )

                rule = (
                    "Ratings should normally be "
                    "between 0 and 5."
                )

        # -----------------------------------
        # Count validation
        # -----------------------------------

        elif (
            "count" in column_name
            or "quantity" in column_name
            or "number_of" in column_name
        ):

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = df[column] < 0

                rule = (
                    "Counts and quantities should "
                    "not normally be negative."
                )

        # -----------------------------------
        # Price / income / salary validation
        # -----------------------------------

        elif (
            "price" in column_name
            or "income" in column_name
            or "salary" in column_name
            or "amount" in column_name
            or "revenue" in column_name
        ):

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = df[column] < 0

                rule = (
                    "Financial values should not "
                    "normally be negative."
                )

        # -----------------------------------
        # Year validation
        # -----------------------------------

        elif "year" in column_name:

            if pd.api.types.is_numeric_dtype(df[column]):

                invalid_mask = (
                    (df[column] < 1900)
                    | (df[column] > 2100)
                )

                rule = (
                    "Year appears to be outside "
                    "the expected range 1900–2100."
                )

        # -----------------------------------
        # Store detected problems
        # -----------------------------------

        invalid_count = int(invalid_mask.sum())

        if invalid_count > 0:

            invalid_values = (
                df.loc[
                    invalid_mask,
                    column
                ]
                .dropna()
                .tolist()
            )

            results[column] = {
                "invalid_count": invalid_count,
                "invalid_values": invalid_values,
                "rule": rule,
                "severity": "HIGH",
                "recommendation": (
                    f"Review the {invalid_count} "
                    f"suspicious value(s) in '{column}'. "
                    f"Validation rule: {rule}"
                )
            }

    return results