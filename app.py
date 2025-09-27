import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# Load Dataset
# ==============================
df = pd.read_csv("Data/netflix_titles.csv",on_bad_lines='skip')

# ==============================
# Data Cleaning
# ==============================

# Drop columns not required for analysis
df = df.drop(columns=["director", "cast"])

# Fill missing countries with "Unknown"
df["country"] = df["country"].fillna("Unknown")

# Drop rows where critical columns are missing
df = df.dropna(subset=["date_added", "rating", "duration"])

# Check duplicates
print("Duplicate rows:", df.duplicated().sum())

# ==============================
# Outlier Detection
# ==============================
# Example: The 'duration' column has strings like "90 min".
# Since we are doing a Matplotlib-only project, we are not using seaborn (sns).
# Matplotlib's plt.boxplot() requires numeric data, so we must remove " min" 
# and convert the values to integers before plotting.
# Filter only movie durations with 'min'

# ==============================
# Outlier Detection
# ==============================
movie_df = df[df["type"] == "Movie"].copy()
movie_df["duration_int"] = movie_df["duration"].str.replace(" min","").astype(int)

plt.figure(figsize=(8,5))
plt.boxplot(movie_df["duration_int"], vert=False, patch_artist=True,
            boxprops=dict(facecolor="orange", color="black"),
            medianprops=dict(color="red", linewidth=2))
plt.title("Movie Duration (With Outliers)")
plt.xlabel("Duration (Minutes)")
plt.savefig("Movie_dist_outlier_plot.png",dpi=300)
plt.show()

# ==============================
# Outlier Handling (IQR Method)
# ==============================
Q1 = movie_df["duration_int"].quantile(0.25)
Q3 = movie_df["duration_int"].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5*IQR
upper_bound = Q3 + 1.5*IQR

movie_no_outliers = movie_df[
    (movie_df["duration_int"] >= lower_bound) &
    (movie_df["duration_int"] <= upper_bound)
]

plt.figure(figsize=(8,5))
plt.boxplot(movie_no_outliers["duration_int"], vert=False, patch_artist=True,
            boxprops=dict(facecolor="green", color="black"),
            medianprops=dict(color="red", linewidth=2))
plt.title("Movie Duration (Outliers Removed)")
plt.xlabel("Duration (Minutes)")
plt.savefig("Movie_dist_outlier_removed_plot.png",dpi=300)
plt.show()

# ==============================
# Q1. How Many Movies And Tv Shows
# ==============================

                            
shows_count=df["type"].value_counts()
plt.figure(figsize=(6,4)) 
plt.bar(shows_count.index,shows_count.values,color="orange",label="Type Counts",width=0.3)
plt.title("Number Of Movies vs TV Shows on Netflix") 
plt.xlabel("Types")
plt.ylabel("Counts")
plt.legend()
plt.tight_layout()
plt.savefig('movies_tvshows_plot.png',dpi=300)
plt.show()

# ==============================
# Q2. Rating Percentage
# ==============================
content_rating=df["rating"].value_counts()
vals=content_rating.values
norm=plt.Normalize(min(vals),max(vals))
colors=plt.cm.Reds(norm(vals))
plt.figure(figsize=(8,6))
plt.pie(content_rating,labels=content_rating.index,autopct="%1.1f%%",colors=colors,startangle=90)
plt.title("Percentage Count Per Rating")
plt.tight_layout()
plt.savefig("Rating_Percentage_pie.png",dpi=250)
plt.show()

# ==============================
# Q3. Distribution of Movie Duration (Histogram)
# ==============================
plt.figure(figsize=(8, 6))
plt.hist(movie_no_outliers["duration_int"], bins=30, color="purple", edgecolor="black")
plt.title("Distribution of Movie Durations")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Number of Movies")
plt.tight_layout()
plt.savefig("dist_movie_dura_plot.png")
plt.show()

# ==============================
# Q4. Number of Releases Over the Years (Movies)
# ==============================
group = movie_no_outliers.groupby("release_year")["type"].count().reset_index()
group.rename(columns={"type": "count"}, inplace=True)

plt.figure(figsize=(6, 4))
plt.plot(group["release_year"], group["count"], label="Movies Released", marker="o")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.title("Number of Movies Released Over the Years")
plt.xlabel("Release Year")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("Num_movies_release_plot")
plt.show()


# ==============================
# Q5. TV Shows Released Over the Years
# ==============================
tv_df = df[df["type"] == "TV Show"]
show_count = tv_df.groupby("release_year")["type"].count().reset_index()
show_count.rename(columns={"type": "count"}, inplace=True)

plt.figure(figsize=(8, 6))
plt.scatter(
    show_count["release_year"],
    show_count["count"],
    label="TV Shows",
    color="purple",
    s=100,
    alpha=0.7,
    edgecolors="black"
)
plt.title("TV Shows Released Over the Years")
plt.xlabel("Release Year")
plt.ylabel("Number of TV Shows")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("tv_show_over_years_plot.png",dpi=300)
plt.show()

# ==============================
# Q6. Top 10 Countries with Highest Number of TV Shows
# ==============================
shows_df = df[df["type"] == "TV Show"].copy()
shows_df["country"] = shows_df["country"].str.split(", ")
shows_df = shows_df.explode("country")
shows_df = shows_df[shows_df["country"] != "Unknown"]

top_10_con = (
    shows_df.groupby("country")["type"]
    .count()
    .reset_index(name="count")
    .sort_values(by="count", ascending=False)
    .head(10)
)

color_count = np.array(top_10_con["count"])
norm = plt.Normalize(min(color_count), max(color_count))
color = plt.cm.Reds(norm(color_count))

plt.figure(figsize=(15, 7))
plt.bar(top_10_con["country"], top_10_con["count"], color=color, alpha=0.9)
plt.title("Top 10 Countries with Highest Number of TV Shows", fontsize=15, fontweight="bold")
plt.xlabel("Countries", fontsize=12, fontweight="bold")
plt.ylabel("Number of TV Shows", fontsize=12, fontweight="bold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("coun_high_tvShows_plot.png",dpi=300)
plt.show()

# ==============================
# Q7. Compare Movies & TV Shows by Year (Subplots)
# ==============================
movies_group = movie_no_outliers.groupby("release_year")["type"].count().reset_index()
tv_group = tv_df.groupby("release_year")["type"].count().reset_index()
movies_group.rename(columns={"release_year": "year", "type": "count"}, inplace=True)
tv_group.rename(columns={"release_year": "year", "type": "count"}, inplace=True)

fig, ax = plt.subplots(1, 2, figsize=(13, 6))

# Movies per year
ax[0].bar(movies_group["year"], movies_group["count"], label="Movies")
ax[0].set_title("Movies Released Per Year", fontweight="bold")
ax[0].set_xlabel("Release Year")
ax[0].set_ylabel("Number of Movies")
ax[0].legend()

# TV shows per year
ax[1].scatter(tv_group["year"], tv_group["count"], label="TV Shows",
              color="purple", s=100, alpha=0.7, edgecolors="black")
ax[1].set_title("TV Shows Released Per Year", fontweight="bold")
ax[1].set_xlabel("Release Year")
ax[1].set_ylabel("Number of TV Shows")
ax[1].legend()
plt.tight_layout()
plt.savefig("tv_shows_release_per_year_plot.png",dpi=300)
plt.show()

df.to_csv("cleand_netflix_data.csv",index=False)