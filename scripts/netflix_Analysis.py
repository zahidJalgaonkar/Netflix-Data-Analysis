import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# Load Dataset
# ==============================
df = pd.read_csv("Data/netflix_titles.csv")

# ==============================
# Data Cleaning
# ==============================
df = df.drop(columns=["director", "cast"])
df["country"] = df["country"].fillna("Unknown")
df = df.dropna(subset=["date_added", "rating", "duration"])
print("Duplicate rows:", df.duplicated().sum())

# ==============================
# Outlier Detection (Movies)
# ==============================
movie_df = df[df["type"] == "Movie"].copy()
movie_df["duration_int"] = movie_df["duration"].str.replace(" min","").astype(int)

plt.figure(figsize=(8,5))
plt.boxplot(movie_df["duration_int"], vert=False, patch_artist=True,
            boxprops=dict(facecolor="#FFA500", color="black"),
            medianprops=dict(color="red", linewidth=2))
plt.title("Movie Duration (With Outliers)", fontsize=14, fontweight="bold")
plt.xlabel("Duration (Minutes)", fontsize=12)
plt.tight_layout()
# plt.savefig("movie_outliers.png", dpi=300)
plt.show()

# ==============================
# Outlier Handling (IQR)
# ==============================
Q1 = movie_df["duration_int"].quantile(0.25)
Q3 = movie_df["duration_int"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
movie_no_outliers = movie_df[(movie_df["duration_int"] >= lower) & (movie_df["duration_int"] <= upper)]

plt.figure(figsize=(8,5))
plt.boxplot(movie_no_outliers["duration_int"], vert=False, patch_artist=True,
            boxprops=dict(facecolor="#32CD32", color="black"),
            medianprops=dict(color="red", linewidth=2))
plt.title("Movie Duration (Outliers Removed)", fontsize=14, fontweight="bold")
plt.xlabel("Duration (Minutes)", fontsize=12)
plt.tight_layout()
# plt.savefig("movie_no_outliers.png", dpi=300)
plt.show()

# ==============================
# Q1. Movies vs TV Shows
# ==============================
shows_count = df["type"].value_counts()
plt.figure(figsize=(6,4))
plt.bar(shows_count.index, shows_count.values, color="#FFA500", width=0.3)
plt.title("Movies vs TV Shows", fontsize=14, fontweight="bold")
plt.xlabel("Type", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.tight_layout()
# plt.savefig("type_counts.png", dpi=300)
plt.show()

# ==============================
# Q2. Rating Percentage
# ==============================
rating_counts = df["rating"].value_counts()
vals = rating_counts.values
norm = plt.Normalize(min(vals), max(vals))
colors = plt.cm.Reds(norm(vals))

plt.figure(figsize=(8,6))
plt.pie(rating_counts, labels=rating_counts.index, autopct="%1.1f%%", colors=colors, startangle=90)
plt.title("Percentage of Ratings", fontsize=14, fontweight="bold")
plt.tight_layout()
# plt.savefig("rating_pct.png", dpi=300)
plt.show()

# ==============================
# Q3. Movie Duration Histogram
# ==============================
plt.figure(figsize=(8,6))
plt.hist(movie_no_outliers["duration_int"], bins=30, color="#800080", edgecolor="black")
plt.title("Distribution of Movie Durations", fontsize=14, fontweight="bold")
plt.xlabel("Duration (Minutes)", fontsize=12)
plt.ylabel("Number of Movies", fontsize=12)
plt.tight_layout()
# plt.savefig("movie_duration.png", dpi=300)
plt.show()

# ==============================
# Q4. Movies Released Over Years
# ==============================
movies_group = movie_no_outliers.groupby("release_year")["type"].count().reset_index()
movies_group.rename(columns={"type":"count"}, inplace=True)

plt.figure(figsize=(8,5))
plt.plot(movies_group["release_year"], movies_group["count"], marker="o", color="#1f77b4")
plt.title("Movies Released Over Years", fontsize=14, fontweight="bold")
plt.xlabel("Release Year", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
# plt.savefig("movies_year.png", dpi=300)
plt.show()

# ==============================
# Q5. TV Shows Released Over Years
# ==============================
tv_df = df[df["type"]=="TV Show"]
tv_group = tv_df.groupby("release_year")["type"].count().reset_index()
tv_group.rename(columns={"type":"count"}, inplace=True)

plt.figure(figsize=(8,5))
plt.scatter(tv_group["release_year"], tv_group["count"], color="#800080", s=100, alpha=0.7, edgecolors="black")
plt.title("TV Shows Released Over Years", fontsize=14, fontweight="bold")
plt.xlabel("Release Year", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
# plt.savefig("tv_year.png", dpi=300)
plt.show()

# ==============================
# Q6. Top 10 Countries by TV Shows
# ==============================
shows_df = tv_df.copy()
shows_df["country"] = shows_df["country"].str.split(", ")
shows_df = shows_df.explode("country")
shows_df = shows_df[shows_df["country"] != "Unknown"]

top10 = shows_df.groupby("country")["type"].count().reset_index(name="count").sort_values(by="count", ascending=False).head(10)
colors = plt.cm.Reds(plt.Normalize(top10["count"].min(), top10["count"].max())(top10["count"]))

plt.figure(figsize=(12,6))
plt.bar(top10["country"], top10["count"], color=colors, alpha=0.9)
plt.title("Top 10 Countries by TV Shows", fontsize=14, fontweight="bold")
plt.xlabel("Country", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig("top10_countries.png", dpi=300)
plt.show()

# ==============================
# Q7. Compare Movies & TV Shows Per Year
# ==============================
movies_group.rename(columns={"release_year":"year"}, inplace=True)
tv_group.rename(columns={"release_year":"year"}, inplace=True)

fig, ax = plt.subplots(1,2,figsize=(13,6))

ax[0].bar(movies_group["year"], movies_group["count"], color="#1f77b4")
ax[0].set_title("Movies Per Year", fontsize=14, fontweight="bold")
ax[0].set_xlabel("Year", fontsize=12)
ax[0].set_ylabel("Count", fontsize=12)

ax[1].scatter(tv_group["year"], tv_group["count"], color="#800080", s=100, alpha=0.7, edgecolors="black")
ax[1].set_title("TV Shows Per Year", fontsize=14, fontweight="bold")
ax[1].set_xlabel("Year", fontsize=12)
ax[1].set_ylabel("Count", fontsize=12)
ax[1].grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
# plt.savefig("movies_vs_tv.png", dpi=300)
plt.show()
