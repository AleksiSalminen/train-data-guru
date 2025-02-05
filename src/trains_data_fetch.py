import requests
import json


def query_railway_api(departure_date="2020-10-05"):
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
                    {{ operator: {{ shortCode: {{ equals: "vr" }} }} }},
                    {{ commuterLineid: {{ unequals: "Z" }} }}
                ]
            }},
            orderBy:{{trainNumber:DESCENDING}}
        ) {{
            trainNumber
            departureDate
            commuterLineid
            operator {{
                shortCode
            }}
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


def main():
    departure_date = "2020-10-05"
    result = query_railway_api(departure_date)

    if result:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
