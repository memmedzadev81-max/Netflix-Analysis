"""
Netflix titles sample analysis — content mix by type, country, year, rating.
Sample data in data/netflix_titles_sample.csv.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "netflix_titles_sample.csv"
IMG = BASE / "images"
IMG.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")


def load():
    df = pd.read_csv(DATA, parse_dates=["date_added"])
    print(f"Loaded {len(df)} titles")
    return df


def clean(df):
    df = df.copy()
    df["country"] = df["country"].fillna("Unknown")
    df["primary_country"] = df["country"].astype(str).str.split(",").str[0].str.strip()
    df["year_added"] = df["date_added"].dt.year
    return df


def summary(df):
    print("\n=== Mix by type ===")
    print(df["type"].value_counts())
    print("\n=== Top countries ===")
    print(df["primary_country"].value_counts().head(10))
    print("\n=== Rating mix ===")
    print(df["rating"].value_counts().head(8))


def charts(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    df["type"].value_counts().plot(kind="bar", ax=ax, color=["#E50914", "#564d4d"])
    ax.set_title("Titles by type")
    ax.set_xlabel("")
    plt.tight_layout()
    fig.savefig(IMG / "01_type_mix.png", dpi=120)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4))
    df["primary_country"].value_counts().head(8).plot(kind="barh", ax=ax, color="#E50914")
    ax.set_title("Top countries (primary)")
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(IMG / "02_top_countries.png", dpi=120)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4))
    df.groupby("release_year").size().plot(ax=ax, color="#E50914")
    ax.set_title("Titles by release year")
    ax.set_ylabel("Count")
    plt.tight_layout()
    fig.savefig(IMG / "03_release_year.png", dpi=120)
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 4))
    top_ratings = df["rating"].value_counts().head(6).index
    sub = df[df["rating"].isin(top_ratings)]
    pd.crosstab(sub["rating"], sub["type"]).plot(kind="bar", ax=ax)
    ax.set_title("Type by rating (top ratings)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    fig.savefig(IMG / "04_type_by_rating.png", dpi=120)
    plt.close()
    print("Charts saved to images/")


def main():
    df = clean(load())
    summary(df)
    charts(df)
    movie_pct = (df["type"] == "Movie").mean() * 100
    us_pct = (df["primary_country"] == "United States").mean() * 100
    print(f"\nMovie share: {movie_pct:.1f}%")
    print(f"US primary share: {us_pct:.1f}%")
    print("Done.")


if __name__ == "__main__":
    main()
