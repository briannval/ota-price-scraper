from datetime import datetime as dt

import pandas as pd
from selenium import webdriver as wd
from selenium_stealth import stealth

from data import HOTEL_EXAMPLES
from utils import save_as_excel, tiket_scraping, traveloka_scraping


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

    scraping_results = {
        "Date & Time": [],
        "Hotel Name": [],
        "Tiket Price": [],
        "Traveloka Price": [],
    }

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS")

        traveloka_result = traveloka_scraping(hotel, driver)
        tiket_result = tiket_scraping(hotel, driver)

        scraping_results["Date & Time"].append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        scraping_results["Hotel Name"].append(hotel)
        scraping_results["Tiket Price"].append(tiket_result)
        scraping_results["Traveloka Price"].append(traveloka_result)
        print(f"Result for tiket: {tiket_result} \n")

    final_df = pd.DataFrame(scraping_results)

    save_as_excel(final_df)

    driver.quit()


main()
