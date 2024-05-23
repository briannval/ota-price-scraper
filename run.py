from selenium import webdriver as wd
from selenium_stealth import stealth

from models.ota_download import OtaDownload

chrome_options = wd.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate_errors")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("detach", True)
driver = wd.Chrome(options=chrome_options)

stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

HOTEL_EXAMPLES = [
    "Hotel Indonesia Kempinski Jakarta",
    "Hotel Ciputra Jakarta",
    "The Hermitage Jakarta",
    "Grand Hyatt Jakarta",
    "The Orient Jakarta",
    "Hotel Mulia",
    "Raffles Jakarta",
    "Four Seasons Jakarta",
    "Bulgari Resort Bali",
]


def run_ota_download():

    ota_download = OtaDownload()

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS \n")

        ota_download.init_hotel(hotel)
        ota_download.tiket_scraping(hotel, driver)
        ota_download.traveloka_scraping(hotel, driver)
        ota_download.agoda_scraping(hotel, driver)

    ota_download.finish()


def main():
    run_ota_download()


main()

driver.quit()
