import json
import math
import os.path as path
import sys
from functools import partial


def get_bar_features(filepath):
    if filepath is None:
        filepath = path.join(path.dirname(path.abspath(__file__)), "bars.json")

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


def print_bar_info(bar, message=""):
    output_string = "{message}{name}, seats: {seats}, latitude: {lat:.3f}, longitude: {lon:.3f}".format(
        name=bar["properties"]["Attributes"]["Name"],
        seats=bar["properties"]["Attributes"]["SeatsCount"],
        lat=bar["geometry"]["coordinates"][1],
        lon=bar["geometry"]["coordinates"][0],
        message=message,
    )
    print(output_string)


def is_valid_coordinates(latitude, longitude):
    if latitude < -90 or latitude > 90:
        return False
    if longitude <= -180 or longitude > 180:
        return False
    return True


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    bar_features = get_bar_features(filepath)

    biggest = get_biggest_bar(bar_features)
    smallest = get_smallest_bar(bar_features)
    print_bar_info(biggest, message="Biggest: ")
    print_bar_info(smallest, message="Smallest: ")

    latitude = float(input("Your latitude: "))
    longitude = float(input("Your longitude: "))
    if not is_valid_coordinates(latitude, longitude):
        raise ValueError("Incorrect coordinate values")

    closest = get_closest_bar(bar_features, longitude, latitude)
    print_bar_info(closest, message="Closest: ")


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        sys.exit("No such file")
    except json.JSONDecodeError:
        sys.exit("File contents is not a valid JSON document")
    except KeyError as err:
        sys.exit("Field {} not found".format(err))
    except ValueError as err:
        sys.exit(err)
