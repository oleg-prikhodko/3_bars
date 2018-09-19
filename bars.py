import json
import math
import sys


def load_data(filepath):
    with open(filepath) as f:
        data = json.load(f)
        return data


def get_biggest_bar(data):
    max_elem = max(
        data["features"], key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return max_elem


def get_smallest_bar(data):
    min_elem = min(
        data["features"], key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return min_elem


def degree_to_rad(deegrees):
    return (math.pi / 180) * deegrees


def get_closest_bar(data, longitude, latitude):
    def calc_distance(bar):
        bar_longitude, bar_latitude = bar["geometry"]["coordinates"]
        delta_longitude = bar_longitude - longitude
        delta_latitude = bar_latitude - latitude
        mean_latitude = (bar_latitude + latitude) / 2
        earth_radius = 6371
        distance = earth_radius * math.sqrt(
            delta_latitude ** 2 + (math.cos(mean_latitude) * delta_longitude) ** 2
        )
        return distance

    return min(data["features"], key=calc_distance)


if __name__ == "__main__":
    data = load_data("bars.json")
    biggest = get_biggest_bar(data)
    smallest = get_smallest_bar(data)

    print(
        "Biggest:",
        biggest["properties"]["Attributes"]["Name"],
        ", seats:",
        biggest["properties"]["Attributes"]["SeatsCount"],
    )

    print(
        "Smallest:",
        smallest["properties"]["Attributes"]["Name"],
        ", seats:",
        smallest["properties"]["Attributes"]["SeatsCount"],
    )

    try:
        latitude = float(input("Your latitude: "))
        if latitude < -90 or latitude > 90:
            print("Incorrect latitude value")
            sys.exit()

        longitude = float(input("Your longitude: "))
        if longitude < -180 or longitude > 180:
            print("Incorrect longitude value")
            sys.exit()

        closest = get_closest_bar(data, longitude, latitude)
        print(
            "Closest:",
            closest["properties"]["Attributes"]["Name"],
            ", latitude:",
            closest["geometry"]["coordinates"][1],
            ", longitude:",
            closest["geometry"]["coordinates"][0],
        )
    except ValueError:
        print("Incorrect input data, should be digits")
