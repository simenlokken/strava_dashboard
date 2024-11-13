import polars as pl
from pathlib import Path
import time

class StravaDataProcessor:

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.raw_data_path = self.root / "data" / "raw" / "raw_data.parquet"
        self.processed_data_path = self.root / "data" / "processed" / "processed_data.parquet"
        self.columns_to_keep = [
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
    
    def process_data(self):

        print("Initialized data processing...")
        time.sleep(1)

        raw_data = pl.read_parquet(self.raw_data_path)

        data_processed = raw_data.select(self.columns_to_keep)

        data_processed = data_processed.with_columns([
            (pl.col("average_speed") * 3.6).round(2),
            (pl.col("max_speed") * 3.6).round(2),
            (pl.col("moving_time") / 3600).round(2),
            (pl.col("elapsed_time") / 3600).round(2),
            (pl.col("start_date_local").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").dt.date().alias("date")),
            (pl.col("start_date_local").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%SZ").dt.time().alias("time_of_day"))
        ]) \
        .drop("start_date_local")

        cum_columns = ["moving_time", "distance", "kilojoules", "total_elevation_gain"]

        for col in cum_columns:
            data_processed = data_processed \
            .with_columns(pl.col(col).cum_sum().alias(f"cumulative_{col}"))

        print("Data has been processed. Initalizing saving...")
        time.sleep(1)

        return data_processed
    
    def save_processed_data(self, data_processed):
        self.processed_data_path.parent.mkdir(parents=True, exist_ok=True)
        data_processed.write_parquet(self.processed_data_path)
        print(f"Processed data saved has been saved to file path: {self.processed_data_path}")

if __name__ == "__main__":
    processor = StravaDataProcessor()
    data = processor.process_data()
    processor.save_processed_data(data)