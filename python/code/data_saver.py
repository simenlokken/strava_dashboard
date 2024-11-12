import time
from pathlib import Path

class DataSaver:
    @staticmethod

    def save_activities(activities):
        print("Saving activities as CSV...")
        time.sleep(1)
        root = root / Path(__file__).resolve().parent.parent
        file_path = root / "data" / "raw" / "raw_data.csv"
        activities.write_csv(file_path)