import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
def geofon_clean():

    df = pd.read_csv("base_csv/JAPAN_GEOFONN.csv", header=None)

    df = df[[0, 1, 2, 3, 4, 5, 6]].rename(columns={
        0: 'magnitude',
        1: 'place',
        2: 'date',
        3: 'time',
        4: 'longitude',
        5: 'latitude',
        6: 'depth'
    })
    # پاکسازی داده‌ها (حذف °E و °N)
    df['longitude'] = df['longitude'].str.replace('°E', '', regex=False)
    df['latitude'] = df['latitude'].str.replace('°N', '', regex=False)

    # تبدیل نوع داده‌ها
    df = df.astype({
        'magnitude': float,
        'longitude': float,
        'latitude': float,
        'depth': float
    })

    # ساخت ستون تاریخ‌زمان
    df['time'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')


    def req_category(m):
        if m < 4:
            return "zaeif"
        elif 4 <= m < 6:
            return "motevaset"
        else:
            return "shadid"

    # افزودن ستون ماه و دسته‌بندی
    df["Month"] = df['time'].dt.month
    df["Category"] = df['magnitude'].apply(req_category)

    # مرتب‌سازی بر اساس زمان
    df = df.sort_values(by='time')

    # ذخیره فایل تمیزشده
    df["region"] = df["place"]
    tokyo_latitude = 35.6895
    tokyo_longitude = 139.6917

    # فاصله تا توکیو (درجه جغرافیایی)
    df['distance_to_tokyo'] = np.sqrt(
        (df['latitude'] - tokyo_latitude) ** 2 +
        (df['longitude'] - tokyo_longitude) ** 2
    )



    # گروه‌بندی بر اساس ماه و دسته
    month_grouped = df.groupby(['Month', 'Category'])
    mag_mean = month_grouped['magnitude'].mean()
    count_month = month_grouped.size()
    # ایجاد ستون regionبرای تشخیص منطقه زلزله زده

    region_group = df.groupby("region")

    # شمارش تعداد زلزله در هر منطقه
    count_region = region_group.size().reset_index(name='count')

    # محاسبه میانگین بزرگی mag در هر منطقه
    mean_mag_region = region_group[["magnitude","depth"]].mean().reset_index()

    # محاسبه بیشترین بزرگی و عمق در هر منطقه
    max_mag_or_depth = df.groupby("region")[["magnitude", "depth"]].max().reset_index()

    count_region.plot(kind='bar', x='region', y='count')
    plt.savefig("jpg/JAPAN_GEOFON_cleaned.png",bbox_inches='tight')
    plt.show()


    x1=df["latitude"]
    y1=df["longitude"]
    #tokyo (lat and long):
    x2=35.6581
    y2=139.7414
    df["distance_to_tokyo"]= np.sqrt((x2-x1)**2+(y2-y1)**2)
    dist=df["distance_to_tokyo"]
    #محاسبات آماری روی آرایه ها
    dist_mean=np.mean(dist)
    dist_var=np.var(dist)
    dist_std=np.std(dist)
    #percentile
    dist_percentile_1=np.percentile(dist , 25)
    dist_percentile_2=np.percentile(dist , 50)
    dist_percentile_3=np.percentile(dist , 75)
    df['source'] = df['place']
    df.to_csv("clean_csv/JAPAN_GEOFON_cleaned.csv", index=False)

    # محاسبات آماری
    print("Mean of distance :", np.mean(df['distance_to_tokyo']))
    print("Standard deviation of distance :", np.std(df['distance_to_tokyo']))
    print("Variance of distance :", np.var(df['distance_to_tokyo']))
    print(df)
    print("\nمیانگین بزرگی بر اساس ماه و دسته:\n", mag_mean)
    print("\nتعداد زلزله‌ها بر اساس ماه و دسته:\n", count_month)
    print("\nمنطقه وقوع زلزله:\n",mean_mag_region )
    print("\n  منطقه وقوع زلزله بر اساس بزرگی :\n",max_mag_or_depth )


