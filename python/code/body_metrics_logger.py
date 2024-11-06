import polars as pl
from datetime import datetime
from pathlib import Path

class BodyMetricsLogger:
    def log_body_metrics(self):

        try:
            body_weight = float(input("Enter body weight (in kg): "))
            fat_mass = float(input("Enter fat mass (in %): "))
            muscle_mass = float(input("Enter muscle mass (in kg): "))
            bone_mass = float(input("Enter bone mass (in kg): "))

            todays_date = datetime.today().strftime("%d-%m-%Y")
            height = 1.85

            new_entry = pl.DataFrame({
                "date": [todays_date],
                "weight": [body_weight],
                "bmi": [round(body_weight / (height**2), 2)],
                "fat_mass_percentage": [fat_mass],
                "muscle_mass": [muscle_mass],
                "bone_mass": [bone_mass]
            })

            root = Path(__file__).resolve().parent.parent
            body_metrics_path = root / "data" / "processed" / "body_metrics.csv"
            body_metrics_path.parent.mkdir(parents=True, exist_ok=True)
            
            if body_metrics_path.exists():
                existing_data = pl.read_csv(body_metrics_path)
                updated_data = pl.concat([existing_data, new_entry])
            else:
                updated_data = new_entry

            updated_data.write_csv(body_metrics_path)
            print("Body metrics have been logged properly!")
        
        except ValueError:
            print("Invalid input! Please enter numeric values.")