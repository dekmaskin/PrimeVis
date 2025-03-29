"""
Control panel component for the Prime Visualizer GUI.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Callable


class ControlPanel(ttk.Frame):
    """
    Control panel for the Prime Visualizer GUI.
    Contains settings controls and statistics display.

    Attributes:
        parent (tk.Widget): The parent widget
        config (Dict[str, Any]): The application configuration
        on_generate (Callable): Function to call when the generate button is clicked
    """

    def __init__(self, parent, config, on_generate):
        """
        Initialize the control panel.

        Args:
            parent (tk.Widget): The parent widget
            config (Dict[str, Any]): The application configuration
            on_generate (Callable): Function to call when the generate button is clicked
        """
        super().__init__(parent)
        self.parent = parent
        self.config = config
        self.on_generate = on_generate

        # Create the panel
        self.create_panel()

    def create_panel(self):
        """Create the control panel widgets."""
        # Main wrapper frame
        self.main_frame = ttk.LabelFrame(self, text="Controls")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Grid settings group
        self.grid_frame = ttk.LabelFrame(self.main_frame, text="Grid Settings")
        self.grid_frame.pack(fill=tk.X, padx=5, pady=5)

        # Columns
        ttk.Label(self.grid_frame, text="Columns:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cols_var = tk.IntVar(value=self.config["grid"]["columns"])
        self.cols_spinbox = ttk.Spinbox(
            self.grid_frame, from_=10, to=1000, textvariable=self.cols_var, width=5)
        self.cols_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # Rows
        ttk.Label(self.grid_frame, text="Rows:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.rows_var = tk.IntVar(value=self.config["grid"]["rows"])
        self.rows_spinbox = ttk.Spinbox(
            self.grid_frame, from_=10, to=1000, textvariable=self.rows_var, width=5)
        self.rows_spinbox.grid(row=1, column=1, padx=5, pady=5)

        # Dot size
        ttk.Label(self.grid_frame, text="Dot Size:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.dot_size_var = tk.IntVar(value=self.config["grid"]["dot_size"])
        self.dot_size_spinbox = ttk.Spinbox(
            self.grid_frame, from_=1, to=20, textvariable=self.dot_size_var, width=5)
        self.dot_size_spinbox.grid(row=2, column=1, padx=5, pady=5)

        # Spacing
        ttk.Label(self.grid_frame, text="Spacing:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.spacing_var = tk.IntVar(value=self.config["grid"]["spacing"])
        self.spacing_spinbox = ttk.Spinbox(
            self.grid_frame, from_=0, to=10, textvariable=self.spacing_var, width=5)
        self.spacing_spinbox.grid(row=3, column=1, padx=5, pady=5)

        # Action buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(self.button_frame, text="Generate", command=self.on_generate).pack(
            fill=tk.X, pady=5)

        # Statistics frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.stats_text = tk.Text(self.stats_frame, height=15, width=30, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def get_settings(self) -> Dict[str, Any]:
        """
        Get the current settings from the control panel.

        Returns:
            Dict[str, Any]: The current settings
        """
        return {
            "columns": self.cols_var.get(),
            "rows": self.rows_var.get(),
            "dot_size": self.dot_size_var.get(),
            "spacing": self.spacing_var.get()
        }

    def update_from_config(self, config):
        """
        Update the control panel with values from a configuration.

        Args:
            config (Dict[str, Any]): The configuration to use
        """
        self.config = config
        self.cols_var.set(config["grid"]["columns"])
        self.rows_var.set(config["grid"]["rows"])
        self.dot_size_var.set(config["grid"]["dot_size"])
        self.spacing_var.set(config["grid"]["spacing"])

    def update_statistics(self, stats):
        """
        Update the statistics display.

        Args:
            stats (Dict[str, Any]): Statistics to display
        """
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)

        self.stats_text.insert(tk.END, f"Image: {stats['width']}x{stats['height']} pixels\n")
        self.stats_text.insert(tk.END, f"Grid: {stats['grid_columns']}x{stats['grid_rows']}\n")
        self.stats_text.insert(tk.END, f"Total positions: {stats['total_positions']}\n")
        self.stats_text.insert(tk.END, f"Total primes: {stats['total_primes']}\n")
        self.stats_text.insert(tk.END, f"Prime density: {stats['density']:.2f}%\n\n")

        self.stats_text.insert(tk.END, "Prime types:\n")
        sorted_types = sorted(stats['prime_types'].items(),
                              key=lambda x: x[1], reverse=True)

        for prime_type, count in sorted_types:
            percentage = (count / stats['total_primes']) * 100
            self.stats_text.insert(tk.END, f"  {prime_type}: {count} ({percentage:.1f}%)\n")

        self.stats_text.config(state=tk.DISABLED)

    def set_ui_state(self, state):
        """
        Enable or disable UI elements.

        Args:
            state (str): The state to set (tk.NORMAL or tk.DISABLED)
        """
        widgets = [
            self.cols_spinbox,
            self.rows_spinbox,
            self.dot_size_spinbox,
            self.spacing_spinbox
        ]

        for widget in widgets:
            widget.config(state=state)
