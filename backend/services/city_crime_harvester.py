import pandas as pd
from sodapy import Socrata
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataHarvester:
    def __init__(self):
        self.chicago_client = Socrata("data.cityofchicago.org", None, timeout=60)
        self.nyc_client = Socrata("data.cityofnewyork.us", None, timeout=60)
        self.la_client = Socrata("data.lacity.org", None, timeout=60)

    def fetch_global_data(self, node="Chicago", limit=5000):
        logger.info(f"Establishing secure uplink to {node} for {limit} records...")
        
        try:
            if "Chicago" in node:
                query = f"SELECT date as Timestamp, primary_type as Crime_Category, description as Description, latitude as Latitude, longitude as Longitude WHERE latitude IS NOT NULL ORDER BY date DESC LIMIT {limit}"
                results = self.chicago_client.get("ijzp-q8t2", query=query)
            elif "New York" in node:
                # 5uac-w243 is current year NYPD data
                query = f"SELECT cmplnt_fr_dt as Timestamp, ofns_desc as Crime_Category, pd_desc as Description, latitude as Latitude, longitude as Longitude WHERE latitude IS NOT NULL ORDER BY cmplnt_fr_dt DESC LIMIT {limit}"
                results = self.nyc_client.get("5uac-w243", query=query)
            elif "Los Angeles" in node:
                query = f"SELECT date_occ as Timestamp, crm_cd_desc as Crime_Category, premis_desc as Description, lat as Latitude, lon as Longitude WHERE lat IS NOT NULL AND lat != '0' ORDER BY date_occ DESC LIMIT {limit}"
                results = self.la_client.get("2nrs-mtv8", query=query)
            else:
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Global Uplink Failure: {e}")
            return pd.DataFrame()

        df = pd.DataFrame.from_records(results)
        
        if df.empty:
            return df

        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        df = df.dropna(subset=['Timestamp'])
        df['Latitude'] = df['Latitude'].astype(float)
        df['Longitude'] = df['Longitude'].astype(float)
        
        return df[['Timestamp', 'Latitude', 'Longitude', 'Crime_Category', 'Description']]
