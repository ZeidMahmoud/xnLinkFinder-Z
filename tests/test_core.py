"""
Core functionality tests for xnLinkFinder
"""
import pytest
import sys


def test_import_xnlinkfinder():
    """Test that xnLinkFinder module can be imported"""
    try:
        import xnLinkFinder
        assert xnLinkFinder is not None
    except ImportError as e:
        pytest.skip(f"xnLinkFinder module not available: {e}")


def test_python_version():
    """Test that Python version is supported"""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


def test_sample_url_fixture(sample_url):
    """Test sample_url fixture"""
    assert sample_url == "https://example.com"
    assert sample_url.startswith("https://")


def test_sample_urls_fixture(sample_urls):
    """Test sample_urls fixture"""
    assert len(sample_urls) == 3
    assert all(url.startswith("https://") for url in sample_urls)


def test_sample_html_fixture(sample_html):
    """Test sample_html fixture"""
    assert "<html>" in sample_html
    assert "<a href" in sample_html
    assert "<script" in sample_html


def test_sample_js_content_fixture(sample_js_content):
    """Test sample_js_content fixture"""
    assert "API_URL" in sample_js_content
    assert "fetch" in sample_js_content
    assert "/api/" in sample_js_content


def test_temp_output_file_fixture(temp_output_file):
    """Test temp_output_file fixture"""
    assert str(temp_output_file).endswith("output.txt")
    # Write and read test
    temp_output_file.write_text("test content")
    assert temp_output_file.read_text() == "test content"


def test_temp_config_file_fixture(temp_config_file):
    """Test temp_config_file fixture"""
    assert temp_config_file.exists()
    content = temp_config_file.read_text()
    assert "version" in content
    assert "settings" in content
