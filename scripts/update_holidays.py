"""
Holiday Configuration Manager
Script to add new regions and years to holidays.json
"""
import json
import os
from pathlib import Path
from datetime import datetime

class HolidayUpdater:
    def __init__(self, config_file="config/holidays.json"):
        self.config_file = Path(__file__).parent.parent / config_file
        self.data = self._load_config()
    
    def _load_config(self):
        """Load existing configuration"""
        if not self.config_file.exists():
            return {}
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_config(self):
        """Save configuration to file"""
        # Ensure directory exists
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_region(self, region_name):
        """
        Add a new region
        
        Args:
            region_name (str): Name of the region (e.g., "bavaria", "hamburg")
        """
        region_name = region_name.lower()
        
        if region_name in self.data:
            print(f"⚠️  Region '{region_name}' already exists!")
            return False
        
        self.data[region_name] = {}
        self._save_config()
        print(f"✅ Region '{region_name}' added successfully!")
        return True
    
    def add_year(self, region_name, year, holidays_list):
        """
        Add holidays for a specific year in a region
        
        Args:
            region_name (str): Name of the region
            year (int): Year to add
            holidays_list (list): List of dicts with 'date' and 'name' keys
        """
        region_name = region_name.lower()
        year_str = str(year)
        
        if region_name not in self.data:
            print(f"⚠️  Region '{region_name}' does not exist. Creating it...")
            self.add_region(region_name)
        
        if year_str in self.data[region_name]:
            print(f"⚠️  Year {year} already exists for {region_name}. Overwriting...")
        
        self.data[region_name][year_str] = holidays_list
        self._save_config()
        print(f"✅ Added {len(holidays_list)} holidays for {region_name} {year}")
        return True
    
    def list_regions(self):
        """List all available regions"""
        if not self.data:
            print("No regions found in configuration.")
            return []
        
        print("\n📍 Available regions:")
        for region in self.data.keys():
            years = list(self.data[region].keys())
            print(f"  • {region}: {len(years)} year(s) - {', '.join(years)}")
        return list(self.data.keys())
    
    def list_years(self, region_name):
        """List all years for a specific region"""
        region_name = region_name.lower()
        
        if region_name not in self.data:
            print(f"⚠️  Region '{region_name}' not found!")
            return []
        
        years = list(self.data[region_name].keys())
        print(f"\n📅 Years available for {region_name}: {', '.join(years)}")
        return years
    
    def remove_region(self, region_name):
        """Remove a region"""
        region_name = region_name.lower()
        
        if region_name not in self.data:
            print(f"⚠️  Region '{region_name}' not found!")
            return False
        
        del self.data[region_name]
        self._save_config()
        print(f"✅ Region '{region_name}' removed successfully!")
        return True
    
    def remove_year(self, region_name, year):
        """Remove a specific year from a region"""
        region_name = region_name.lower()
        year_str = str(year)
        
        if region_name not in self.data:
            print(f"⚠️  Region '{region_name}' not found!")
            return False
        
        if year_str not in self.data[region_name]:
            print(f"⚠️  Year {year} not found in {region_name}!")
            return False
        
        del self.data[region_name][year_str]
        self._save_config()
        print(f"✅ Year {year} removed from {region_name}!")
        return True


def interactive_mode():
    """Interactive command-line interface"""
    updater = HolidayUpdater()
    
    print("=" * 60)
    print("🗓️  HOLIDAY CONFIGURATION MANAGER")
    print("=" * 60)
    
    while True:
        print("\n📋 Menu:")
        print("  1. List all regions")
        print("  2. Add new region")
        print("  3. Add year to region")
        print("  4. Remove region")
        print("  5. Remove year from region")
        print("  6. Quick add common German holidays")
        print("  0. Exit")
        
        choice = input("\n➤ Choose an option: ").strip()
        
        if choice == "1":
            updater.list_regions()
        
        elif choice == "2":
            region = input("Enter region name (e.g., bavaria, hamburg): ").strip()
            updater.add_region(region)
        
        elif choice == "3":
            region = input("Enter region name: ").strip()
            year = input("Enter year (e.g., 2026): ").strip()
            
            print("\nEnter holidays (format: YYYY-MM-DD | Holiday Name)")
            print("Type 'done' when finished, or 'template' for common German holidays")
            
            holidays = []
            while True:
                entry = input("  ➤ ").strip()
                
                if entry.lower() == 'done':
                    break
                
                if entry.lower() == 'template':
                    holidays = get_german_template(int(year))
                    print(f"✅ Added {len(holidays)} common German holidays")
                    break
                
                try:
                    date_part, name_part = entry.split("|")
                    date_str = date_part.strip()
                    name = name_part.strip()
                    
                    # Validate date format
                    datetime.strptime(date_str, "%Y-%m-%d")
                    
                    holidays.append({"date": date_str, "name": name})
                    print(f"    ✓ Added: {name} on {date_str}")
                except ValueError:
                    print("    ✗ Invalid format! Use: YYYY-MM-DD | Holiday Name")
            
            if holidays:
                updater.add_year(region, int(year), holidays)
        
        elif choice == "4":
            region = input("Enter region name to remove: ").strip()
            confirm = input(f"⚠️  Are you sure you want to remove '{region}'? (yes/no): ")
            if confirm.lower() == 'yes':
                updater.remove_region(region)
        
        elif choice == "5":
            region = input("Enter region name: ").strip()
            year = input("Enter year to remove: ").strip()
            updater.remove_year(region, int(year))
        
        elif choice == "6":
            region = input("Enter region name: ").strip()
            year = input("Enter year: ").strip()
            holidays = get_german_template(int(year))
            updater.add_year(region, int(year), holidays)
        
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option!")


def get_german_template(year):
    """
    Get template for common German holidays
    Note: This is a simplified version. Easter-dependent dates need calculation.
    """
    return [
        {"date": f"{year}-01-01", "name": "New Year's Day"},
        {"date": f"{year}-05-01", "name": "Labour Day"},
        {"date": f"{year}-10-03", "name": "German Unity Day"},
        {"date": f"{year}-12-25", "name": "Christmas Day"},
        {"date": f"{year}-12-26", "name": "Second Christmas Day"}
    ]


def quick_add_example():
    """Example of programmatic usage"""
    updater = HolidayUpdater()
    
    # Add Bavaria region with 2026 holidays
    bavaria_2026 = [
        {"date": "2026-01-01", "name": "New Year's Day"},
        {"date": "2026-01-06", "name": "Epiphany"},
        {"date": "2026-04-03", "name": "Good Friday"},
        {"date": "2026-04-06", "name": "Easter Monday"},
        {"date": "2026-05-01", "name": "Labour Day"},
        {"date": "2026-05-14", "name": "Ascension Day"},
        {"date": "2026-05-25", "name": "Whit Monday"},
        {"date": "2026-06-04", "name": "Corpus Christi"},
        {"date": "2026-08-15", "name": "Assumption Day"},
        {"date": "2026-10-03", "name": "German Unity Day"},
        {"date": "2026-11-01", "name": "All Saints' Day"},
        {"date": "2026-12-25", "name": "Christmas Day"},
        {"date": "2026-12-26", "name": "Second Christmas Day"}
    ]
    
    updater.add_year("bavaria", 2026, bavaria_2026)
    
    # Add Hamburg region with 2026 holidays
    hamburg_2026 = [
        {"date": "2026-01-01", "name": "New Year's Day"},
        {"date": "2026-04-03", "name": "Good Friday"},
        {"date": "2026-04-06", "name": "Easter Monday"},
        {"date": "2026-05-01", "name": "Labour Day"},
        {"date": "2026-05-14", "name": "Ascension Day"},
        {"date": "2026-05-25", "name": "Whit Monday"},
        {"date": "2026-10-03", "name": "German Unity Day"},
        {"date": "2026-10-31", "name": "Reformation Day"},
        {"date": "2026-12-25", "name": "Christmas Day"},
        {"date": "2026-12-26", "name": "Second Christmas Day"}
    ]
    
    updater.add_year("hamburg", 2026, hamburg_2026)
    
    updater.list_regions()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        print("Running example: Adding Bavaria and Hamburg for 2026...")
        quick_add_example()
    else:
        interactive_mode()