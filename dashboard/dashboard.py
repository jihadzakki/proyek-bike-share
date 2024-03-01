import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


def create_monthly_count_df(df):
    df["mnth"] = pd.Categorical(df["mnth"], categories=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    monthly_count = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index()

    return monthly_count

def create_sum_byhour_df(df):
    sum_byhour_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    
    return sum_byhour_df

def create_sum_byseason_df(df):
    sum_byseason_df = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    
    return sum_byseason_df

def create_weather_counts_sorted_df(df):
    # Mapping angka menjadi label kondisi cuaca
    weather_labels = {
        1: 'Clear, Few clouds, Partly cloudy',
        2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds',
        3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds',
        4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
    }

    # Mengganti nilai angka weathersit dengan label kondisi cuaca
    df['weather_label'] = df['weathersit'].map(weather_labels)

    # Menghitung total jumlah penyewaan sepeda untuk setiap kondisi cuaca
    weather_counts = df.groupby('weather_label')['cnt'].sum().reset_index()

    # Mengurutkan DataFrame berdasarkan jumlah penyewaan sepeda
    weather_counts_sorted = weather_counts.sort_values(by='cnt', ascending=False)
    
    return weather_counts_sorted

def create_size_registeredcasual(df):
    # Data
    sizes = [df['casual'].sum(), df['registered'].sum()]

    return sizes

def create_rfm_df(df):
    current_date = max(day_df['dteday'])
    rfm_df = day_df.groupby(by="registered", as_index=False).agg({
        "instant": "count", #frequency
        "cnt": "sum", #monetary
        "dteday": lambda x: (current_date - x.max()).days #recency
    })

    rfm_df.columns = ["registered", "frequency", "monetary", "recency"]
    
    return rfm_df

day_df = pd.read_csv("https://raw.githubusercontent.com/jihadzakki/proyek-bike-share/main/dashboard/cleaned_day_df.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/jihadzakki/proyek-bike-share/main/dashboard/cleaned_hour_df.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="instant", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/jihadzakki/proyek-bike-share/main/dashboard/logocompany.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
main_df2 = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

monthly_count = create_monthly_count_df(main_df)
sum_byhour_df = create_sum_byhour_df(main_df2)
sum_byseason_df = create_sum_byseason_df(main_df)
weather_counts_sorted = create_weather_counts_sorted_df(main_df)
sizes = create_size_registeredcasual(main_df)
rfm_df = create_rfm_df(main_df)

st.header('Bike Share Dashboard :sparkles:')

st.subheader("Performance of The Number of Customers In The Last Two Years")

# Membuat plot dengan ukuran gambar yang ditentukan
fig, ax = plt.subplots(figsize=(35, 15))

# Mendefinisikan warna untuk setiap tahun
colors = {2011: 'blue', 2012: 'black'}

sns.lineplot(
    data=monthly_count,
    x="mnth",
    y="cnt",
    hue="yr",
    palette=colors,  # Menggunakan warna yang ditentukan sebelumnya
    marker="o")

ax.set_title("Jumlah Pelanggan Per Bulan Selama Dua Tahun Terakhir", fontsize=50)
ax.set_xlabel(None)
ax.set_ylabel(None)
legend = ax.legend(title="Tahun", loc="upper right", fontsize=40)
legend.get_title().set_fontsize('35')  # Adjust font size as needed
plt.tight_layout()
ax.tick_params(axis='x', labelrotation=45, labelsize=45)
ax.tick_params(axis='y', labelsize=45)

st.pyplot(fig)

st.subheader("Most and Least Number of Customers")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hr", y="cnt", data=sum_byhour_df.sort_values(by="hr", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam", fontsize=25)
ax[0].yaxis.set_label_position("right")
ax[0].set_title("Pelanggan Paling Sedikit", loc="center", fontsize=30)
ax[0].tick_params(axis='x', labelsize=25)
ax[0].tick_params(axis ='y', labelsize=25)

sns.barplot(x="hr", y="cnt", data=sum_byhour_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#72BCD4",  "#D3D3D3", "#D3D3D3"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam", fontsize=25)
ax[1].set_title("Pelanggan Paling Banyak", loc="center", fontsize=30)
ax[1].tick_params(axis ='x', labelsize=25)
ax[1].tick_params(axis ='y', labelsize=25)
ax[1].yaxis.tick_right()

st.pyplot(fig)

st.subheader("Customer Performance by Season")
 
# Menentukan warna untuk setiap musim
colors = ("#72BCD4", "#D3D3D3", "#D3D3D3", "#72BCD4")

# Membuat plot dengan ukuran gambar yang ditentukan
fig, ax = plt.subplots(figsize=(20, 10))

# Membuat bar plot dengan seaborn
sns.barplot(
    y="cnt",  # Nilai di sumbu y
    x="season",  # Nilai di sumbu x
    data=sum_byseason_df.sort_values(by="cnt", ascending=False),  # Data yang digunakan
    palette=colors  # Warna yang digunakan
)

# Plot
ax.set_title("Jumlah Pelanggan Berdasarkan Musim", loc="center", fontsize=25)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

st.subheader("Customer Performance by Weather")
# Membuat bar plot
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=weather_counts_sorted, x='cnt', y='weather_label', palette=[ "#72BCD4",  "#D3D3D3", "#D3D3D3", "#D3D3D3"])
ax.set_xlabel('Jumlah Pelanggan Sepeda', fontsize=30)
ax.set_ylabel(None)
ax.set_title('Jumlah Pelanggan Berdasarkan Cuaca', fontsize=35)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)

st.pyplot(fig)

st.subheader("Distribution of Customers Between Casual and Registered Renters")
# Plot Pie Chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(sizes, labels=None, colors=['#D3D3D3','#72BCD4'], autopct='%1.2f%%', startangle=140)
ax.set_title('Perbandingan Jumlah Pelanggan antara Sepeda Casual dan Registered')
ax.axis('equal')  # Membuat pie chart menjadi lingkaran
ax.legend(['Casual', 'Registered'], loc='best')  # Menampilkan legenda

# Menambahkan jumlah angka
total = sum(sizes)
ax.text(0.3, -1.2, f'Total: {total}', fontsize=12, ha='right')

st.pyplot(fig)

st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="registered", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="registered", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="registered", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)
 
st.caption('Copyright (c) Embun Company Bike Shares 2024')
