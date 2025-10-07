import pandas as pd
import numpy as np
#خواندن فایل csv:
df=pd.read_csv("data/japan_earthquakes.csv")
print(df.shape)
print(df.columns)
#تبدیل ستون تاریخ به datetime:
df["time"]=pd.to_datetime(df["time"],errors="coerce")
digit_column_list=["latitude" ,"longitude","depth","mag","nst","gap","dmin","rms",]
