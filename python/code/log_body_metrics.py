import polars as pl
from datetime import datetime
from pathlib import Path

# Function that logs body metrics
def log_body_metrics():

    try:
        # Take user input with error handling
        body_weight = float(input("Enter body weight (in kg): "))
        fat_mass = float(input("Enter fat mass (in %): "))
        muscle_mass = float(input("Enter muscle mass (in kg): "))
        bone_mass = float(input("Enter bone mass (in kg): "))

        # Get today's date in day-month-year format
        todays_date = datetime.today().strftime("%d-%m-%Y")

        # Define height in meters for BMI calculation
        height = 1.85

        # Create a new entry
        new_entry = pl.DataFrame({
            "date": [todays_date],
            "weight": [body_weight],
            "bmi": [round(body_weight / (height**2), 2)],
            "fat_mass_percentage": [fat_mass],
            "muscle_mass": [muscle_mass],
            "bone_mass": [bone_mass]
        })

        # Define the file path
        root = Path(__file__).resolve().parent.parent
        body_metrics_path = root / "data" / "processed" / "body_metrics.csv"
        body_metrics_path.parent.mkdir(parents=True, exist_ok=True)

        # Append or create new CSV
        if body_metrics_path.exists():
            existing_data = pl.read_csv(body_metrics_path)
            updated_data = pl.concat([existing_data, new_entry])
        else:
            updated_data = new_entry

        # Save updated/new data to file
        updated_data.write_csv(body_metrics_path)

        print("Body metrics have been logged properly!")

    except ValueError:
        print("Invalid input! Please enter numeric values.")

# Call the function
log_body_metrics()
