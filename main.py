"""
Holiday Planner Application
Entry point for the vacation planner
Author: Maëlys Flohimont, 2025
"""
import tkinter as tk
from tkinter import ttk
from gui.holiday_planner import HolidayPlanner

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure("Holiday.TButton", background="lightgreen")
    app = HolidayPlanner(root, total_holidays=30)
    root.mainloop()

if __name__ == "__main__":
    main()