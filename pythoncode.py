import pandas as pd
import numpy as np
#خواندن فایل csv:
df=pd.read_csv("data/japan_earthquakes.csv")
print(df.shape)
print(df.columns)
#تبدیل ستون تاریخ به datetime:
df["time"]=pd.to_datetime(df["time"],errors="coerce")

df["year"]=df["time"].dt.year
df["mounth"]=df["time"].dt.month
#تبدیل ستون های عددی به float:
digit_column_list=["latitude" ,"longitude","depth","mag","nst","gap","dmin","rms","horizontalError","depthError","magError","magNst"]
for i in digit_column_list:
    if i in df.columns:
        df[i]=pd.to_numeric(df[i],errors='coerce')
df=df.dropna()

#تابع شدت زلزله
def req_category(c):
    if c<4:
        return "zaeif"
    elif 4<c<6:
        return "motevaset"
    elif 6<c:
        return "shadid"

df["Category"] = df["mag"].apply(req_category)

#کتگوری زلزله بر اساس ماه 
mc_group= df.groupby(['mounth', 'Category'])

mag_mean= mc_group['mag'].mean()

count_mc=mc_group.size()

table = pd.DataFrame({
    "Mag_mean": mag_mean,
    "Count": count_mc
}).reset_index()


#استخراج نام مخل از ستون place
df["region"]=df["place"].str.extract(r'of(.*?),')

# گروه‌بندی بر اساس region
region_group = df.groupby("region")

# شمارش تعداد زلزله در هر منطقه
count_region = region_group.size().reset_index()

# محاسبه میانگین بزرگی mag در هر منطقه
mean_mag_region = region_group["mag"].mean().reset_index()

# محاسبه بیشترین بزرگی و عمق در هر منطقه
max_mag_or_depth = df.groupby("region")[["mag", "depth"]].max().reset_index()
