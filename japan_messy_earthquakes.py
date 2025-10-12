import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime  # اضافه: از datetime import datetime

# خواندن فایل csv
data_f = pd.read_csv("JAPAN_DATASET.csv")

# نمایش اطلاعات اولیه
print(data_f.shape)

def change_time(c):
    if pd.isna(c) or c is None or c == '':
        return pd.NaT
    c = str(c).strip().strip('"')
    time_formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.Z",  # برای .Z
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%b %d, %Y, %H:%M:%S",
        "%b %d, %Y, %I:%M:%S %p",
        "%b %d, %Y, %H:%M:%S",
        "%Y-%m-%d %I:%M %p",  # کلیدی: بدون %S
        "%d/%m/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M:%S",
        "%b %d %Y %H:%M:%S",
        "%b %d %Y, %H:%M:%S",
    ]
    for fmt in time_formats:
        try:
            x = datetime.strptime(c, fmt)
            return x
        except ValueError:  # دقیق‌تر
            continue
    print(f"Failed: {c}")  # فقط اگر fail بشه
    return pd.NaT

# مرحله ۳: اعمال تابع
data_f['time'] = data_f['time'].apply(change_time)
data_f['time'] = pd.to_datetime(data_f['time'])
# data_f['time'] = data_f['time'].fillna(data_f['time'],method='ffill')
data_f['latitude'] = pd.to_numeric(data_f['latitude'], errors='coerce')
data_f['longitude'] = pd.to_numeric(data_f['longitude'], errors='coerce')
data_f['depth'] = data_f['depth'].astype(str).str.extract(r'(\d+\.?\d*)').astype(float)

def number(c):
    if pd.isna(c) or c is None or c == '':
        return pd.NaT
    num = {
        "zero" : 0 ,
        "one" : 1 ,
        "two" : 2 ,
        "three" : 3 ,
        "four" : 4 ,
        "five" : 5 ,
        "six" : 6 ,
        "seven" : 7 ,
        "eight" : 8 ,
        "nine" : 9 ,
        "ten" : 10 ,
    }
    STR = ""
    if isinstance(c, (int, float)):
        return c
    if isinstance(c, str):
        c = c.strip().lower()
        if c.replace(".","",1).isdigit():
            return c
        if "." in c:
            c =c.split(".")
            if len(c) != 2:
                return pd.NaT
            try :
                first = num[c[0]]
                second = num[c[1]]
                return  float(f"{first}.{second}")
            except :
                return pd.NaT
        else :
            try :
                first = num[c]
                return float(f"{first}")

            except:
                return pd.NaT


data_f['mag'] = data_f['mag'].apply(number)
data_f['mag'] = pd.to_numeric(data_f['mag'], errors='coerce')

# حذف داده‌های گمشده
data_f = data_f.dropna(subset=['latitude', 'longitude', 'mag'])
data_f['depth'] = data_f['depth'].fillna(data_f['depth'].mean())
print(data_f.isna().sum())

# مختصات توکیو
tokyo_latitude = 35.6895
tokyo_longitude = 139.6917

# فاصله تا توکیو (درجه جغرافیایی)
data_f['distance_to_tokyo'] = np.sqrt(
    (data_f['latitude'] - tokyo_latitude) ** 2 +
    (data_f['longitude'] - tokyo_longitude) ** 2
)

# محاسبات آماری
print("Mean of distance :", np.mean(data_f['distance_to_tokyo']))
print("Standard deviation of distance :", np.std(data_f['distance_to_tokyo']))
print("Variance of distance :", np.var(data_f['distance_to_tokyo']))

# ذخیره تغییرات
data_f.to_csv("JAPAN_DATASET.csv", index=False)
print("JAPAN_DATASET file saved with new changes!")

# استخراج ماه
data_f['Month'] = data_f['time'].dt.month

# دسته‌بندی شدت
def category(i):
    if i < 4:
        return "Weak"
    elif 4 <= i <= 6:
        return "Moderate"
    elif i > 6:
        return "Strong"

data_f['Category'] = data_f['mag'].apply(category)

# استخراج منطقه (در صورت وجود ستون place)
if 'place' in data_f.columns:
    data_f['region'] = data_f['place'].astype(str).apply(lambda x: x.split(',')[0].strip())
else:
    print(" ستون 'place' در فایل وجود ندارد!")

# گروه‌بندی‌ها

group_1 = data_f.groupby(['Month', 'Category']).agg(
    count=('mag', 'size'),
    mean_mag=('mag', 'mean')
)
print(group_1)

if 'region' in data_f.columns:
    group_2 = data_f.groupby('region').agg(
        quake_count=('mag', 'size'),
        mean_mag=('mag', 'mean'),
        mean_depth=('depth', 'mean'),
        max_mag=('mag', 'max'),
        max_depth=('depth', 'max')
    )
    print(group_2)

    # نمودار
    plt.figure(figsize=(12, 6))
    plt.bar(group_2.index, group_2['quake_count'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Region')
    plt.ylabel('Number of Earthquakes')
    plt.title('Number of Earthquakes by Region')
    plt.show()
