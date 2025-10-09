from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time, os, glob

download_path = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_path, exist_ok=True)

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "safebrowsing.disable_download_protection": True
})

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get("https://www.emsc-csem.org/Earthquake/")

today = datetime.today().strftime("%Y-%m-%d")
one_month_ago = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

try:
    driver.execute_script("document.getElementById('datemin').value = arguments[0];", one_month_ago)
    driver.execute_script("document.getElementById('datemax').value = arguments[0];", today)
    regions = (
        "BONIN ISLANDS, JAPAN REGION|EASTERN HONSHU, JAPAN|EASTERN SEA OF JAPAN|"
        "HOKKAIDO, JAPAN REGION|IZU ISLANDS, JAPAN REGION|KYUSHU, JAPAN|"
        "MINAMI-TORI-SHIMA, JAPAN REGION|NEAR EAST COAST OF HONSHU, JAPAN|"
        "NEAR S. COAST OF HONSHU, JAPAN|NEAR WEST COAST OF HONSHU, JAPAN|"
        "OFF COAST OF HOKKAIDO, JAPAN|OFF EAST COAST OF HONSHU, JAPAN|"
        "RYUKYU ISLANDS, JAPAN|SEA OF JAPAN|SHIKOKU, JAPAN|SOUTHEAST OF SHIKOKU, JAPAN|"
        "SOUTHWESTERN RYUKYU ISL., JAPAN|VOLCANO ISLANDS, JAPAN REGION|WESTERN HONSHU, JAPAN"
    )
    region_input = driver.find_element(By.ID, "reg")
    region_input.clear()
    region_input.send_keys(regions)
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.ID, "download"))
    ).click()

    timeout = 90
    filename = None
    for _ in range(timeout):
        files = glob.glob(os.path.join(download_path, "*.csv"))
        if files:
            filename = files[0]
            break
        time.sleep(1)
    if filename:
        print(f"CSV ذخیره شد: {filename}")
    else:
        print("دانلود انجام نشد.")
except Exception as e:
    print("خطا:", e)

input("برای بستن مرورگر Enter بزن...")
driver.quit()

