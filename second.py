import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
def geofon():
    index = []
    final_index = []

    end = datetime.today().date()
    start = end - timedelta(days=30)

    params = {
        'datemin': str(start),
        'datemax': str(end),
        'latmin': 24,
        'latmax': 46,
        'lonmin': 123,
        'lonmax': 146,
        'magmin': 1,
        'fmt': 'html',
    }

    url = "https://geofon.gfz-potsdam.de/eqinfo/list.php"
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    results = soup.find("div", class_='container-fluid eqlist')
    if not results:
        print("Not Found")
        exit()

    information = results.find_all("a", href=re.compile(r'event\.php\?id='))

    print(f"we found {len(information)} information")

    for result in information:
        mag = result.find('span', class_='magbox').text
        mag = mag.strip()
        city = result.find('strong').text
        city = city.split(",")[0]
        times = result.find_all('div', class_='col-xs-12')[1]
        time = times.get_text("", strip=True)
        patern = r"\d{4}-\d{2}-\d{2}"
        time_e = re.findall(patern, time)[0]
        patern_h = r"\d{2}:\d{2}:\d{2}.\d{1}"
        time_e_h = re.findall(patern_h, time)[0]
        location = result.find('div', class_='col-xs-12')
        location = location.get("title")
        depth = result.find('span', class_='pull-right').text
        depth = depth.strip()
        pattern = r"(^\d+)"
        depth = re.findall(pattern, depth)[0]
        finall = f"{mag},{city},{time_e},{time_e_h},{location},{depth}"
        final_index.append(finall)

    with open("JAPAN_GEOFONN.csv", "w", encoding="utf-8") as f:
        for i in final_index:
            f.write(i)
            f.write("\n")

    print("Saved to JAPAN_GEOFONN.csv")