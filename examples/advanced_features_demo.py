#!/usr/bin/env python3
"""
Example script demonstrating the new xnLinkFinder-Z advanced features.

This script shows how to use the new modules for:
- Async crawling
- GraphQL discovery
- OpenAPI discovery
- Link classification
- Vulnerability analysis
- Secrets detection
- Multiple output formats
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from xnLinkFinder.core.async_crawler import AsyncCrawler
from xnLinkFinder.discovery.graphql import discover_graphql
from xnLinkFinder.discovery.openapi import discover_openapi
from xnLinkFinder.discovery.cloud_services import detect_cloud_services
from xnLinkFinder.analysis.classifier import classify_links
from xnLinkFinder.analysis.vuln_hints import analyze_vulnerabilities
from xnLinkFinder.analysis.secrets import detect_secrets
from xnLinkFinder.output.json_output import JSONOutputFormatter
from xnLinkFinder.output.html_report import HTMLReportGenerator
from xnLinkFinder.output.markdown_output import MarkdownOutputFormatter
from xnLinkFinder.ui.tui import create_tui


async def example_async_crawling():
    """Example: Async HTTP crawling."""
    print("\n=== Example 1: Async HTTP Crawling ===")
    
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml",
    ]
    
    async with AsyncCrawler(max_concurrent=3, timeout=10) as crawler:
        results = await crawler.fetch_many(urls)
        
        for result in results:
            print(f"URL: {result['url']}")
            print(f"Status: {result['status']}")
            print(f"Size: {result['size']} bytes")
            print(f"Error: {result['error'] or 'None'}")
            print()


async def example_graphql_discovery():
    """Example: GraphQL endpoint discovery."""
    print("\n=== Example 2: GraphQL Discovery ===")
    
    # Example target (won't work without actual GraphQL endpoint)
    target = "https://api.example.com"
    
    try:
        results = await discover_graphql(target)
        print(f"Discovered endpoints: {results['endpoints']}")
        
        for endpoint, schema_info in results['schemas'].items():
            print(f"\nEndpoint: {endpoint}")
            print(f"Queries: {len(schema_info['endpoints']['queries'])}")
            print(f"Mutations: {len(schema_info['endpoints']['mutations'])}")
    except Exception as e:
        print(f"Note: GraphQL discovery requires valid endpoint: {e}")


async def example_openapi_discovery():
    """Example: OpenAPI/Swagger discovery."""
    print("\n=== Example 3: OpenAPI Discovery ===")
    
    target = "https://petstore.swagger.io/v2"
    
    try:
        results = await discover_openapi(target)
        
        print(f"Found {len(results['spec_urls'])} OpenAPI specs")
        
        for spec_url, spec_info in results['specs'].items():
            print(f"\nSpec: {spec_url}")
            print(f"Version: {spec_info['version']}")
            print(f"Endpoints: {len(spec_info['endpoints'])}")
            
            # Show first few endpoints
            for endpoint in spec_info['endpoints'][:3]:
                print(f"  {endpoint['method']} {endpoint['path']}")
    except Exception as e:
        print(f"Note: OpenAPI discovery example: {e}")


def example_link_classification():
    """Example: Link classification."""
    print("\n=== Example 4: Link Classification ===")
    
    example_urls = [
        "https://example.com/api/v1/users",
        "https://example.com/admin/dashboard",
        "https://example.com/login",
        "https://example.com/upload",
        "https://example.com/user/123/profile",
        "https://example.com/config/app.json",
        "https://example.com/.git/config",
    ]
    
    results = classify_links(example_urls)
    
    print("\nBy Category:")
    for category, links in results['by_category'].items():
        print(f"  {category}: {len(links)} links")
    
    print("\nBy Priority:")
    for priority, links in results['by_priority'].items():
        if links:
            print(f"  {priority}: {len(links)} links")
    
    print("\nHigh Priority Links:")
    for link in results['by_priority']['high'][:5]:
        print(f"  [{link['priority']}] {link['url']}")


def example_vulnerability_analysis():
    """Example: Vulnerability hints."""
    print("\n=== Example 5: Vulnerability Analysis ===")
    
    example_urls = [
        "https://example.com/user/12345",
        "https://example.com/api?url=https://internal.com",
        "https://example.com/download?file=../../etc/passwd",
        "https://example.com/search?q=test",
        "https://example.com/debug/info",
    ]
    
    results = analyze_vulnerabilities(example_urls)
    
    print(f"\nTotal hints: {len(results['all'])}")
    
    print("\nBy Type:")
    for vuln_type, hints in results['by_type'].items():
        print(f"  {vuln_type}: {len(hints)}")
    
    print("\nBy Severity:")
    for severity, hints in results['by_severity'].items():
        if hints:
            print(f"  {severity}: {len(hints)}")
    
    print("\nExample Hints:")
    for hint in results['all'][:3]:
        print(f"  [{hint['severity']}] {hint['type']}: {hint['description']}")


def example_secrets_detection():
    """Example: Secrets detection."""
    print("\n=== Example 6: Secrets Detection ===")
    
    example_content = """
    const config = {
        apiKey: 'AIzaSyDaGmWKa4JsXZ-HjGw7ISLn_3namBGewQe',
        awsAccessKey: 'AKIAIOSFODNN7EXAMPLE',
        githubToken: 'ghp_16C7e42F292c6912E7710c838347Ae178B4a',
        stripeKey: '[REDACTED]',
        password: 'superSecretPassword123',
        dbConnection: 'mongodb://admin:password@localhost:27017/mydb'
    }
    """
    
    secrets = detect_secrets(example_content, "config.js")
    
    print(f"\nFound {len(secrets)} secrets:")
    
    for secret in secrets:
        print(f"\n  Type: {secret['type']}")
        print(f"  Severity: {secret['severity']}")
        print(f"  Description: {secret['description']}")
        print(f"  Value: {secret['value'][:20]}...")


def example_cloud_detection():
    """Example: Cloud service detection."""
    print("\n=== Example 7: Cloud Service Detection ===")
    
    example_content = """
    https://my-bucket.s3.amazonaws.com/file.pdf
    https://my-function.azurewebsites.net/api/endpoint
    https://storage.googleapis.com/my-bucket/data.json
    https://my-app.firebaseapp.com/
    https://abcd1234.execute-api.us-east-1.amazonaws.com/prod
    """
    
    results = detect_cloud_services(example_content)
    
    print("\nDetected Cloud Services:")
    for provider, services in results.items():
        if services:
            print(f"\n  {provider.upper()}: {len(services)} services")
            for service in services[:3]:
                print(f"    - {service['service']}: {service['url']}")


def example_output_formats():
    """Example: Multiple output formats."""
    print("\n=== Example 8: Output Formats ===")
    
    # Example data
    links = [
        {
            "url": "https://example.com/api/users",
            "category": "api",
            "priority": "high",
            "status_code": 200,
            "origin": "https://example.com",
        },
        {
            "url": "https://example.com/admin",
            "category": "admin",
            "priority": "critical",
            "status_code": 403,
            "origin": "https://example.com",
        },
    ]
    
    parameters = ["id", "user", "token", "callback"]
    
    # JSON output
    print("\n1. JSON Output:")
    json_formatter = JSONOutputFormatter()
    json_formatter.set_metadata("example.com")
    for link in links:
        json_formatter.add_link(**link)
    for param in parameters:
        json_formatter.add_parameter(param)
    json_formatter.set_statistics({"total_links": len(links)})
    print("  Created JSON output (see output.json)")
    json_formatter.save_to_file("/tmp/example_output.json")
    
    # HTML output
    print("\n2. HTML Report:")
    html_generator = HTMLReportGenerator()
    html_generator.set_metadata("example.com")
    html_generator.add_links(links)
    html_generator.add_parameters(parameters)
    html_generator.save_to_file("/tmp/example_report.html")
    print("  Created HTML report (see /tmp/example_report.html)")
    
    # Markdown output
    print("\n3. Markdown Output:")
    md_formatter = MarkdownOutputFormatter()
    md_formatter.add_metadata("example.com")
    md_formatter.add_summary({"total_links": len(links), "total_parameters": len(parameters)})
    md_formatter.add_links_table(links)
    md_formatter.save_to_file("/tmp/example_report.md")
    print("  Created Markdown report (see /tmp/example_report.md)")


def example_tui():
    """Example: Terminal UI."""
    print("\n=== Example 9: Terminal UI ===")
    
    tui = create_tui()
    
    # Show banner
    tui.show_banner("xnLinkFinder-Z Example", "1.0.0")
    
    # Show stats
    stats = {
        "total_links": 150,
        "total_parameters": 45,
        "critical_findings": 3,
        "high_findings": 12,
    }
    tui.show_stats_table(stats)
    
    # Show example links
    example_links = [
        {"url": "https://example.com/api/users", "category": "api", "priority": "high"},
        {"url": "https://example.com/admin", "category": "admin", "priority": "critical"},
        {"url": "https://example.com/login", "category": "authentication", "priority": "high"},
    ]
    tui.show_links_table(example_links)
    
    tui.print_success("Examples completed successfully!")


async def main():
    """Run all examples."""
    print("=" * 70)
    print("xnLinkFinder-Z Advanced Features Examples")
    print("=" * 70)
    
    # Async examples
    await example_async_crawling()
    await example_graphql_discovery()
    await example_openapi_discovery()
    
    # Sync examples
    example_link_classification()
    example_vulnerability_analysis()
    example_secrets_detection()
    example_cloud_detection()
    example_output_formats()
    example_tui()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("Check /tmp/ directory for generated output files")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
