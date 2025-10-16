from scraping import first,scrap,second
from pandas_sorted import clean_deta

def call_scraper():
    first.earthquake_api()
    second.geofon()
    scrap.emsc()
    print("داده ها استخراج شدند")
    return
def sort_data():





if __name__ == '__main__':
    call_scraper()


