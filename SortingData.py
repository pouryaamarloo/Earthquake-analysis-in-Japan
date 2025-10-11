import pandas as pd
import numpy as np

file_path = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC.csv"
output_path = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC_final.xlsx"

# خواندن CSV با جداکننده ;
df = pd.read_csv(file_path, sep=';')

# کوتاه کردن اسم ستون‌ها
df.rename(columns={
    "Date": "date",
    "Time (UTC)": "time",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Region name": "place",
    "Depth": "depth",
    "Magnitude": "magnitude"
}, inplace=True)

# تبدیل date و time به datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')

# حذف ردیف‌هایی که datetime یا magnitude ندارند
df.dropna(subset=['datetime', 'magnitude'], inplace=True)

# فقط ستون‌های ضروری
df = df[['datetime', 'latitude', 'longitude', 'depth', 'magnitude', 'place']]

# تبدیل ستون‌های عددی به float
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)
df['depth'] = df['depth'].astype(float)
df['magnitude'] = df['magnitude'].astype(float)

# ساخت ستون Month
df['Month'] = df['datetime'].dt.month

# ساخت ستون Category بر اساس بزرگی زلزله
def categorize(mag):
    if mag < 4:
        return 'Weak'
    elif 4 <= mag <= 6:
        return 'Moderate'
    else:
        return 'Strong'

df['Category'] = df['magnitude'].apply(categorize)

# استخراج منطقه از ستون place
# ساده‌ترین روش: جدا کردن بر اساس کاما و گرفتن اولین بخش
df['region'] = df['place'].apply(lambda x: str(x).split(',')[0].strip())

# گروه‌بندی بر اساس Month و Category
grouped_month_cat = df.groupby(['Month', 'Category']).agg(
    count=('magnitude', 'size'),
    mean_magnitude=('magnitude', 'mean'),
    mean_depth=('depth', 'mean'),
    max_magnitude=('magnitude', 'max')
).reset_index()

# گروه‌بندی بر اساس منطقه
grouped_region = df.groupby('region').agg(
    count=('magnitude', 'size'),
    mean_magnitude=('magnitude', 'mean'),
    mean_depth=('depth', 'mean'),
    max_magnitude=('magnitude', 'max')
).reset_index()

# ذخیره به Excel با دو شیت: داده تمیز و آماری
with pd.ExcelWriter(output_path) as writer:
    df.to_excel(writer, sheet_name='Cleaned_Data', index=False)
    grouped_month_cat.to_excel(writer, sheet_name='Monthly_Category', index=False)
    grouped_region.to_excel(writer, sheet_name='Region_Stats', index=False)
