import sys
import requests
import csv
from math import sqrt

def closest_coffee_shops(user_x, user_y, shop_data_url):
    # Fetch the CSV data from the provided URL
    try:
        response = requests.get(shop_data_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)

    # Create a CSV reader from the fetched data
    reader = csv.reader(response.text.splitlines())

    try:
        # Calculate the distance for each coffee shop and sort them by distance
        coffee_shops = sorted(
            [
                (
                    name,
                    round(sqrt((float(x) - user_x) ** 2 + (float(y) - user_y) ** 2), 4)
                )
                for name, x, y in reader
            ],
            key=lambda x: x[1]
        )
    except ValueError as e:
        print(f"Malformed data: {e}")
        sys.exit(1)

    # Return the three closest coffee shops
    return coffee_shops[:3]

if __name__ == "__main__":
    # Check for correct number of command line arguments
    if len(sys.argv) != 4:
        print("Usage: python coffee_shops.py <user x coordinate> <user y coordinate> <shop data url>")
        sys.exit(1)

    # Parse command line arguments
    user_x, user_y, shop_data_url = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]

    # Find the closest coffee shops and print them
    closest_shops = closest_coffee_shops(user_x, user_y, shop_data_url)

    for shop, dist in closest_shops:
        print(f"{shop},{dist:.4f}")
