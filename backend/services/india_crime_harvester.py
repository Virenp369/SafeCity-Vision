import pandas as pd
import numpy as np
import datetime
import logging

logger = logging.getLogger(__name__)

class IndiaDataHarvester:
    def __init__(self):
        # 30+ Major Indian Hubs/States with approx coordinates
        self.cities = {
            "Mumbai, MH": {"lat": 19.0760, "lon": 72.8777},
            "Delhi, NCR": {"lat": 28.7041, "lon": 77.1025},
            "Bangalore, KA": {"lat": 12.9716, "lon": 77.5946},
            "Hyderabad, TS": {"lat": 17.3850, "lon": 78.4867},
            "Chennai, TN": {"lat": 13.0827, "lon": 80.2707},
            "Kolkata, WB": {"lat": 22.5726, "lon": 88.3639},
            "Pune, MH": {"lat": 18.5204, "lon": 73.8567},
            "Ahmedabad, GJ": {"lat": 23.0225, "lon": 72.5714},
            "Jaipur, RJ": {"lat": 26.9124, "lon": 75.7873},
            "Surat, GJ": {"lat": 21.1702, "lon": 72.8311},
            "Lucknow, UP": {"lat": 26.8467, "lon": 80.9462},
            "Kanpur, UP": {"lat": 26.4499, "lon": 80.3319},
            "Nagpur, MH": {"lat": 21.1458, "lon": 79.0882},
            "Indore, MP": {"lat": 22.7196, "lon": 75.8577},
            "Thane, MH": {"lat": 19.2183, "lon": 72.9781},
            "Bhopal, MP": {"lat": 23.2599, "lon": 77.4126},
            "Visakhapatnam, AP": {"lat": 17.6868, "lon": 83.2185},
            "Patna, BR": {"lat": 25.5941, "lon": 85.1376},
            "Vadodara, GJ": {"lat": 22.3072, "lon": 73.1812},
            "Ghaziabad, UP": {"lat": 28.6692, "lon": 77.4538},
            "Ludhiana, PB": {"lat": 30.9010, "lon": 75.8573},
            "Agra, UP": {"lat": 27.1767, "lon": 78.0081},
            "Nashik, MH": {"lat": 19.9975, "lon": 73.7898},
            "Faridabad, HR": {"lat": 28.4089, "lon": 77.3178},
            "Meerut, UP": {"lat": 28.9845, "lon": 77.7064},
            "Rajkot, GJ": {"lat": 22.3039, "lon": 70.8022},
            "Kalyan, MH": {"lat": 19.2403, "lon": 73.1305},
            "Vasai-Virar, MH": {"lat": 19.3919, "lon": 72.8397},
            "Varanasi, UP": {"lat": 25.3176, "lon": 82.9739},
            "Srinagar, JK": {"lat": 34.0837, "lon": 74.7973},
            "Aurangabad, MH": {"lat": 19.8762, "lon": 75.3433},
            "Dhanbad, JH": {"lat": 23.7957, "lon": 86.4304},
            "Amritsar, PB": {"lat": 31.6340, "lon": 74.8723},
        }
        
        self.categories = [
            "IPC 420 - Fraud / Cheating",
            "IPC 378 - Theft / Burglary",
            "IPC 302 - Murder / Homicide",
            "IPC 354 - Assault / Outraging Modesty",
            "IPC 392 - Robbery",
            "NDPS Act - Narcotics / Drugs",
            "IT Act 2000 Sec 66 - Cyber Security Breach",
            "IPC 498A - Domestic Violence",
            "IPC 143 - Unlawful Assembly / Riot"
        ]

    def fetch_simulated_ncrb_data(self, limit=5000):
        """
        Simulates a scalable API connection to NCRB databases based on a record limit.
        Generates massive datasets for realistic rendering.
        """
        logger.info(f"Establishing secure uplink to India NCRB Node... Simulating {limit} records.")
        
        records = []
        now = datetime.datetime.now()
        
        for _ in range(limit):
            city_name = np.random.choice(list(self.cities.keys()))
            city_data = self.cities[city_name]
            
            # Coordinate variance (~20km radius)
            lat_offset = np.random.normal(0, 0.1)
            lon_offset = np.random.normal(0, 0.1)
            
            # Regional Crime weighting
            if "Bangalore" in city_name or "Pune" in city_name or "Hyderabad" in city_name:
                probs = [0.3, 0.1, 0.05, 0.1, 0.05, 0.05, 0.3, 0.02, 0.03] # High cyber/fraud
            elif "Delhi" in city_name or "UP" in city_name:
                probs = [0.1, 0.25, 0.1, 0.2, 0.1, 0.05, 0.05, 0.05, 0.1] # High theft/assault
            else:
                probs = [0.15, 0.2, 0.05, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05]
                
            cat = np.random.choice(self.categories, p=probs)
            
            # Random time in the past 30 days
            hours_ago = np.random.randint(0, 30 * 24)
            timestamp = now - datetime.timedelta(hours=hours_ago)
            
            records.append({
                "Timestamp": timestamp,
                "City": city_name,
                "Latitude": city_data["lat"] + lat_offset,
                "Longitude": city_data["lon"] + lon_offset,
                "Crime_Category": cat,
                "Description": f"NCRB Log: Subject reported under {cat} in {city_name} sector."
            })
            
        df = pd.DataFrame(records)
        df = df.sort_values(by="Timestamp", ascending=False).reset_index(drop=True)
        return df
