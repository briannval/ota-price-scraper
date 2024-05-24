from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

parser = reqparse.RequestParser()
parser.add_argument("hotel", type=str, required=True)


class HotelScrapeEntry(Resource):

    def get(self):
        return {
            "message": "OTA Scraper is working! Please do a POST method to get a hotel."
        }, 200

    def post(self):
        try:
            args = parser.parse_args()
        except BadRequest:
            return {"message": "Please provide a JSON body"}, 400
        
        if args["hotel"] is None:
            return {"message": "Hotel name is required"}, 400
        
        if args["ota"] is None:
            pass
        
        if args["ota"] not in ["Tiket", "Traveloka", "Agoda"]:
            return {"message": "OTA name is invalid"}, 400
        
        return {"message": f"{args["hotel"]}"}, 200
