#!/usr/bin/env python3
"""
Entry point for the Prime Visualizer application.
This script handles command line arguments and launches either the GUI or CLI version.
"""

import argparse
import sys

from prime_visualizer.config.config_manager import ConfigManager
from prime_visualizer.core.image_generator import generate_visualization


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Prime Number Visualization Tool")

    parser.add_argument("--cols", type=int, help="Number of columns in the grid")
    parser.add_argument("--rows", type=int, help="Number of rows in the grid")
    parser.add_argument("--dot-size", type=int, help="Size of each dot in pixels")
    parser.add_argument("--spacing", type=int, help="Spacing between dots in pixels")
    parser.add_argument("--output", help="Output image path")
    parser.add_argument("--config", help="Path to custom configuration file")
    parser.add_argument("--no-gui", action="store_true", help="Run in headless mode (no GUI)")

    return parser.parse_args()


def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_args()

    # Load configuration
    config_path = args.config if args.config else None
    config_manager = ConfigManager(config_path)
    config = config_manager.get_config()

    # Override config with command line arguments
    if args.cols:
        config["grid"]["columns"] = args.cols
    if args.rows:
        config["grid"]["rows"] = args.rows
    if args.dot_size:
        config["grid"]["dot_size"] = args.dot_size
    if args.spacing:
        config["grid"]["spacing"] = args.spacing

    # Determine output path
    output_path = args.output if args.output else config["application"]["default_output_file"]

    # Run in CLI mode if --no-gui is specified or if specific parameters are provided
    if args.no_gui or any([args.cols, args.rows, args.dot_size, args.spacing, args.output]):
        # Generate visualization directly
        print("Generating prime visualization...")

        stats = generate_visualization(
            columns=config["grid"]["columns"],
            rows=config["grid"]["rows"],
            dot_size=config["grid"]["dot_size"],
            spacing=config["grid"]["spacing"],
            colors=config["colors"],
            background_color=config["grid"]["background_color"],
            output_path=output_path
        )

        # Print statistics
        print(f"\nImage generated: {output_path}")
        print(f"Image dimensions: {stats['width']}x{stats['height']} pixels")
        print(f"Grid size: {stats['grid_columns']}x{stats['grid_rows']}")
        print(f"Total primes: {stats['total_primes']}")
        print(f"Prime density: {stats['density']:.2f}%")

        print("\nPrime distribution:")
        for prime_type, count in sorted(stats["prime_types"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {prime_type}: {count}")
    else:
        # Run in GUI mode
        try:
            from prime_visualizer.gui.app import PrimeVisualizerApp
            import tkinter as tk

            root = tk.Tk()
            app = PrimeVisualizerApp(root, config_manager)
            root.mainloop()
        except Exception as e:
            print(f"Error starting GUI: {e}")
            print("Falling back to CLI mode. Use --help to see available options.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
