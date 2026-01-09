"""
Secrets detection module.
Scans for API keys, tokens, credentials, and other sensitive information.
"""

import re
from typing import List, Dict, Set, Optional


class SecretsDetector:
    """Detector for secrets and sensitive information."""

    # Secret patterns with their descriptions
    SECRET_PATTERNS = {
        "aws_access_key": {
            "pattern": r'AKIA[0-9A-Z]{16}',
            "description": "AWS Access Key ID",
            "severity": "critical",
        },
        "aws_secret_key": {
            "pattern": r'aws(.{0,20})?[\'"][0-9a-zA-Z/+]{40}[\'"]',
            "description": "AWS Secret Access Key",
            "severity": "critical",
        },
        "github_token": {
            "pattern": r'ghp_[0-9a-zA-Z]{36}',
            "description": "GitHub Personal Access Token",
            "severity": "critical",
        },
        "github_oauth": {
            "pattern": r'gho_[0-9a-zA-Z]{36}',
            "description": "GitHub OAuth Token",
            "severity": "critical",
        },
        "slack_token": {
            "pattern": r'xox[baprs]-([0-9a-zA-Z]{10,48})',
            "description": "Slack Token",
            "severity": "high",
        },
        "slack_webhook": {
            "pattern": r'https://hooks\.slack\.com/services/T[0-9A-Z]{8}/B[0-9A-Z]{8}/[0-9a-zA-Z]{24}',
            "description": "Slack Webhook URL",
            "severity": "high",
        },
        "google_api_key": {
            "pattern": r'AIza[0-9A-Za-z\\-_]{35}',
            "description": "Google API Key",
            "severity": "high",
        },
        "google_oauth": {
            "pattern": r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com',
            "description": "Google OAuth Client ID",
            "severity": "medium",
        },
        "azure_client_secret": {
            "pattern": r'[a-zA-Z0-9~_\-\.]{34,40}',
            "description": "Azure Client Secret",
            "severity": "high",
        },
        "jwt_token": {
            "pattern": r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*',
            "description": "JWT Token",
            "severity": "medium",
        },
        "private_key": {
            "pattern": r'-----BEGIN (RSA |EC |DSA |PGP |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
            "description": "Private Key",
            "severity": "critical",
        },
        "generic_api_key": {
            "pattern": r'[aA][pP][iI][_]?[kK][eE][yY][\'":\s]*[\'"]([0-9a-zA-Z\-_]{20,})[\'"]',
            "description": "Generic API Key",
            "severity": "medium",
        },
        "generic_secret": {
            "pattern": r'[sS][eE][cC][rR][eE][tT][\'":\s]*[\'"]([0-9a-zA-Z\-_]{20,})[\'"]',
            "description": "Generic Secret",
            "severity": "medium",
        },
        "password": {
            "pattern": r'[pP][aA][sS][sS][wW][oO][rR][dD][\'":\s]*[\'"]([^\'"]{8,})[\'"]',
            "description": "Password",
            "severity": "high",
        },
        "stripe_key": {
            "pattern": r'(sk|pk)_(test|live)_[0-9a-zA-Z]{24,}',
            "description": "Stripe API Key",
            "severity": "critical",
        },
        "twilio_api_key": {
            "pattern": r'SK[0-9a-fA-F]{32}',
            "description": "Twilio API Key",
            "severity": "high",
        },
        "mailgun_api_key": {
            "pattern": r'key-[0-9a-zA-Z]{32}',
            "description": "Mailgun API Key",
            "severity": "high",
        },
        "sendgrid_api_key": {
            "pattern": r'SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}',
            "description": "SendGrid API Key",
            "severity": "high",
        },
        "facebook_access_token": {
            "pattern": r'EAACEdEose0cBA[0-9A-Za-z]+',
            "description": "Facebook Access Token",
            "severity": "medium",
        },
        "twitter_access_token": {
            "pattern": r'[1-9][0-9]+-[0-9a-zA-Z]{40}',
            "description": "Twitter Access Token",
            "severity": "medium",
        },
        "heroku_api_key": {
            "pattern": r'[hH][eE][rR][oO][kK][uU].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}',
            "description": "Heroku API Key",
            "severity": "high",
        },
        "mailchimp_api_key": {
            "pattern": r'[0-9a-f]{32}-us[0-9]{1,2}',
            "description": "Mailchimp API Key",
            "severity": "medium",
        },
        "basic_auth": {
            "pattern": r'://[a-zA-Z0-9]+:[a-zA-Z0-9]+@',
            "description": "Basic Auth in URL",
            "severity": "high",
        },
        "connection_string": {
            "pattern": r'(mongodb|mysql|postgresql|redis)://[^\s\'"<>]+',
            "description": "Database Connection String",
            "severity": "high",
        },
    }

    def __init__(self):
        """Initialize secrets detector."""
        self.findings: List[Dict] = []

    def scan_content(self, content: str, source: Optional[str] = None) -> List[Dict]:
        """
        Scan content for secrets.

        Args:
            content: Content to scan
            source: Source identifier (e.g., URL or filename)

        Returns:
            List of detected secrets
        """
        findings = []

        for secret_type, info in self.SECRET_PATTERNS.items():
            pattern = info["pattern"]
            matches = re.finditer(pattern, content)

            for match in matches:
                # Extract the matched secret
                secret_value = match.group(0)

                # Try to get context (surrounding text)
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end]

                finding = {
                    "type": secret_type,
                    "description": info["description"],
                    "severity": info["severity"],
                    "value": secret_value,
                    "context": context,
                    "position": match.start(),
                    "source": source,
                }

                findings.append(finding)
                self.findings.append(finding)

        return findings

    def scan_url(self, url: str) -> List[Dict]:
        """
        Scan URL for secrets.

        Args:
            url: URL to scan

        Returns:
            List of detected secrets
        """
        return self.scan_content(url, source=f"URL: {url}")

    def scan_batch(self, contents: Dict[str, str]) -> Dict[str, List[Dict]]:
        """
        Scan multiple content sources.

        Args:
            contents: Dictionary mapping source names to content

        Returns:
            Dictionary mapping sources to findings
        """
        results = {}

        for source, content in contents.items():
            findings = self.scan_content(content, source)
            if findings:
                results[source] = findings

        return results

    def get_summary(self) -> Dict[str, any]:
        """
        Get summary of all findings.

        Returns:
            Summary statistics
        """
        summary = {
            "total_findings": len(self.findings),
            "by_severity": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "by_type": {},
        }

        for finding in self.findings:
            # Count by severity
            severity = finding["severity"]
            summary["by_severity"][severity] += 1

            # Count by type
            secret_type = finding["type"]
            summary["by_type"][secret_type] = summary["by_type"].get(secret_type, 0) + 1

        return summary

    def filter_by_severity(self, min_severity: str = "medium") -> List[Dict]:
        """
        Filter findings by minimum severity.

        Args:
            min_severity: Minimum severity level (critical, high, medium, low)

        Returns:
            Filtered findings
        """
        severity_order = {"critical": 3, "high": 2, "medium": 1, "low": 0}
        min_level = severity_order.get(min_severity, 0)

        return [
            f for f in self.findings
            if severity_order.get(f["severity"], 0) >= min_level
        ]

    def deduplicate_findings(self) -> List[Dict]:
        """
        Remove duplicate findings.

        Returns:
            Deduplicated findings
        """
        seen = set()
        unique_findings = []

        for finding in self.findings:
            # Create a key based on type and value
            key = (finding["type"], finding["value"])
            if key not in seen:
                seen.add(key)
                unique_findings.append(finding)

        return unique_findings


def detect_secrets(content: str, source: Optional[str] = None) -> List[Dict]:
    """
    Convenience function to detect secrets in content.

    Args:
        content: Content to scan
        source: Source identifier

    Returns:
        List of detected secrets
    """
    detector = SecretsDetector()
    return detector.scan_content(content, source)
