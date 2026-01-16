"""
Holiday data loader and manager
Handles loading holidays from JSON configuration
"""
import json
import os
from datetime import datetime
from pathlib import Path

class HolidayLoader:
    def __init__(self, config_file="config/holidays.json"):
        self.config_file = config_file
        self.holidays_data = self._load_config()
    
    def _load_config(self):
        """Load holidays configuration from JSON file"""
        config_path = Path(__file__).parent.parent / self.config_file
        
        if not config_path.exists():
            print(f"Warning: Holiday config file not found at {config_path}")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing holiday config: {e}")
            return {}
    
    def get_holidays_for_year(self, year, region="berlin"):
        """
        Get public holidays for a specific year and region
        
        Args:
            year (int): The year to get holidays for
            region (str): The region (default: "berlin")
        
        Returns:
            set: Set of datetime objects representing holidays
        """
        holidays = set()
        
        if region not in self.holidays_data:
            print(f"Warning: Region '{region}' not found in config")
            return holidays
        
        year_str = str(year)
        if year_str not in self.holidays_data[region]:
            print(f"Warning: No holidays defined for {region} in {year}")
            return holidays
        
        for holiday in self.holidays_data[region][year_str]:
            try:
                date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                holidays.add(date)
            except (KeyError, ValueError) as e:
                print(f"Error parsing holiday {holiday}: {e}")
        
        return holidays
    
    def get_holiday_name(self, date, region="berlin"):
        """Get the name of a holiday for a specific date"""
        year_str = str(date.year)
        
        if region not in self.holidays_data:
            return None
        
        if year_str not in self.holidays_data[region]:
            return None
        
        for holiday in self.holidays_data[region][year_str]:
            try:
                holiday_date = datetime.strptime(holiday["date"], "%Y-%m-%d")
                if holiday_date.date() == date.date():
                    return holiday["name"]
            except (KeyError, ValueError):
                continue
        
        return None
    
    def get_available_regions(self):
        """Get list of available regions in the config"""
        return list(self.holidays_data.keys())
    
    def get_available_years(self, region="berlin"):
        """Get list of years available for a region"""
        if region not in self.holidays_data:
            return []
        return [int(year) for year in self.holidays_data[region].keys()]