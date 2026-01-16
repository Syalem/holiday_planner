Holiday Planner 🗓️
A modern vacation planning application with multi-region support and automatic public holiday management.

✨ Features
📅 Visual calendar for current and next year
🌍 Multi-region support with dropdown selector
🎯 Automatic public holiday blocking
💾 Auto-save vacation selections
📊 Real-time vacation day counter
🔄 Carryover days from previous year
🎨 Intuitive color-coded interface
📁 Project Structure
holiday_planner/
├── main.py                      # Application entry point
├── config/
│   └── holidays.json           # Public holidays configuration
├── data/
│   └── holidays_status.json    # User's saved vacation days (auto-generated)
├── gui/
│   ├── __init__.py
│   ├── holiday_planner.py      # Main application window
│   └── calendar_widget.py      # Calendar display widget
├── utils/
│   ├── __init__.py
│   ├── holiday_loader.py        # Loads public holidays from JSON
│   └── storage.py               # Handles user data persistence
└── scripts/
    └── update_holidays.py       # Holiday configuration manager
🚀 Quick Start
1. Run the Application
bash
python main.py

2. Select Your Region
Use the dropdown menu at the top to select your region (Berlin, Bavaria, Hamburg, etc.)

3. Plan Your Vacation
Click on working days to select vacation days
Selected days are highlighted in blue
Weekends and public holidays are automatically disabled
View remaining days in real-time
🛠️ Managing Holiday Configuration
Interactive CLI Tool
Run the holiday configuration manager:

bash
python scripts/update_holidays.py
This opens an interactive menu where you can:

List all regions
Add new regions
Add holidays for a year
Remove regions or years
Quick-add common German holidays
Quick Example Setup
Add example regions (Bavaria & Hamburg for 2026):

bash
python scripts/update_holidays.py example
Manual JSON Editing
Edit config/holidays.json directly:

json
{
  "berlin": {
    "2025": [
      {"date": "2025-01-01", "name": "New Year's Day"},
      {"date": "2025-03-08", "name": "International Women's Day"}
    ]
  },
  "bavaria": {
    "2025": [
      {"date": "2025-01-06", "name": "Epiphany"},
      {"date": "2025-08-15", "name": "Assumption Day"}
    ]
  }
}
📋 Adding a New Region
Method 1: Using the CLI Tool
bash
python scripts/update_holidays.py
# Select option 2 (Add new region)
# Enter region name
# Select option 3 (Add year to region)
# Enter holidays
Method 2: Programmatically
Create a Python script:

python
from scripts.update_holidays import HolidayUpdater

updater = HolidayUpdater()

# Add Saxony region with 2026 holidays
saxony_2026 = [
    {"date": "2026-01-01", "name": "New Year's Day"},
    {"date": "2026-04-03", "name": "Good Friday"},
    {"date": "2026-10-31", "name": "Reformation Day"},
    # ... more holidays
]

updater.add_year("saxony", 2026, saxony_2026)
🎯 Use Cases
Adding a New Year
When a new year approaches:

bash
python scripts/update_holidays.py
# Option 3: Add year to region
# Enter region: berlin
# Enter year: 2027
# Enter holidays or type 'template' for common German holidays
Adding Multiple Regions at Once
Create a setup script:

python
from scripts.update_holidays import HolidayUpdater

updater = HolidayUpdater()

regions = {
    "saxony": [...],
    "thuringia": [...],
    "brandenburg": [...]
}

for region, holidays in regions.items():
    updater.add_year(region, 2026, holidays)
⚙️ Configuration
Change Default Region
In main.py:

python
app = HolidayPlanner(root, total_holidays=30, region="bavaria")
Change Total Holiday Days
python
app = HolidayPlanner(root, total_holidays=28)  # For 28 days
Change Storage Location
In utils/storage.py:

python
StorageManager(storage_file="data/my_custom_file.json")
📊 Data Files
holidays.json (Configuration)
Contains public holidays by region and year
Manually managed or updated via CLI tool
Version controlled in your repository
holidays_status.json (User Data)
Auto-generated when saving
Contains user's vacation selections
Should be in .gitignore
Automatically saves on window close
🎨 Color Scheme
Blue (#307CAF): Selected vacation days (current year)
Light Blue (#6EC6FF): Selected vacation days (next year)
Gray (disabled): Weekends and public holidays
White: Available working days
🔧 Customization
Add New Holiday Calculation
For regions with moveable holidays (Easter, Whit Monday, etc.), you can integrate a library like workalendar:

python
pip install workalendar

from workalendar.europe import Germany

# In update_holidays.py
def calculate_easter_holidays(year):
    cal = Germany()
    holidays = cal.holidays(year)
    return [{"date": date.strftime("%Y-%m-%d"), "name": name} 
            for date, name in holidays]
Custom Colors
In gui/calendar_widget.py, modify the button colors:

python
# For selected days
button.config(bg="#YOUR_COLOR_HERE")
🐛 Troubleshooting
"No holiday data available for [region] in [year]"
Solution: Add holidays for that year using the CLI tool or JSON editor.

Region dropdown is empty
Solution: Check that config/holidays.json exists and is valid JSON.

Changes not saving
Solution: Ensure the data/ directory is writable and you have proper permissions.

Public holidays not showing
Solution:

Verify the region name matches exactly (case-insensitive)
Check that the year exists in the configuration
Validate date format in JSON (YYYY-MM-DD)
📝 Tips
Backup Your Data: Regularly backup data/holidays_status.json
Plan Ahead: Add holidays for upcoming years in advance
Team Setup: Share config/holidays.json with your team via git
Carryover Days: Use the "previous year" field to track unused vacation days
Multiple Regions: Useful if you work across different German states
🤝 Contributing
To add support for more regions:

Research public holidays for the region
Use the CLI tool or create a script
Submit the updated holidays.json configuration
📜 License
Free to use and modify for personal or commercial projects.

👨‍💻 Author
Maëlys Flohimont, 2025

Need Help? Check the interactive CLI tool: python scripts/update_holidays.py

