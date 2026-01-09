"""
Vulnerability hints module.
Flags potential security issues like IDOR, SSRF, debug endpoints, etc.
"""

import re
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse, parse_qs


class VulnerabilityHinter:
    """Analyzer for identifying potential security vulnerabilities in URLs."""

    def __init__(self):
        """Initialize vulnerability hinter."""
        self.hints: List[Dict] = []

    def analyze_url(self, url: str) -> List[Dict]:
        """
        Analyze URL for potential vulnerabilities.

        Args:
            url: URL to analyze

        Returns:
            List of vulnerability hints
        """
        hints = []
        parsed = urlparse(url)
        path = parsed.path
        query = parsed.query
        params = parse_qs(query)

        # Check for IDOR patterns
        idor_hints = self._check_idor(url, path, params)
        hints.extend(idor_hints)

        # Check for SSRF patterns
        ssrf_hints = self._check_ssrf(url, params)
        hints.extend(ssrf_hints)

        # Check for LFI/Path Traversal
        lfi_hints = self._check_lfi(url, params)
        hints.extend(lfi_hints)

        # Check for SQL injection
        sqli_hints = self._check_sqli(url, params)
        hints.extend(sqli_hints)

        # Check for XSS
        xss_hints = self._check_xss(url, params)
        hints.extend(xss_hints)

        # Check for debug/test endpoints
        debug_hints = self._check_debug_endpoints(url, path)
        hints.extend(debug_hints)

        # Check for deprecated API versions
        deprecated_hints = self._check_deprecated_api(url, path)
        hints.extend(deprecated_hints)

        # Check for open redirects
        redirect_hints = self._check_open_redirect(url, params)
        hints.extend(redirect_hints)

        # Check for XXE
        xxe_hints = self._check_xxe(url, params)
        hints.extend(xxe_hints)

        # Store all hints
        self.hints.extend(hints)

        return hints

    def _check_idor(self, url: str, path: str, params: Dict) -> List[Dict]:
        """Check for Insecure Direct Object Reference patterns."""
        hints = []

        # Numeric IDs in path
        numeric_id_pattern = r'/(\d+)(?:/|$|\?)'
        matches = re.finditer(numeric_id_pattern, path)
        
        for match in matches:
            hints.append({
                "type": "idor",
                "severity": "high",
                "description": "Numeric ID in URL path - potential IDOR vulnerability",
                "url": url,
                "pattern": match.group(0),
                "recommendation": "Test if changing the ID allows access to other users' data",
            })

        # UUID patterns
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        if re.search(uuid_pattern, path, re.IGNORECASE):
            hints.append({
                "type": "idor",
                "severity": "medium",
                "description": "UUID in URL path - potential IDOR vulnerability",
                "url": url,
                "recommendation": "Test if changing the UUID allows access to other resources",
            })

        # ID parameters
        id_params = ["id", "user_id", "userid", "uid", "account_id", "profile_id"]
        for param_name in params:
            if any(id_param in param_name.lower() for id_param in id_params):
                hints.append({
                    "type": "idor",
                    "severity": "high",
                    "description": f"ID parameter '{param_name}' - potential IDOR vulnerability",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test if changing the ID parameter allows unauthorized access",
                })

        return hints

    def _check_ssrf(self, url: str, params: Dict) -> List[Dict]:
        """Check for Server-Side Request Forgery patterns."""
        hints = []

        ssrf_params = [
            "url", "uri", "path", "dest", "destination", "redirect",
            "callback", "return", "continue", "next", "target",
            "rurl", "link", "load", "file", "fetch", "request"
        ]

        for param_name in params:
            if any(ssrf_param in param_name.lower() for ssrf_param in ssrf_params):
                hints.append({
                    "type": "ssrf",
                    "severity": "critical",
                    "description": f"URL parameter '{param_name}' - potential SSRF vulnerability",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test if you can make the server request internal resources or external URLs",
                })

        return hints

    def _check_lfi(self, url: str, params: Dict) -> List[Dict]:
        """Check for Local File Inclusion patterns."""
        hints = []

        lfi_params = [
            "file", "path", "dir", "folder", "document", "page",
            "include", "template", "load", "read", "download"
        ]

        for param_name in params:
            if any(lfi_param in param_name.lower() for lfi_param in lfi_params):
                hints.append({
                    "type": "lfi",
                    "severity": "high",
                    "description": f"File path parameter '{param_name}' - potential LFI/Path Traversal",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test with path traversal sequences (../, etc.)",
                })

        return hints

    def _check_sqli(self, url: str, params: Dict) -> List[Dict]:
        """Check for SQL Injection patterns."""
        hints = []

        sqli_params = [
            "id", "user", "username", "email", "search", "query",
            "filter", "sort", "order", "category", "type"
        ]

        for param_name in params:
            if any(sqli_param in param_name.lower() for sqli_param in sqli_params):
                hints.append({
                    "type": "sqli",
                    "severity": "high",
                    "description": f"Database query parameter '{param_name}' - potential SQL injection",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test with SQL injection payloads",
                })

        return hints

    def _check_xss(self, url: str, params: Dict) -> List[Dict]:
        """Check for Cross-Site Scripting patterns."""
        hints = []

        xss_params = [
            "q", "query", "search", "keyword", "name", "title",
            "message", "comment", "description", "text", "content"
        ]

        for param_name in params:
            if any(xss_param in param_name.lower() for xss_param in xss_params):
                hints.append({
                    "type": "xss",
                    "severity": "medium",
                    "description": f"User input parameter '{param_name}' - potential XSS",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test with XSS payloads to see if input is reflected without sanitization",
                })

        return hints

    def _check_debug_endpoints(self, url: str, path: str) -> List[Dict]:
        """Check for debug/test endpoints."""
        hints = []

        debug_patterns = [
            (r'/debug', "Debug endpoint exposed"),
            (r'/test', "Test endpoint exposed"),
            (r'/dev', "Development endpoint exposed"),
            (r'/staging', "Staging endpoint exposed"),
            (r'/trace', "Trace endpoint exposed"),
            (r'/phpinfo', "PHPInfo endpoint exposed"),
            (r'/server-status', "Server status endpoint exposed"),
            (r'/actuator', "Spring Boot Actuator endpoint exposed"),
            (r'/__', "Special/internal endpoint exposed"),
        ]

        for pattern, description in debug_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                hints.append({
                    "type": "debug_endpoint",
                    "severity": "high",
                    "description": description,
                    "url": url,
                    "recommendation": "Debug endpoints should not be accessible in production",
                })

        return hints

    def _check_deprecated_api(self, url: str, path: str) -> List[Dict]:
        """Check for deprecated API versions."""
        hints = []

        # Check for old API versions (v1, v0, etc.)
        deprecated_versions = r'/v[01](?:/|$|\?)'
        if re.search(deprecated_versions, path):
            hints.append({
                "type": "deprecated_api",
                "severity": "medium",
                "description": "Deprecated API version detected",
                "url": url,
                "recommendation": "Old API versions may have known vulnerabilities",
            })

        return hints

    def _check_open_redirect(self, url: str, params: Dict) -> List[Dict]:
        """Check for open redirect patterns."""
        hints = []

        redirect_params = [
            "redirect", "redir", "return", "returnurl", "next",
            "continue", "goto", "target", "dest", "destination"
        ]

        for param_name in params:
            if any(redir_param in param_name.lower() for redir_param in redirect_params):
                hints.append({
                    "type": "open_redirect",
                    "severity": "medium",
                    "description": f"Redirect parameter '{param_name}' - potential open redirect",
                    "url": url,
                    "parameter": param_name,
                    "recommendation": "Test if you can redirect to arbitrary external URLs",
                })

        return hints

    def _check_xxe(self, url: str, params: Dict) -> List[Dict]:
        """Check for XML External Entity patterns."""
        hints = []

        # Check for XML-related endpoints
        if any(x in url.lower() for x in ["xml", "soap", "wsdl"]):
            hints.append({
                "type": "xxe",
                "severity": "high",
                "description": "XML processing endpoint - potential XXE vulnerability",
                "url": url,
                "recommendation": "Test with XXE payloads if endpoint processes XML",
            })

        return hints

    def analyze_batch(self, urls: List[str]) -> Dict[str, List[Dict]]:
        """
        Analyze multiple URLs.

        Args:
            urls: List of URLs to analyze

        Returns:
            Results grouped by vulnerability type
        """
        results = {
            "by_type": {},
            "by_severity": {"critical": [], "high": [], "medium": [], "low": []},
            "all": [],
        }

        for url in urls:
            hints = self.analyze_url(url)
            results["all"].extend(hints)

            # Group by type
            for hint in hints:
                hint_type = hint["type"]
                if hint_type not in results["by_type"]:
                    results["by_type"][hint_type] = []
                results["by_type"][hint_type].append(hint)

                # Group by severity
                severity = hint["severity"]
                results["by_severity"][severity].append(hint)

        return results

    def get_summary(self) -> Dict[str, any]:
        """Get summary of all hints."""
        summary = {
            "total_hints": len(self.hints),
            "by_type": {},
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        }

        for hint in self.hints:
            # Count by type
            hint_type = hint["type"]
            summary["by_type"][hint_type] = summary["by_type"].get(hint_type, 0) + 1

            # Count by severity
            severity = hint["severity"]
            summary["by_severity"][severity] += 1

        return summary


def analyze_vulnerabilities(urls: List[str]) -> Dict[str, List[Dict]]:
    """
    Convenience function to analyze URLs for vulnerabilities.

    Args:
        urls: List of URLs to analyze

    Returns:
        Vulnerability hints grouped by type
    """
    hinter = VulnerabilityHinter()
    return hinter.analyze_batch(urls)
