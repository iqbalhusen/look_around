__author__ = 'iqbal'

import requests

from haversine import distance as compute_distance

def find_neighborhood(place_name, key):

    try:
        url1 = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={0}&key={1}".format(place_name, key)
        json_obj1 = requests.get(url1).json()

        if "error_message" in json_obj1:
            return {"success": False, "message": json_obj1["error_message"]}

        if json_obj1["status"] == "ZERO_RESULTS":
            return {"success": False, "message": "Place not found."}

        place_lat = json_obj1["results"][0]["geometry"]["location"]["lat"]
        place_lng = json_obj1["results"][0]["geometry"]["location"]["lng"]

        destinations = (
            # Destinations are in Google Map API types supported in place search and addition
            # (https://developers.google.com/places/documentation/supported_types)

            'train_station|subway_station',
            'bus_station',
            'shopping_mall',
            'restaurant|food',
            'police',
            'movie_theater',
            'atm',
            'hospital'
        )

        response = {}

        for destination in destinations:
            try:
                url2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&rankby=distance&types={2}&key={3}".format(place_lat, place_lng, destination, key)
                json_obj2 = requests.get(url2).json()

                dest_lat = json_obj2["results"][0]["geometry"]["location"]["lat"]
                dest_lng = json_obj2["results"][0]["geometry"]["location"]["lng"]

                distance = compute_distance((place_lat, place_lng), (dest_lat, dest_lng))
                response[destination] = {"name": json_obj2["results"][0]["name"], "distance": distance}
            except:
                pass

        # Exception for airport because searching with nearbysearch with "types=airport" fetches no or irrelevant results

        url2 = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&rankby=distance&keyword=airport&key={2}".format(place_lat, place_lng, key)
        json_obj2 = requests.get(url2).json()

        dest_lat = json_obj2["results"][0]["geometry"]["location"]["lat"]
        dest_lng = json_obj2["results"][0]["geometry"]["location"]["lng"]

        distance = compute_distance((place_lat, place_lng), (dest_lat, dest_lng))

        response["airport"] = {"name": json_obj2["results"][0]["name"], "distance": distance}

        return {"success": True, "result": response}

    except Exception as exc:
        return {"success": False, "message": str(exc)}
