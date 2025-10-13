"""Configuration reader utility for test framework."""
import yaml
import os
from typing import Dict, Any


class ConfigReader:
    """Read and manage configuration from YAML file."""
    
    def __init__(self, config_file: str = "config.yaml"):
        """Initialize config reader with config file path."""
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file {self.config_file} not found")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key with optional default."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_base_url(self) -> str:
        """Get base URL for the application."""
        return self.get('base_url', 'https://www.profitero.com')
    
    def get_api_base_url(self) -> str:
        """Get API base URL."""
        return self.get('api_base_url', 'https://api.profitero.com')
    
    def get_browser(self) -> str:
        """Get browser configuration."""
        return self.get('browser', 'chrome')
    
    def get_timeout(self) -> int:
        """Get timeout configuration."""
        return self.get('timeout', 30)
    
    def is_headless(self) -> bool:
        """Check if browser should run in headless mode."""
        return self.get('headless', False)
    
    def get_window_size(self) -> tuple:
        """Get window size as tuple."""
        size = self.get('window_size', '1920,1080')
        return tuple(map(int, size.split(',')))
    
    def get_test_data_path(self) -> str:
        """Get test data directory path."""
        return self.get('test_data_path', 'test_data/')
    
    def get_screenshots_path(self) -> str:
        """Get screenshots directory path."""
        return self.get('screenshots_path', 'reports/screenshots/')
    
    def get_reports_path(self) -> str:
        """Get reports directory path."""
        return self.get('reports_path', 'reports/')


# Global config instance
config = ConfigReader()