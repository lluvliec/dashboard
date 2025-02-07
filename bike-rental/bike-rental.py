import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

sns.set(style='whitegrid')

# Load dataset
all_df = pd.read_csv("all_data.csv")

# Convert datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Sidebar filter
st.sidebar.title("💖 Filter Data")
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
start_date, end_date = st.sidebar.date_input(
    '📅 Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
)

main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

# Fungsi untuk membuat dataframe harian
def create_daily_rentals_df(df):
    daily_rentals_df = df.groupby("dteday").agg({
        "cnt_day": "sum", "casual_day": "sum", "registered_day": "sum"
    }).reset_index()
    return daily_rentals_df

# Membuat dataframe harian
daily_rentals_df = create_daily_rentals_df(main_df)

if daily_rentals_df is not None:
    st.title('🚴‍♀️ **Bike Rental Dashboard**')
    st.markdown("## 🎀 Daily Rentals Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💗 Total Rentals", value=f"{daily_rentals_df['cnt_day'].sum():,}")
    col2.metric("👩‍🎤 Casual Users", value=f"{daily_rentals_df['casual_day'].sum():,}")
    col3.metric("🛡 Registered Users", value=f"{daily_rentals_df['registered_day'].sum():,}")
    
    # Visualisasi jumlah peminjaman harian
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(daily_rentals_df["dteday"], daily_rentals_df["cnt_day"], marker='o', linewidth=2, color="#FF69B4")
    ax.set_title("💖 Daily Bike Rentals", fontsize=18)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Best & Worst Rental Days
    st.markdown("## 🌟 Best & Worst Rental Days")
    col1, col2 = st.columns(2)
    best_day = daily_rentals_df.loc[daily_rentals_df["cnt_day"].idxmax()]
    worst_day = daily_rentals_df.loc[daily_rentals_df["cnt_day"].idxmin()]
    col1.metric("💎 Best Day", value=best_day["dteday"].strftime('%Y-%m-%d'), delta=int(best_day["cnt_day"]))
    col2.metric("💔 Worst Day", value=worst_day["dteday"].strftime('%Y-%m-%d'), delta=int(worst_day["cnt_day"]))

    # Casual vs Registered Users
    st.markdown("## 💕 Casual vs Registered Users")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=["Casual", "Registered"], y=[daily_rentals_df["casual_day"].sum(), daily_rentals_df["registered_day"].sum()], palette=["#FFB6C1", "#FF69B4"], ax=ax)
    ax.set_ylabel("Total Users", fontsize=12)
    ax.set_title("Casual vs Registered Users", fontsize=14)
    st.pyplot(fig)
    
    # Seasonal Trends
    st.markdown("## 🌸 Seasonal Trends")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x=all_df["season_label"], y=all_df["cnt_day"], palette="pink", ax=ax)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.set_title("Bike Rentals by Season", fontsize=14)
    st.pyplot(fig)
    
    # Hourly Rental Distribution
    st.markdown("## ⏳ Hourly Rental Distribution")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(x=all_df["hr"], y=all_df["cnt_hour"], palette="coolwarm", ax=ax)
    ax.set_ylabel("Total Rentals", fontsize=12)
    ax.set_xlabel("Hour of the Day", fontsize=12)
    ax.set_title("Bike Rentals by Hour", fontsize=14)
    st.pyplot(fig)
    
    # Additional Features
    st.markdown("## 🎀 Informasi Tambahan")
    if st.checkbox("Rangkuman Statistik"):
        st.write(main_df.describe())
    if st.checkbox("Data Mentah"):
        st.dataframe(main_df)
    
# Footer
st.markdown("---")
st.caption("MS079D5X0584 syarifah alya alhasni")
