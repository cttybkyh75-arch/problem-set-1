

import sys
import requests

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python bitcoin.py <number_of_bitcoins>")

    try:
        bitcoins = float(sys.argv[1])
    except ValueError:
        sys.exit("Error: Command-line argument must be a number.")
        
    api_url = "https://rest.coincap.io/v2/assets/bitcoin"
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        json_data = response.json()
        price_per_bitcoin = float(json_data["data"]["priceUsd"])
        
    except (requests.RequestException, ValueError, KeyError):
        sys.exit("Error: Could not retrieve or parse current Bitcoin price.")
    total_cost = bitcoins * price_per_bitcoin
    print(f"${total_cost:,.4f}")


main()