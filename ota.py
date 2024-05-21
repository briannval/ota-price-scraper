from datetime import datetime as dt

import pandas as pd
from selenium import webdriver as wd

from data import HOTEL_EXAMPLES
from utils import save_as_excel, tiket_scraping


def main():

    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate_errors")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("detach", True)
    driver = wd.Chrome(options=chrome_options)

    dt_series = []
    tiket_res_series = []

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS")

        tiket_result = tiket_scraping(hotel, driver)
        dt_series.append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        tiket_res_series.append(tiket_result)
        print(f"Result for tiket: {tiket_result} \n")

    final_df = pd.DataFrame(
        {
            "Date & Time": dt_series,
            "Hotel Name": HOTEL_EXAMPLES,
            "Tiket Price": tiket_res_series,
        }
    )

    save_as_excel(final_df)


main()
