
import pandas as pd

def apply_filters(df, category=None, nutrient=None, data_type=None,
                  year_range=None, amount_range=None, search_text=None):

    filtered = df.copy()

    if category and category != "All":
        filtered = filtered[filtered["category"] == category]

    if nutrient and nutrient != "All":
        filtered = filtered[filtered["nutrient_name"] == nutrient]

    if data_type and data_type != "All":
        filtered = filtered[filtered["data_type"] == data_type]

    if year_range:
        filtered = filtered[
            (filtered["year"] >= year_range[0]) &
            (filtered["year"] <= year_range[1])
        ]

    if amount_range:
        filtered = filtered[
            (filtered["nutrient_amount"] >= amount_range[0]) &
            (filtered["nutrient_amount"] <= amount_range[1])
        ]

    if search_text and search_text.strip() != "":
        filtered = filtered[
            filtered["food_name"].str.contains(search_text, case=False, na=False)
        ]

    return filtered


def get_filter_options(df):
    return {
        "categories": ["All"] + sorted(df["category"].dropna().unique().tolist()),
        "nutrients": ["All"] + sorted(df["nutrient_name"].dropna().unique().tolist()),
        "data_types": ["All"] + sorted(df["data_type"].dropna().unique().tolist()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "amount_min": float(df["nutrient_amount"].min()),
        "amount_max": float(df["nutrient_amount"].max()),
    }
