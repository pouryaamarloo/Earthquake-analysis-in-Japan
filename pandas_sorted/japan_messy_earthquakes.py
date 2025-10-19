import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# خواندن فایل csv
def japan_messy_earthquakes():
    data_f = pd.read_csv("base_csv/japan_messy_earthquakes.csv")
    print(os.getcwd())
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
            "%Y-%m-%dT%H:%M:%S.Z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%b %d, %Y, %H:%M:%S",
            "%b %d, %Y, %I:%M:%S %p",
            "%b %d, %Y, %H:%M:%S",
            "%Y-%m-%d %I:%M %p",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%b %d %Y %H:%M:%S",
            "%b %d %Y, %H:%M:%S",
        ]
        for fmt in time_formats:
            try:
                x = datetime.strptime(c, fmt)
                return x
            except ValueError:
                continue
        print(f"Failed: {c}")
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
            if 'point' in c:
                c =c.replace('point',".")
            if c.replace(".","",1).isdigit():
                return c
            if "." in c:
                c =c.split(".")
                index = []
                for i in c :
                    if " " in i:
                        i = i.replace(" ","")
                        index.append(i)
                    else :
                        index = c


                if len(c) != 2:
                    return pd.NaT
                try :

                    first = num[index[0]]
                    second = num[index[1]]
                    return  float(f"{first}.{second}")
                except :
                    return pd.NaT
            else :
                try :
                    first = num[c]
                    return float(f"{first}")

                except:
                    return pd.NaT

    data_f.rename(columns={'mag': 'magnitude'}, inplace=True)

    data_f['magnitude'] = data_f['magnitude'].apply(number)
    data_f['magnitude'] = pd.to_numeric(data_f['magnitude'], errors='coerce')

    # حذف داده‌های گمشده
    data_f = data_f.dropna(subset=['latitude', 'longitude', 'magnitude'])
    data_f['depth'] = data_f['depth'].fillna(data_f['depth'].mean())
    print(data_f.isna().sum())

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

    data_f['Category'] = data_f['magnitude'].apply(category)

    # استخراج منطقه (در صورت وجود ستون place)
    if 'place' in data_f.columns:
        data_f['region'] = data_f['place'].astype(str).apply(lambda x: x.split(',')[0].strip())
    else:
        print(" ستون 'place' در فایل وجود ندارد!")

    # گروه‌بندی‌ها

    group_1 = data_f.groupby(['Month', 'Category']).agg(
        count=('magnitude', 'size'),
        mean_mag=('magnitude', 'mean')
    )
    print(group_1)

    if 'region' in data_f.columns:
        group_2 = data_f.groupby('region').agg(
            quake_count=('magnitude', 'size'),
            mean_mag=('magnitude', 'mean'),
            mean_depth=('depth', 'mean'),
            max_mag=('magnitude', 'max'),
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
        plt.savefig("jpg/JAPAN_messy_cleaned.png", bbox_inches='tight')

        plt.show()


    # مختصات توکیو
    tokyo_latitude = 35.6895
    tokyo_longitude = 139.6917

    # فاصله تا توکیو (درجه جغرافیایی)
    data_f['distance_to_tokyo'] = np.sqrt(
        (data_f['latitude'] - tokyo_latitude) ** 2 +
        (data_f['longitude'] - tokyo_longitude) ** 2
    )

    #استخراج آرایه فاصله
    distance = data_f['distance_to_tokyo']
    # محاسبات آماری
    distance_mean = np.mean(distance)
    distance_variance = np.var(distance)
    distance_standard_deviation = np.std(distance)
    #محاسبات آماری قسمت صدک(percentile)
    dist_percentile_1 = np.percentile(distance , 25)
    dist_percentile_2 = np.percentile(distance , 50)
    dist_percentile_3 = np.percentile(distance , 75)
    data_f['source'] =data_f['region']
    data_f.drop(columns=['status'], inplace=True)
    data_f.drop(columns=['notes'], inplace=True)
    data_f.to_csv("clean_csv/JAPAN_DATASET.csv", index=False)
    #مصورسازی نمودارها

