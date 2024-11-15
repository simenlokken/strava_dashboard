import polars as pl
from datetime import datetime
from pathlib import Path

class BodyMetricsLogger:

    def input_body_metrics(self):

        metrics = {}
        while True:
            try:
                date = input("Enter the date (dd-mm-yyy) or 'done' to finish logging body metrics: ")
                if date.lower() == "done":
                    break
                date = datetime.strptime(date, "%d-%m-%Y").strftime("%d-%m-%Y")

                body_weight = float(input("Enter body weight (in kg): "))
                fat_mass = float(input("Enter fat mass (in %): "))
                muscle_mass = float(input("Enter muscle mass (in kg): "))
                bone_mass = float(input("Enter bone mass (in kg): "))

                metrics[date] = {
                     "weight": body_weight,
                     "fat_mass": fat_mass,
                     "muscle_mass": muscle_mass,
                     "bone_mass": bone_mass
                }

            except ValueError:
                 print("Invalid input. Please try again.")

        return metrics

    def log_body_metrics(self, metrics):
            
        try:
            height = 1.85
            new_entries = []

            for date, data in metrics.items():
                new_entry = pl.DataFrame(
                    {
                        "date": [date],
                        "weight": [data["weight"]],
                        "bmi": [round(data["weight"] / (height**2), 1)],
                        "fat_mass": [data["fat_mass"]],
                        "bone_mass": [data["bone_mass"]]
                    },
                    schema={
                        "date": pl.String,
                        "weight": pl.Float32,
                        "bmi": pl.Float32,
                        "fat_mass": pl.Float32,
                        "bone_mass": pl.Float32
                        },
                        strict=True
                )
                
                new_entries.append(new_entry)

            root = Path(__file__).resolve().parent.parent
            body_metrics_path = root / "data" / "processed" / "body_metrics.csv"
            body_metrics_path.parent.mkdir(parents=True, exist_ok=True)
        
            if body_metrics_path.exists():
                existing_data = pl.read_csv(body_metrics_path)
                updated_data = pl.concat([existing_data] + new_entries)
            else:
                updated_data = pl.concat(new_entries)

            updated_data.write_csv(body_metrics_path)
            print("Body metrics have been logged properly!")

        except ValueError:
            print("Invalid input! Please enter float (decimal) values.")

if __name__ == "__main__":
    logger = BodyMetricsLogger()
    metrics = logger.input_body_metrics()
    if metrics:
        logger.log_body_metrics(metrics)
    else:
        print("No metrics to log.")