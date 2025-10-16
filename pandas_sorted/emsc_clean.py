import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def emsc_clean():
    # file_path = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC.csv"
    # output_clean = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC_clean.csv"
    # output_month_cat = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC_month_cat.csv"
    # output_region = r"C:\Users\pro\Documents\python\Earthquake-analysis-in-Japan\downloads\export_EMSC_region.csv"

    # خواندن CSV با جداکننده ;
    df = pd.read_csv('base_csv/export_EMSC.csv', sep=';')

    # کوتاه کردن اسم ستون‌ها
    df.rename(columns={
        "Date": "date",
        "Time (UTC)": "time",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Region name": "place",
        "Depth": "depth",
        "Magnitude": "magnitude",

    }, inplace=True)

    # تبدیل date و time به datetime
    df['time'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')

    # حذف ردیف‌هایی که datetime یا magnitude ندارند
    df.dropna(subset=['time', 'magnitude'], inplace=True)

    # فقط ستون‌های ضروری
    df = df[['time', 'latitude', 'longitude', 'depth', 'magnitude', 'place']]

    # تبدیل ستون‌های عددی به float
    df[['latitude','longitude','depth','magnitude']] = df[['latitude','longitude','depth','magnitude']].astype(float)

    # ساخت ستون Month
    df['Month'] = df['time'].dt.month

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
    region_group = df.groupby("region")

    # شمارش تعداد زلزله در هر منطقه
    count_region = region_group.size().reset_index(name='count')

    # محاسبه میانگین بزرگی mag در هر منطقه
    mean_mag_region = region_group[["magnitude","depth"]].mean().reset_index()

    # محاسبه بیشترین بزرگی و عمق در هر منطقه
    max_mag_or_depth = df.groupby("region")[["magnitude", "depth"]].max().reset_index()

    count_region.plot(kind='bar', x='region', y='count')
    plt.savefig("jpg/JAPAN_emsc.png",bbox_inches='tight')
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
    # ذخیره CSV با جداکننده کاما و encoding مناسب برای Excel
    df['source'] = df['place']
    df.to_csv("clean_csv/Japan_emsc.csv", )
    # grouped_month_cat.to_csv("/clean_csv/emsc_month.csv", index=False, sep=',', encoding='utf-8-sig')
    # grouped_region.to_csv("/clean_csv/emsc_region.csv", index=False, sep=',', encoding='utf-8-sig')
    return

