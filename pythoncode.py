import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#خواندن فایل csv:
df=pd.read_csv("data/japan_earthquakes.csv")
print(df.shape)
print(df.columns)
#تبدیل ستون تاریخ به datetime:
df["time"] = pd.to_datetime(df["time"],errors="coerce")

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
#تبدیل ستون های عددی به float:
digit_column_list=["latitude" ,"longitude","depth","mag","nst","gap",
                   "dmin","rms","horizontalError","depthError","magError","magNst"]
for i in digit_column_list:
    if i in df.columns:
        df[i]=pd.to_numeric(df[i],errors='coerce')
#print (df["mag"].apply(lambda x :isinstance(x ,(int , float))))

df.dropna(subset=["time","latitude","longitude","mag","depth"], inplace=True)

#تابع شدت زلزله
def req_category(c):
    if c<4:
        return "zaeif"
    elif 4<=c<6:
        return "motevaset"
    else:
        return "shadid"

df["Category"] = df["mag"].apply(req_category)

#کتگوری زلزله بر اساس ماه 
mc_group= df.groupby(['month', 'Category'])

mag_mean= mc_group['mag'].mean()

count_mc=mc_group.size()

table = pd.DataFrame({
    "Mag_mean": mag_mean,
    "Count": count_mc
}).reset_index()

#استخراج نام محل از ستون place

df["region"]= df["place"].str.extract(r'of\s*([^,]+)')[0]

df.loc[df["region"].isna(), "region"]= df["place"].str.extract(r'^\s*([^,]+)')[0]

df["region"]=df["region"].fillna("unknown").str.strip()

# گروه‌بندی بر اساس region

region_group = df.groupby("region")
# شمارش تعداد زلزله در هر منطقه

count_region = region_group.size().reset_index(name="count_region")
#  محاسبه میانگین بزرگی mag در هر منطقه
#محاسبه ی میانگین عمق در هر منطقه (depth)

mean_mag_region = region_group[["mag" , "depth"]].mean().reset_index()
# محاسبه بیشترین بزرگی یا عمق در هر منطقه

max_mag_or_depth =region_group[["mag", "depth"]].max().reset_index()
#رسم نمودار میله ای 
count_region.plot(kind="bar",figsize=(10,5), x="region" , y="count_region")
plt.title("count of earthquakes by region")
plt.xlabel("Region")
plt.ylabel("Count")
plt.show()
#محاسبه ی distance to tokyo
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
# ذخیره نتایج در فایل جدید
df.to_csv("data/japan_earthquakes_full.csv", index=False)

processed_columns= ["time","latitude","longitude","depth","mag","Category","region","month","year","distance_to_tokyo"]
df[processed_columns].to_csv("data/japan_earthquakes_processed.csv", index=False, encoding="utf-8-sig")

test_df=pd.read_csv("data/japan_earthquakes_processed.csv")
print(test_df.head())
print(test_df.info())

