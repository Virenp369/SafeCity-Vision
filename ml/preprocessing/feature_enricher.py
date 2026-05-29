import pandas as pd

class DataEnricher:
    def enrich(self, df):
        """
        Takes a dataframe with Timestamp, Latitude, Longitude and adds contextual features.
        Note: For this real-time interactive dashboard, pulling row-by-row historical weather 
        and OpenStreetMap nodes takes several minutes per 1,000 rows. 
        To keep the app feeling instantaneous, we simulate these environmental factors 
        based on the geographic coordinates and temporal data. In a production pipeline, 
        this runs as a nightly batch job via Open-Meteo and OSMnx APIs.
        """
        required_columns = ["Timestamp", "Latitude", "Longitude"]
        missing_columns = [column for column in required_columns if column not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns for enrichment: {', '.join(missing_columns)}")

        df = df.copy()
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
        df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
        df = df.dropna(subset=required_columns)

        if df.empty:
            return df

        # Temporal Features
        df['Hour'] = df['Timestamp'].dt.hour
        df['DayOfWeek'] = df['Timestamp'].dt.dayofweek
        df['Month'] = df['Timestamp'].dt.month
        
        # Simulated Environmental Features (Weather & Urban Density proxy)
        df['Temperature'] = 25 + (df['Month'] - 6).abs() * -2
        df['Is_Raining'] = (df['Month'] % 3 == 0).astype(int)
        
        # Geo-proxy: Distance to Transit (Creates pseudo-random structural variance based on coordinates)
        df['Dist_to_Transit'] = df['Latitude'].apply(lambda x: abs(x * 100) % 5)
        
        return df
