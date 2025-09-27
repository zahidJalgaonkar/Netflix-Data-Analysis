Netflix Titles Data Analysis (Python | Pandas | Matplotlib)

 Overview
This project analyzes the **Netflix Titles Dataset** using Python, Pandas, NumPy, and Matplotlib to uncover key insights about content distribution, ratings, duration patterns, country-wise trends, and release dynamics.  
The project demonstrates an **end-to-end data analytics workflow** including cleaning, preprocessing, exploratory data analysis (EDA), outlier treatment, and visualization — all implemented in a single Python script.


 Project Objectives
- Clean and preprocess the Netflix dataset for analysis.
- Explore the distribution of movies vs TV shows.
- Analyze ratings, durations, and release year trends.
- Identify top content-producing countries.
- Visualize key insights with Matplotlib.


 Dataset Information
- **Source:** [Netflix Titles Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)  
- **File:** `netflix_titles.csv`
- **Size:** ~8,800 entries  
- **Features:**

| Column         | Description                                            |
|---------------|--------------------------------------------------------|
| `show_id`     | Unique identifier for each title                       |
| `type`        | Type of content — Movie or TV Show                     |
| `title`       | Title of the content                                   |
| `country`     | Country of origin                                      |
| `date_added`  | Date when added to Netflix                             |
| `release_year`| Original release year                                  |
| `rating`      | Age/content rating (e.g., TV-MA, PG-13)                |
| `duration`    | Duration (minutes for movies / seasons for shows)      |


 Tools & Technologies
- **Language:** Python 3.13.5
- **Libraries:**  
  - `pandas` – Data cleaning and manipulation  
  - `numpy` – Numerical operations  
  - `matplotlib` – Data visualization  

*(Seaborn is intentionally not used — to focus on mastering core Matplotlib visualization first.)*

 Data Cleaning & Preparation
Performed key preprocessing steps:
- Removed unnecessary columns: `director`, `cast`
- Filled missing `country` values with `"Unknown"`
- Dropped rows with missing `date_added`, `rating`, or `duration`
- Converted movie duration from string to integer  
- Detected and removed outliers using the **IQR (Interquartile Range)** method

        
 Exploratory Data Analysis (EDA)

1. Movies vs TV Shows  
- Bar chart comparison showing content distribution.
- **Insight:** Movies dominate Netflix’s catalog compared to TV shows.

2. Rating Distribution  
- Pie chart visualizing content rating percentages.
- **Insight:** `TV-MA` and `TV-14` are the most common ratings.

3. Movie Duration Analysis  
- Boxplots (with and without outliers)  
- Histogram of movie durations  
- **Insight:** Most movies fall in the 80–120 minute range.

4. Release Trends Over the Years  
- Line and scatter plots showing number of releases per year.  
- **Insight:** Significant growth in content releases between **2015–2020**.

5. Top 10 Countries Producing TV Shows  
- Horizontal bar chart of top producers.  
- **Insight:** USA, India, and UK lead in original content creation.

6. Movies vs TV Shows Comparison Per Year  
- Side-by-side visualization of both categories over time.


 Key Insights & Findings
-  **Movies outnumber TV shows**, but TV show growth is steady.  
-  Peak content production occurred during **2018–2020**.  
-  Most Netflix movies are **~90 minutes**, aligning with viewer engagement norms.  
-  Top content-producing countries: **USA, India, UK**.  
-  Most content is rated **TV-MA** or **TV-14**, targeting mature audiences.


 How to Run the Project

1. Clone the Repository
```bash
git clone https://github.com/your-username/netflix-analysis.git
cd netflix-analysis
