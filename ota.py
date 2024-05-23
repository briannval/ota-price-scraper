import os
import re
import time
from datetime import datetime as dt

import pandas as pd
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By

from data import AGODA_URL, TIKET_URL, TRAVELOKA_URL


class Ota:
    """
    Class to scrape prices from various OTA websites
    """

    def __init__(self):
        self.name = "OTA Price Scraper"
        self.scraping_results = {}
        self.df = None

    def __convert_scraped_string(self, s):
        """
        Utility: convert string with IDR and RP to int
        """
        return int(
            "".join(
                re.findall(r"\d+", s),
            ),
        )

    def __add_to_scraping_results(self, column, res):
        """
        Utility: create if not exist column in dict and append
        """
        if column not in self.scraping_results:
            self.scraping_results[column] = []
        self.scraping_results[column].append(res)

    def __get_comparison(self, comparator, comparison):
        """
        Utility: compare target OTA with others
        """
        if comparator == comparison:
            return "NO DIFF", 0

        if comparator > comparison:
            return "HIGHER", ((comparator - comparison) / comparator)

        return "LOWER", ((comparison - comparator) / comparator)

    def init_hotel(self, hotel):
        """
        Initialize hotel name and scraping time & date
        """
        self.__add_to_scraping_results(
            "Date & Time", dt.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.__add_to_scraping_results("Hotel Name", hotel)

    def tiket_scraping(self, hotel_name, driver):
        """
        Scraping source from tiket.com
        """
        try:
            driver.get(TIKET_URL)
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/div[1]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[5]/div/div/section/div/div/div/div[1]/div/div/div/label/input",
            ).send_keys(
                hotel_name,
            )
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[2]/div[5]/div/div/section/div/div/div/div[2]/div",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/button",
            ).click()
            time.sleep(5)
            res = self.__convert_scraped_string(
                driver.find_element(
                    By.XPATH,
                    "//h3[contains(text(), 'IDR')]",
                ).text
            )
            self.__add_to_scraping_results("Tiket Price", res)
            print(f"Result for tiket: {res} \n")
        except NoSuchElementException:
            self.__add_to_scraping_results("Tiket Price", "UNAVALABLE")
            print(f"Unable to scrape for {hotel_name} in Tiket")

    def traveloka_scraping(self, hotel_name, driver):
        """
        Scraping source from traveloka.com
        """
        try:
            driver.get(TRAVELOKA_URL)
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/input",
            ).send_keys(
                hotel_name,
            )
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div[2]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[5]/div[2]/div/div[2]/div/div[5]/div[2]/div",
            ).click()
            time.sleep(4)
            res = self.__convert_scraped_string(
                driver.find_element(
                    By.XPATH,
                    "/html/body/div[1]/div[5]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/div/div[1]/div[3]/div/div[3]/div[1]",
                ).text
            )
            self.__add_to_scraping_results("Traveloka Price", res)
            print(f"Result for traveloka: {res} \n")
        except NoSuchElementException:
            self.__add_to_scraping_results("Traveloka Price", "UNAVAILABLE")
            print(f"Unable to scrape for {hotel_name} in Traveloka")

    def agoda_scraping(self, hotel_name, driver):
        """
        Scraping source from agoda.com
        """
        try:
            driver.get(AGODA_URL)
            time.sleep(2)
            input_element = driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/input",
            )
            input_element.clear()
            input_element.send_keys(
                hotel_name,
            )
            time.sleep(1)
            while True:
                try:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/ul/li",
                    ).click()
                    break
                except ElementClickInterceptedException:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[16]/div[2]/button",
                    ).click()
                    time.sleep(1)

            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/div[3]",
            ).click()
            time.sleep(1)
            driver.find_element(
                By.XPATH,
                "/html/body/div[9]/div[2]/div/section/section/div/div[2]/div[2]/div/div/div[2]/div/button",
            ).click()
            time.sleep(4)
            res = self.__convert_scraped_string(
                driver.find_elements(
                    By.XPATH, "//span[@class='PropertyCardPrice__Value']"
                )[0].text
            )
            self.__add_to_scraping_results("Agoda Price", res)
            print(f"Result for Agoda: {res} \n")
        except NoSuchElementException:
            self.__add_to_scraping_results("Agoda Price", "UNAVAILABLE")
            print(f"Unable to scrape for {hotel_name} in Agoda")

    def hb_scraping(self, hotel_name, driver):
        pass

    def expedia_scraping(self, hotel_name, driver):
        pass

    def __prepare_for_download(self):
        """
        Utility: Convert to df and creating result/ directory
        """
        if self.df is None:
            self.df = pd.DataFrame(self.scraping_results)
        if not os.path.exists("result"):
            os.makedirs("result")

    def download_as_excel(self):
        """
        Download result df as excel
        """
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.xlsx")  # Default output path
        self.df.to_excel(file_path, sheet_name="Hotels", index=False)
        print(f"Successfully downloaded to {file_path}")

    def download_as_csv(self):
        """
        Download result df as csv
        """
        self.__prepare_for_download()
        file_path = os.path.join("result", "ota.csv")  # Default output path
        self.df.to_csv(file_path, sep=",", index=False)
        print(f"Successfully downloaded to {file_path}")
