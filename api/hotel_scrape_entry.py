from datetime import datetime as dt

from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from driver.ota_driver import OtaDriver
from scrapers.ota_api import OtaApi

parser = reqparse.RequestParser()
parser.add_argument("hotel", type=str, required=False)
parser.add_argument("ota", type=str, required=False)


class HotelScrapeEntry(Resource):

    ota_driver = OtaDriver.get_driver()
    ota_api = OtaApi()

    def get(self):
        return {
            "message": "OTA Scraper is working! Please do a POST method to get a hotel."
        }, 200

    def post(self):
        args = parser.parse_args()

        if args["hotel"] is None:
            return {"message": "Hotel name is required"}, 400

        if args["ota"] is None:
            tiket, traveloka, agoda = self.ota_api.all_ota_scraping(
                args["hotel"], self.ota_driver
            )
            return {
                "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Hotel Name": args["hotel"],
                "Tiket Price": tiket,
                "Traveloka Price": traveloka,
                "Agoda Price": agoda,
            }

        if args["ota"] not in ["Tiket", "Traveloka", "Agoda"]:
            return {"message": "OTA name is invalid"}, 400

        if args["ota"] == "Tiket":
            return {
                "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Hotel Name": args["hotel"],
                "Tiket Price": self.ota_api.tiket_only_scraping(
                    args["hotel"], self.ota_driver
                ),
            }

        if args["ota"] == "Traveloka":
            return {
                "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Hotel Name": args["hotel"],
                "Traveloka Price": self.ota_api.traveloka_only_scraping(
                    args["hotel"], self.ota_driver
                ),
            }

        if args["ota"] == "Agoda":
            return {
                "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Hotel Name": args["hotel"],
                "Agoda Price": self.ota_api.agoda_only_scraping(
                    args["hotel"], self.ota_driver
                ),
            }

        return {"message": "An unexpected error occured"}, 500
