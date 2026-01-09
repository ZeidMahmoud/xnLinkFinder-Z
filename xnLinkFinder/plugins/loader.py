"""
Plugin loader for dynamically loading plugins from a directory.
"""

import os
import importlib.util
import sys
from typing import List, Dict, Optional, Type
from pathlib import Path

from .base import LinkFinderPlugin


class PluginLoader:
    """Loader for xnLinkFinder-Z plugins."""

    def __init__(self, plugin_dir: Optional[str] = None):
        """
        Initialize plugin loader.

        Args:
            plugin_dir: Directory containing plugins
        """
        self.plugin_dir = plugin_dir or self._get_default_plugin_dir()
        self.plugins: Dict[str, LinkFinderPlugin] = {}
        self.loaded_modules = []

    def _get_default_plugin_dir(self) -> str:
        """Get default plugin directory."""
        # Try user config directory first
        home = Path.home()
        config_dir = home / ".config" / "xnLinkFinder" / "plugins"
        
        if config_dir.exists():
            return str(config_dir)
        
        # Fall back to current directory
        return "./plugins"

    def load_plugins(self) -> List[LinkFinderPlugin]:
        """
        Load all plugins from plugin directory.

        Returns:
            List of loaded plugins
        """
        if not os.path.exists(self.plugin_dir):
            return []

        plugin_files = [
            f for f in os.listdir(self.plugin_dir)
            if f.endswith('.py') and not f.startswith('_')
        ]

        for plugin_file in plugin_files:
            try:
                self._load_plugin_file(plugin_file)
            except Exception as e:
                print(f"Failed to load plugin {plugin_file}: {e}")

        return list(self.plugins.values())

    def _load_plugin_file(self, filename: str):
        """
        Load a plugin from file.

        Args:
            filename: Plugin filename
        """
        filepath = os.path.join(self.plugin_dir, filename)
        module_name = filename[:-3]  # Remove .py extension

        # Load module
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            self.loaded_modules.append(module)

            # Find plugin classes in module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                # Check if it's a plugin class
                if (isinstance(attr, type) and 
                    issubclass(attr, LinkFinderPlugin) and 
                    attr is not LinkFinderPlugin):
                    
                    # Instantiate plugin
                    plugin = attr()
                    self.plugins[plugin.name] = plugin

    def get_plugin(self, name: str) -> Optional[LinkFinderPlugin]:
        """
        Get a plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance or None
        """
        return self.plugins.get(name)

    def get_all_plugins(self) -> List[LinkFinderPlugin]:
        """
        Get all loaded plugins.

        Returns:
            List of plugins
        """
        return list(self.plugins.values())

    def get_enabled_plugins(self) -> List[LinkFinderPlugin]:
        """
        Get enabled plugins.

        Returns:
            List of enabled plugins
        """
        return [p for p in self.plugins.values() if p.enabled]

    def enable_plugin(self, name: str):
        """
        Enable a plugin.

        Args:
            name: Plugin name
        """
        plugin = self.plugins.get(name)
        if plugin:
            plugin.enable()

    def disable_plugin(self, name: str):
        """
        Disable a plugin.

        Args:
            name: Plugin name
        """
        plugin = self.plugins.get(name)
        if plugin:
            plugin.disable()

    def process_with_plugins(self, data: any, plugin_type: Optional[Type] = None) -> any:
        """
        Process data through all enabled plugins.

        Args:
            data: Data to process
            plugin_type: Optional plugin type filter

        Returns:
            Processed data
        """
        result = data

        for plugin in self.get_enabled_plugins():
            # Filter by type if specified
            if plugin_type and not isinstance(plugin, plugin_type):
                continue

            # Check if plugin can process the data
            if plugin.can_process(result):
                result = plugin.process(result)

        return result

    def get_plugin_info(self) -> List[Dict[str, str]]:
        """
        Get information about all loaded plugins.

        Returns:
            List of plugin info dictionaries
        """
        return [plugin.get_info() for plugin in self.plugins.values()]


def load_plugins(plugin_dir: Optional[str] = None) -> PluginLoader:
    """
    Convenience function to create and load plugins.

    Args:
        plugin_dir: Plugin directory

    Returns:
        PluginLoader instance with loaded plugins
    """
    loader = PluginLoader(plugin_dir)
    loader.load_plugins()
    return loader
