import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#خواندن فایل csv 
data_f = pd.read_csv("JAPAN_DATASET.csv")
#نمایش تعداد ردیف ها و ستون ها
print(data_f.shape)
#نمایش نوع داده هر ستون
print(data_f.dtypes)
#تبدیل نوع داده ها
data_f['time'] = pd.to_datetime(data_f['time'] , errors='coerce') #time -> datetime
data_f['latitude'] = pd.to_numeric(data_f['latitude'] , errors='coerce')  #latitude -> float
data_f['longitude'] = pd.to_numeric(data_f['longitude'] , errors='coerce')  #longitude -> float
data_f['depth_m'] = pd.to_numeric(data_f['depth_m'] , errors='coerce')  #depth_m -> float
data_f['mag'] = pd.to_numeric(data_f['mag'] , errors='coerce')  #mag -> float

#بررسی داده های گمشده
#حذف ردیف هایی که مقدار mag / longitude / latitude ندارند!
data_f = data_f.dropna(subset=['latitude' , 'longitude' , 'mag'])
#جایگزین کردن میانگین  عمق به جای مقادیر گمشده
data_f['depth_m'] = data_f['depth_m'].fillna(data_f['depth_m'].mean())
print(data_f.isna().sum())

#مختصات شهر توکیو
#از فایل csv متخصات برداشته شده!
tokyo_latitude = 35.6895
tokyo_longitude = 139.6917
#محاسبه فاصله اقلیدسی هر زلزله تا توکیو
#فرمول : dist = np.sqrt((x2 - x1)2 + (y2 - y1)2) {--> x1,y1 طول و عرض جغرافیایی توکیو هستند}
data_f['distance_to_tokyo'] = np.sqrt(
    (data_f['latitude'] - tokyo_latitude)**2 +
    (data_f['longitude'] - tokyo_longitude)**2
    )
#محاسبات آماری و ریاضی
print("Mean of distance :" , np.mean(data_f['distance_to_tokyo']))
print("Standard deviation of distance :" , np.std(data_f['distance_to_tokyo']))
print("Variance of distance :" , np.var(data_f['distance_to_tokyo']))
print("Percentile of distance :" , np.percentile(data_f['distance_to_tokyo'] , ))  #صدک چندم؟
                                                 
#ذخیره ستون جدید در فایل(ستون فاصله تا توکیو)
data_f.to_csv("JAPAN_DATASET.csv" , index = False)

print("JAPAN_DATASET file saved with new changes!")

#زلزله در هر ماه
data_f['Month'] = data_f['time'].dt.month

#ساخت ستون category
#دسته بندی براساس mag
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

#رسم نمودار میله ای
plt.figure(figsize = (12 , 6))
plt.bar(group_2.index , group_2['quake_count'])
plt.xticks(rotation = 45 , ha = 'right')
plt.xlabel('Region')
plt.ylabel('Number of Earthquakes')
plt.title('Number of Earthquakes by Region')
plt.show()