"""
JSON output formatter with full metadata.
Exports results with status codes, response types, and discovery context.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class JSONOutputFormatter:
    """Formatter for JSON output with rich metadata."""

    def __init__(self):
        """Initialize JSON formatter."""
        self.data = {
            "scan_metadata": {},
            "links": [],
            "parameters": [],
            "statistics": {},
        }

    def set_metadata(
        self,
        target: str,
        start_time: Optional[datetime] = None,
        config: Optional[Dict] = None,
    ):
        """
        Set scan metadata.

        Args:
            target: Target URL or domain
            start_time: Scan start time
            config: Scan configuration
        """
        self.data["scan_metadata"] = {
            "target": target,
            "timestamp": (start_time or datetime.now()).isoformat(),
            "tool": "xnLinkFinder-Z",
            "config": config or {},
        }

    def add_link(
        self,
        url: str,
        origin: Optional[str] = None,
        method: str = "GET",
        status_code: Optional[int] = None,
        content_type: Optional[str] = None,
        response_time: Optional[float] = None,
        category: Optional[str] = None,
        **kwargs
    ):
        """
        Add a link to the output.

        Args:
            url: Link URL
            origin: Origin URL where link was found
            method: HTTP method
            status_code: Response status code
            content_type: Response content type
            response_time: Response time in seconds
            category: Link category
            **kwargs: Additional metadata
        """
        link_data = {
            "url": url,
            "origin": origin,
            "method": method,
            "status_code": status_code,
            "content_type": content_type,
            "response_time": response_time,
            "category": category,
        }

        # Add any additional metadata
        for key, value in kwargs.items():
            if value is not None:
                link_data[key] = value

        self.data["links"].append(link_data)

    def add_parameter(
        self,
        name: str,
        source: Optional[str] = None,
        type_hint: Optional[str] = None,
        **kwargs
    ):
        """
        Add a parameter to the output.

        Args:
            name: Parameter name
            source: Source of discovery
            type_hint: Inferred parameter type
            **kwargs: Additional metadata
        """
        param_data = {
            "name": name,
            "source": source,
            "type": type_hint,
        }

        # Add any additional metadata
        for key, value in kwargs.items():
            if value is not None:
                param_data[key] = value

        self.data["parameters"].append(param_data)

    def set_statistics(self, stats: Dict[str, Any]):
        """
        Set scan statistics.

        Args:
            stats: Statistics dictionary
        """
        self.data["statistics"] = stats

    def add_section(self, section_name: str, section_data: Any):
        """
        Add a custom section to the output.

        Args:
            section_name: Section name
            section_data: Section data
        """
        self.data[section_name] = section_data

    def to_json(self, indent: int = 2, sort_keys: bool = False) -> str:
        """
        Convert to JSON string.

        Args:
            indent: JSON indentation
            sort_keys: Sort keys alphabetically

        Returns:
            JSON string
        """
        return json.dumps(self.data, indent=indent, sort_keys=sort_keys, default=str)

    def save_to_file(self, filepath: str, indent: int = 2, sort_keys: bool = False):
        """
        Save to JSON file.

        Args:
            filepath: Output file path
            indent: JSON indentation
            sort_keys: Sort keys alphabetically
        """
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=indent, sort_keys=sort_keys, default=str)

    def add_vulnerability_hints(self, hints: List[Dict]):
        """
        Add vulnerability hints section.

        Args:
            hints: List of vulnerability hints
        """
        self.data["vulnerability_hints"] = hints

    def add_secrets(self, secrets: List[Dict]):
        """
        Add detected secrets section.

        Args:
            secrets: List of detected secrets
        """
        self.data["secrets"] = secrets

    def add_cloud_services(self, cloud_services: Dict[str, List[Dict]]):
        """
        Add cloud services section.

        Args:
            cloud_services: Detected cloud services
        """
        self.data["cloud_services"] = cloud_services

    def add_classifications(self, classifications: Dict[str, List[Dict]]):
        """
        Add link classifications section.

        Args:
            classifications: Link classifications
        """
        self.data["classifications"] = classifications

    def get_data(self) -> Dict:
        """
        Get the complete data structure.

        Returns:
            Complete data dictionary
        """
        return self.data


def create_json_output(
    links: List[str],
    target: Optional[str] = None,
    metadata: Optional[Dict] = None,
) -> str:
    """
    Convenience function to create JSON output.

    Args:
        links: List of links
        target: Target URL
        metadata: Additional metadata

    Returns:
        JSON string
    """
    formatter = JSONOutputFormatter()
    
    if target:
        formatter.set_metadata(target, config=metadata)
    
    for link in links:
        formatter.add_link(link)
    
    formatter.set_statistics({
        "total_links": len(links),
    })
    
    return formatter.to_json()
