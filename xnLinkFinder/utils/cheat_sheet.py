"""Cheat Sheet Generator"""

EXAMPLES = """
# xnLinkFinder-Z Cheat Sheet

## Basic Usage
xnLinkFinder -i https://example.com -o results.txt

## Security Scanning
xnLinkFinder -i urls.txt --scan-cors --scan-jwt

## OSINT Mode
xnLinkFinder -i domain.com --google-dork --find-buckets
"""

def generate_cheat_sheet() -> str:
    """Generate cheat sheet"""
    return EXAMPLES

def export_cheat_sheet(format: str = "markdown"):
    """Export cheat sheet"""
    return generate_cheat_sheet()
