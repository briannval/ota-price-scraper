from selenium import webdriver as wd
from selenium_stealth import stealth

from data import HOTEL_EXAMPLES
from ota import Ota


def main():

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

    ota = Ota()

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS \n")

        ota.init_hotel(hotel)
        ota.traveloka_scraping(hotel, driver)
        ota.tiket_scraping(hotel, driver)

    ota.download_as_excel()

    driver.quit()


main()
