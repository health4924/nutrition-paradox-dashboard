import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# ------------------- Database Connection -------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mama@4924",
        database="nutrition"
    )

# ------------------- Run SQL Query and Return DataFrame -------------------
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ------------------- Page Config and Title -------------------
st.set_page_config(page_title="Nutrition Paradox Dashboard", layout="wide")
st.title("🌍 Nutrition Paradox: A Global View on Obesity and Malnutrition")

# ------------------- Obesity Queries -------------------
st.header("Obesity Queries")
obesity_query = st.selectbox("Select an obesity query", [
    "Top 5 regions with the highest average obesity levels in the most recent year(2022)",
    "Top 5 countries with highest obesity estimates",
    "Obesity trend in India over the years(Mean_estimate)",
    "Average obesity by gender",
    "Country count by obesity level category and age group",
    "Top 5 least reliable countries (highest CI_Width) and top 5 most consistent countries (smallest CI_Width)",
    "Average obesity by age group",
    "Top 10 countries with consistent low obesity (low average + low CI) over the years",
    "Countries where female obesity exceeds male by a large margin (same year)",
    "Global average obesity percentage per year"
])

if st.button("Run Obesity Query"):
    if obesity_query == "Top 5 regions with the highest average obesity levels in the most recent year(2022)":
        query = """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
            FROM obesity
            WHERE Year = 2022
            GROUP BY Region
            ORDER BY avg_obesity DESC
            LIMIT 5;
        """
    elif obesity_query == "Top 5 countries with highest obesity estimates":
        query = """
            SELECT Country, MAX(Mean_Estimate) AS max_obesity
            FROM obesity
            GROUP BY Country
            ORDER BY max_obesity DESC
            LIMIT 5;
        """
    elif obesity_query == "Obesity trend in India over the years(Mean_estimate)":
        query = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS obesity_trend
            FROM obesity
            WHERE Country = 'India'
            GROUP BY Year
            ORDER BY Year;
        """
    elif obesity_query == "Average obesity by gender":
        query = """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
            FROM obesity
            GROUP BY Gender;
        """
    elif obesity_query == "Country count by obesity level category and age group":
        query = """
            SELECT obesity_level, age_group, COUNT(DISTINCT Country) AS country_count
            FROM obesity
            GROUP BY obesity_level, age_group;
        """
    elif obesity_query == "Top 5 least reliable countries (highest CI_Width) and top 5 most consistent countries (smallest CI_Width)":
        query = """
            (
                SELECT Country, ROUND(AVG(CI_Width), 3) AS avg_ci
                FROM obesity
                GROUP BY Country
                ORDER BY avg_ci DESC
                LIMIT 5
            )
            UNION
            (
                SELECT Country, ROUND(AVG(CI_Width), 3) AS avg_ci
                FROM obesity
                GROUP BY Country
                ORDER BY avg_ci ASC
                LIMIT 5
            );
        """
    elif obesity_query == "Average obesity by age group":
        query = """
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS avg_obesity
            FROM obesity
            GROUP BY age_group;
        """
    elif obesity_query == "Top 10 countries with consistent low obesity (low average + low CI) over the years":
        query = """
            SELECT Country, ROUND(AVG(Mean_Estimate), 2) AS avg_obesity, ROUND(AVG(CI_Width), 2) AS avg_ci
            FROM obesity
            GROUP BY Country
            ORDER BY avg_obesity ASC, avg_ci ASC
            LIMIT 10;
        """
    elif obesity_query == "Countries where female obesity exceeds male by a large margin (same year)":
        query = """
            SELECT o1.Country, o1.Year, (o1.Mean_Estimate - o2.Mean_Estimate) AS diff
            FROM obesity o1
            JOIN obesity o2 ON o1.Country = o2.Country AND o1.Year = o2.Year
            WHERE o1.Gender = 'Female' AND o2.Gender = 'Male'
            AND (o1.Mean_Estimate - o2.Mean_Estimate) > 5
            ORDER BY diff DESC;
        """
    elif obesity_query == "Global average obesity percentage per year":
        query = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS global_avg_obesity
            FROM obesity
            GROUP BY Year
            ORDER BY Year;
        """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# ------------------- Malnutrition Queries -------------------
st.header("Malnutrition Queries")
malnutrition_query = st.selectbox("Select a malnutrition query", [
    "Avg. malnutrition by age group",
    "Top 5 countries with highest malnutrition (Mean_Estimate)",
    "Malnutrition trend in African region over the years",
    "Gender-based average malnutrition",
    "Malnutrition level-wise (average CI_Width by age group)",
    "Yearly malnutrition change in specific countries (India, Nigeria, Brazil)",
    "Regions with lowest malnutrition averages"
])

if st.button("Run Malnutrition Query"):
    if malnutrition_query == "Avg. malnutrition by age group":
        query = """
            SELECT age_group, ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
            FROM malnutrition
            GROUP BY age_group;
        """
    elif malnutrition_query == "Top 5 countries with highest malnutrition (Mean_Estimate)":
        query = """
            SELECT Country, MAX(Mean_Estimate) AS max_malnutrition
            FROM malnutrition
            GROUP BY Country
            ORDER BY max_malnutrition DESC
            LIMIT 5;
        """
    elif malnutrition_query == "Malnutrition trend in African region over the years":
        query = """
            SELECT Year, ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
            FROM malnutrition
            WHERE Region = 'Africa'
            GROUP BY Year
            ORDER BY Year;
        """
    elif malnutrition_query == "Gender-based average malnutrition":
        query = """
            SELECT Gender, ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
            FROM malnutrition
            GROUP BY Gender;
        """
    elif malnutrition_query == "Malnutrition level-wise (average CI_Width by age group)":
        query = """
            SELECT age_group, ROUND(AVG(CI_Width), 3) AS avg_ci
            FROM malnutrition
            GROUP BY age_group;
        """
    elif malnutrition_query == "Yearly malnutrition change in specific countries (India, Nigeria, Brazil)":
        query = """
            SELECT Country, Year, ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
            FROM malnutrition
            WHERE Country IN ('India', 'Nigeria', 'Brazil')
            GROUP BY Country, Year
            ORDER BY Country, Year;
        """
    elif malnutrition_query == "Regions with lowest malnutrition averages":
        query = """
            SELECT Region, ROUND(AVG(Mean_Estimate), 2) AS avg_malnutrition
            FROM malnutrition
            GROUP BY Region
            ORDER BY avg_malnutrition ASC
            LIMIT 5;
        """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# ------------------- Combined Queries -------------------
st.header("Combined Obesity & Malnutrition Queries")
combined_query = st.selectbox("Select a combined query", [
    "Obesity vs malnutrition comparison by country (any 5 countries)",
    "Gender-based disparity in both obesity and malnutrition",
    "Region-wise avg estimates side-by-side (Africa and America)",
    "Countries with obesity up & malnutrition down",
    "Age-wise trend analysis"
])

if st.button("Run Combined Query"):
    if combined_query == "Obesity vs malnutrition comparison by country (any 5 countries)":
        query = """
            SELECT o.Country, ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity, ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON TRIM(o.Country) = TRIM(m.Country) AND o.Year = m.Year
            WHERE o.Country IN ('India', 'USA', 'Brazil', 'Nigeria', 'Germany')
            GROUP BY o.Country;
        """
    elif combined_query == "Gender-based disparity in both obesity and malnutrition":
        query = """
            SELECT o.Gender, ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity, ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON TRIM(o.Country) = TRIM(m.Country) AND o.Year = m.Year AND o.Gender = m.Gender
            GROUP BY o.Gender;
        """
    elif combined_query == "Region-wise avg estimates side-by-side (Africa and America)":
        query = """
            SELECT o.Region, ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity, ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON TRIM(o.Country) = TRIM(m.Country) AND o.Year = m.Year AND o.Region = m.Region
            WHERE o.Region IN ('Africa', 'Americas')
            GROUP BY o.Region;
        """
    elif combined_query == "Countries with obesity up & malnutrition down":
        query = """
            SELECT o.Country, ROUND(AVG(o.Mean_Estimate), 2) AS obesity, ROUND(AVG(m.Mean_Estimate), 2) AS malnutrition
            FROM obesity o
            JOIN malnutrition m ON TRIM(o.Country) = TRIM(m.Country) AND o.Year = m.Year
            GROUP BY o.Country
            HAVING obesity > 30 AND malnutrition < 10;
        """
    elif combined_query == "Age-wise trend analysis":
        query = """
            SELECT o.age_group, ROUND(AVG(o.Mean_Estimate), 2) AS avg_obesity, ROUND(AVG(m.Mean_Estimate), 2) AS avg_malnutrition
            FROM obesity o
            JOIN malnutrition m ON TRIM(o.Country) = TRIM(m.Country) AND o.Year = m.Year AND o.age_group = m.age_group
            GROUP BY o.age_group;
        """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

st.header("Dataset Visualizations")

# Select dataset to visualize
dataset_to_visualize = st.selectbox("Select Dataset to Visualize", ["Obesity", "Malnutrition"])

@st.cache_data
def load_data(table_name):
    return run_query(f"SELECT * FROM {table_name}")

if dataset_to_visualize == "Obesity":
    df = load_data("obesity")

    vis_options = [
        "Distribution of Mean_Estimate & CI_Width",
        "Yearly Average Obesity Trend",
        "Mean Obesity Estimate by Region",
        "Obesity Estimate by Region and Year"
    ]

    selected_vis = st.selectbox("Select Visualization", vis_options)

    if selected_vis == "Distribution of Mean_Estimate & CI_Width":
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        sns.histplot(df['Mean_Estimate'], kde=True, ax=axs[0])
        axs[0].set_title('Distribution of Mean_Estimate')

        sns.histplot(df['CI_Width'], kde=True, ax=axs[1])
        axs[1].set_title('Distribution of CI_Width')

        st.pyplot(fig)

    elif selected_vis == "Yearly Average Obesity Trend":
        yearly_trend = df.groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=yearly_trend, x="Year", y="Mean_Estimate", marker="o", ax=ax)
        ax.set_title("Average Obesity Rate Over Years")
        ax.set_ylabel("Obesity Rate (%)")
        ax.set_xlabel("Year")
        ax.grid(True)
        st.pyplot(fig)

    elif selected_vis == "Mean Obesity Estimate by Region":
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Region', y='Mean_Estimate', data=df, ax=ax)
        ax.set_title('Mean Obesity Estimate by Region')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

    elif selected_vis == "Obesity Estimate by Region and Year":
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Region', y='Mean_Estimate', hue='Year', data=df, ax=ax)
        ax.set_title('Obesity Estimate by Region and Year')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)


else:  # Malnutrition visualizations
    df = load_data("malnutrition")

    vis_options = [
        "Distribution of Mean_Estimate & CI_Width",
        "Yearly Average Malnutrition Trend",
        "Mean Malnutrition Estimate by Region",
        "Malnutrition Estimate by Region and Year"
    ]

    selected_vis = st.selectbox("Select Visualization", vis_options)

    if selected_vis == "Distribution of Mean_Estimate & CI_Width":
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        sns.histplot(df['Mean_Estimate'], kde=True, ax=axs[0])
        axs[0].set_title('Distribution of Mean_Estimate')

        sns.histplot(df['CI_Width'], kde=True, ax=axs[1])
        axs[1].set_title('Distribution of CI_Width')

        st.pyplot(fig)

    elif selected_vis == "Yearly Average Malnutrition Trend":
        yearly_trend = df.groupby("Year")["Mean_Estimate"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=yearly_trend, x="Year", y="Mean_Estimate", marker="o", ax=ax)
        ax.set_title("Average Malnutrition Rate Over Years")
        ax.set_ylabel("Malnutrition Rate (%)")
        ax.set_xlabel("Year")
        ax.grid(True)
        st.pyplot(fig)

    elif selected_vis == "Mean Malnutrition Estimate by Region":
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Region', y='Mean_Estimate', data=df, ax=ax)
        ax.set_title('Mean Malnutrition Estimate by Region')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)

    elif selected_vis == "Malnutrition Estimate by Region and Year":
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='Region', y='Mean_Estimate', hue='Year', data=df, ax=ax)
        ax.set_title('Malnutrition Estimate by Region and Year')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        st.pyplot(fig)
