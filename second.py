import requests
from bs4 import BeautifulSoup
import re

index = []
finall = ""
final_index = []

url = "https://geofon.gfz.de/eqinfo/list.php?datemin=2025-09-06&datemax=2025-10-07&latmax=46&lonmin=124&lonmax=146&latmin=24&magmin=1&fmt=html&nmax="

results =BeautifulSoup(requests.get(url).content , "html.parser")
results=results.find("div", class_ ='container-fluid eqlist')
# print(results)
information = results.find_all("a")
for info in information:
    results = info.select(
        'div.flex-row.row.eqinfo-big.text-danger, '
        'div.flex-row.row.eqinfo-all.evnrow, '
        'div.flex-row.row.eqinfo-all.oddrow'
    )
    if results:
        index.extend(results)
for result in index:
        mag = result.find('span', class_='magbox').text
        mag = mag.strip()
        city = result.find('strong').text
        times = result.find_all('div', class_='col-xs-12')[1]
        time = times.get_text("",strip=True)
        patern =r"\d{4}-\d{2}-\d{2}"
        time_e = re.findall(patern, time)[0]
        patern_h = r"\d{2}:\d{2}:\d{2}.\d{1}"
        time_e_h = re.findall(patern_h, time)[0]
        location = result.find('div',class_='col-xs-12')
        location = location.get("title")
        depth =result.find('span',class_='pull-right').text
        depth = depth.strip()
        pattern =r"(^\d+)"
        depth= re.findall(pattern, depth)[0]
        finall = f"{mag},{city},{time_e},{time_e_h},{location},{depth}"
        final_index.append(finall)

with open ("GEOFON.csv","w",encoding="utf-8") as f :
        for i in final_index :
                f.write(i)
                f.write("\n")








