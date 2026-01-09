"""
Source map parsing support for JavaScript files.
Recovers original unminified code and finds hidden endpoints in development comments.
"""

import json
import base64
from typing import Dict, Optional, List
from urllib.parse import urljoin


class SourceMapParser:
    """Parser for JavaScript source maps (.map files)."""

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize source map parser.

        Args:
            base_url: Base URL for resolving relative source map URLs
        """
        self.base_url = base_url

    async def discover_source_map(self, js_content: str, js_url: str) -> Optional[str]:
        """
        Discover source map URL from JavaScript content.

        Args:
            js_content: JavaScript file content
            js_url: URL of the JavaScript file

        Returns:
            Source map URL or None
        """
        # Check for sourceMappingURL comment
        lines = js_content.split("\n")
        
        for line in reversed(lines):
            line = line.strip()
            
            # Check for //# sourceMappingURL=
            if line.startswith("//# sourceMappingURL=") or line.startswith("//@ sourceMappingURL="):
                map_url = line.split("=", 1)[1].strip()
                
                # Handle data URLs
                if map_url.startswith("data:"):
                    return map_url
                
                # Resolve relative URLs
                if self.base_url or js_url:
                    base = self.base_url or js_url
                    return urljoin(base, map_url)
                
                return map_url

        # Try default .map file
        if js_url:
            return f"{js_url}.map"

        return None

    async def fetch_source_map(self, map_url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict]:
        """
        Fetch and parse source map.

        Args:
            map_url: Source map URL
            headers: Optional HTTP headers

        Returns:
            Parsed source map or None
        """
        headers = headers or {}

        try:
            # Handle data URLs
            if map_url.startswith("data:"):
                return self._parse_data_url(map_url)

            # Fetch from URL
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        map_url,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:
                        if response.status == 200:
                            text = await response.text()
                            return json.loads(text)
            except ImportError:
                import requests
                response = requests.get(map_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    return response.json()

        except Exception:
            pass

        return None

    def _parse_data_url(self, data_url: str) -> Optional[Dict]:
        """
        Parse source map from data URL.

        Args:
            data_url: Data URL containing source map

        Returns:
            Parsed source map
        """
        try:
            # Format: data:application/json;base64,<data>
            if ";base64," in data_url:
                encoded_data = data_url.split(";base64,", 1)[1]
                decoded_data = base64.b64decode(encoded_data).decode("utf-8")
                return json.loads(decoded_data)
            elif "," in data_url:
                # Plain JSON
                json_data = data_url.split(",", 1)[1]
                return json.loads(json_data)
        except Exception:
            pass

        return None

    def extract_sources(self, source_map: Dict) -> List[str]:
        """
        Extract source file paths from source map.

        Args:
            source_map: Parsed source map

        Returns:
            List of source file paths
        """
        return source_map.get("sources", [])

    def extract_source_content(self, source_map: Dict) -> Dict[str, str]:
        """
        Extract embedded source content from source map.

        Args:
            source_map: Parsed source map

        Returns:
            Dictionary mapping source paths to content
        """
        sources = source_map.get("sources", [])
        contents = source_map.get("sourcesContent", [])

        source_content = {}
        for i, source in enumerate(sources):
            if i < len(contents) and contents[i]:
                source_content[source] = contents[i]

        return source_content

    def extract_urls_from_sources(self, source_content: Dict[str, str]) -> List[str]:
        """
        Extract URLs from source code content.

        Args:
            source_content: Dictionary of source files and their content

        Returns:
            List of discovered URLs
        """
        import re
        
        urls = set()
        
        # URL regex patterns
        url_patterns = [
            # Full URLs
            r'https?://[^\s\'"<>]+',
            # Relative URLs
            r'["\'](/[a-zA-Z0-9/_\-\.]+)["\']',
            # API endpoints
            r'["\']([/a-zA-Z0-9_\-]+/api/[^"\']+)["\']',
        ]

        for source_path, content in source_content.items():
            for pattern in url_patterns:
                matches = re.findall(pattern, content)
                urls.update(matches)

        return list(urls)

    def extract_comments(self, source_content: Dict[str, str]) -> List[str]:
        """
        Extract comments from source code.

        Args:
            source_content: Dictionary of source files and their content

        Returns:
            List of comments
        """
        import re
        
        comments = []
        
        # Comment patterns
        single_line_pattern = r'//.*?$'
        multi_line_pattern = r'/\*.*?\*/'

        for source_path, content in source_content.items():
            # Single line comments
            single_matches = re.findall(single_line_pattern, content, re.MULTILINE)
            comments.extend(single_matches)
            
            # Multi-line comments
            multi_matches = re.findall(multi_line_pattern, content, re.DOTALL)
            comments.extend(multi_matches)

        return comments

    async def full_analysis(
        self,
        js_content: str,
        js_url: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, any]:
        """
        Perform full source map analysis.

        Args:
            js_content: JavaScript content
            js_url: JavaScript URL
            headers: Optional HTTP headers

        Returns:
            Analysis results
        """
        # Discover source map
        map_url = await self.discover_source_map(js_content, js_url)
        if not map_url:
            return {"found": False}

        # Fetch source map
        source_map = await self.fetch_source_map(map_url, headers)
        if not source_map:
            return {"found": True, "map_url": map_url, "fetched": False}

        # Extract information
        sources = self.extract_sources(source_map)
        source_content = self.extract_source_content(source_map)
        urls = self.extract_urls_from_sources(source_content)
        comments = self.extract_comments(source_content)

        return {
            "found": True,
            "map_url": map_url,
            "fetched": True,
            "sources": sources,
            "source_count": len(sources),
            "has_embedded_content": len(source_content) > 0,
            "discovered_urls": urls,
            "comments": comments[:100],  # Limit to first 100 comments
            "comment_count": len(comments),
        }


async def analyze_source_maps(
    js_files: List[Dict[str, str]],
    headers: Optional[Dict[str, str]] = None,
) -> List[Dict[str, any]]:
    """
    Analyze multiple JavaScript files for source maps.

    Args:
        js_files: List of dicts with 'content' and 'url' keys
        headers: Optional HTTP headers

    Returns:
        List of analysis results
    """
    parser = SourceMapParser()
    results = []

    for js_file in js_files:
        result = await parser.full_analysis(
            js_file.get("content", ""),
            js_file.get("url", ""),
            headers,
        )
        result["js_url"] = js_file.get("url")
        results.append(result)

    return results
