"""
Pytest configuration and fixtures for xnLinkFinder tests
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_url():
    """Sample URL for testing"""
    return "https://example.com"


@pytest.fixture
def sample_urls():
    """List of sample URLs for testing"""
    return [
        "https://example.com/api/v1/users",
        "https://example.com/api/v1/products",
        "https://example.com/admin/dashboard",
    ]


@pytest.fixture
def sample_html():
    """Sample HTML content for testing"""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <script src="/js/app.js"></script>
            <script>
                var apiUrl = "https://api.example.com/v1/data";
                fetch('/api/endpoint').then(r => r.json());
            </script>
        </body>
    </html>
    """


@pytest.fixture
def sample_js_content():
    """Sample JavaScript content for testing"""
    return """
    const API_URL = "https://api.example.com";
    const endpoints = {
        users: "/api/v1/users",
        products: "/api/v1/products",
        auth: "/api/auth/login"
    };
    
    fetch(API_URL + endpoints.users);
    """


@pytest.fixture
def temp_output_file(tmp_path):
    """Temporary output file for testing"""
    return tmp_path / "output.txt"


@pytest.fixture
def temp_config_file(tmp_path):
    """Temporary config file for testing"""
    config_path = tmp_path / "config.yml"
    config_content = """
version: 1
settings:
  timeout: 30
  max_depth: 5
"""
    config_path.write_text(config_content)
    return config_path
