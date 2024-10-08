import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Amazon Reviews EDA with Language Detection & Translation")

df = pd.read_csv("customer_data/processed_data.csv")
# EDA Section
st.subheader("Exploratory Data Analysis")

# Rating distribution
st.write("### Rating Distribution")
plt.figure(figsize=(12, 8))
rating_counts = df["rating"].value_counts()
plt.bar(rating_counts.index, rating_counts.values, color="blue")
plt.xlabel("Rating")
plt.ylabel("Count")
plt.title("Distribution of Ratings")
plt.show()
plt.title("Distribution of Ratings")
st.pyplot(plt.gcf())
plt.clf()

st.write("### Helpful Vote Distribution")
col_left, col_right = st.columns([2, 1])
with col_left:
    st.write("Vote distribution and description")
    plt.figure(figsize=(12, 8))
    plt.hist(df["helpful_vote"], bins=20, color="skyblue", edgecolor="black")
    plt.title("Distribution of Helpful Votes")
    plt.xlabel("Votes")
    plt.ylabel("Frequency")
    plt.show()
    st.pyplot(plt.gcf())

with col_right:
    st.dataframe(df["helpful_vote"].describe())

plt.clf()

plt.figure(figsize=(12, 8))
max = df["helpful_vote"].quantile(0.99)
plt.hist(
    df.loc[df["helpful_vote"] <= max, "helpful_vote"],
    bins=15,
    color="skyblue",
    edgecolor="black",
)
plt.title("Distribution of Helpful Votes")
plt.xlabel("Helpful Votes (<99% quantile)")
plt.ylabel("Frequency")
plt.show()
st.pyplot(plt.gcf())
plt.clf()

# Trends over time
st.write("### Average Rating Over Time")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
start_time = df["timestamp"].quantile(0.01)
df = df[df["timestamp"] > start_time]
plt.figure(figsize=(10, 6))
df.set_index("timestamp")["rating"].resample("M").mean().plot()
plt.title("Average Rating Over Time")
st.pyplot(plt.gcf())
plt.clf()

average_rating_counts = (
    df.groupby("asin")
    .agg(average_rating=("rating", "mean"), total_count=("rating", "size"))
    .reset_index()
)

highly_rated_products = average_rating_counts[
    (average_rating_counts["average_rating"].round(0) == 5)
    & (average_rating_counts["total_count"] >= 10)
]

top_five_star_products = highly_rated_products.sort_values(
    by="total_count", ascending=False
).head(25)


plt.figure(figsize=(12, 8))
bars = plt.bar(
    top_five_star_products["asin"],
    top_five_star_products["total_count"],
    color="lightgreen",
    edgecolor="black",
)
plt.title("Top Products by Number of 5-Star Ratings")
plt.xlabel("Product ASIN")
plt.ylabel("Number of 5-Star Ratings")
plt.tight_layout()
plt.xticks(rotation=45)
plt.ylim(0, top_five_star_products["total_count"].max() + 10)

for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

st.pyplot(plt.gcf())
plt.clf()

st.write("### Products with Lowest Ratings (< 3 Stars)")
# Filter for products with an average rating of 1 star and at least 10 total ratings
low_rated_products = average_rating_counts[
    average_rating_counts["average_rating"].round(0) <= 3
]

lowest_rated_products = low_rated_products.sort_values(
    by="total_count", ascending=False
).head(25)


plt.figure(figsize=(12, 6))
bars = plt.bar(
    lowest_rated_products["asin"],
    lowest_rated_products["total_count"],
    color="lightcoral",
    edgecolor="black",
)
plt.title("Products need improvement (<= 3 Stars)")
plt.xlabel("Product ASIN")
plt.ylabel("Number of <= 3-Star Ratings")
plt.xticks(rotation=45)
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        f"{yval}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

plt.tight_layout()
st.pyplot(plt.gcf())
plt.clf()
