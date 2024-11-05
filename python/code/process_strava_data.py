# Import libraries
import polars as pl
from pathlib import Path

# Set project root 
root = Path(__file__).resolve().parent.parent

# Read raw data
data = pl.read_csv(root / "data/raw/raw_data.csv")

# Keep columns needed
columns_to_keep = [
    "id",
    "name",
    "sport_type",
    "start_date_local",
    "distance",
    "moving_time",
    "elapsed_time",
    "average_speed",
    "average_watts",
    "weighted_average_watts",
    "average_cadence",
    "average_heartrate",
    "kilojoules",
    "average_temp",
    "max_speed",
    "max_watts",
    "max_heartrate",
    "total_elevation_gain",
    "suffer_score",
]

data_processed = data.select(columns_to_keep)

# Change units on average speed and create date and time variables
data_processed = data_processed \
    .with_columns([
        (pl.col("average_speed") * 3.6).round(2),
        (pl.col("max_speed") * 3.6).round(2),
        (pl.col("moving_time") / 3600).round(2),
        (pl.col("elapsed_time") / 3600).round(2),
        (pl.col("start_date_local").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").dt.date().alias("date")),
        (pl.col("start_date_local").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").dt.time().alias("time_of_day"))
    ]) \
    .drop("start_date_local")

# Calculate cumulative columns
cum_columns = ["moving_time", "distance", "kilojoules", "total_elevation_gain"]

for col in cum_columns:
    data_processed = data_processed \
        .with_columns(pl.col(col).cum_sum().alias(f"cumulative_{col}"))

# Save
processed_data_path = root / "data" / "processed"
processed_data_path.mkdir(parents=True, exist_ok=True)

data_processed.write_csv(processed_data_path / "processed_data.csv")