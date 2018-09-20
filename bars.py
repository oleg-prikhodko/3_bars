import json
import math
import sys
from functools import partial


def get_bar_features(filepath):
    with open(filepath) as json_file:
        bar_features = json.load(json_file)["features"]
        return bar_features


def get_biggest_bar(bar_features):
    biggest = max(
        bar_features, key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return biggest


def get_smallest_bar(bar_features):
    smallest = min(
        bar_features, key=lambda bar: bar["properties"]["Attributes"]["SeatsCount"]
    )
    return smallest


def convert_degree_to_rad(deegrees):
    return (math.pi / 180) * deegrees


def calculate_distance_to_bar(longitude, latitude, bar):
    bar_longitude, bar_latitude = bar["geometry"]["coordinates"]
    delta_longitude = convert_degree_to_rad(longitude - bar_longitude)
    delta_latitude = convert_degree_to_rad(latitude - bar_latitude)
    mean_latitude = convert_degree_to_rad((latitude + bar_latitude) / 2)
    earth_radius = 6371

    distance = earth_radius * math.sqrt(
        delta_latitude ** 2 + (math.cos(mean_latitude) * delta_longitude) ** 2
    )
    return distance


def get_closest_bar(bar_features, longitude, latitude):
    return min(
        bar_features, key=partial(calculate_distance_to_bar, longitude, latitude)
    )


if __name__ == "__main__":
    bar_features = get_bar_features("bars.json")
    biggest = get_biggest_bar(bar_features)
    smallest = get_smallest_bar(bar_features)

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
        if longitude <= -180 or longitude > 180:
            print("Incorrect longitude value")
            sys.exit()

        closest = get_closest_bar(bar_features, longitude, latitude)
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
