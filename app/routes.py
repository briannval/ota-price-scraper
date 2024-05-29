from datetime import datetime as dt

from flask import Blueprint, jsonify, render_template, request

from driver.ota_driver import OtaDriver
from scrapers.ota_api import OtaApi

main = Blueprint("main", __name__)
ota_api = OtaApi()


@main.route("/", methods=["GET"])
def index():
    """Serves the HTML form for hotel price scraping."""
    return render_template("index.html")


@main.route("/hotels/tiket", methods=["POST"])
def scrape_tiket():
    ota_driver = OtaDriver.get_driver()
    hotel_name = request.json.get("hotel")
    if not hotel_name:
        return jsonify({"message": "Hotel name is required"}), 400
    price = ota_api.tiket_only_scraping(hotel_name, ota_driver)
    ota_driver.quit()
    return jsonify(
        {
            "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hotel Name": hotel_name,
            "Tiket Price": price,
        }
    )


@main.route("/hotels/traveloka", methods=["POST"])
def scrape_traveloka():
    ota_driver = OtaDriver.get_driver()
    hotel_name = request.json.get("hotel")
    if not hotel_name:
        return jsonify({"message": "Hotel name is required"}), 400
    price = ota_api.traveloka_only_scraping(hotel_name, ota_driver)
    ota_driver.quit()
    return jsonify(
        {
            "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hotel Name": hotel_name,
            "Traveloka Price": price,
        }
    )


@main.route("/hotels/agoda", methods=["POST"])
def scrape_agoda():
    ota_driver = OtaDriver.get_driver()
    hotel_name = request.json.get("hotel")
    if not hotel_name:
        return jsonify({"message": "Hotel name is required"}), 400
    price = ota_api.agoda_only_scraping(hotel_name, ota_driver)
    ota_driver.quit()
    return jsonify(
        {
            "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hotel Name": hotel_name,
            "Agoda Price": price,
        }
    )


@main.route("/hotels", methods=["POST"])
def scrape_all():
    ota_driver = OtaDriver.get_driver()
    hotel_name = request.json.get("hotel")
    if not hotel_name:
        return jsonify({"message": "Hotel name is required"}), 400
    tiket, traveloka, agoda = ota_api.all_ota_scraping(hotel_name, ota_driver)
    ota_driver.quit()
    return jsonify(
        {
            "Date & Time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hotel Name": hotel_name,
            "Tiket Price": tiket,
            "Traveloka Price": traveloka,
            "Agoda Price": agoda,
        }
    )
