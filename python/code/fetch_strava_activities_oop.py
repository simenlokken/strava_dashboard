import os
import requests
import csv
import json
from pathlib import Path

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

        response = requests.post(self.auth_url, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch access token: {response.status_code}")
        
        self.access_token = response.json().get("access_token")
        print("Access token fetched successfully.")
        return self.access_token
    
    def get_activities(self, per_page=200):
        if not self.access_token:
            self.fetch_access_token()

        activities = []
        page = 1
        headers = {"Authorization": f"Bearer {self.access_token}"}

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

        print(f"Fetched {len(activities)} activities.")
        return activities   

class DataSaver:
    @staticmethod
    def save_activities_as_csv(activities, filepath=None):
        # Set default filepath to data/raw_data in the root directory of the script
        if filepath is None:
            script_dir = Path(__file__).resolve().parent.parent
            filepath = script_dir / "data" / "raw" / "raw_data.csv"

        filepath.parent.mkdir(parents=True, exist_ok=True)

        if not activities:
            print("No activities to save.")
            return
        
        headers = activities[0].keys()
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(activities)

        print(f"Data saved to {filepath}")

if __name__ == "__main__":
    try:
        client = StravaClient()
        activities = client.get_activities()
        DataSaver.save_activities_as_csv(activities)
    except Exception as ex:
        print(f"An error occurred: {ex}")