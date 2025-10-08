import pandas as pd 

#reading file you send to this
df=pd.read_CSV("JAPAN_GEOFON.csv", header=None)

#cut data(,)
df=df[0].str.spilit(',' , expand=True)

#colums name
df.columns = ['Magnitude' , 'location' , 'data' , 'time' , 'Longitude' , 'Latitude' , 'Depth'] 

#cleaning data
# first step cleaning data and del extra Character
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

#
df = df.sort_values(by='Datetime')

#
df = df.dropna(subset=['Datetime'])

#
df.to_csv("JAPAN_GEOFON_cleaned.csv", index=False)

print("✅ داده‌ها با موفقیت تمیز و در فایل JAPAN_GEOFON_cleaned.csv ذخیره شدند!")
print(df.head())