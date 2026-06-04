
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Color theme
COLORS = sns.color_palette("viridis", 10)
sns.set_theme(style="whitegrid")

def pie_chart(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    category_counts = df["category"].value_counts().head(10)
    ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%",
           colors=sns.color_palette("viridis", len(category_counts)))
    ax.set_title("Food Category Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig

def histogram(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    data = df[df["nutrient_amount"] < df["nutrient_amount"].quantile(0.95)]
    sns.histplot(data["nutrient_amount"], bins=40, color=COLORS[2], ax=ax)
    ax.set_title("Nutrient Amount Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Frequency")
    plt.tight_layout()
    return fig

def line_chart(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    yearly = df.groupby("year")["nutrient_amount"].mean().reset_index()
    ax.plot(yearly["year"], yearly["nutrient_amount"], marker="o",
            color=COLORS[3], linewidth=2)
    ax.set_title("Average Nutrient Amount Over Years", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average Amount")
    plt.tight_layout()
    return fig

def bar_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_nutrients = df.groupby("nutrient_name")["nutrient_amount"].mean().nlargest(10)
    sns.barplot(x=top_nutrients.values, y=top_nutrients.index,
                palette="viridis", ax=ax)
    ax.set_title("Top 10 Nutrients by Average Amount", fontsize=14, fontweight="bold")
    ax.set_xlabel("Average Amount")
    ax.set_ylabel("Nutrient")
    plt.tight_layout()
    return fig

def scatter_plot(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    sample = df[df["nutrient_name"].isin(["Energy", "Protein"])].head(500)
    energy = sample[sample["nutrient_name"] == "Energy"][["fdc_id", "nutrient_amount"]].rename(columns={"nutrient_amount": "energy"})
    protein = sample[sample["nutrient_name"] == "Protein"][["fdc_id", "nutrient_amount"]].rename(columns={"nutrient_amount": "protein"})
    merged = energy.merge(protein, on="fdc_id")
    ax.scatter(merged["energy"], merged["protein"], alpha=0.6, color=COLORS[4])
    ax.set_title("Energy vs Protein", fontsize=14, fontweight="bold")
    ax.set_xlabel("Energy")
    ax.set_ylabel("Protein")
    plt.tight_layout()
    return fig

def box_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_cats = df["category"].value_counts().head(6).index
    data = df[df["category"].isin(top_cats) & (df["nutrient_amount"] < df["nutrient_amount"].quantile(0.90))]
    sns.boxplot(data=data, x="category", y="nutrient_amount", palette="viridis", ax=ax)
    ax.set_title("Nutrient Amount by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig

def heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 7))
    top_nutrients = df["nutrient_name"].value_counts().head(10).index
    pivot = df[df["nutrient_name"].isin(top_nutrients)].pivot_table(
        index="category", columns="nutrient_name", values="nutrient_amount", aggfunc="mean"
    ).fillna(0)
    sns.heatmap(pivot, cmap="viridis", ax=ax, linewidths=0.5)
    ax.set_title("Nutrient Heatmap by Category", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig

def area_chart(df):
    fig, ax = plt.subplots(figsize=(8, 6))
    yearly = df.groupby("year")["nutrient_amount"].sum().reset_index()
    ax.fill_between(yearly["year"], yearly["nutrient_amount"],
                    color=COLORS[5], alpha=0.6)
    ax.plot(yearly["year"], yearly["nutrient_amount"], color=COLORS[5], linewidth=2)
    ax.set_title("Total Nutrient Amount Over Years", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Amount")
    plt.tight_layout()
    return fig

def count_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    order = df["data_type"].value_counts().index
    sns.countplot(data=df, y="data_type", order=order, palette="viridis", ax=ax)
    ax.set_title("Food Count by Data Type", fontsize=14, fontweight="bold")
    ax.set_xlabel("Count")
    ax.set_ylabel("Data Type")
    plt.tight_layout()
    return fig

def violin_plot(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_nutrients = df["nutrient_name"].value_counts().head(5).index
    data = df[df["nutrient_name"].isin(top_nutrients) &
              (df["nutrient_amount"] < df["nutrient_amount"].quantile(0.90))]
    sns.violinplot(data=data, x="nutrient_name", y="nutrient_amount",
                   palette="viridis", ax=ax)
    ax.set_title("Nutrient Distribution (Violin)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Nutrient")
    ax.set_ylabel("Amount")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    return fig
