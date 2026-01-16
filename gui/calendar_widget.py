"""
Calendar widget for displaying and selecting vacation days
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class CalendarWidget:
    def __init__(self, parent_frame, year, holidays_set, public_holidays, toggle_callback, base_year=None):
        """
        Create a calendar widget
        
        Args:
            parent_frame: Parent tkinter frame
            year: Year to display
            holidays_set: Set of selected vacation days
            public_holidays: Set of public holidays
            toggle_callback: Function to call when a day is clicked
        """
        self.frame = parent_frame
        self.year = year
        self.holidays = holidays_set
        self.public_holidays = public_holidays
        self.toggle_callback = toggle_callback
        self.day_buttons = {}  # Store references to day buttons
        # Base year used for coloring/current-year logic (defaults to real current year)
        self.base_year = base_year if base_year is not None else datetime.now().year
        
    def create_calendar(self):
        """Create the full calendar display"""
        frame_width = 200
        frame_height = 210
        
        # Configure grid
        for i in range(3):
            self.frame.grid_rowconfigure(i+3, weight=1, minsize=frame_height)
        for j in range(4):
            self.frame.grid_columnconfigure(j, weight=1, minsize=frame_width)
        
        # Create 12 months in 4x3 grid
        for m_idx in range(12):
            month = m_idx + 1
            grid_row = m_idx // 4 + 3
            grid_col = m_idx % 4
            self._create_month(month, grid_row, grid_col, frame_width, frame_height)
    
    def _create_month(self, month, grid_row, grid_col, width, height):
        """Create a single month display"""
        month_frame = ttk.Frame(self.frame, borderwidth=1, relief="solid")
        month_frame.grid(row=grid_row, column=grid_col, padx=2, pady=2)
        month_frame.config(width=width, height=height)
        month_frame.grid_propagate(False)
        
        # Month name
        month_name = datetime(self.year, month, 1).strftime("%B")
        month_label = ttk.Label(
            month_frame, 
            text=month_name, 
            font=('Helvetica', 9, 'bold')
        )
        month_label.grid(row=0, column=0, columnspan=7, sticky=tk.W, padx=1, pady=1)
        
        month_frame.grid_columnconfigure(0, weight=1)
        month_frame.grid_columnconfigure(8, weight=1)
        
        # Day headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            label = ttk.Label(month_frame, text=day, font=('Helvetica', 7))
            label.grid(row=2, column=i+1, pady=1, sticky='n')
        
        # Calculate days in month
        if month == 12:
            days_in_month = 31
        else:
            days_in_month = (datetime(self.year, month + 1, 1) - timedelta(days=1)).day
        
        # Get first day of month (0=Monday, 6=Sunday)
        first_day = datetime(self.year, month, 1).weekday()
        
        # Create day buttons
        row = 3
        col = first_day + 1
        
        for day in range(1, days_in_month + 1):
            date = datetime(self.year, month, day)
            
            # Check if day is weekend or public holiday
            is_weekend = date.weekday() in [5, 6]  # Saturday, Sunday
            is_public_holiday = date in self.public_holidays
            
            if is_weekend or is_public_holiday:
                # Disabled button for non-working days
                day_btn = tk.Button(
                    month_frame, 
                    text=str(day), 
                    width=2, 
                    state=tk.DISABLED
                )
            else:
                # Clickable button for working days
                day_btn = tk.Button(
                    month_frame, 
                    text=str(day), 
                    width=2,
                    command=lambda d=date, b=None: self._on_day_click(d, b)
                )
                # Set the button reference properly
                day_btn.config(
                    command=lambda d=date, b=day_btn: self._on_day_click(d, b)
                )
                
                # Highlight if already selected
                if date in self.holidays:
                    color = "#307CAF" if self.year == self.base_year else "#6EC6FF"
                    day_btn.config(bg=color)
                
                # Store button reference
                self.day_buttons[date] = day_btn
            
            day_btn.grid(row=row, column=col, padx=1, pady=1, sticky='n')
            
            col += 1
            if col > 7:
                col = 1
                row += 1
    
    def _on_day_click(self, date, button):
        """Handle day button click"""
        self.toggle_callback(date, button)
    
    def update_button_color(self, date, is_selected):
        """Update the color of a specific day button"""
        if date in self.day_buttons:
            if is_selected:
                color = "#307CAF" if self.year == self.base_year else "#6EC6FF"
                self.day_buttons[date].config(bg=color)
            else:
                self.day_buttons[date].config(bg="SystemButtonFace")
    
    def clear(self):
        """Clear all day button references"""
        self.day_buttons.clear()