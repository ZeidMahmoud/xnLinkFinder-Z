"""
HTML report generator with interactive filtering.
"""

from typing import List, Dict, Optional
from datetime import datetime


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>xnLinkFinder-Z Report - {{ target }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .metadata-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 5px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .stat-number {
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 10px;
        }
        .filters {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .filter-group {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        .filter-group label {
            margin-right: 10px;
            font-weight: 500;
        }
        input, select {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .table-container {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            cursor: pointer;
            user-select: none;
        }
        th:hover {
            background: #5568d3;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        tr:hover {
            background: #f9f9f9;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-critical { background: #f56565; color: white; }
        .badge-high { background: #ed8936; color: white; }
        .badge-medium { background: #ecc94b; color: #333; }
        .badge-low { background: #48bb78; color: white; }
        .badge-info { background: #4299e1; color: white; }
        .link-url {
            font-family: 'Courier New', monospace;
            font-size: 13px;
            word-break: break-all;
        }
        .section {
            margin-bottom: 30px;
        }
        .section-title {
            font-size: 1.8em;
            margin-bottom: 15px;
            color: #2d3748;
        }
        #filterStats {
            margin-top: 10px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 xnLinkFinder-Z Report</h1>
            <div class="metadata">
                <div class="metadata-item">
                    <strong>Target:</strong> {{ target }}
                </div>
                <div class="metadata-item">
                    <strong>Scan Date:</strong> {{ timestamp }}
                </div>
                <div class="metadata-item">
                    <strong>Tool Version:</strong> {{ tool_version }}
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ total_links }}</div>
                <div class="stat-label">Total Links</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ total_parameters }}</div>
                <div class="stat-label">Parameters</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ critical_hints }}</div>
                <div class="stat-label">Critical Findings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ secrets_found }}</div>
                <div class="stat-label">Secrets Found</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">Discovered Links</h2>
            
            <div class="filters">
                <div class="filter-group">
                    <label>Search:</label>
                    <input type="text" id="searchInput" placeholder="Filter by URL..." oninput="filterTable()">
                </div>
                <div class="filter-group">
                    <label>Category:</label>
                    <select id="categoryFilter" onchange="filterTable()">
                        <option value="">All Categories</option>
                        {{ category_options }}
                    </select>
                </div>
                <div class="filter-group">
                    <label>Priority:</label>
                    <select id="priorityFilter" onchange="filterTable()">
                        <option value="">All Priorities</option>
                        <option value="critical">Critical</option>
                        <option value="high">High</option>
                        <option value="medium">Medium</option>
                        <option value="low">Low</option>
                    </select>
                </div>
                <div id="filterStats"></div>
            </div>

            <div class="table-container">
                <table id="linksTable">
                    <thead>
                        <tr>
                            <th onclick="sortTable(0)">URL</th>
                            <th onclick="sortTable(1)">Category</th>
                            <th onclick="sortTable(2)">Priority</th>
                            <th onclick="sortTable(3)">Status</th>
                            <th onclick="sortTable(4)">Origin</th>
                        </tr>
                    </thead>
                    <tbody>
                        {{ links_rows }}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let sortDirection = {};

        function filterTable() {
            const searchValue = document.getElementById('searchInput').value.toLowerCase();
            const categoryValue = document.getElementById('categoryFilter').value.toLowerCase();
            const priorityValue = document.getElementById('priorityFilter').value.toLowerCase();
            
            const table = document.getElementById('linksTable');
            const rows = table.getElementsByTagName('tr');
            let visibleCount = 0;
            
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                const cells = row.getElementsByTagName('td');
                
                const url = cells[0].textContent.toLowerCase();
                const category = cells[1].textContent.toLowerCase();
                const priority = cells[2].textContent.toLowerCase();
                
                const matchesSearch = url.includes(searchValue);
                const matchesCategory = !categoryValue || category.includes(categoryValue);
                const matchesPriority = !priorityValue || priority.includes(priorityValue);
                
                if (matchesSearch && matchesCategory && matchesPriority) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            }
            
            document.getElementById('filterStats').textContent = 
                `Showing ${visibleCount} of ${rows.length - 1} links`;
        }

        function sortTable(columnIndex) {
            const table = document.getElementById('linksTable');
            const rows = Array.from(table.rows).slice(1);
            const ascending = !sortDirection[columnIndex];
            sortDirection[columnIndex] = ascending;
            
            rows.sort((a, b) => {
                const aValue = a.cells[columnIndex].textContent;
                const bValue = b.cells[columnIndex].textContent;
                return ascending ? 
                    aValue.localeCompare(bValue) : 
                    bValue.localeCompare(aValue);
            });
            
            rows.forEach(row => table.tBodies[0].appendChild(row));
        }

        // Initialize filter stats
        filterTable();
    </script>
</body>
</html>
"""


class HTMLReportGenerator:
    """Generator for interactive HTML reports."""

    def __init__(self):
        """Initialize HTML report generator."""
        self.data = {
            "target": "",
            "timestamp": datetime.now().isoformat(),
            "tool_version": "7.18",
            "links": [],
            "parameters": [],
            "vulnerability_hints": [],
            "secrets": [],
        }

    def set_metadata(self, target: str, timestamp: Optional[datetime] = None):
        """Set report metadata."""
        self.data["target"] = target
        if timestamp:
            self.data["timestamp"] = timestamp.isoformat()

    def add_links(self, links: List[Dict]):
        """Add links to report."""
        self.data["links"] = links

    def add_parameters(self, parameters: List[str]):
        """Add parameters to report."""
        self.data["parameters"] = parameters

    def add_vulnerability_hints(self, hints: List[Dict]):
        """Add vulnerability hints."""
        self.data["vulnerability_hints"] = hints

    def add_secrets(self, secrets: List[Dict]):
        """Add detected secrets."""
        self.data["secrets"] = secrets

    def generate_html(self) -> str:
        """Generate HTML report."""
        # Calculate statistics
        total_links = len(self.data["links"])
        total_parameters = len(self.data["parameters"])
        critical_hints = sum(
            1 for h in self.data["vulnerability_hints"]
            if h.get("severity") == "critical"
        )
        secrets_found = len(self.data["secrets"])

        # Generate links table rows
        links_rows = []
        categories = set()
        
        for link in self.data["links"]:
            url = link.get("url", "")
            category = link.get("category", "N/A")
            priority = link.get("priority", "low")
            status = link.get("status_code", "N/A")
            origin = link.get("origin", "N/A")

            categories.add(category)

            badge_class = f"badge badge-{priority}"
            
            row = f"""
                <tr>
                    <td class="link-url">{url}</td>
                    <td>{category}</td>
                    <td><span class="{badge_class}">{priority.upper()}</span></td>
                    <td>{status}</td>
                    <td class="link-url">{origin}</td>
                </tr>
            """
            links_rows.append(row)

        # Generate category options
        category_options = "\n".join(
            f'<option value="{cat}">{cat}</option>'
            for cat in sorted(categories) if cat != "N/A"
        )

        # Replace template variables
        html = HTML_TEMPLATE
        html = html.replace("{{ target }}", self.data["target"])
        html = html.replace("{{ timestamp }}", self.data["timestamp"])
        html = html.replace("{{ tool_version }}", self.data["tool_version"])
        html = html.replace("{{ total_links }}", str(total_links))
        html = html.replace("{{ total_parameters }}", str(total_parameters))
        html = html.replace("{{ critical_hints }}", str(critical_hints))
        html = html.replace("{{ secrets_found }}", str(secrets_found))
        html = html.replace("{{ category_options }}", category_options)
        html = html.replace("{{ links_rows }}", "\n".join(links_rows))

        return html

    def save_to_file(self, filepath: str):
        """Save HTML report to file."""
        html = self.generate_html()
        with open(filepath, 'w') as f:
            f.write(html)


def create_html_report(
    links: List[Dict],
    target: str,
    parameters: Optional[List[str]] = None,
    vulnerability_hints: Optional[List[Dict]] = None,
    secrets: Optional[List[Dict]] = None,
) -> str:
    """
    Convenience function to create HTML report.

    Args:
        links: List of links
        target: Target URL
        parameters: List of parameters
        vulnerability_hints: List of vulnerability hints
        secrets: List of secrets

    Returns:
        HTML string
    """
    generator = HTMLReportGenerator()
    generator.set_metadata(target)
    generator.add_links(links)
    
    if parameters:
        generator.add_parameters(parameters)
    if vulnerability_hints:
        generator.add_vulnerability_hints(vulnerability_hints)
    if secrets:
        generator.add_secrets(secrets)
    
    return generator.generate_html()
