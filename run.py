from driver.ota_driver import OtaDriver
from models.ota_download import OtaDownload

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

    ota_driver = OtaDriver.get_driver()
    ota_download = OtaDownload()

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS \n")

        ota_download.scrape(hotel, ota_driver)

    ota_download.finish()
    ota_driver.quit()


def main():
    run_ota_download()


main()
