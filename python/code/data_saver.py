import csv
from pathlib import Path

class DataSaver:
    @staticmethod
    
    def save_activities_as_csv(activities, filepath=None):
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