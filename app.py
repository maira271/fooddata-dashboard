
import streamlit as st
import pandas as pd
import sys
sys.path.append(".")
from filters import apply_filters, get_filter_options
from charts import (pie_chart, histogram, line_chart, bar_chart,
                    scatter_plot, box_plot, heatmap, area_chart,
                    count_plot, violin_plot)

st.set_page_config(
    page_title="FoodData Central Dashboard",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 FoodData Central - Nutrition Dashboard")
st.markdown("Explore nutritional data across food categories, nutrients, and years.")
st.markdown("---")

@st.cache_data
def load_data():
    # GitHub par path alag hota hai - yeh fix hai
    path = "data/FoodData_Central_foundation_food_csv_2026-04-30/"

    food = pd.read_csv(path + "food.csv")
    food_nutrient = pd.read_csv(path + "food_nutrient.csv", low_memory=False)
    nutrient = pd.read_csv(path + "nutrient.csv")
    food_category = pd.read_csv(path + "food_category.csv")

    df = food.merge(food_category, left_on="food_category_id", right_on="id", how="left")
    nutrients_merged = food_nutrient.merge(nutrient, left_on="nutrient_id", right_on="id", how="left")
    nutrients_merged = nutrients_merged[["fdc_id", "name", "amount", "unit_name"]]
    master = df.merge(nutrients_merged, on="fdc_id", how="left")
    master = master.rename(columns={
        "description_x": "food_name",
        "description_y": "category",
        "name": "nutrient_name",
        "amount": "nutrient_amount",
        "unit_name": "nutrient_unit"
    })
    master = master.dropna(subset=["nutrient_name", "nutrient_amount"])
    master["food_name"] = master["food_name"].fillna("Unknown Food")
    master["category"] = master["category"].fillna("Uncategorized")
    master = master.drop_duplicates()
    master = master[master["nutrient_amount"] >= 0]
    master["publication_date"] = pd.to_datetime(master["publication_date"], format="mixed")
    master["year"] = master["publication_date"].dt.year
    return master

df = load_data()
options = get_filter_options(df)

st.sidebar.title("🔍 Filters")
search = st.sidebar.text_input("🔎 Search Food Name")
category = st.sidebar.selectbox("📂 Category", options["categories"])
nutrient = st.sidebar.selectbox("💊 Nutrient", options["nutrients"])
data_type = st.sidebar.selectbox("📋 Data Type", options["data_types"])
year_range = st.sidebar.slider(
    "📅 Year Range",
    min_value=options["year_min"],
    max_value=options["year_max"],
    value=(options["year_min"], options["year_max"])
)
amount_range = st.sidebar.slider(
    "📊 Nutrient Amount Range",
    min_value=options["amount_min"],
    max_value=min(options["amount_max"], 1000.0),
    value=(options["amount_min"], min(options["amount_max"], 1000.0))
)
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

filtered_df = apply_filters(
    df,
    category=category,
    nutrient=nutrient,
    data_type=data_type,
    year_range=year_range,
    amount_range=amount_range,
    search_text=search
)

st.subheader("📌 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🍽️ Total Records", f"{len(filtered_df):,}")
col2.metric("📂 Categories", filtered_df["category"].nunique())
col3.metric("💊 Nutrients", filtered_df["nutrient_name"].nunique())
col4.metric("📊 Avg Amount", f"{filtered_df['nutrient_amount'].mean():.2f}")
st.markdown("---")

st.subheader("📊 Category & Distribution Analysis")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(pie_chart(filtered_df))
with col2:
    st.pyplot(histogram(filtered_df))

st.subheader("📈 Trends Over Time")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(line_chart(filtered_df))
with col2:
    st.pyplot(area_chart(filtered_df))

st.subheader("🔬 Nutrient Comparisons")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(bar_chart(filtered_df))
with col2:
    st.pyplot(scatter_plot(filtered_df))

st.subheader("📦 Statistical Distributions")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(box_plot(filtered_df))
with col2:
    st.pyplot(violin_plot(filtered_df))

st.subheader("🗺️ Heatmap & Count Analysis")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(heatmap(filtered_df))
with col2:
    st.pyplot(count_plot(filtered_df))

st.markdown("---")
st.caption("FoodData Central Dashboard | Exploratory Data Analysis Project")
