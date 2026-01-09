# xnLinkFinder-Z Examples

This directory contains examples demonstrating the advanced features of xnLinkFinder-Z.

## Running the Examples

### All-in-One Demo

Run the comprehensive demo that showcases all features:

```bash
cd examples
python3 advanced_features_demo.py
```

This will demonstrate:
1. Async HTTP crawling
2. GraphQL discovery
3. OpenAPI/Swagger discovery
4. Link classification
5. Vulnerability analysis
6. Secrets detection
7. Cloud service detection
8. Multiple output formats (JSON, HTML, Markdown)
9. Terminal UI features

### Output Files

The demo will create example output files in `/tmp/`:
- `/tmp/example_output.json` - JSON format
- `/tmp/example_report.html` - Interactive HTML report
- `/tmp/example_report.md` - Markdown report

## Individual Feature Examples

Each function in `advanced_features_demo.py` can be called independently:

```python
import asyncio
from examples.advanced_features_demo import example_link_classification

# Run individual example
example_link_classification()

# Or for async examples
asyncio.run(example_async_crawling())
```

## API Usage Examples

### Async Crawling

```python
from xnLinkFinder.core.async_crawler import AsyncCrawler

async with AsyncCrawler(max_concurrent=50, rate_limit=10) as crawler:
    results = await crawler.fetch_many(urls)
    for result in results:
        print(f"{result['url']}: {result['status']}")
```

### Link Classification

```python
from xnLinkFinder.analysis.classifier import LinkClassifier

classifier = LinkClassifier()
results = classifier.classify_batch(urls)

# Get high priority links
high_priority = classifier.get_high_priority_urls(urls)
```

### Vulnerability Analysis

```python
from xnLinkFinder.analysis.vuln_hints import VulnerabilityHinter

hinter = VulnerabilityHinter()
hints = hinter.analyze_url(url)

for hint in hints:
    print(f"[{hint['severity']}] {hint['type']}: {hint['description']}")
```

### Secrets Detection

```python
from xnLinkFinder.analysis.secrets import SecretsDetector

detector = SecretsDetector()
secrets = detector.scan_content(content, source="config.js")

# Filter by severity
critical_secrets = detector.filter_by_severity("critical")
```

### Database Operations

```python
from xnLinkFinder.core.database import LinkDatabase

with LinkDatabase("scan.db") as db:
    scan_id = db.start_scan("example.com")
    
    # Add links
    link_id = db.add_link(
        url="https://example.com/api",
        category="api",
        status_code=200
    )
    
    # Export results
    db.export_to_json("results.json", scan_id)
```

### Output Formats

```python
from xnLinkFinder.output.json_output import JSONOutputFormatter
from xnLinkFinder.output.html_report import HTMLReportGenerator
from xnLinkFinder.output.markdown_output import MarkdownOutputFormatter

# JSON
json_formatter = JSONOutputFormatter()
json_formatter.set_metadata("example.com")
json_formatter.add_link("https://example.com", category="api")
json_formatter.save_to_file("output.json")

# HTML
html_gen = HTMLReportGenerator()
html_gen.set_metadata("example.com")
html_gen.add_links(links)
html_gen.save_to_file("report.html")

# Markdown
md_formatter = MarkdownOutputFormatter()
md_formatter.add_metadata("example.com")
md_formatter.add_links_table(links)
md_formatter.save_to_file("report.md")
```

### Terminal UI

```python
from xnLinkFinder.ui.tui import create_tui

tui = create_tui()
tui.show_banner("My Tool", "1.0")
tui.show_stats_table({"total": 100, "found": 50})
tui.show_links_table(links)
tui.print_success("Scan complete!")
```

## Notes

- Most examples are self-contained and don't require external services
- GraphQL and OpenAPI examples will show "Note" messages if endpoints don't exist
- Async examples require Python 3.7+
- Some features require additional dependencies (install with `pip install -r requirements.txt`)

## See Also

- [ADVANCED_FEATURES.md](../ADVANCED_FEATURES.md) - Complete feature documentation
- [README.md](../README.md) - Main project documentation
