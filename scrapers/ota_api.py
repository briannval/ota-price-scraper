from .ota import Ota


class OtaApi(Ota):

    def __init__(self):
        super().__init__()

    def finish(self):
        return self.scraping_results

    def tiket_only_scraping(self, hotel, driver):
        return super()._tiket_scraping(hotel, driver, api=True)

    def traveloka_only_scraping(self, hotel, driver):
        return super()._traveloka_scraping(hotel, driver, api=True)

    def agoda_only_scraping(self, hotel, driver):
        return super()._agoda_scraping(hotel, driver, api=True)

    def all_ota_scraping(self, hotel, driver):
        return (
            super()._tiket_scraping(hotel, driver, api=True),
            super()._traveloka_scraping(hotel, driver, api=True),
            super()._agoda_scraping(hotel, driver, api=True),
        )
