"""
Main application class for the Prime Visualizer GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
import sys

from prime_visualizer.config.config_manager import ConfigManager
from prime_visualizer.gui.control_panel import ControlPanel
from prime_visualizer.gui.canvas_panel import CanvasPanel
from prime_visualizer.gui.dialogs import show_about, show_legend


class PrimeVisualizerApp:
    """
    Main application class for the Prime Visualizer GUI.

    Attributes:
        root (tk.Tk): The tkinter root window
        config_manager (ConfigManager): The configuration manager
    """

    def __init__(self, root, config_manager):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The tkinter root window
            config_manager (ConfigManager): The configuration manager
        """
        self.root = root
        self.config_manager = config_manager
        self.config = config_manager.get_config()

        # Configure the main window
        self.root.title("Prime Number Visualizer")
        self.root.geometry("1200x800")
        self.root.minsize(900, 700)

        # Set macOS specific settings if on macOS
        if sys.platform == "darwin":
            self.root.tk.call('::tk::unsupported::MacWindowStyle', 'style',
                              self.root._w, 'document', 'closeBox')

        # Create menus
        self.create_menu()

        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create control panel (left side)
        self.control_panel = ControlPanel(
            parent=self.main_frame,
            config=self.config,
            on_generate=self.on_generate_clicked
        )
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Create canvas panel (right side)
        self.canvas_panel = CanvasPanel(
            parent=self.main_frame,
            config=self.config
        )
        self.canvas_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Default image path
        self.image_path = self.config["application"]["default_output_file"]

        # Bind events
        self.root.bind("<Configure>", self.on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Load existing image if available
        if os.path.exists(self.image_path):
            self.canvas_panel.load_image(self.image_path)
            self.status_var.set(f"Loaded existing image: {self.image_path}")

    def create_menu(self):
        """Create the application menu."""
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Generate Image", command=self.on_generate_clicked)
        file_menu.add_command(label="Save Image As...", command=self.on_save_clicked)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)

        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Reset to Defaults", command=self.on_reset_clicked)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.on_about_clicked)
        help_menu.add_command(label="Prime Types Legend", command=self.on_legend_clicked)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def on_generate_clicked(self):
        """Handle generate button click."""
        # Update config with current control panel values
        settings = self.control_panel.get_settings()
        for key, value in settings.items():
            if key in self.config["grid"]:
                self.config["grid"][key] = value

        # Set status
        self.status_var.set("Generating prime visualization...")
        self.root.update_idletasks()

        try:
            # Disable controls during generation
            self.control_panel.set_ui_state(tk.DISABLED)

            # Import here to avoid circular imports
            from prime_visualizer.core.image_generator import generate_visualization

            # Generate visualization
            stats = generate_visualization(
                columns=self.config["grid"]["columns"],
                rows=self.config["grid"]["rows"],
                dot_size=self.config["grid"]["dot_size"],
                spacing=self.config["grid"]["spacing"],
                colors=self.config["colors"],
                background_color=self.config["grid"]["background_color"],
                output_path=self.image_path
            )

            # Load the generated image
            self.canvas_panel.load_image(self.image_path)

            # Update statistics
            self.control_panel.update_statistics(stats)

            # Update status
            self.status_var.set(f"Image generated: {stats['width']}x{stats['height']} pixels")

        except Exception as e:
            messagebox.showerror("Error", f"Error generating image: {str(e)}")
            self.status_var.set("Error generating image")
            logging.error(f"Error generating image: {e}", exc_info=True)
        finally:
            # Re-enable controls
            self.control_panel.set_ui_state(tk.NORMAL)

    def on_save_clicked(self):
        """Handle save button click."""
        from tkinter import filedialog

        if not os.path.exists(self.image_path):
            messagebox.showerror("Error", "No image has been generated yet.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if file_path:
            try:
                from PIL import Image
                # If the selected path is different from the current image, copy it
                if file_path != self.image_path:
                    img = Image.open(self.image_path)
                    img.save(file_path)
                self.status_var.set(f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving image: {str(e)}")
                self.status_var.set("Error saving image")

    def on_reset_clicked(self):
        """Handle reset button click."""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to defaults?"):
            # Load the default configuration
            self.config_manager = ConfigManager(None)  # Reset to default config
            self.config = self.config_manager.get_config()

            # Update control panel
            self.control_panel.update_from_config(self.config)

            self.status_var.set("Settings reset to defaults")

    def on_about_clicked(self):
        """Handle about menu item click."""
        show_about(self.root)

    def on_legend_clicked(self):
        """Handle legend menu item click."""
        show_legend(self.root, self.config)

    def on_resize(self, event):
        """Handle window resize event."""
        # Only process events from the main window
        if event.widget == self.root:
            pass  # Add any resize handling here if needed

    def on_close(self):
        """Handle window close event."""
        # Save config if configured to do so
        if self.config["application"]["save_config_on_exit"]:
            self.config_manager.save_config(self.config)

        # Close window
        self.root.destroy()
