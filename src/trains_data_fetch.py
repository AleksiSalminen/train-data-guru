import requests
import json
from datetime import datetime


#
# File handlers
#


def write_json_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def read_json_data(filename):
    with open(filename, "r") as f:
        return json.load(f)


#
# Helpers
#


def get_train_numbers(rw_data):
    trains = rw_data.get("data").get("trainsByDepartureDate")
    train_numbers = [train.get("trainNumber") for train in trains]
    return train_numbers


#
# Data fetch from the API
#


def query_railway_api(departure_date="2024-01-01"):
    """
    Query the Finnish railway API for train information.

    Args:
        departure_date (str): Date in YYYY-MM-DD format

    Returns:
        dict: API response data
    """
    url = "https://rata.digitraffic.fi/api/v2/graphql/graphql"

    headers = {"Content-Type": "application/json", "Accept-Encoding": "gzip"}

    query = f"""
    {{
        trainsByDepartureDate(
            departureDate:"{departure_date}",
            where: {{ 
                and: [
                    {{ timeTableRows: 
                        {{ contains: 
                            {{ station: 
                                {{ shortCode: 
                                    {{ equals: "MSS" }}
                                }}
                            }}
                        }}
                    }}, 
                    {{ timeTableRows:
                        {{ contains:
                            {{ train:
                                {{ trainType:
                                    {{ trainCategory:
                                        {{ name:
                                            {{ equals: "Cargo" }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}, 
                    {{ timeTableRows:
                        {{ contains:
                            {{ cancelled:
                                {{ equals: false }}
                            }}
                        }}
                    }}
                ]
            }},
            orderBy:{{trainNumber:ASCENDING}}
        ) {{
            trainNumber
        }}
    }}
    """

    payload = {"query": query, "variables": None, "operationName": None}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


#
# Main handler
#


def main():
    departure_date = "2024-01-01"
    result = query_railway_api(departure_date)

    if result:
        trains = get_train_numbers(result)
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/{departure_date}_-_{current_datetime}.json"
        write_json_data(filename, result)


if __name__ == "__main__":
    main()
