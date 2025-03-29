"""
Configuration management for the Prime Visualizer.
"""

import os
import yaml
import logging
import pkg_resources

class ConfigManager:
    """
    Manages loading, saving, and accessing configuration settings.

    Attributes:
        config_path (str): Path to the configuration file
        config (dict): The loaded configuration
    """

    def __init__(self, config_path=None):
        """
        Initialize the configuration manager.

        Args:
            config_path (str, optional): Path to a custom configuration file.
                If None, the default configuration will be used.
        """
        self.logger = logging.getLogger(__name__)

        # If no custom path is provided, use the default
        if config_path is None:
            # Try different locations for the config file
            possible_locations = [
                # Within the package (original location)
                pkg_resources.resource_filename("prime_visualizer", "config.yaml"),
                # In the root directory (where start.py is)
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "config.yaml"),
                # Current working directory
                os.path.join(os.getcwd(), "config.yaml")
            ]

            # Use the first location that exists
            for location in possible_locations:
                if os.path.exists(location):
                    self.config_path = location
                    break
            else:
                # If none exist, use the root directory path anyway (it will create default config)
                self.config_path = possible_locations[1]
        else:
            self.config_path = config_path

        self.logger.debug(f"Using configuration file: {self.config_path}")

        # Load the configuration
        self.config = self._load_config()

    def _load_config(self):
        """
        Load configuration from the YAML file.

        Returns:
            dict: The loaded configuration dictionary
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                self.logger.warning(f"Configuration file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return self._get_default_config()

    def _get_default_config(self):
        """
        Get the default configuration.

        Returns:
            dict: Default configuration dictionary
        """
        return {
            "grid": {
                "columns": 100,
                "rows": 100,
                "dot_size": 8,
                "spacing": 2,
                "background_color": [255, 255, 255]
            },
            "colors": {
                "regular_prime": [0, 0, 0],
                "twin_prime": [255, 0, 0],
                "mersenne_prime": [0, 255, 0],
                "safe_prime": [0, 0, 255]
            },
            "application": {
                "default_output_file": "prime_visualization.png",
                "enable_statistics": True,
                "save_config_on_exit": True
            }
        }

    def get_config(self):
        """
        Get the current configuration.

        Returns:
            dict: The current configuration dictionary
        """
        return self.config

    def save_config(self, config=None):
        """
        Save the configuration to the YAML file.

        Args:
            config (dict, optional): Configuration to save. If None, save the current configuration.

        Returns:
            bool: True if successful, False otherwise
        """
        if config is not None:
            self.config = config

        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            self.logger.debug(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False

    def update_config(self, updates):
        """
        Update specific configuration values.

        Args:
            updates (dict): Dictionary with updates to apply to the configuration

        Returns:
            dict: The updated configuration
        """
        def _update_dict(target, source):
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    _update_dict(target[key], value)
                else:
                    target[key] = value

        _update_dict(self.config, updates)
        return self.config
