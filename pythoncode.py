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
def re_category(c):
    if c<4:
        return "zaeif"
    elif 4<c<6:
        return "motevaset"
    elif 6<c:
        return "shadid"
