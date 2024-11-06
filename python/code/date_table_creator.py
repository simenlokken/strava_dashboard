from datetime import datetime
import pandas as pd
from pathlib import Path

class DateTableCreator:
    
    def create_date_table(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime.now().date()
        date_range = pd.date_range(start_date, end_date)
        date_table = pd.DataFrame({"date": date_range})
        date_table["week"] = date_table["date"].dt.isocalendar().week
        date_table["month"] = date_table["date"].dt.month_name(locale="no")
        date_table["quarter"] = date_table["date"].dt.quarter
        date_table["year"] = date_table["date"].dt.year
        root = Path(__file__).resolve().parent.parent
        date_table_path = root / "data" / "processed"
        date_table_path.mkdir(parents=True, exist_ok=True)
        date_table.to_csv(date_table_path / "date_table.csv", index=False)