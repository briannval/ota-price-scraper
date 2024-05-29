from driver.ota_driver import OtaDriver
from scrapers.ota_download import OtaDownload
from scrapers.ota_mongo import OtaMongo

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


def run():
    ota_driver = OtaDriver.get_driver()

    driver_choice = int(input("Choose: \n1. Download\n2. Mongo\n>"))

    if driver_choice == 1:
        ota_download = OtaDownload()
    else:
        ota_download = OtaMongo()

    for i, hotel in enumerate(HOTEL_EXAMPLES):
        print("=========================================")
        print(f"Scraping for {hotel}...")
        print(f"Progress: {str(i+1)}/{len(HOTEL_EXAMPLES)} HOTELS \n")

        ota_download.scrape(hotel, ota_driver)

    ota_download.finish()
    ota_driver.quit()


if __name__ == "__main__":
    run()
