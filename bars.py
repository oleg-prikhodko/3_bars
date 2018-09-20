import json
import math
import os.path as path
import sys
from functools import partial


def get_bar_features(
    filepath=path.join(path.dirname(path.abspath(__file__)), "bars.json")
):
    try:
        with open(filepath) as json_file:
            bar_features = json.load(json_file)["features"]
            return bar_features
    except FileNotFoundError:
        sys.exit("No such file")
    except OSError:
        sys.exit("File cannot be opened")
    except UnicodeDecodeError:
        sys.exit("Not a text file")
    except json.JSONDecodeError:
        sys.exit("File contents is not a valid JSON document")
    except KeyError:
        sys.exit("JSON document should have 'features' field in it")


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


def print_bar_info(bar):
    output = "{name}, seats: {seats}, latitude: {lat:.3f}, longitude: {lon:.3f}".format(
        name=bar["properties"]["Attributes"]["Name"],
        seats=bar["properties"]["Attributes"]["SeatsCount"],
        lat=bar["geometry"]["coordinates"][1],
        lon=bar["geometry"]["coordinates"][0],
    )
    print(output)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        bar_features = get_bar_features(sys.argv[1])
    else:
        bar_features = get_bar_features()

    biggest = get_biggest_bar(bar_features)
    smallest = get_smallest_bar(bar_features)

    print("Biggest:")
    print_bar_info(biggest)

    print("Smallest:")
    print_bar_info(smallest)

    try:
        latitude = float(input("Your latitude: "))
        if latitude < -90 or latitude > 90:
            sys.exit("Incorrect latitude value")

        longitude = float(input("Your longitude: "))
        if longitude <= -180 or longitude > 180:
            sys.exit("Incorrect longitude value")

        closest = get_closest_bar(bar_features, longitude, latitude)
        print("Closest:")
        print_bar_info(closest)
    except ValueError:
        sys.exit("Incorrect input data, should be digits")
