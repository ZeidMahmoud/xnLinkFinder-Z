"""
OpenAPI/Swagger specification auto-detection and parsing.
Discovers and parses OpenAPI/Swagger specs to extract all API endpoints.
"""

import json
import yaml
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin


class OpenAPIDiscovery:
    """OpenAPI/Swagger specification discovery and parsing."""

    # Common OpenAPI/Swagger spec paths
    COMMON_SPEC_PATHS = [
        "/swagger.json",
        "/swagger.yaml",
        "/swagger.yml",
        "/api/swagger.json",
        "/api/swagger.yaml",
        "/api/swagger.yml",
        "/openapi.json",
        "/openapi.yaml",
        "/openapi.yml",
        "/api/openapi.json",
        "/api/openapi.yaml",
        "/api/openapi.yml",
        "/api-docs",
        "/api-docs/swagger.json",
        "/api-docs/swagger.yaml",
        "/v1/swagger.json",
        "/v2/swagger.json",
        "/v3/swagger.json",
        "/v1/api-docs",
        "/v2/api-docs",
        "/v3/api-docs",
        "/swagger-ui.html",
        "/docs/swagger.json",
        "/docs/openapi.json",
        "/api/v1/swagger.json",
        "/api/v2/swagger.json",
        "/api/v3/swagger.json",
    ]

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize OpenAPI discovery.

        Args:
            base_url: Base URL of the target
            headers: Optional HTTP headers
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.discovered_specs: Dict[str, Dict] = {}

    async def discover_specs(self, custom_paths: Optional[List[str]] = None) -> List[str]:
        """
        Discover OpenAPI/Swagger specification files.

        Args:
            custom_paths: Additional paths to check

        Returns:
            List of discovered spec URLs
        """
        paths_to_check = self.COMMON_SPEC_PATHS.copy()
        if custom_paths:
            paths_to_check.extend(custom_paths)

        discovered = []
        
        for path in paths_to_check:
            url = urljoin(self.base_url, path)
            spec = await self._fetch_spec(url)
            if spec:
                discovered.append(url)
                self.discovered_specs[url] = spec

        return discovered

    async def _fetch_spec(self, url: str) -> Optional[Dict]:
        """
        Fetch and parse OpenAPI spec.

        Args:
            url: Spec URL

        Returns:
            Parsed spec or None
        """
        try:
            # Try async first
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        headers=self.headers,
                        timeout=aiohttp.ClientTimeout(total=10),
                    ) as response:
                        if response.status == 200:
                            content_type = response.headers.get("Content-Type", "")
                            text = await response.text()
                            return self._parse_spec(text, content_type)
            except ImportError:
                # Fallback to sync
                import requests
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    return self._parse_spec(response.text, content_type)
        except Exception:
            pass

        return None

    def _parse_spec(self, content: str, content_type: str) -> Optional[Dict]:
        """
        Parse OpenAPI spec from content.

        Args:
            content: Spec content
            content_type: Content type header

        Returns:
            Parsed spec dictionary
        """
        try:
            # Try JSON first
            if "json" in content_type.lower() or content.strip().startswith("{"):
                spec = json.loads(content)
            else:
                # Try YAML
                spec = yaml.safe_load(content)

            # Validate it's an OpenAPI/Swagger spec
            if self._is_valid_spec(spec):
                return spec
        except Exception:
            pass

        return None

    def _is_valid_spec(self, spec: Dict) -> bool:
        """
        Check if parsed content is a valid OpenAPI/Swagger spec.

        Args:
            spec: Parsed spec dictionary

        Returns:
            True if valid spec
        """
        # Check for OpenAPI 3.x
        if "openapi" in spec and spec["openapi"].startswith("3"):
            return "paths" in spec

        # Check for Swagger 2.x
        if "swagger" in spec and spec["swagger"].startswith("2"):
            return "paths" in spec

        return False

    def extract_endpoints(self, spec: Dict) -> List[Dict[str, any]]:
        """
        Extract all endpoints from OpenAPI spec.

        Args:
            spec: OpenAPI specification

        Returns:
            List of endpoint dictionaries
        """
        endpoints = []

        # Get base path
        base_path = ""
        if "servers" in spec:
            # OpenAPI 3.x
            if spec["servers"]:
                base_path = spec["servers"][0].get("url", "")
        elif "basePath" in spec:
            # Swagger 2.x
            base_path = spec["basePath"]

        # Extract paths
        for path, path_item in spec.get("paths", {}).items():
            full_path = f"{base_path}{path}"

            # Extract operations (GET, POST, etc.)
            for method in ["get", "post", "put", "patch", "delete", "options", "head", "trace"]:
                if method in path_item:
                    operation = path_item[method]
                    
                    endpoint = {
                        "path": full_path,
                        "method": method.upper(),
                        "summary": operation.get("summary", ""),
                        "description": operation.get("description", ""),
                        "operationId": operation.get("operationId", ""),
                        "tags": operation.get("tags", []),
                        "parameters": [],
                        "security": operation.get("security", []),
                    }

                    # Extract parameters
                    for param in operation.get("parameters", []):
                        endpoint["parameters"].append({
                            "name": param.get("name"),
                            "in": param.get("in"),
                            "required": param.get("required", False),
                            "type": param.get("type") or param.get("schema", {}).get("type"),
                        })

                    # Extract request body (OpenAPI 3.x)
                    if "requestBody" in operation:
                        request_body = operation["requestBody"]
                        endpoint["requestBody"] = {
                            "required": request_body.get("required", False),
                            "content": list(request_body.get("content", {}).keys()),
                        }

                    endpoints.append(endpoint)

        return endpoints

    def extract_models(self, spec: Dict) -> Dict[str, Dict]:
        """
        Extract data models/schemas from spec.

        Args:
            spec: OpenAPI specification

        Returns:
            Dictionary of model definitions
        """
        models = {}

        # OpenAPI 3.x
        if "components" in spec and "schemas" in spec["components"]:
            models = spec["components"]["schemas"]

        # Swagger 2.x
        elif "definitions" in spec:
            models = spec["definitions"]

        return models

    def extract_security_schemes(self, spec: Dict) -> Dict[str, Dict]:
        """
        Extract security schemes from spec.

        Args:
            spec: OpenAPI specification

        Returns:
            Dictionary of security schemes
        """
        schemes = {}

        # OpenAPI 3.x
        if "components" in spec and "securitySchemes" in spec["components"]:
            schemes = spec["components"]["securitySchemes"]

        # Swagger 2.x
        elif "securityDefinitions" in spec:
            schemes = spec["securityDefinitions"]

        return schemes

    async def full_discovery(self, custom_paths: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Perform full OpenAPI discovery and parsing.

        Args:
            custom_paths: Additional paths to check

        Returns:
            Discovery results with endpoints and models
        """
        # Discover specs
        spec_urls = await self.discover_specs(custom_paths)

        results = {
            "spec_urls": spec_urls,
            "specs": {},
        }

        # Parse each spec
        for url, spec in self.discovered_specs.items():
            results["specs"][url] = {
                "version": spec.get("openapi") or spec.get("swagger"),
                "info": spec.get("info", {}),
                "endpoints": self.extract_endpoints(spec),
                "models": self.extract_models(spec),
                "security_schemes": self.extract_security_schemes(spec),
            }

        return results


async def discover_openapi(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    custom_paths: Optional[List[str]] = None,
) -> Dict[str, any]:
    """
    Convenience function for OpenAPI discovery.

    Args:
        base_url: Base URL to scan
        headers: Optional HTTP headers
        custom_paths: Additional paths to check

    Returns:
        Discovery results
    """
    discovery = OpenAPIDiscovery(base_url, headers)
    return await discovery.full_discovery(custom_paths)
