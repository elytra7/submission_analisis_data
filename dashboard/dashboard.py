import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

sns.set_theme(style="whitegrid", context="talk")

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

day_df = load_data()

st.sidebar.title("🚲 Bike Sharing Filters")
st.sidebar.markdown("Silakan filter rentang waktu data di bawah ini:")

min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

date_range = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

main_df = day_df[(day_df["dteday"].dt.date >= start_date) & 
                 (day_df["dteday"].dt.date <= end_date)]

st.title("🚲 Bike Sharing Data Dashboard")
st.markdown("Dashboard ini menampilkan hasil analisis data historis penyewaan sepeda berdasarkan faktor lingkungan (musim & cuaca) serta demografi tipe pengguna.")

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_df.cnt.sum()
    st.metric("Total Rentals", value=f"{total_rentals:,}")

with col2:
    total_registered = main_df.registered.sum()
    st.metric("Registered User Rentals", value=f"{total_registered:,}")

with col3:
    total_casual = main_df.casual.sum()
    st.metric("Casual User Rentals", value=f"{total_casual:,}")

st.divider()

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Penyewaan Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    sns.barplot(data=main_df, x="season_label", y="cnt", color="#E67E22", ax=ax, errorbar=None)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.set_xlabel("Musim", fontsize=12)
    
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f"{p.get_height():.0f}", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 8), 
                        textcoords='offset points', fontsize=10, fontweight='bold')
    sns.despine(left=True, bottom=False)
    st.pyplot(fig)

with col_chart2:
    st.subheader("Penyewaan Berdasarkan Cuaca")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    sns.barplot(data=main_df, x="weather_label", y="cnt", color="#2C3E50", ax=ax, errorbar=None)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    ax.set_xlabel("Kondisi Cuaca", fontsize=12)
    
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f"{p.get_height():.0f}", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', xytext=(0, 8), 
                        textcoords='offset points', fontsize=10, fontweight='bold')
    sns.despine(left=True, bottom=False)
    st.pyplot(fig)

st.divider()

st.subheader("Perbandingan Tipe Pengguna: Hari Kerja vs Libur")

melted_df = pd.melt(main_df, id_vars=['workingday_label'], value_vars=['casual', 'registered'], 
                    var_name='User Type', value_name='Average Rentals')

fig, ax = plt.subplots(figsize=(13, 6))

custom_palette = {"registered": "#2C3E50", "casual": "#E67E22"}
sns.barplot(data=melted_df, x="workingday_label", y="Average Rentals", hue="User Type", palette=custom_palette, ax=ax, errorbar=None)

ax.set_ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
ax.set_xlabel("Tipe Hari", fontsize=12)
ax.legend(title="Tipe Pengguna", loc='upper left', frameon=True, facecolor='white', edgecolor='lightgray')

for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{p.get_height():.0f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 8), 
                    textcoords='offset points', fontsize=10, fontweight='bold')

sns.despine(left=True, bottom=False)
st.pyplot(fig)

st.caption("Copyright © 2026. Built with Streamlit by [King Elytra].")