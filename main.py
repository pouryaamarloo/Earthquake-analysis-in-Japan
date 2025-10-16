from scraping import usgs,emsc,geofon
from pandas_sorted import geofon_clean,japan_messy_earthquakes,emsc_clean,usgs_clean
from database_sql.sql import SQLConnector
import pandas as pd
import glob
from visualization.visualization import EarthquakeVisualizer
#
# def call_scraper():
#     usgs.earthquake_api()
#     geofon.geofon()
#     emsc.emsc()
#     print("داده ها استخراج شدند")
# #     return
def sort_data():
    geofon_clean.geofon_clean()
    japan_messy_earthquakes.japan_messy_earthquakes()
    emsc_clean.emsc_clean()
    usgs_clean.usgs_clean()
    return
def database_e(df,csv_name):
    database = SQLConnector()
    database.insert(df)
    all_earthquakes = database.fetch_all()
    earthquakes_by_month_region = database.get_all_earthquakes()
    avg_magnitude_region = database.get_average_magnitude_by_region()
    recent_earthquakes= database.get_recent_earthquakes_by_region()
    depth_stats_region = database.get_depth_by_region()
    deleted_rows_count= database.delete_suspicious_rows()
    visualizer = EarthquakeVisualizer(database)
    visualizer.plot_magnitude_histogram(csv_name)
    visualizer.plot_time_trends(csv_name)
    visualizer.plot_scatter(csv_name)
    visualizer.plot_box_distribution(csv_name)
    visualizer.plot_heatmap(csv_name)



if __name__ == '__main__':
    #call_scraper()
    sort_data()
    csv_files = glob.glob("clean_csv/*.csv")
    for file in csv_files:
        df = pd.read_csv(file)
        if df.empty:
            continue
        else :
            database_e(df,file)





