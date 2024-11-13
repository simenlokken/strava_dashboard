import polars as pl
import requests
from pathlib import Path

class WeatherData:

    def __init__(self) -> None:
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.root = Path(__file__).resolve().parent.parent
        self.processed_data = pl.read_parquet(self.root / "data" / "processed" / "processed_data.parquet")
        self.weather_data = []

    def load_processed_data(self):
        return self.processed_data
    
    def get_weather_data(self, processed_data):
        for row in processed_data.iter_rows(named=True):
            lat = row["latitude"]
            lon = row["longitude"]
            time_obj = row["date"]
            date_str = time_obj.strftime("%Y-%m-%d")

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["temperature_2m", "rain"],
            "timezone": "auto",
            "start_date": date_str,
            "end_date": date_str
        }

        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.weather_data.append({
                "date": date_str,
                "latitude": lat,
                "longitude": lon,
                "weather": data
            })
        else:
            print(f"Failed to fetch weather data for lat: {lat}, {lon}.")

if __name__ == "__main__":
    weather_data = WeatherData()
    processed_data = weather_data.load_processed_data()
    weather_data = weather_data.get_weather_data(processed_data)
    print(weather_data)
