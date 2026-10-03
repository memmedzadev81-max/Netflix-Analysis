"""
Netflix titles analysis — content mix by type, country, year, rating.
Creates a sample CSV automatically if data/netflix_titles_sample.csv is missing.
"""
from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "netflix_titles_sample.csv"
IMG = BASE / "images"
IMG.mkdir(exist_ok=True)
(BASE / "data").mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")
random.seed(42)


def ensure_sample_csv(path: Path, n: int = 250) -> None:
    if path.exists():
        return
    types = ["Movie", "TV Show"]
    ratings = ["TV-MA", "TV-14", "R", "PG-13", "TV-PG", "PG"]
    countries = [
        "United States", "India", "United Kingdom", "Japan",
        "South Korea", "Turkey", "Canada", "France", "Spain", "Mexico",
    ]
    genres = [
        "Dramas", "Comedies", "Documentaries", "Action & Adventure",
        "International Movies", "Kids' TV", "Thrillers", "Romance",
    ]
    rows = []
    for i in range(1, n + 1):
        t = "Movie" if i % 3 else "TV Show"
        if i % 5 == 0:
            country = "United States"
        else:
            country = random.choice(countries)
        rows.append(
            {
                "show_id": f"s{i}",
                "type": t,
                "title": f"Title {i}",
                "country": country,
                "release_year": random.randint(2010, 2024),
                "rating": random.choice(ratings),
                "duration": f"{random.randint(80, 160)} min" if t == "Movie" else f"{random.randint(1, 4)} Seasons",
                "listed_in": ", ".join(random.sample(genres, k=2)),
                "date_added": (datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2000))).strftime("%Y-%m-%d"),
            }
        )
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f"Created sample data: {path} ({n} rows)")


def load():
    ensure_sample_csv(DATA)
    df = pd.read_csv(DATA, parse_dates=["date_added"])
    print(f"Loaded {len(df)} titles")
    return df


def clean(df):
    df = df.copy()
    df["country"] = df["country"].fillna("Unknown")
    df["primary_country"] = df["country"].astype(str).str.split(",").str[0].str.strip()
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
    print(f"\nMovie share: {(df['type']=='Movie').mean()*100:.1f}%")
    print(f"US primary share: {(df['primary_country']=='United States').mean()*100:.1f}%")
    print("Done.")


if __name__ == "__main__":
    main()
