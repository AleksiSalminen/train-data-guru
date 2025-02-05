import requests
import json
from datetime import datetime, timedelta
import pandas as pd

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
# User input
#


def get_date_input(prompt):
    while True:
        try:
            date_str = input(prompt + " (YYYY-MM-DD): ")
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")


def get_dates_from_input():
    start_date = get_date_input("Enter start date")
    end_date = get_date_input("Enter end date")
    while end_date < start_date:
        print("End date must be after start date!")
        end_date = get_date_input("Enter end date")
    return start_date, end_date


#
# Data formatting
#


def append_train_data(train_data, data_length, new_date, new_data):
    # Find the trains which are missing from train data
    missing_trains = [train for train in new_data if train not in train_data]

    # For those trains which already exist in the data, update information for the new date
    for train in train_data:
        train_info = train_data[train]
        if train == "Date":
            train_info.append(new_date)
        elif train in new_data:
            train_info.append(1)
        else:
            train_info.append(0)

    for missing_train in missing_trains:
        # If the train data doesn't yet exist in the dictionary, create it and populate with empty data
        new_train_empty_data = []
        for i in range(data_length - 1):
            new_train_empty_data.append(0)
        new_train_empty_data.append(1)
        train_data[missing_train] = new_train_empty_data

    return train_data


def generate_date_range(start_date, end_date):
    current_date = start_date
    dates = []
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates


def get_train_numbers(rw_data):
    trains = rw_data.get("data").get("trainsByDepartureDate")
    train_numbers = [train.get("trainNumber") for train in trains]
    return train_numbers


#
# Data fetch from the API
#


def query_railway_api(departure_date="2024-01-01"):
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
    # Generate date range from user input
    start_date, end_date = get_dates_from_input()
    date_list = generate_date_range(start_date, end_date)

    # Data fetching
    print(f"\nFetching train data for time range {start_date} - {end_date}...")
    train_data = {"Date": []}
    data_length = 0
    for date in date_list:
        data_length += 1
        data = query_railway_api(date)
        if data:
            trains = get_train_numbers(data)
            print(f"{date} - trains: {trains}")
            train_data = append_train_data(train_data, data_length, date, trains)
        else:
            print(f"{date} - ERROR: failed to fetch data for trains")

    # Transfer data to Excel
    print("\nTransferring data to Excel...")
    # current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# Bruh
if __name__ == "__main__":
    main()
