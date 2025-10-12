import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("JAPAN_GEOFON.csv", header=None)

df = df[[0, 1, 2, 3, 4, 5, 6]].rename(columns={
    0: 'mag',
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
    'mag': float,
    'longitude': float,
    'latitude': float,
    'depth': float
})

# ساخت ستون تاریخ‌زمان
df['Datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')

# حذف ردیف‌های بدون تاریخ معتبر
df = df.dropna(subset=['Datetime'])

def req_category(m):
    if m < 4:
        return "zaeif"
    elif 4 <= m < 6:
        return "motevaset"
    else:
        return "shadid"

# افزودن ستون ماه و دسته‌بندی
df["Month"] = df['Datetime'].dt.month
df["Category"] = df['mag'].apply(req_category)

# مرتب‌سازی بر اساس زمان
df = df.sort_values(by='Datetime')

# ذخیره فایل تمیزشده
df.drop(columns=['Datetime'], inplace=True)

df.to_csv("JAPAN_GEOFON_cleaned.csv", index=False)

# گروه‌بندی بر اساس ماه و دسته
month_grouped = df.groupby(['Month', 'Category'])
mag_mean = month_grouped['mag'].mean()
count_month = month_grouped.size()
# ایجاد ستون regionبرای تشخیص منطقه زلزله زده

df["region"] = df["place"]
region_group = df.groupby("region")

# شمارش تعداد زلزله در هر منطقه
count_region = region_group.size().reset_index(name='count')

# محاسبه میانگین بزرگی mag در هر منطقه
mean_mag_region = region_group[["mag","depth"]].mean().reset_index()

# محاسبه بیشترین بزرگی و عمق در هر منطقه
max_mag_or_depth = df.groupby("region")[["mag", "depth"]].max().reset_index()

count_region.plot(kind='bar', x='region', y='count')
plt.savefig("jpg/JAPAN_GEOFON_cleaned.png",bbox_inches='tight')
plt.show()

tokyo_latitude = 35.6895
tokyo_longitude = 139.6917

# فاصله تا توکیو (درجه جغرافیایی)
df['distance_to_tokyo'] = np.sqrt(
    (df['latitude'] - tokyo_latitude) ** 2 +
    (df['longitude'] - tokyo_longitude) ** 2
)

# محاسبات آماری
print("Mean of distance :", np.mean(df['distance_to_tokyo']))
print("Standard deviation of distance :", np.std(df['distance_to_tokyo']))
print("Variance of distance :", np.var(df['distance_to_tokyo']))
print(df)
print("\nمیانگین بزرگی بر اساس ماه و دسته:\n", mag_mean)
print("\nتعداد زلزله‌ها بر اساس ماه و دسته:\n", count_month)
print("\nمنطقه وقوع زلزله:\n",mean_mag_region )
print("\n  منطقه وقوع زلزله بر اساس بزرگی :\n",max_mag_or_depth )



