import re
import time
from abc import ABC, abstractmethod
from datetime import datetime as dt

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

TIKET_URL = "https://www.tiket.com/hotel"
AGODA_URL = "https://www.agoda.com/"
TRAVELOKA_URL = "https://www.traveloka.com/en-id/hotel"


class Ota(ABC):
    """
    Abstract Class to scrape prices from various OTA websites
    """

    def __init__(self):
        self.name = "OTA Price Scraper"
        self.scraping_results = {}

    @abstractmethod
    def finish(self):
        pass

    def reset(self):
        self.scraping_results = {}

    def get_recently_scraped(self):
        if len(self.scraping_results["Tiket Price"]) == 0:
            return "Empty"
        return {
            "Hotel": self.scraping_results["Hotel Name"][-1],
            "Tiket": self.scraping_results["Tiket Price"][-1],
            "Traveloka": self.scraping_results["Traveloka Price"][-1],
            "Agoda": self.scraping_results["Agoda Price"][-1],
        }

    def get_tiket_to_compare(self):
        return self.scraping_results["Tiket Price"][-1]

    def scrape(self, hotel, driver):
        self.__init_hotel(hotel)
        self.__tiket_scraping(hotel, driver)
        self.__traveloka_scraping(hotel, driver)
        self.__agoda_scraping(hotel, driver)

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
            return "="

        if comparator > comparison:
            return f"+{(comparator - comparison)}"

        return f"-{(comparison - comparator)}"

    def __init_hotel(self, hotel):
        """
        Initialize hotel name and scraping time & date
        """
        self.__add_to_scraping_results(
            "Date & Time", dt.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        self.__add_to_scraping_results("Hotel Name", hotel)

    def __tiket_scraping(self, hotel_name, driver):
        """
        Scraping source from tiket.com
        """
        res = "UNAVAILABLE"
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
            print(f"Result for tiket: {res} \n")
        except Exception:
            print(f"Unable to scrape for {hotel_name} in Tiket")
        self.__add_to_scraping_results("Tiket Price", res)

    def __traveloka_scraping(self, hotel_name, driver):
        """
        Scraping source from traveloka.com
        """
        res = "UNAVAILABLE"
        comparison = "UNAVAILABLE"
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
            comparison = self.__get_comparison(
                self.get_tiket_to_compare(),
                res,
            )
            print(f"Result for traveloka: {res} \n")
        except Exception:
            print(f"Unable to scrape for {hotel_name} in Traveloka")
        self.__add_to_scraping_results("Traveloka Price", res)
        self.__add_to_scraping_results("Traveloka Comparison", comparison)

    def __agoda_scraping(self, hotel_name, driver):
        """
        Scraping source from agoda.com
        """
        res = "UNAVAILABLE"
        comparison = "UNAVAILABLE"
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
            comparison = self.__get_comparison(
                self.get_tiket_to_compare(),
                res,
            )
            print(f"Result for Agoda: {res} \n")
        except Exception:
            print(f"Unable to scrape for {hotel_name} in Agoda")
        self.__add_to_scraping_results("Agoda Price", res)
        self.__add_to_scraping_results("Agoda Comparison", comparison)

    def __hb_scraping(self, hotel_name, driver):
        pass

    def __expedia_scraping(self, hotel_name, driver):
        pass
