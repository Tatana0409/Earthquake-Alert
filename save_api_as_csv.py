import csv
from earthguake_api_client import EarthquakeApiClient
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SaveData(EarthquakeApiClient):

    def save_all_data(self):
        all_data = self.get_all_data()

        if all_data and 'features' in all_data and all_data["features"]:
            filename = f"earthquake_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            logger.warning("No data to save or API returned an empty response.")
            return  # Exit method if no valid data is found
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                fieldnames = all_data['features'][0]['properties'].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for feature in all_data['features']:
                    writer.writerow(feature['properties'])
            logger.info(f"Data successfully saved to {filename}")
        except IOError as e:
            logger.error(f"Failed to write CSV file: {e}")

# client = SaveData(EarthquakeApiClient.api_url)
# client.save_all_data()

