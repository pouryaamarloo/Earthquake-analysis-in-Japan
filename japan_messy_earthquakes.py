import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#خواندن فایل csv 
data_f = pd.read_csv("JAPAN_DATASET.csv")
print(data_f.shape)
print(data_f.dtypes)
#تبدیل سنون ها
data_f['time'] = pd.to_datetime(data_f['time'] , errors='coerce') #time -> datetime
data_f['latitude'] = pd.to_numeric(data_f['latitude'] , errors='coerce')  #latitude -> float
data_f['longitude'] = pd.to_numeric(data_f['longitude'] , errors='coerce')  #longitude -> float
data_f['depth_m'] = pd.to_numeric(data_f['depth_m'] , errors='coerce')  #depth_m -> float
data_f['mag'] = pd.to_numeric(data_f['mag'] , errors='coerce')  #mag -> float

#بررسی داده های گمشده
#تعداد داده های گمشده در هر ستون
#ردیف های گمشده را باید حذف کنیم که اشتباه نشه
data_f = data_f.dropna(subset=['latitude' , 'longitude' , 'mag'])
data_f['depth_m'] = data_f['depth_m'].fillna(data_f['depth_m'].mean())
print(data_f.isna().sum())
#زلزله در هر ماه
data_f['Month'] = data_f['time'].dt.month
#ساخت ستون category
def category(i) : #i=شدت زلزله 
    if i < 4 :
        return "Weak"
    elif 4<= i <= 6 :
        return "Moderate"
    elif i > 6 :
        return "Strong"

data_f['Category'] = data_f['mag'].apply(category)
#استخراج ستون جدید region از place
data_f['region'] = data_f['place'].astype(str).apply(lambda x : x.split(',')[0].strip())
#گروهبندی بر اساس ماه و category
group_1 = data_f.groupby(['Month' , 'Category']).agg(
        count = ('mag' , 'size') ,
        mean_mag = ('mag' , 'mean') 
    )
print(group_1)
#گروهبندی بر اساس منطقه
group_2 = data_f.groupby('region').agg(
    quake_count = ('mag' , 'size') ,
    mean_mag = ('mag' , 'mean') ,
    mean_depth = ('depth_m' , 'mean') ,
    max_mag = ('mag' , 'max') ,
    max_depth = ('depth_m' , 'max')
    )
print(group_2)

plt.figure(figsize = (12 , 6))
plt.bar(group_2.index , group_2['quake_count'])
plt.xticks(rotation = 45 , ha = 'right')
plt.xlabel('Region')
plt.ylabel('Number of Earthquakes')
plt.title('Number of Earthquakes by Region')
plt.show()