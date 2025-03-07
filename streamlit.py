import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
hour_df = pd.read_csv("hour.csv")
day_df = pd.read_csv("day.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

st.sidebar.image("sepeda.jpg")
st.sidebar.title("Bike Sharing Dashboard")
st.sidebar.title("Filter Visualisasi")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=[2011, 2012])
selected_weather = st.sidebar.selectbox("Pilih Kondisi Cuaca", options=[1, 2, 3, 4], 
                                        format_func=lambda x: {
                                            1: ' (1) Clear, Few clouds, Partly cloudy',
                                            2: ' (2) Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
                                            3: ' (3) Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
                                            4: ' (4) Heavy Rain + Ice Pellets + Thunderstorm + Mist, Snow + Fog'
                                        }[x])
selected_season = st.sidebar.selectbox("Pilih Musim", options=[1, 2, 3, 4], 
                                      format_func=lambda x: {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}[x])
# Filter by year
filtered_day_df = day_df[day_df['dteday'].dt.year == selected_year]
filtered_hour_df = hour_df[hour_df['dteday'].dt.year == selected_year]
# Filter by weather and season
filtered_day_df = filtered_day_df[filtered_day_df['season'] == selected_season]
filtered_hour_df = filtered_hour_df[filtered_hour_df['weathersit'] == selected_weather]

# 1. Persentase jumlah total pengguna registered dan casual
st.subheader("Persentase Jumlah Total Pengguna")
total_registered = filtered_day_df['registered'].sum() + filtered_hour_df['registered'].sum()
total_casual = filtered_day_df['casual'].sum() + filtered_hour_df['casual'].sum()
sizes = [total_registered, total_casual]
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#0055cc', '#ffcc00']
labels = ['Registered', 'Casual']
ax.pie(sizes, explode=(0.1, 0), labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
ax.axis('equal')
st.pyplot(fig)

# 2. Pengaruh hari kerja terhadap jumlah penyewaan sepeda
st.subheader("Presentase Penyewa Berdasarkan Working Day")
combined_df = pd.merge(filtered_hour_df, filtered_day_df, on='dteday', suffixes=('_hour', '_day'))
workday_counts = combined_df.groupby('workingday_day')[['registered_day', 'casual_day']].sum()
total_workday = workday_counts.loc[1, 'registered_day'] + workday_counts.loc[1, 'casual_day']
total_holiday = workday_counts.loc[0, 'registered_day'] + workday_counts.loc[0, 'casual_day']
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie([total_workday, total_holiday], labels=['Hari Kerja', 'Hari Libur'], colors=['#1f77b4', '#ff7f0e'], autopct='%1.1f%%')
plt.title('Persentase Penyewaan Sepeda pada Hari Kerja dan Hari Libur')
st.pyplot(fig)

# 3. Pengaruh jam penyewaan terhadap jumlah penyewa sepeda
st.subheader("Pengaruh Jam Penyewaan Terhadap Jumlah Penyewa Sepeda")
hourly_rentals = filtered_hour_df.groupby('hr')['cnt'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_rentals.index, hourly_rentals.values)
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Pengaruh Jam Penyewaan terhadap Jumlah Penyewaan Sepeda')
ax.grid(True)
st.pyplot(fig)

# 4. Pengaruh jam penyewaan terhadap jumlah penyewaan sepeda (registered vs casual)
st.subheader("Pengaruh Jam Penyewaan Terhadap Jumlah Penyewaan Sepeda (Registered vs Casual)")
hour_registered = filtered_hour_df.groupby('hr')['registered'].sum()
hour_casual = filtered_hour_df.groupby('hr')['casual'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hour_registered.index, hour_registered.values, label='Registered')
ax.plot(hour_casual.index, hour_casual.values, label='Casual')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Pengaruh Jam Penyewaan terhadap Jumlah Penyewaan Sepeda (Registered vs Casual)')
ax.grid(True)
ax.legend()
st.pyplot(fig)

# 5. Total dan proporsi penyewaan sepeda pada hari kerja dan hari libur
st.subheader("Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(workday_counts.index, workday_counts['registered_day'], label='Registered', color='#1f77b4')
ax.bar(workday_counts.index, workday_counts['casual_day'], bottom=workday_counts['registered_day'], label='Casual', color='#ff7f0e')
ax.set_title('Total dan Proporsi Penyewaan Sepeda pada Hari Kerja dan Hari Libur')
ax.set_xlabel('Kategori')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(ticks=workday_counts.index, labels=['Hari Libur', 'Hari Kerja'])
ax.legend(title='Tipe Pengguna')
st.pyplot(fig)

# 6. Total penyewaan sepeda berdasarkan cluster
st.subheader("Total Penyewaan Sepeda Berdasarkan Musim Dan Working Day (Clustering)")
def cluster_group(row):
    if row['season_day'] == 1:
        return 'Winter_Workday' if row['workingday_day'] == 1 else 'Winter_Holiday'
    elif row['season_day'] == 2:
        return 'Spring_Workday' if row['workingday_day'] == 1 else 'Spring_Holiday'
    elif row['season_day'] == 3:
        return 'Summer_Workday' if row['workingday_day'] == 1 else 'Summer_Holiday'
    elif row['season_day'] == 4:
        return 'Fall_Workday' if row['workingday_day'] == 1 else 'Fall_Holiday'

combined_df['cluster'] = combined_df.apply(cluster_group, axis=1)
cluster_counts = combined_df.groupby('cluster')[['registered_day', 'casual_day']].sum()

fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
ax.barh(cluster_counts.index, cluster_counts['registered_day'], height=bar_width, label='Registered', color='#1f77b4')
ax.barh(cluster_counts.index, cluster_counts['casual_day'], height=bar_width, label='Casual', color='#ff7f0e', left=cluster_counts['registered_day'])
ax.set_xlabel('Jumlah Penyewaan', fontsize=14)
ax.set_ylabel('Clustering Berdasarkan Musim Dan Hari', fontsize=14)
ax.set_title('Total Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
ax.legend(title='Tipe Pengguna')
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)

# 7. Jumlah penyewaan berdasarkan cuaca dan jenis hari 
cluster_counts2 = filtered_hour_df.groupby(['weathersit', 'workingday'])['cnt'].sum().reset_index()
st.subheader("Jumlah Penyewaan Berdasarkan Cuaca dan Working Day")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', hue='workingday', data=cluster_counts2, ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Jumlah Penyewaan Berdasarkan Cuaca dan Jenis Hari')
st.pyplot(fig)
