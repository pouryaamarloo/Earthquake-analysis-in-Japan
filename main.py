from scraping import usgs,emsc,geofon
from pandas_sorted import geofon_clean,japan_messy_earthquakes,emsc_clean,usgs_clean


# def call_scraper():
#     usgs.earthquake_api()
#     geofon.geofon()
#     emsc.emsc()
#     print("داده ها استخراج شدند")
#     return
def sort_data():
    geofon_clean.geofon_clean()
    japan_messy_earthquakes.japan_messy_earthquakes()
    emsc_clean.emsc_clean()
    usgs_clean.usgs_clean()
    return



if __name__ == '__main__':
    # call_scraper()
    sort_data()
