# 1.Analisis Tren Waktu (Time Series) per Produk
# Untuk tiap produk, identifikasi pola musiman (seasonality) atau tren jangka panjang pada metrik penjualan (asumsi: tambahkan kolom monthly_sales pada product_launch.csv). Apakah ada periode ‘aman’ atau ‘berisiko’ untuk meluncurkan produk di masing-masing negara?

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
import calendar

# # Read product launch CSV and save it as df_product
# df_product = pd.read_csv('product_launch.csv')

# # Cleaning: hapus baris dengan nilai kosong
# df_product = df_product.dropna()

# # Remove outliers using z-score (hanya kolom numerik)
# z_scores = np.abs(zscore(df_product.select_dtypes(include=[np.number])))
# df_product_filtered = df_product[(z_scores < 3).all(axis=1)]

# # Visualize the presence of outliers using a boxplot
# plt.figure(figsize=(10, 6))
# sns.boxplot(data=df_product_filtered.select_dtypes(include=[np.number]))
# plt.title('Boxplot Variabel Numerik setelah Hapus Outlier')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()


# import pandas as pd

# # 1. Baca data
# df = pd.read_csv('product_launch.csv')

# # 2. Convert launch_date ke datetime
# df['launch_date'] = pd.to_datetime(df['launch_date'])

# # 3. Hitung “sales_amount” per baris:
# #    asumsinya: success=1 artinya unit terjual sebanyak 1 × price = revenue
# df['sales_amount'] = df['success'] * df['price']

# # 4. Ekstrak periode bulan (year–month)
# #    Kita pakai tipe Period, tapi kamu juga bisa pake string jika mau
# df['year_month'] = df['launch_date'].dt.to_period('M')

# # 5. Agregasi total sales per (country, product_id, year_month)
# #    Lalu gunakan transform agar hasilnya otomatis melabeli tiap baris
# df['monthly_sales'] = (
#     df
#     .groupby(['country', 'product_id', 'year_month'])['sales_amount']
#     .transform('sum')
# )

# # 6. (Opsional) Jika mau convert kembali 'year_month' ke datetime awal bulan:
# df['year_month_start'] = df['year_month'].dt.to_timestamp()

# # Cek hasil:
# print(df[['product_id','country','launch_date','sales_amount','year_month','monthly_sales']].head())


# Create an empty dictionary to store dataframes per country
nation_dfs = {}

# Loop through each row in the DataFrame
for _, row in df_product.iterrows():
    country = row['country']
    
    # If this country is not in the dictionary, create a new DataFrame
    if country not in nation_dfs:
        nation_dfs[country] = pd.DataFrame(columns=df_product.columns)
    
    # Append the row to the appropriate DataFrame
    nation_dfs[country] = pd.concat(
        [nation_dfs[country], pd.DataFrame([row])],
        ignore_index=True
    )

# for loop access the dictionary and delete the country column, and make the month and year from the column offor country in nation_dfs:
for country, df in nation_dfs.items():
    df['month'] = pd.to_datetime(df['launch_date']).dt.month
    df['year'] = pd.to_datetime(df['launch_date']).dt.year
    df = df.drop('country', axis=1)
    df = df.drop('launch_date', axis=1)
    print(f"Country: {country}")
    print(df.head())

# Loop through each DataFrame in the dictionary find using distributin plot
for country, df in nation_dfs.items():
    df['month'] = pd.to_datetime(df['month'], format='%m')

    # Group by month number (1 to 12) and calculate average success
    monthly_avg = df.groupby(df['month'].dt.month)['success'].mean()

    # Get month names
    month_names = [calendar.month_name[m] for m in monthly_avg.index]

    # Plot
    plt.figure(figsize=(8, 5))
    sns.barplot(x=month_names, y=monthly_avg.values)
    plt.title(f'Average Success by Month - {country}')
    plt.xlabel('Month')
    plt.ylabel('Average Success')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    #ambil month tertinggi
    max_month = monthly_avg.idxmax()
    max_month_name = calendar.month_name[max_month]

    #ambil month terendah
    min_month = monthly_avg.idxmin()
    min_month_name = calendar.month_name[min_month]

    print(f"Country: {country}")
    print(f"Max Month: {max_month_name}")
    print(f"Min Month: {min_month_name}")