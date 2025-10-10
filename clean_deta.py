import pandas as pd 

#reading file you send to this
df=pd.read_csv("JAPAN_GEOFON.csv", header=None)

#cut data(,)
print(df.shape)
#colums name
# df.columns = ['Magnitude' , 'location' , 'data' , 'time' , 'Longitude' , 'Latitude' , 'Depth']
df = df[[0, 1, 2, 3, 4, 5, 6]].rename(columns={0:'Magnitude', 1:'location', 2:'Date',3:'Time',4:'Longitude',5:'Latitude',6:'Depth'})

# #cleaning data
# # first step cleaning data and del extra Character
df['Longitude'] = df['Longitude'].str.replace('°E', '', regex=False)
df['Latitude'] = df['Latitude'].str.replace('°N', '', regex=False)


#  casting to intiger
df['Magnitude'] = df['Magnitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)
df['Latitude'] = df['Latitude'].astype(float)
df['Depth'] = df['Depth'].astype(float)


#
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')

#
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
df["Month"] = df['Datetime'].dt.month
# df["Category"] = df['Magnitude'].apply(lambda x )
#
df = df.sort_values(by='Datetime')

#
df = df.dropna(subset=['Datetime'])

#
df.to_csv("JAPAN_GEOFON_cleaned.csv", index=False)

print(" داده‌ها با موفقیت تمیز و در فایل JAPAN_GEOFON_cleaned.csv ذخیره شدند!")
print(df)
