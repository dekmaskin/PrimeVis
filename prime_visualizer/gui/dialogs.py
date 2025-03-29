"""
Dialog components for the Prime Visualizer GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any


def show_about(parent):
    """
    Show the about dialog.

    Args:
        parent: The parent window
    """
    messagebox.showinfo(
        "About Prime Visualizer",
        "Prime Number Visualizer\n\n"
        "A tool for visualizing the distribution and patterns of prime numbers "
        "in a grid, with color-coding for different types of primes.\n\n"
        "Version 1.0.0"
    )


def show_legend(parent, config):
    """
    Show the legend dialog for prime types and colors.

    Args:
        parent: The parent window
        config: The application configuration
    """
    legend_window = tk.Toplevel(parent)
    legend_window.title("Prime Types Legend")
    legend_window.geometry("500x600")
    legend_window.minsize(400, 400)

    # Make the window modal
    legend_window.transient(parent)
    legend_window.grab_set()

    # Add a scrollable frame
    main_frame = ttk.Frame(legend_window)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add title
    ttk.Label(
        scrollable_frame,
        text="Prime Types and Their Colors",
        font=("TkDefaultFont", 12, "bold")
    ).grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

    # Add headers
    ttk.Label(scrollable_frame, text="Color", font=("TkDefaultFont", 10, "bold")).grid(
        row=1, column=0, padx=5, pady=5, sticky="w")
    ttk.Label(scrollable_frame, text="Prime Type", font=("TkDefaultFont", 10, "bold")).grid(
        row=1, column=1, padx=5, pady=5, sticky="w")
    ttk.Label(scrollable_frame, text="Description", font=("TkDefaultFont", 10, "bold")).grid(
        row=1, column=2, padx=5, pady=5, sticky="w")

    # Prime types info
    prime_types_info = [
        {"type": "regular_prime", "desc": "Standard prime numbers"},
        {"type": "twin_prime", "desc": "Primes that differ by 2 (e.g., 3 and 5)"},
        {"type": "mersenne_prime", "desc": "Primes of form 2^p-1"},
        {"type": "safe_prime", "desc": "Primes p where (p-1)/2 is also prime"},
        {"type": "palindromic_prime", "desc": "Primes that read the same backward"},
        {"type": "circular_prime", "desc": "All rotations of digits are prime"},
        {"type": "sophie_germain_prime", "desc": "Primes p where 2p+1 is also prime"},
        {"type": "factorial_prime", "desc": "Primes of form n!±1"},
        {"type": "fibonacci_prime", "desc": "Primes that are also Fibonacci numbers"},
        {"type": "sexy_prime", "desc": "Primes that differ by 6"},
        {"type": "cuban_prime", "desc": "Primes of form (3m²+3m+1)"},
        {"type": "happy_prime", "desc": "Primes that are also happy numbers"},
        {"type": "chen_prime", "desc": "Primes p where p+2 is prime or semiprime"},
        {"type": "wieferich_prime", "desc": "Primes p where 2^(p-1)≡1 (mod p²)"},
        {"type": "isolated_prime", "desc": "Primes with no primes at distance 2"}
    ]

    # Add rows
    for i, info in enumerate(prime_types_info):
        # Color swatch
        color_rgb = config["colors"].get(info["type"], [0, 0, 0])
        color_hex = "#{:02x}{:02x}{:02x}".format(*color_rgb)

        color_frame = ttk.Frame(scrollable_frame, width=30, height=20)
        color_frame.grid(row=i+2, column=0, padx=5, pady=5)
        color_swatch = tk.Canvas(color_frame, width=30, height=20, bg=color_hex,
                                 highlightthickness=1)
        color_swatch.pack()

        # Type name
        type_label = ttk.Label(
            scrollable_frame,
            text=info["type"].replace("_", " ").title()
        )
        type_label.grid(row=i+2, column=1, padx=5, pady=5, sticky="w")

        # Description
        desc_label = ttk.Label(
            scrollable_frame,
            text=info["desc"],
            wraplength=250
        )
        desc_label.grid(row=i+2, column=2, padx=5, pady=5, sticky="w")

    # Add close button
    close_button = ttk.Button(legend_window, text="Close", command=legend_window.destroy)
    close_button.pack(pady=10)

    # Make window resizable
    legend_window.resizable(True, True)

    # Center the window on the parent
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (500 // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (600 // 2)
    legend_window.geometry(f"+{x}+{y}")

    # Wait until the window is closed
    parent.wait_window(legend_window)


def show_error(parent, message):
    """
    Show an error dialog.

    Args:
        parent: The parent window
        message: The error message
    """
    messagebox.showerror("Error", message)
