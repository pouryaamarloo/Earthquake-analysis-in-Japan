import requests
from bs4 import BeautifulSoup
import re
index = []

url = "https://geofon.gfz.de/eqinfo/list.php?datemin=2025-09-07&datemax=2025-10-07&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=1&fmt=html&nmax="

results =BeautifulSoup(requests.get(url).content, "html.parser")
results=results.find("div", class_ ='container-fluid eqlist')
# print(results)
information = results.find_all("a")
for info in information:
        results = info.find('div', class_='flex-row row eqinfo-all evnrow')
        if results is None:
            continue
        else :
                index.append(results)
        for result in index:
            mag = result.find('span', class_='magbox').text
            city = result.find('strong').text
            times = result.find_all('div', class_='col-xs-12')[1]
            time = times.get_text("",strip=True)
            patern =r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{1}"
            time_e = re.findall(patern, time)
            if time_e:
                print (city, mag, time_e)


        # for result in results:
        #     if result is not None:
        #         mag = result.find('span', class_='magbox')
        #         print(mag.text)
