import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from data import TIKET_URL, TRAVELOKA_URL


def get_comparison(comparator, comparison):
    if comparator == comparison:
        return "NO DIFF", 0

    if comparator > comparison:
        return "HIGHER", ((comparator - comparison) / comparator)

    return "LOWER", ((comparison - comparator) / comparator)


def tiket_scraping(hotel_name, driver):
    driver.get(TIKET_URL)
    time.sleep(1)
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
        Keys.ENTER,
    )
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        "/html/body/div[2]/div[5]/div/div/section/div/div/div/div[2]/div",
    ).click()
    time.sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/div[2]/div[2]/div/div[2]/button"
    ).click()
    time.sleep(4)
    element_text = ""
    try:
        element_text = driver.find_element(
            By.XPATH, "//h3[contains(text(), 'IDR')]"
        ).text
    except NoSuchElementException:
        element_text = "ROOM IS FULL !"
    return element_text


def traveloka_scraping(hotel_name, driver):
    # TODO: THINK ABOUT CAPTCHA
    driver.get(TRAVELOKA_URL)
    time.sleep(1)
    driver.find_element(
        By.XPATH,
        "//input[@placeholder='Kota, hotel, tempat wisata']",
    ).send_keys(
        hotel_name,
        Keys.ENTER,
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
    return driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[5]/div[2]/div/div[2]/div[3]/div/div/div[2]/div[3]/div/div/div[1]/div[3]/div/div[3]/div[1]",
    ).text


def agoda_scraping(hotel_name):
    pass


def hb_scraping(hotel_name):
    pass


def expedia_scraping(hotel_name):
    pass
