import requests
import pandas as pd
from datetime import datetime, timedelta


def Hydro_quebec_data(api_key: str, data_type: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches electricity demand data from the Hydro Quebec API for a specified date range.

    Args:
    api_key (str): The API key required to access the Hydro Quebec API.
    data_type (str): The type of data to fetch. Currently, only 'demand' is supported.
    start_date (str): The start date for the data in any date format recognized by pandas (e.g., '2024-08-01', '01/08/2024').
    end_date (str): The end date for the data in any date format recognized by pandas (e.g., '2024-08-01', '01/08/2024').

    Returns:
    pd.DataFrame: A DataFrame containing the electricity demand data with the time column as the index.
    """

    # Convert start_date and end_date to datetime objects using pandas for flexibility
    start_date_dt = pd.to_datetime(start_date)
    end_date_dt = pd.to_datetime(end_date)

    # Add one day to the end_date to include the full last day in the query
    end_date_dt += timedelta(days=1)

    # Convert dates back to yyyy-mm-dd format for the API request
    start_date_str = start_date_dt.strftime('%Y-%m-%d')
    end_date_str = end_date_dt.strftime('%Y-%m-%d')

    # Prepare the headers with the API key
    headers = {
        "x-api-key": api_key
    }

    # Construct the URL for the demand data request
    url = f"https://api.electricite-quebec.info/HQ_API?start_date={start_date_str}&end_date={end_date_str}"

    # Send the GET request with headers to the API
    response = requests.get(url, headers=headers)

    # Check if the response was successful (status code 200)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

    # Parse the JSON response from the API
    data = response.json()

    # Extract the 'data' part of the response which contains the records
    data_records = data.get('data', [])

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(data_records)

    # Check if the 'time' column exists in the DataFrame
    if 'time' in df.columns:
        # Convert the 'time' column to datetime format for proper indexing
        df['time'] = pd.to_datetime(df['time'])
        # Set the 'time' column as the index of the DataFrame
        df.set_index('time', inplace=True)

    # Return the resulting DataFrame
    return df
