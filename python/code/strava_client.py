import os
import requests
from dotenv import load_dotenv
import polars as pl
import time

load_dotenv()

class StravaClient:
    def __init__(self) -> None:
        self.auth_url = "https://www.strava.com/oauth/token"
        self.activities_url = "https://www.strava.com/api/v3/athlete/activities"
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.access_token = None

    def fetch_access_token(self):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }

        print("Fetching access token...")
        time.sleep(2)

        response = requests.post(self.auth_url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch access token. Error message: {response.status_code}")
        
        self.access_token = response.json().get("access_token")
        print("Access token has been successfully retrieved.")
        return self.access_token
    
    def get_activities(self, per_page=200):
        if not self.access_token:
            self.fetch_access_token()

        activities = []
        page = 1
        headers = {"Authorization": f"Bearer {self.access_token}"}

        print("Fetching Strava activities...")

        while True:
            response = requests.get(self.activities_url, headers=headers, params={"per_page": per_page, "page": page})
            if response.status_code != 200:
                print(f"Error fetching activities: {response.status_code}")
                break
            
            page_activities = response.json()
            if not page_activities:
                break

            activities.extend(page_activities)
            page += 1

        print(f"Succesfully fetched {len(activities)} activities.")
        return activities

if __name__ == "__main__":
    client = StravaClient()
    activities = client.get_activities()
    print(pl.DataFrame(activities))