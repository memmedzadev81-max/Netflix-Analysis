# Netflix Titles Analysis

Content mix for a sample of streaming titles — type, country, release year and rating.

Finished EDA on sample data (not an empty scaffold). You can replace the CSV with the full Kaggle Netflix titles file for catalog-scale numbers.

---

## Questions

1. Movies vs TV shows — what is the mix?
2. Which countries show up most often?
3. How does volume look by release year?
4. How do ratings differ by type?

---

## Data

| Item | Detail |
|------|--------|
| File | `data/netflix_titles_sample.csv` |
| Rows | 250 sample titles |
| Fields | type, title, country, release_year, rating, duration, listed_in, date_added |

Sample is built so the project runs without a large download. Swap for a real extract when you need real-market figures.

---

## Stack

Python · pandas · matplotlib · seaborn

---

## How to run

```bash
pip install -r requirements.txt
python analysis.py
```

Charts are written to `images/`.

---

## Structure

```
Netflix-Analysis/
├── data/netflix_titles_sample.csv
├── images/
├── analysis.py
├── requirements.txt
└── README.md
```

---

Vusal Mammadzade · [memmedzadev81-max](https://github.com/memmedzadev81-max)
