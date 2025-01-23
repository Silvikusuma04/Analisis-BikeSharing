import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

hour_df = pd.read_csv('hour.csv')
day_df = pd.read_csv('day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.sidebar.image('logo/sepeda.jpg')
st.sidebar.header('Bike Sharing Dashboard')

tanggal_filter = st.sidebar.date_input('Pilih Tanggal', value=pd.to_datetime('2011-01-01'))
tahun_filter = st.sidebar.slider('Filter Tahun', 2011, 2012, (2011, 2012))

filtered_day_df = day_df[(day_df['dteday'].dt.year >= tahun_filter[0]) & (day_df['dteday'].dt.year <= tahun_filter[1])]
filtered_hour_df = hour_df[(hour_df['dteday'].dt.year >= tahun_filter[0]) & (hour_df['dteday'].dt.year <= tahun_filter[1])]

st.header('Dashboard Analisis Penyewaan Sepeda')

st.subheader("Persentase jumlah penyewa")
total_registered = filtered_day_df['registered'].sum() + filtered_hour_df['registered'].sum()
total_casual = filtered_day_df['casual'].sum() + filtered_hour_df['casual'].sum()
sizes = [total_registered, total_casual]
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#0088FE', '#00C49F']
ax.pie(sizes, labels=['Registered', 'Casual'], colors=colors, autopct='%1.1f%%', startangle=90, explode=(0.1, 0))
ax.axis('equal')
st.pyplot(fig)

st.subheader("Pengaruh Hari Kerja terhadap Penyewaan")
workday_df = filtered_day_df.groupby('workingday')[['registered', 'casual']].sum()
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#FF8042', '#FFBB28']
workday_df.plot(kind='bar', stacked=True, ax=ax, color=colors)
st.pyplot(fig)

st.subheader("Pengaruh Hari Kerja terhadap Penyewaan - Registered")
workday_df = filtered_day_df.groupby('workingday')[['registered', 'casual']].sum()
colors_registered = ['#ff9999', '#66b3ff']  
fig1, ax1 = plt.subplots(figsize=(10, 6))
workday_df['registered'].plot(kind='pie', ax=ax1, labels=['Bukan Hari Kerja', 'Hari Kerja'], colors=colors_registered, autopct='%1.1f%%', startangle=90, explode=(0.1, 0))
ax1.set_title('Registered')
ax1.set_ylabel('')
st.pyplot(fig1)

st.subheader("Pengaruh Hari Kerja terhadap Penyewaan - Casual")
colors_casual = ['#99ff99', '#ffcc99'] 
fig2, ax2 = plt.subplots(figsize=(10, 6))
workday_df['casual'].plot(kind='pie', ax=ax2, labels=['Bukan Hari Kerja', 'Hari Kerja'], colors=colors_casual, autopct='%1.1f%%', startangle=90, explode=(0.1, 0))
ax2.set_title('Casual')
ax2.set_ylabel('')
st.pyplot(fig2)

st.subheader("Penyewaan Berdasarkan Musim")
season_df = filtered_day_df.groupby('season')[['registered', 'casual']].sum()
season_labels = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#FF6361', '#58508D']
season_df.plot(kind='bar', ax=ax, color=colors)
ax.set_xticklabels(season_labels, rotation=0)
st.pyplot(fig)
