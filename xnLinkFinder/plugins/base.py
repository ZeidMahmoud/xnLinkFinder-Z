"""
Base plugin class for extending xnLinkFinder-Z functionality.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class LinkFinderPlugin(ABC):
    """
    Base class for xnLinkFinder-Z plugins.
    
    Plugins can extend functionality by:
    - Adding custom parsers for new file types
    - Implementing specialized link extraction
    - Adding post-processing logic
    - Integrating with external tools
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize plugin.

        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.enabled = True

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process data through the plugin.

        Args:
            data: Input data

        Returns:
            Processed data
        """
        pass

    def can_process(self, data: Any) -> bool:
        """
        Check if plugin can process the given data.

        Args:
            data: Input data

        Returns:
            True if plugin can process the data
        """
        return True

    def get_info(self) -> Dict[str, str]:
        """
        Get plugin information.

        Returns:
            Dictionary with plugin info
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "description": self.__doc__ or "",
        }

    def enable(self):
        """Enable the plugin."""
        self.enabled = True

    def disable(self):
        """Disable the plugin."""
        self.enabled = False


class LinkParserPlugin(LinkFinderPlugin):
    """Base class for link parser plugins."""

    @abstractmethod
    def extract_links(self, content: str, source: Optional[str] = None) -> List[str]:
        """
        Extract links from content.

        Args:
            content: Content to parse
            source: Source identifier

        Returns:
            List of extracted links
        """
        pass

    def process(self, data: Any) -> List[str]:
        """
        Process content and extract links.

        Args:
            data: Content to process

        Returns:
            List of links
        """
        if isinstance(data, dict):
            content = data.get("content", "")
            source = data.get("source")
        else:
            content = str(data)
            source = None

        return self.extract_links(content, source)


class PostProcessorPlugin(LinkFinderPlugin):
    """Base class for post-processor plugins."""

    @abstractmethod
    def post_process(self, links: List[str]) -> List[str]:
        """
        Post-process discovered links.

        Args:
            links: List of links

        Returns:
            Processed links
        """
        pass

    def process(self, data: Any) -> Any:
        """
        Process links.

        Args:
            data: Links to process

        Returns:
            Processed links
        """
        if isinstance(data, list):
            return self.post_process(data)
        return data


class FilterPlugin(LinkFinderPlugin):
    """Base class for filter plugins."""

    @abstractmethod
    def filter_links(self, links: List[str]) -> List[str]:
        """
        Filter links based on custom criteria.

        Args:
            links: List of links

        Returns:
            Filtered links
        """
        pass

    def process(self, data: Any) -> Any:
        """
        Filter links.

        Args:
            data: Links to filter

        Returns:
            Filtered links
        """
        if isinstance(data, list):
            return self.filter_links(data)
        return data


class ExampleCustomParserPlugin(LinkParserPlugin):
    """Example custom parser plugin."""

    def __init__(self):
        """Initialize example parser."""
        super().__init__("ExampleParser", "1.0.0")

    def extract_links(self, content: str, source: Optional[str] = None) -> List[str]:
        """
        Extract links using custom logic.

        Args:
            content: Content to parse
            source: Source identifier

        Returns:
            List of links
        """
        # Example: Extract custom patterns
        import re
        
        links = []
        
        # Custom pattern example
        custom_pattern = r'customLink\("([^"]+)"\)'
        matches = re.findall(custom_pattern, content)
        links.extend(matches)
        
        return links


class ExampleFilterPlugin(FilterPlugin):
    """Example filter plugin."""

    def __init__(self, exclude_patterns: Optional[List[str]] = None):
        """
        Initialize example filter.

        Args:
            exclude_patterns: Patterns to exclude
        """
        super().__init__("ExampleFilter", "1.0.0")
        self.exclude_patterns = exclude_patterns or []

    def filter_links(self, links: List[str]) -> List[str]:
        """
        Filter links based on patterns.

        Args:
            links: List of links

        Returns:
            Filtered links
        """
        if not self.exclude_patterns:
            return links

        filtered = []
        for link in links:
            should_exclude = False
            for pattern in self.exclude_patterns:
                if pattern in link:
                    should_exclude = True
                    break
            if not should_exclude:
                filtered.append(link)

        return filtered
