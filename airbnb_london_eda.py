import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv("D:\Projects_DA\AirBnb_London_ACleaned.csv")

# Streamlit Page Configuration
st.set_page_config(page_title="Airbnb London Dashboard", layout="wide")

# Title
st.title("🏡 Airbnb London - Interactive Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Filter by Price Range
price_range = st.sidebar.slider("Select Price Range (£)", int(df["price"].min()), int(df["price"].max()), (50, 300))

# Filter by Room Type
room_types = df["room_type"].unique().tolist()
selected_room_type = st.sidebar.multiselect("Select Room Type", room_types, default=room_types)

# Filter by Neighbourhood
neighbourhoods = df["neighbourhood"].unique().tolist()
selected_neighbourhood = st.sidebar.multiselect("Select Neighbourhood", neighbourhoods, default=neighbourhoods[:5])

# Apply Filters
filtered_df = df[
    (df["price"] >= price_range[0]) & (df["price"] <= price_range[1]) &
    (df["room_type"].isin(selected_room_type)) &
    (df["neighbourhood"].isin(selected_neighbourhood))
]

# Display Filtered Data
st.write(f"### Showing {len(filtered_df)} Listings Based on Filters")
st.dataframe(filtered_df.head(10))  # Show first 10 filtered rows

# Price Distribution Chart
st.subheader("💰 Price Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df["price"], bins=30, kde=True, ax=ax)
plt.xlabel("Price (£)")
plt.ylabel("Count")
st.pyplot(fig)

# Average Price by Neighbourhood
st.subheader("📍 Average Price by Neighbourhood")
neighbourhood_price = filtered_df.groupby("neighbourhood")["price"].mean().sort_values(ascending=False).head(10)
st.bar_chart(neighbourhood_price)

# Scatter Plot: Availability vs Price
st.subheader("📅 Availability vs. Price")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=filtered_df["availability_365"], y=filtered_df["price"], alpha=0.5, ax=ax)
plt.xlabel("Days Available in a Year")
plt.ylabel("Price (£)")
st.pyplot(fig)

# Correlation Heatmap
st.subheader("📊 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(filtered_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

st.write("💡 **Insights:** Filter listings based on price, room type, and neighborhood. The charts update dynamically!")
