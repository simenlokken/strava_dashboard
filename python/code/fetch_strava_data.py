# Import libraries
import requests
import os
import pandas as pd
from pandas import DataFrame
from pathlib import Path

# Fetch access token from Strava v3 API
def fetch_access_token() -> str:

    """
    This function fetches an Strava access token using a POST request with a refresh token obtained from the Strava Application.

    Returns:
        access_token (str): The access token needed for fetching Strava activities.

    """

    auth_url = "https://www.strava.com/oauth/token"

    CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")   
    CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
    REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': "refresh_token",
    }

    result = requests.post(url = auth_url, data = payload)
    result = result.json()
    return result["access_token"]

access_token = fetch_access_token()

# Fetch activities from Strava v3 API
def get_strava_activities(access_token: str) -> DataFrame:
    
    """
    This function fetches all the Strava activities and stores the activities in a Pandas DataFrame.
    The Strava API has a limit of 200 activites per page per API request, so this function runs a While loop until all activities are fetched.

    Args:
        access_token (str): A string containing the access token needed for making a request to the Strava API

    Returns:
        DataFrame (Pandas): A Pandas DataFrame with activities requsted from the Strava API

    """
    activities = []
    page = 1
    per_page = 200
    
    while True:
        response = requests.get(
            url=f"https://www.strava.com/api/v3/athlete/activities",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"per_page": per_page, "page": page},
        )
        
        if response.status_code != 200:
            print(f"Error fetching activities: {response.status_code}")
            break
        
        data = response.json()
        
        if not data:
            break
        
        activities.extend(data)
        page += 1
        
        return pd.DataFrame(activities)
    
# Store data into an object and write
data = get_strava_activities(access_token)

root = Path(__file__).resolve().parent.parent
raw_data_dir = root / "data" / "raw"
raw_data_dir.mkdir(parents=True, exist_ok=True)

data.to_csv(raw_data_dir / "raw_data.csv")

# Confirm that script works
if data.empty:
    print("DataFrame is empty, code may not have run properly!")
else:
    print("DataFrame is not empty, code have run properly!")