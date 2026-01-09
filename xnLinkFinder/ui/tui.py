"""
Terminal User Interface (TUI) using rich for progress visualization.
"""

from typing import List, Dict, Optional, Callable
from datetime import datetime
import time


class SimpleTUI:
    """
    Simple Terminal UI for xnLinkFinder-Z.
    
    Provides real-time progress visualization and interactive features.
    """

    def __init__(self):
        """Initialize TUI."""
        self.rich_available = False
        
        try:
            from rich.console import Console
            from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
            from rich.table import Table
            from rich.live import Live
            from rich.panel import Panel
            from rich.layout import Layout
            
            self.Console = Console
            self.Progress = Progress
            self.Table = Table
            self.Live = Live
            self.Panel = Panel
            self.Layout = Layout
            self.SpinnerColumn = SpinnerColumn
            self.BarColumn = BarColumn
            self.TextColumn = TextColumn
            self.TimeElapsedColumn = TimeElapsedColumn
            
            self.console = Console()
            self.rich_available = True
        except ImportError:
            pass

    def show_banner(self, tool_name: str = "xnLinkFinder-Z", version: str = "7.18"):
        """Display tool banner."""
        if not self.rich_available:
            print(f"\n{tool_name} v{version}\n{'=' * 50}\n")
            return

        banner = self.Panel(
            f"[bold cyan]{tool_name}[/bold cyan]\n[dim]Version {version}[/dim]",
            border_style="cyan",
            expand=False,
        )
        self.console.print(banner)

    def create_progress_bar(self, description: str = "Processing"):
        """
        Create a progress bar.

        Args:
            description: Progress description

        Returns:
            Progress object or None
        """
        if not self.rich_available:
            return None

        return self.Progress(
            self.SpinnerColumn(),
            self.TextColumn("[progress.description]{task.description}"),
            self.BarColumn(),
            self.TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            self.TimeElapsedColumn(),
            console=self.console,
        )

    def show_stats_table(self, stats: Dict[str, any]):
        """
        Display statistics table.

        Args:
            stats: Statistics dictionary
        """
        if not self.rich_available:
            print("\nStatistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            print()
            return

        table = self.Table(title="Scan Statistics", show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        for key, value in stats.items():
            formatted_key = key.replace("_", " ").title()
            table.add_row(formatted_key, str(value))

        self.console.print(table)

    def show_links_table(self, links: List[Dict], max_rows: int = 20):
        """
        Display links table.

        Args:
            links: List of link dictionaries
            max_rows: Maximum rows to display
        """
        if not self.rich_available:
            print("\nDiscovered Links:")
            for i, link in enumerate(links[:max_rows]):
                print(f"  {i+1}. {link.get('url', '')}")
            if len(links) > max_rows:
                print(f"  ... and {len(links) - max_rows} more")
            print()
            return

        table = self.Table(title="Discovered Links", show_header=True)
        table.add_column("URL", style="cyan", no_wrap=False)
        table.add_column("Category", style="yellow")
        table.add_column("Priority", style="magenta")

        for link in links[:max_rows]:
            url = link.get("url", "")
            category = link.get("category", "N/A")
            priority = link.get("priority", "low")
            
            # Color code priority
            if priority == "critical":
                priority_str = "[bold red]CRITICAL[/bold red]"
            elif priority == "high":
                priority_str = "[red]HIGH[/red]"
            elif priority == "medium":
                priority_str = "[yellow]MEDIUM[/yellow]"
            else:
                priority_str = "[green]LOW[/green]"
            
            table.add_row(url, category, priority_str)

        if len(links) > max_rows:
            table.caption = f"Showing {max_rows} of {len(links)} links"

        self.console.print(table)

    def show_vulnerability_hints(self, hints: List[Dict], max_rows: int = 10):
        """
        Display vulnerability hints.

        Args:
            hints: List of vulnerability hints
            max_rows: Maximum rows to display
        """
        if not self.rich_available:
            print("\nVulnerability Hints:")
            for i, hint in enumerate(hints[:max_rows]):
                print(f"  {i+1}. [{hint.get('severity', 'unknown')}] {hint.get('description', '')}")
            if len(hints) > max_rows:
                print(f"  ... and {len(hints) - max_rows} more")
            print()
            return

        table = self.Table(title="Vulnerability Hints", show_header=True)
        table.add_column("Type", style="cyan")
        table.add_column("Severity", style="red")
        table.add_column("Description", no_wrap=False)

        for hint in hints[:max_rows]:
            hint_type = hint.get("type", "unknown")
            severity = hint.get("severity", "unknown").upper()
            description = hint.get("description", "")
            
            table.add_row(hint_type, severity, description)

        if len(hints) > max_rows:
            table.caption = f"Showing {max_rows} of {len(hints)} hints"

        self.console.print(table)

    def print_success(self, message: str):
        """Print success message."""
        if self.rich_available:
            self.console.print(f"[green]✓[/green] {message}")
        else:
            print(f"✓ {message}")

    def print_error(self, message: str):
        """Print error message."""
        if self.rich_available:
            self.console.print(f"[red]✗[/red] {message}")
        else:
            print(f"✗ {message}")

    def print_warning(self, message: str):
        """Print warning message."""
        if self.rich_available:
            self.console.print(f"[yellow]⚠[/yellow] {message}")
        else:
            print(f"⚠ {message}")

    def print_info(self, message: str):
        """Print info message."""
        if self.rich_available:
            self.console.print(f"[blue]ℹ[/blue] {message}")
        else:
            print(f"ℹ {message}")


def create_tui() -> SimpleTUI:
    """
    Create TUI instance.

    Returns:
        SimpleTUI instance
    """
    return SimpleTUI()


# Example usage
if __name__ == "__main__":
    tui = create_tui()
    
    # Show banner
    tui.show_banner()
    
    # Show progress
    if tui.rich_available:
        with tui.create_progress_bar() as progress:
            task = progress.add_task("Scanning...", total=100)
            for i in range(100):
                time.sleep(0.02)
                progress.update(task, advance=1)
    
    # Show stats
    tui.show_stats_table({
        "total_links": 150,
        "total_parameters": 45,
        "critical_findings": 3,
        "high_findings": 12,
    })
    
    # Show example links
    example_links = [
        {"url": "https://example.com/api/users", "category": "api", "priority": "high"},
        {"url": "https://example.com/admin", "category": "admin", "priority": "critical"},
        {"url": "https://example.com/login", "category": "authentication", "priority": "high"},
    ]
    tui.show_links_table(example_links)
    
    tui.print_success("Scan completed successfully!")
