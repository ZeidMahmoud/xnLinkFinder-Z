"""
Markdown output formatter for documentation.
"""

from typing import List, Dict, Optional
from datetime import datetime


class MarkdownOutputFormatter:
    """Formatter for Markdown output."""

    def __init__(self):
        """Initialize Markdown formatter."""
        self.sections = []
        self.metadata = {}

    def add_header(self, title: str, level: int = 1):
        """
        Add a header.

        Args:
            title: Header title
            level: Header level (1-6)
        """
        prefix = "#" * level
        self.sections.append(f"{prefix} {title}\n")

    def add_metadata(self, target: str, timestamp: Optional[datetime] = None):
        """
        Add scan metadata section.

        Args:
            target: Target URL
            timestamp: Scan timestamp
        """
        self.metadata = {
            "target": target,
            "timestamp": (timestamp or datetime.now()).isoformat(),
        }

        self.add_header("xnLinkFinder-Z Scan Report", 1)
        self.sections.append(f"**Target:** `{target}`\n")
        self.sections.append(f"**Scan Date:** {self.metadata['timestamp']}\n")
        self.sections.append("\n---\n\n")

    def add_summary(self, stats: Dict):
        """
        Add summary statistics section.

        Args:
            stats: Statistics dictionary
        """
        self.add_header("Summary", 2)
        
        for key, value in stats.items():
            formatted_key = key.replace("_", " ").title()
            self.sections.append(f"- **{formatted_key}:** {value}\n")
        
        self.sections.append("\n")

    def add_links_table(self, links: List[Dict]):
        """
        Add links as a table.

        Args:
            links: List of link dictionaries
        """
        self.add_header("Discovered Links", 2)
        
        if not links:
            self.sections.append("No links found.\n\n")
            return

        # Create table header
        self.sections.append("| URL | Category | Status | Origin |\n")
        self.sections.append("|-----|----------|--------|--------|\n")

        # Add rows
        for link in links[:1000]:  # Limit to first 1000
            url = link.get("url", "")
            category = link.get("category", "N/A")
            status = link.get("status_code", "N/A")
            origin = link.get("origin", "N/A")
            
            self.sections.append(f"| `{url}` | {category} | {status} | `{origin}` |\n")

        if len(links) > 1000:
            self.sections.append(f"\n*Showing first 1000 of {len(links)} links*\n")

        self.sections.append("\n")

    def add_parameters_list(self, parameters: List[str]):
        """
        Add parameters as a list.

        Args:
            parameters: List of parameter names
        """
        self.add_header("Discovered Parameters", 2)
        
        if not parameters:
            self.sections.append("No parameters found.\n\n")
            return

        for param in sorted(set(parameters)):
            self.sections.append(f"- `{param}`\n")
        
        self.sections.append("\n")

    def add_vulnerability_hints(self, hints: List[Dict]):
        """
        Add vulnerability hints section.

        Args:
            hints: List of vulnerability hints
        """
        self.add_header("Vulnerability Hints", 2)
        
        if not hints:
            self.sections.append("No vulnerability hints.\n\n")
            return

        # Group by type
        by_type = {}
        for hint in hints:
            hint_type = hint.get("type", "unknown")
            if hint_type not in by_type:
                by_type[hint_type] = []
            by_type[hint_type].append(hint)

        for hint_type, type_hints in by_type.items():
            self.add_header(hint_type.upper().replace("_", " "), 3)
            
            for hint in type_hints[:50]:  # Limit per type
                severity = hint.get("severity", "unknown")
                description = hint.get("description", "")
                url = hint.get("url", "")
                
                self.sections.append(f"**[{severity.upper()}]** {description}\n")
                self.sections.append(f"- URL: `{url}`\n")
                if "recommendation" in hint:
                    self.sections.append(f"- Recommendation: {hint['recommendation']}\n")
                self.sections.append("\n")

    def add_classifications(self, classifications: Dict):
        """
        Add link classifications section.

        Args:
            classifications: Classifications dictionary
        """
        self.add_header("Link Classifications", 2)
        
        by_category = classifications.get("by_category", {})
        
        if not by_category:
            self.sections.append("No classifications available.\n\n")
            return

        for category, links in by_category.items():
            self.add_header(category.replace("_", " ").title(), 3)
            self.sections.append(f"Found {len(links)} {category} links:\n\n")
            
            for link in links[:20]:  # Show first 20
                url = link.get("url", "")
                self.sections.append(f"- `{url}`\n")
            
            if len(links) > 20:
                self.sections.append(f"\n*...and {len(links) - 20} more*\n")
            
            self.sections.append("\n")

    def add_custom_section(self, title: str, content: str, level: int = 2):
        """
        Add a custom section.

        Args:
            title: Section title
            content: Section content
            level: Header level
        """
        self.add_header(title, level)
        self.sections.append(content)
        self.sections.append("\n\n")

    def to_markdown(self) -> str:
        """
        Convert to Markdown string.

        Returns:
            Markdown string
        """
        return "".join(self.sections)

    def save_to_file(self, filepath: str):
        """
        Save to Markdown file.

        Args:
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())


def create_markdown_report(
    links: List[Dict],
    target: str,
    stats: Optional[Dict] = None,
) -> str:
    """
    Convenience function to create Markdown report.

    Args:
        links: List of links
        target: Target URL
        stats: Statistics

    Returns:
        Markdown string
    """
    formatter = MarkdownOutputFormatter()
    formatter.add_metadata(target)
    
    if stats:
        formatter.add_summary(stats)
    
    formatter.add_links_table(links)
    
    return formatter.to_markdown()
