"""
Main Holiday Planner GUI
Manages the application window and user interactions for vacation planning.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Set, Dict, Optional, Tuple
from utils.holiday_loader import HolidayLoader
from utils.storage import StorageManager
from gui.calendar_widget import CalendarWidget

# Constants
MAX_HOLIDAYS = 30
DEFAULT_REGION = "berlin"
CURRENT_YEAR = datetime.now().year

class HolidayPlanner:
    """
    Main class for the Holiday Planner application.
    Manages the GUI, user interactions, and vacation day calculations.
    """

    def __init__(self, root: tk.Tk, total_holidays: int = MAX_HOLIDAYS, region: str = DEFAULT_REGION) -> None:
        """
        Initialize the HolidayPlanner application.

        Args:
            root (tk.Tk): The root Tkinter window.
            total_holidays (int): Total vacation days available per year.
            region (str): Default region for public holidays.
        """
        self.root = root
        self.total_holidays = total_holidays
        self.initial_region = region
        self.year = CURRENT_YEAR

        # String variables for GUI components
        self.year_var = tk.StringVar(value=str(self.year))
        self.region_var = tk.StringVar(value=region)
        self.previous_year_var = tk.IntVar(value=0)

        # Initialize managers
        self.holiday_loader = HolidayLoader()
        self.storage_manager = StorageManager()

        # Initialize data
        self.holidays1: Set[datetime] = set()  # Current year
        self.holidays2: Set[datetime] = set()  # Next year (kept for data consistency)
        self.taken_holidays1: int = 0
        self.taken_holidays2: int = 0  # Kept for data consistency

        # Load saved data
        self.load_holidays()

        # Setup window
        self.root.title("Vacation Planner")
        self.root.geometry("940x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create GUI
        self.create_widgets()
        self.update_labels()

    def create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Top control bar with region and year selectors
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Region selector
        ttk.Label(control_frame, text="Region:", font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
        regions = self.holiday_loader.get_available_regions()
        if not regions:
            regions = [DEFAULT_REGION]

        self.region_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.region_var,
            values=regions,
            state="readonly",
            width=15
        )
        self.region_dropdown.pack(side=tk.LEFT, padx=5)
        self.region_dropdown.bind("<<ComboboxSelected>>", self.on_region_change)

        # Year selector
        years = sorted(self.holiday_loader.get_available_years(self.region_var.get()))
        if not years:
            years = [CURRENT_YEAR]
        year_values = [str(y) for y in years]

        ttk.Label(control_frame, text="Year:", font=('Helvetica', 10)).pack(side=tk.LEFT, padx=5)
        self.year_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.year_var,
            values=year_values,
            state="readonly",
            width=6
        )
        self.year_dropdown.pack(side=tk.LEFT, padx=5)
        self.year_dropdown.bind("<<ComboboxSelected>>", self.on_year_change)

        # Main area for year frames with vertical scrollbar
        self.years_container = ttk.Frame(self.root)
        self.years_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Canvas + scrollbar for vertical scrolling
        self.years_canvas = tk.Canvas(self.years_container, borderwidth=0, highlightthickness=0)
        self.years_vscroll = ttk.Scrollbar(self.years_container, orient=tk.VERTICAL, command=self.years_canvas.yview)
        self.years_canvas.configure(yscrollcommand=self.years_vscroll.set)

        self.years_vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.years_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Inner frame inside the canvas
        self.years_inner = ttk.Frame(self.years_canvas)
        self.years_canvas.create_window((0, 0), window=self.years_inner, anchor='nw')

        # Update scroll region when inner frame changes
        def _on_inner_configure(event):
            self.years_canvas.configure(scrollregion=self.years_canvas.bbox('all'))

        self.years_inner.bind('<Configure>', _on_inner_configure)

        # Allow mousewheel scrolling
        def _on_mousewheel(event):
            self.years_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        self.years_canvas.bind_all('<MouseWheel>', _on_mousewheel)

        # Create a single frame for the selected year
        base_year = int(self.year_var.get())
        self.tab1 = ttk.Frame(self.years_inner)
        self.tab1.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create calendar for the selected year only
        self._create_year_tab(self.tab1, base_year, is_current_year=True)

    def _create_year_tab(self, tab: ttk.Frame, year: int, is_current_year: bool) -> None:
        """
        Create a tab with calendar and controls for a specific year.

        Args:
            tab (ttk.Frame): The frame to hold the calendar.
            year (int): The year to display.
            is_current_year (bool): Whether this tab is for the current year.
        """
        calendar_frame = ttk.Frame(tab)
        calendar_frame.pack(fill=tk.BOTH, expand=False, anchor='center')

        # Year label
        year_label = ttk.Label(calendar_frame, text=str(year), font=('Helvetica', 16))
        year_label.grid(row=0, column=0, columnspan=5, pady=10, sticky='n')

        # Info bar
        info_bar = ttk.Frame(calendar_frame)
        info_bar.grid(row=2, column=0, columnspan=5, pady=2, sticky='n')

        # Left side: Previous year carryover
        left_frame = ttk.Frame(calendar_frame)
        left_frame.grid(row=2, column=1, pady=2, sticky='e')

        prev_year_label = ttk.Label(left_frame, text="Previous Year:")
        prev_year_label.pack(side=tk.LEFT, padx=5)

        prev_year_entry = ttk.Entry(left_frame, width=4, textvariable=self.previous_year_var)
        prev_year_entry.pack(side=tk.LEFT, padx=5)

        prev_year_ok = ttk.Button(left_frame, text="OK", width=3, command=self.update_labels)
        prev_year_ok.pack(side=tk.LEFT, padx=5)

        # Days remaining label
        remaining_days = self._calculate_remaining_days(1)
        remaining_label = ttk.Label(left_frame, text=f"Days left: {remaining_days}")
        remaining_label.pack(side=tk.LEFT, padx=5)

        # Right side: Taken days and buttons
        right_frame = ttk.Frame(calendar_frame)
        right_frame.grid(row=2, column=2, pady=2, sticky='w')

        taken_label = ttk.Label(right_frame, text=f"Booked days: {self.taken_holidays1}")
        taken_label.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(right_frame, text="Reset", width=5, command=lambda: self.reset_holidays(1))
        reset_btn.pack(side=tk.LEFT, padx=5)

        save_btn = ttk.Button(right_frame, text="Save Holidays", command=self.save_holidays)
        save_btn.pack(side=tk.LEFT, padx=5)

        # Store references
        self.calendar_frame1 = calendar_frame
        self.remaining_label1 = remaining_label
        self.taken_label1 = taken_label

        # Create calendar
        self.create_calendar_for_frame(calendar_frame, year)

    def create_calendar_for_frame(self, frame: ttk.Frame, year: int) -> None:
        """
        Create a calendar widget for a specific year.

        Args:
            frame (ttk.Frame): The frame to hold the calendar.
            year (int): The year to display.
        """
        region = self.region_var.get()
        public_holidays = self.holiday_loader.get_holidays_for_year(year, region)

        available_years = self.holiday_loader.get_available_years(region)
        if year not in available_years:
            warning_label = ttk.Label(frame, text=f"⚠️ No holiday data for {region} in {year}", font=('Helvetica', 10), foreground="orange")
            warning_label.grid(row=3, column=0, columnspan=5, pady=20)

        holidays_set = self.holidays1
        calendar = CalendarWidget(frame, year, holidays_set, public_holidays, self.toggle_holiday, base_year=year)
        calendar.create_calendar()
        self.calendar1 = calendar

    def on_region_change(self, event: Optional[tk.Event] = None) -> None:
        """
        Handle region change from the dropdown.
        Prompts the user to save current holidays before changing the region.
        """
        new_region = self.region_var.get()

        if self.holidays1 or self.holidays2:
            response = messagebox.askyesnocancel(
                "Region Change",
                "Save current holidays before changing region?\n\nYes: Save and change\nNo: Change without saving\nCancel: Do not change"
            )

            if response is None:
                self.region_var.set(self.initial_region)
                return
            elif response:
                self.save_holidays()

        self.initial_region = new_region
        years = sorted(self.holiday_loader.get_available_years(new_region))
        if not years:
            years = [CURRENT_YEAR]
        year_values = [str(y) for y in years]
        self.year_dropdown['values'] = year_values

        if int(self.year_var.get()) not in years:
            self.year_var.set(str(years[0]))

        self.rebuild_tabs()
        #messagebox.showinfo("Region Changed", f"Region changed to: {new_region.upper()}")

    def on_year_change(self, event: Optional[tk.Event] = None) -> None:
        """Handle year selection change."""
        self.rebuild_tabs()

    def rebuild_tabs(self) -> None:
        """Recreate the tab and calendar for the selected year."""
        base_year = int(self.year_var.get())

        if hasattr(self, 'tab1'):
            self.tab1.destroy()

        self.tab1 = ttk.Frame(self.years_inner)
        self.tab1.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self._create_year_tab(self.tab1, base_year, is_current_year=True)

    def toggle_holiday(self, date: datetime, button: ttk.Button) -> None:
        """
        Toggle a vacation day on/off.

        Args:
            date (datetime): The date to toggle.
            button (ttk.Button): The button representing the date.
        """
        current_year = int(self.year_var.get())

        if date.year == current_year:
            if date in self.holidays1:
                self.holidays1.remove(date)
                self.taken_holidays1 -= 1
                if isinstance(button, tk.Button):
                    button.config(bg="SystemButtonFace")
                else:
                    try:
                        button.config(style="TButton")
                    except tk.TclError:
                        pass
            else:
                max_days = self.total_holidays + self.previous_year_var.get()
                if self.taken_holidays1 >= max_days:
                    messagebox.showwarning("Warning", "No more vacation days left for this year!")
                    return
                self.holidays1.add(date)
                self.taken_holidays1 += 1
                if isinstance(button, tk.Button):
                    button.config(bg="#307CAF")
                else:
                    try:
                        button.config(style="Selected.TButton")
                    except tk.TclError:
                        pass

        self.update_labels()

    def _calculate_remaining_days(self, year_idx: int) -> int:
        """
        Calculate remaining vacation days for a given year.

        Args:
            year_idx (int): 1 for current year.

        Returns:
            int: Remaining vacation days.
        """
        return self.total_holidays + self.previous_year_var.get() - self.taken_holidays1

    def update_labels(self) -> None:
        """Update all label displays."""
        remaining = self._calculate_remaining_days(1)
        self.remaining_label1.config(text=f"Days left: {remaining}")
        self.taken_label1.config(text=f"Booked days: {self.taken_holidays1}")

    def reset_holidays(self, year_idx: int) -> None:
        """
        Reset selected holidays for the current year.

        Args:
            year_idx (int): 1 for current year.
        """
        if not messagebox.askyesno("Confirm Reset", "Reset all holidays for current year?"):
            return

        self.holidays1.clear()
        self.taken_holidays1 = 0

        self.update_labels()
        self.create_calendar_for_frame(self.calendar_frame1, int(self.year_var.get()))

    def save_holidays(self) -> None:
        """Save current holiday selections."""
        try:
            success = self.storage_manager.save_holidays(
                self.holidays1,
                self.holidays2,
                self.previous_year_var.get(),
                self.region_var.get()
            )
            # silent save — do not show popups
            pass
        except Exception:
            # suppress error popups
            pass

    def load_holidays(self) -> None:
        """Load saved holiday selections."""
        holidays1, holidays2, prev_year, saved_region = self.storage_manager.load_holidays()
        self.holidays1 = holidays1
        self.holidays2 = holidays2
        self.taken_holidays1 = len(self.holidays1)
        self.taken_holidays2 = len(self.holidays2)
        self.previous_year_var.set(prev_year)

        if saved_region:
            self.region_var.set(saved_region)
            self.initial_region = saved_region

    def on_close(self) -> None:
        """Handle window close event."""
        self.save_holidays()
        self.root.destroy()
