from strava_client import StravaClient
from data_saver import DataSaver
from log_body_metrics import BodyMetricsLogger
from date_table_creator import DateTableCreator
from strava_data_processor import StravaDataProcessor

if __name__ == "__main__":

    try:
        client = StravaClient()
        activities = client.get_activities()
        DataSaver.save_activities_as_csv(activities)
        
        logger = BodyMetricsLogger()
        logger.log_body_metrics()
        
        date_creator = DateTableCreator()
        date_creator.create_date_table()

        data_processor = StravaDataProcessor()
        data_processor.process_and_save_data()

    except Exception as ex:
        print(f"An error occurred: {ex}")