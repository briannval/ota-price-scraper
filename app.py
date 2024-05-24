from flask import Flask
from flask_restful import Api

from api.hotel_scrape_entry import HotelScrapeEntry

app = Flask(__name__)
api = Api(app)

api.add_resource(HotelScrapeEntry, "/")

if __name__ == "__main__":
    app.run(debug=True)
