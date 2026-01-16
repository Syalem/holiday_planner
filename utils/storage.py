"""
Storage manager for user holiday selections
Handles saving and loading user data
"""
import json
import os
from datetime import datetime

class StorageManager:
    def __init__(self, storage_file="data/holidays_status.json"):
        self.storage_file = storage_file
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.storage_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_holidays(self, holidays1, holidays2, previous_year=0, region="berlin"):
        """
        Save selected holidays to file
        
        Args:
            holidays1 (set): Set of datetime objects for current year
            holidays2 (set): Set of datetime objects for next year
            previous_year (int): Carryover days from previous year
            region (str): Selected region
        """
        data = {
            "holidays1": [d.strftime("%Y-%m-%d") for d in holidays1],
            "holidays2": [d.strftime("%Y-%m-%d") for d in holidays2],
            "previous_year": previous_year,
            "region": region,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(self.storage_file, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving holidays: {e}")
            return False
    
    def load_holidays(self):
        """
        Load selected holidays from file
        
        Returns:
            tuple: (holidays1_set, holidays2_set, previous_year_int, region_str)
        """
        if not os.path.exists(self.storage_file):
            return set(), set(), 0, None
        
        try:
            with open(self.storage_file, "r", encoding='utf-8') as f:
                data = json.load(f)
                
            holidays1 = set(
                datetime.strptime(d, "%Y-%m-%d") 
                for d in data.get("holidays1", [])
            )
            holidays2 = set(
                datetime.strptime(d, "%Y-%m-%d") 
                for d in data.get("holidays2", [])
            )
            previous_year = data.get("previous_year", 0)
            region = data.get("region", None)
            
            return holidays1, holidays2, previous_year, region
            
        except Exception as e:
            print(f"Error loading holidays: {e}")
            return set(), set(), 0, None
    
    def clear_storage(self):
        """Delete the storage file"""
        if os.path.exists(self.storage_file):
            try:
                os.remove(self.storage_file)
                return True
            except Exception as e:
                print(f"Error clearing storage: {e}")
                return False
        return True