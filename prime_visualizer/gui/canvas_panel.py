"""
Canvas panel component for the Prime Visualizer GUI.
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk


class CanvasPanel(ttk.Frame):
    """
    Canvas panel for the Prime Visualizer GUI.
    Displays the generated prime visualization.

    Attributes:
        parent (tk.Widget): The parent widget
        config (dict): The application configuration
    """

    def __init__(self, parent, config):
        """
        Initialize the canvas panel.

        Args:
            parent (tk.Widget): The parent widget
            config (dict): The application configuration
        """
        super().__init__(parent)
        self.parent = parent
        self.config = config

        # Initialize attributes
        self.image = None
        self.photo_image = None
        self.image_id = None
        self.zoom_level = 1.0

        # Create the panel
        self.create_panel()

    def create_panel(self):
        """Create the canvas panel widgets."""
        # Main wrapper frame
        self.main_frame = ttk.LabelFrame(self, text="Visualization")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create a canvas with scrollbars
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Add scrollbars
        self.h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
            bg="white"
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)

        # Add zoom controls
        self.zoom_frame = ttk.Frame(self.main_frame)
        self.zoom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        ttk.Label(self.zoom_frame, text="Zoom:").pack(side=tk.LEFT, padx=5)

        ttk.Button(self.zoom_frame, text="-", width=3,
                   command=lambda: self.zoom(0.8)).pack(side=tk.LEFT, padx=2)

        ttk.Button(self.zoom_frame, text="100%", width=6,
                   command=self.reset_zoom).pack(side=tk.LEFT, padx=2)

        ttk.Button(self.zoom_frame, text="+", width=3,
                   command=lambda: self.zoom(1.25)).pack(side=tk.LEFT, padx=2)

    def load_image(self, path):
        """
        Load and display an image on the canvas.

        Args:
            path (str): Path to the image file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open image and create PhotoImage
            self.image = Image.open(path)
            self.photo_image = ImageTk.PhotoImage(self.image)

            # Update canvas
            self.canvas.delete("all")
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

            # Configure scrollregion
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

            # Reset zoom level tracking
            self.zoom_level = 1.0

            return True

        except (IOError, OSError) as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
            logging.error("Error loading image: %s", e, exc_info=True)
            return False

    def zoom(self, factor):
        """
        Zoom the image by a factor.

        Args:
            factor (float): Zoom factor (e.g., 1.25 for 25% zoom in)
        """
        if self.image is None:
            return

        # Update zoom level
        self.zoom_level *= factor

        # Constrain zoom level within reasonable limits
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))

        # Resize the image
        new_width = int(self.image.width * self.zoom_level)
        new_height = int(self.image.height * self.zoom_level)

        # Remember scroll position
        x_view = self.canvas.xview()
        y_view = self.canvas.yview()

        # Create new resized image - different PIL versions use different constants
        try:
            # Try LANCZOS (newer Pillow versions)
            if hasattr(Image, "LANCZOS"):
                resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
            # Try ANTIALIAS (older Pillow versions)
            elif hasattr(Image, "ANTIALIAS"):
                resized_image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
            # Fallback to integer value 1 (should work in all versions)
            else:
                resized_image = self.image.resize((new_width, new_height), 1)
        except (AttributeError, TypeError):
            # If all else fails, use the default method
            resized_image = self.image.resize((new_width, new_height))

        self.photo_image = ImageTk.PhotoImage(resized_image)

        # Update canvas
        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        # Update scrollregion
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Restore scroll position (approximately)
        self.canvas.xview_moveto(x_view[0])
        self.canvas.yview_moveto(y_view[0])

    def reset_zoom(self):
        """Reset zoom to 100%."""
        if self.image is None:
            return

        # Calculate zoom factor to get back to 100%
        factor = 1.0 / self.zoom_level
        self.zoom(factor)
