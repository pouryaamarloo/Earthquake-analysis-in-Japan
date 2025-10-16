import pandas as pd
import matplotlib.pyplot as plt

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
        "Magnitude": "mag"
    }, inplace=True)

    # تبدیل date و time به datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')

    # حذف ردیف‌هایی که datetime یا magnitude ندارند
    df.dropna(subset=['datetime', 'mag'], inplace=True)

    # فقط ستون‌های ضروری
    df = df[['datetime', 'latitude', 'longitude', 'depth', 'mag', 'place']]

    # تبدیل ستون‌های عددی به float
    df[['latitude','longitude','depth','mag']] = df[['latitude','longitude','depth','mag']].astype(float)

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

    df['Category'] = df['mag'].apply(categorize)

    # استخراج منطقه از ستون place
    df['region'] = df['place'].apply(lambda x: str(x).split(',')[0].strip())

    # گروه‌بندی بر اساس Month و Category
    grouped_month_cat = df.groupby(['Month', 'Category']).agg(
        count=('mag', 'size'),
        mean_magnitude=('mag', 'mean'),
        mean_depth=('depth', 'mean'),
        max_magnitude=('mag', 'max')
    ).reset_index()

    # گروه‌بندی بر اساس منطقه
    grouped_region = df.groupby('region').agg(
        count=('mag', 'size'),
        mean_magnitude=('mag', 'mean'),
        mean_depth=('depth', 'mean'),
        max_magnitude=('mag', 'max')
    ).reset_index()
    region_group = df.groupby("region")

    # شمارش تعداد زلزله در هر منطقه
    count_region = region_group.size().reset_index(name='count')

    # محاسبه میانگین بزرگی mag در هر منطقه
    mean_mag_region = region_group[["mag","depth"]].mean().reset_index()

    # محاسبه بیشترین بزرگی و عمق در هر منطقه
    max_mag_or_depth = df.groupby("region")[["mag", "depth"]].max().reset_index()

    count_region.plot(kind='bar', x='region', y='count')
    plt.savefig("jpg/JAPAN_emsc.png",bbox_inches='tight')
    plt.show()

    # ذخیره CSV با جداکننده کاما و encoding مناسب برای Excel
    df.to_csv("clean_csv/Japan_emsc.csv", index=False)
    # grouped_month_cat.to_csv("/clean_csv/emsc_month.csv", index=False, sep=',', encoding='utf-8-sig')
    # grouped_region.to_csv("/clean_csv/emsc_region.csv", index=False, sep=',', encoding='utf-8-sig')


