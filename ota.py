from selenium import webdriver

from data import HOTEL_EXAMPLES
from utils import tiket_scraping


def main():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--ignore-certificate_errors")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS")
        print(f"Result for tiket: {tiket_scraping(hotel, driver)} \n")


main()
