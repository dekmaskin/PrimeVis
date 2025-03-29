"""
Helper utility functions for the Prime Visualizer.
"""

import os
import sys
import logging
import platform


def setup_logging(level=logging.INFO):
    """
    Set up logging configuration.

    Args:
        level: The logging level
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def initialize_environment():
    """
    Initialize the application environment.

    Returns:
        Dict: Environment information
    """
    # Create necessary directories
    try:
        # Get user home directory
        home_dir = os.path.expanduser("~")

        # Create application directory
        app_dir = os.path.join(home_dir, ".prime_visualizer")
        os.makedirs(app_dir, exist_ok=True)

        # Create output directory
        output_dir = os.path.join(app_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

    except Exception as e:
        logging.warning(f"Could not initialize environment directories: {e}")

    # Collect environment information
    env_info = {
        "os_name": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version,
        "app_directory": app_dir if "app_dir" in locals() else None,
        "output_directory": output_dir if "output_dir" in locals() else None,
    }

    return env_info


def ensure_directory_exists(path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        path: Path to the directory

    Returns:
        bool: True if the directory exists or was created, False otherwise
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Error creating directory {path}: {e}")
        return False


def get_output_path(filename=None):
    """
    Get a path in the output directory.

    Args:
        filename: Optional filename to append to the path

    Returns:
        str: Path in the output directory
    """
    # Get user home directory
    home_dir = os.path.expanduser("~")

    # Get output directory
    output_dir = os.path.join(home_dir, ".prime_visualizer", "output")

    # Ensure output directory exists
    ensure_directory_exists(output_dir)

    # Return path
    if filename:
        return os.path.join(output_dir, filename)
    else:
        return output_dir
