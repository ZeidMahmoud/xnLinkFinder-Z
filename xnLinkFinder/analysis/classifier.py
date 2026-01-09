"""
Link classification and prioritization module.
Automatically categorizes discovered links by type and security relevance.
"""

import re
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse, parse_qs


class LinkClassifier:
    """Classifier for categorizing and prioritizing discovered links."""

    # Category patterns
    CATEGORIES = {
        "authentication": {
            "patterns": [
                r'/login', r'/signin', r'/sign-in', r'/auth', r'/authenticate',
                r'/oauth', r'/sso', r'/saml', r'/jwt', r'/token',
                r'/logout', r'/signout', r'/sign-out',
            ],
            "priority": "high",
        },
        "admin": {
            "patterns": [
                r'/admin', r'/administrator', r'/manage', r'/management',
                r'/dashboard', r'/console', r'/control', r'/panel',
                r'/cpanel', r'/phpmyadmin', r'/wp-admin',
            ],
            "priority": "critical",
        },
        "api": {
            "patterns": [
                r'/api/', r'/v\d+/', r'/rest/', r'/graphql', r'/gql',
                r'/json', r'/xml', r'/rpc', r'/soap', r'/ws/',
            ],
            "priority": "high",
        },
        "upload": {
            "patterns": [
                r'/upload', r'/file', r'/files', r'/attachments',
                r'/media', r'/document', r'/documents',
            ],
            "priority": "high",
        },
        "user": {
            "patterns": [
                r'/user', r'/users', r'/profile', r'/account', r'/settings',
                r'/preferences', r'/member', r'/customer',
            ],
            "priority": "medium",
        },
        "config": {
            "patterns": [
                r'/config', r'/configuration', r'/settings',
                r'\.env', r'\.config', r'/properties',
                r'/web\.config', r'/app\.config',
            ],
            "priority": "critical",
        },
        "backup": {
            "patterns": [
                r'\.bak', r'\.backup', r'\.old', r'\.orig', r'\.save',
                r'\.swp', r'~$', r'/backup', r'/backups',
            ],
            "priority": "high",
        },
        "debug": {
            "patterns": [
                r'/debug', r'/test', r'/dev', r'/development',
                r'/staging', r'/trace', r'/log', r'/logs',
            ],
            "priority": "high",
        },
        "git": {
            "patterns": [
                r'\.git/', r'\.svn/', r'\.hg/', r'\.bzr/',
                r'/\.git', r'/\.svn',
            ],
            "priority": "critical",
        },
        "source": {
            "patterns": [
                r'\.php', r'\.asp', r'\.aspx', r'\.jsp', r'\.jspx',
                r'\.py', r'\.rb', r'\.pl', r'\.cgi',
            ],
            "priority": "medium",
        },
        "static": {
            "patterns": [
                r'\.css', r'\.js', r'\.jpg', r'\.jpeg', r'\.png',
                r'\.gif', r'\.svg', r'\.ico', r'\.woff', r'\.ttf',
            ],
            "priority": "low",
        },
    }

    def __init__(self):
        """Initialize link classifier."""
        self.classified_links: Dict[str, List[str]] = {}

    def classify_url(self, url: str) -> Dict[str, any]:
        """
        Classify a single URL.

        Args:
            url: URL to classify

        Returns:
            Classification result
        """
        parsed = urlparse(url)
        path = parsed.path.lower()
        query = parsed.query.lower()
        full_url = url.lower()

        categories = set()
        max_priority = "low"

        # Check against patterns
        for category, info in self.CATEGORIES.items():
            for pattern in info["patterns"]:
                if re.search(pattern, full_url, re.IGNORECASE):
                    categories.add(category)
                    
                    # Update priority
                    current_priority = info["priority"]
                    if self._compare_priority(current_priority, max_priority) > 0:
                        max_priority = current_priority

        # Check for parameters that might indicate vulnerabilities
        vuln_indicators = self._check_vuln_indicators(url)

        # Check for sensitive patterns
        sensitive = self._check_sensitive_patterns(url)

        return {
            "url": url,
            "categories": list(categories),
            "priority": max_priority,
            "vuln_indicators": vuln_indicators,
            "has_parameters": bool(parsed.query),
            "is_sensitive": sensitive,
        }

    def _compare_priority(self, p1: str, p2: str) -> int:
        """
        Compare two priority levels.

        Returns:
            1 if p1 > p2, -1 if p1 < p2, 0 if equal
        """
        priority_order = {"critical": 3, "high": 2, "medium": 1, "low": 0}
        return priority_order.get(p1, 0) - priority_order.get(p2, 0)

    def _check_vuln_indicators(self, url: str) -> List[str]:
        """
        Check for vulnerability indicators in URL.

        Args:
            url: URL to check

        Returns:
            List of potential vulnerability types
        """
        indicators = []
        parsed = urlparse(url)

        # Check for numeric IDs (potential IDOR)
        if re.search(r'/\d+(?:/|$)', parsed.path):
            indicators.append("idor")

        # Check for file operations
        file_params = ["file", "path", "dir", "folder", "download", "upload"]
        if any(param in url.lower() for param in file_params):
            indicators.append("file_operation")

        # Check for URL parameters (potential SSRF/LFI)
        url_params = ["url", "uri", "redirect", "callback", "return", "next"]
        if any(param in url.lower() for param in url_params):
            indicators.append("ssrf_lfi")

        # Check for SQL-related parameters
        sql_params = ["id", "user", "query", "search", "filter"]
        if any(param in url.lower() for param in sql_params):
            indicators.append("sqli")

        # Check for XSS vectors
        xss_params = ["q", "search", "query", "keyword", "name"]
        if any(param in url.lower() for param in xss_params):
            indicators.append("xss")

        return indicators

    def _check_sensitive_patterns(self, url: str) -> bool:
        """
        Check if URL contains sensitive patterns.

        Args:
            url: URL to check

        Returns:
            True if sensitive patterns found
        """
        sensitive_patterns = [
            r'password', r'passwd', r'pwd', r'secret', r'token',
            r'apikey', r'api_key', r'private', r'credential',
            r'auth', r'session', r'cookie', r'jwt',
        ]

        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in sensitive_patterns)

    def classify_batch(self, urls: List[str]) -> Dict[str, List[Dict]]:
        """
        Classify multiple URLs.

        Args:
            urls: List of URLs to classify

        Returns:
            Classification results grouped by category
        """
        results = {
            "by_category": {},
            "by_priority": {"critical": [], "high": [], "medium": [], "low": []},
            "all": [],
        }

        for url in urls:
            classification = self.classify_url(url)
            results["all"].append(classification)

            # Group by category
            for category in classification["categories"]:
                if category not in results["by_category"]:
                    results["by_category"][category] = []
                results["by_category"][category].append(classification)

            # Group by priority
            priority = classification["priority"]
            results["by_priority"][priority].append(classification)

        return results

    def get_high_priority_urls(self, urls: List[str]) -> List[str]:
        """
        Get high-priority URLs from a list.

        Args:
            urls: List of URLs

        Returns:
            Filtered list of high-priority URLs
        """
        high_priority = []

        for url in urls:
            classification = self.classify_url(url)
            if classification["priority"] in ["critical", "high"]:
                high_priority.append(url)

        return high_priority


def classify_links(urls: List[str]) -> Dict[str, List[Dict]]:
    """
    Convenience function to classify links.

    Args:
        urls: List of URLs to classify

    Returns:
        Classification results
    """
    classifier = LinkClassifier()
    return classifier.classify_batch(urls)
