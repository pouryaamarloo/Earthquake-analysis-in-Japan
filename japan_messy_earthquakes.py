import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#خواندن فایل csv 
data_f = pd.read_csv("japan_messy_earthquakes.csv")
print(data_f.head())
#تبدیل سنون ها
data_f['time'] = pd.to_datetime(data_f['time'], errors='coerce') #time -> datetime
data_f['latitude'] = pd.to_numeric(data_f['latitude'], errors='coerce')  #latitude -> float
data_f['longitude'] = pd.to_numeric(data_f['longitude'], errors='coerce')  #longitude -> float
data_f['depth_m'] = pd.to_numeric(data_f['depth_m'], errors='coerce')  #depth_m -> float
data_f['mag'] = pd.to_numeric(data_f['mag'], errors='coerce')  #mag -> float

#بررسی داده های گمشده
#تعداد داده های گمشده در هر ستون
print(data_f.isna().sum())
#ردیف های عمق و mag دارای مقادیر غیر معقول و خارج از محدوده دارن
print(data_f[(data_f['depth_m']<0) | (data_f['depth_m']>1000)])
print(data_f[(data_f['mag']<0) | (data_f['mag']>10)])
#ردیف های گمشده را باید حذف کنیم که اشتباه نشه
data_f = data_f.dropna(subset=['latitude' , 'longitude' , 'mag'])
#برای ردیف عمق غیر منطقی
data_f.loc[(data_f['depth_m']<0) | (data_f['depth_m']>1000) , 'depth_m'] = np.nan
data_f = data_f.sort_values('time').reset_index(drop=True)
#فیلتر کردن بر اساس اندازه و عمق
#زلزه های بیشتر از 5.0
quakes = data_f[data_f['mag']>5.0]
#زلزله کم عمق
shallow_q = data_f[data_f['depth_m']<70]
#گروه بندی کردن بر اساس مکان و ماه
#گروه بندی بر اساس محل وقوع زلزله
mag_place = data_f.groupby('place')['mag'].mean()
#زلزله در هر ماه
data_f['month'] = data_f['time'].dt.month
quakes_per_month = data_f.groupby('month').size()
data_f[data_f['quality_flag'].notna()]

#اندازه زلزله بر اساس تاریخ
plt.figure(figsize=(10,5))
plt.plot(data_f['time'] , data_f['mag'] , marker = 'o' , linestyle = 'None')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.title('*Earthquake Magnitude Over Time*')
plt.show()
