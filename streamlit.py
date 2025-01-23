import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


hour_df = pd.read_csv('hour.csv')
day_df = pd.read_csv('day.csv')

# Konversi tanggal ke datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Buat sidebar
st.sidebar.image('logo/sepeda.jpg')
st.sidebar.header('Bike Sharing Dashboard')

filtered_day_df = day_df[(day_df['dteday'].dt.year >= 2011) & (day_df['dteday'].dt.year <= 2012)]
filtered_hour_df = hour_df[(hour_df['dteday'].dt.year >= 2011) & (hour_df['dteday'].dt.year <= 2012)]

total_registered_day = filtered_day_df['registered'].sum()
total_casual_day = filtered_day_df['casual'].sum()
total_registered_hour = filtered_hour_df['registered'].sum()
total_casual_hour = filtered_hour_df['casual'].sum()
total_registered = total_registered_day + total_registered_hour
total_casual = total_casual_day + total_casual_hour
st.header('Bike Sharing Dashboard')
st.subheader('Persentase Penyewa BIKE Sharing(2011-2012)')
labels = ['Registered', 'Casual']
sizes = [total_registered, total_casual]
colors = ['#0055cc','#ffcc00']
explode = (0.1, 0)
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
ax.axis('equal')
ax.set_title('Persentase Penyewa BIKE Sharing(2011-2012)', pad=20)
st.pyplot(fig)

st.subheader("Pengaruh Hari Kerja terhadap Jumlah Penyewaan Sepeda pada Tahun 2011-2012")
combined_df = pd.merge(hour_df, day_df, on='dteday', suffixes=('_hour', '_day'))
workday_df = combined_df.groupby('workingday_day')[['registered_day', 'casual_day']].sum()
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(workday_df.index, workday_df['registered_day'], label='Registered', color='#1f77b4')
ax.bar(workday_df.index, workday_df['casual_day'], label='Casual', bottom=workday_df['registered_day'], color='#ff7f0e')
ax.set_xlabel('Hari Kerja')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Pengaruh Hari Kerja terhadap Jumlah Penyewaan Sepeda pada Tahun 2011-2012')
ax.legend(title='Tipe Pengguna')
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.subheader("Demografi Penyewa Berdasarkan Jam")
hr_counts = combined_df.groupby('hr')[['registered_hour', 'casual_hour']].sum()
fig, ax = plt.subplots(figsize=(10, 6))
ax.fill_between(hr_counts.index, hr_counts['registered_hour'], label='Registered')
ax.fill_between(hr_counts.index, hr_counts['casual_hour'], label='Casual')
ax.set_title('Demografi Penyewa Berdasarkan Jam ', fontsize=16)
ax.set_xlabel('Jam ', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
ax.legend(title='Tipe Pengguna')
st.pyplot(fig)

st.subheader("Penyewa Demografi Berdasarkan Musim")
season_counts = combined_df.groupby('season_day')[['registered_day', 'casual_day']].sum()
fig, ax = plt.subplots(figsize=(10, 6))
season_counts.plot(kind='barh', ax=ax, color=['#1f77b4', '#ff7f0e'])
ax.set_title('Penyewa Demografi Berdasarkan Musim (2011-2012)')
ax.set_xlabel('Jumlah Penyewaan')
ax.set_ylabel('Musim')
ax.set_yticks(ticks=[0, 1, 2, 3])
ax.set_yticklabels(labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
ax.legend(title='Tipe Pengguna', labels=['Registered', 'Cas ual'])
st.pyplot(fig)




