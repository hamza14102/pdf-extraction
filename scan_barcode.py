import requests

# Define the API endpoint and any necessary headers
api_endpoint = "https://2ev2053g6i.execute-api.us-east-2.amazonaws.com/default/ShipmentProductTrackingUpdateLocationByBarcode"
headers = {
    "Content-Type": "application/json",
    # Add any other required headers, such as authorization
}


def send_barcode(barcode):
    data = {"barcode": barcode, "location_code": "PKG"}
    # print(f"Sending request to: {api_endpoint}")
    print(f"Sending Request with data payload: {data}")

    try:
        response = requests.post(api_endpoint, json=data, headers=headers)
        response.raise_for_status()
        print(f"API call successful: {response.status_code}")
        print(f"Response content: {response.content.decode('utf-8')}")
    except requests.exceptions.HTTPError as errh:
        # print(f"HTTP Error: {errh}")
        print(f"Response content: {response.content.decode('utf-8')}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")


def main():
    print("Waiting for barcode scanner input...")

    while True:
        try:
            # Wait for the barcode input
            barcode = (
                input().strip()
            )  # Use .strip() to clean up any extra whitespace/newlines
            if barcode:
                print(f"Received barcode: {barcode}")
                send_barcode(barcode)
        except KeyboardInterrupt:
            print("Exiting program.")
            break


if __name__ == "__main__":
    main()
