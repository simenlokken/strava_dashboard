import polars as pl
import requests
from pathlib import Path
from polars import DataFrame
import time

class WeatherData():

    def __init__(self) -> None:
        self.url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    
    def load_strava_activities(self) -> DataFrame:
        
        root = Path(__file__).resolve().parent.parent
        file_path = root / "data" / "processed" / "processed_data.csv"
        print(f"Reading CSV file from: {file_path}")
        time.sleep(1)

        if not file_path.exists():
            print(f"File does not exist: {file_path}")
            return DataFrame()
        
        activities = pl.read_csv(file_path)

    def get_weather_data(self, lat: float, lon: float) -> dict:
        url = self.url.format(lat=lat, lon=lon)
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get data: {response.status_code}")
            return {}

if __name__ == "__main__":    

    weather_data = WeatherData()

    lat, lon = 59.91, 10.75
    weather = weather_data.get_weather_data(lat, lon)
    print(weather)


