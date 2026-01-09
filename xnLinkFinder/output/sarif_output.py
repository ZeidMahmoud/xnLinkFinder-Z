"""
SARIF (Static Analysis Results Interchange Format) output formatter.
For integration with security tooling and CI/CD pipelines.
"""

import json
from typing import List, Dict, Optional
from datetime import datetime


class SARIFOutputFormatter:
    """Formatter for SARIF 2.1.0 format."""

    def __init__(self, tool_name: str = "xnLinkFinder-Z", tool_version: str = "7.18"):
        """
        Initialize SARIF formatter.

        Args:
            tool_name: Tool name
            tool_version: Tool version
        """
        self.tool_name = tool_name
        self.tool_version = tool_version
        self.results = []

    def add_result(
        self,
        rule_id: str,
        message: str,
        uri: str,
        level: str = "warning",
        properties: Optional[Dict] = None,
    ):
        """
        Add a SARIF result.

        Args:
            rule_id: Rule identifier
            message: Result message
            uri: URI where issue was found
            level: Severity level (error, warning, note)
            properties: Additional properties
        """
        result = {
            "ruleId": rule_id,
            "level": level,
            "message": {
                "text": message
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": uri
                        }
                    }
                }
            ]
        }

        if properties:
            result["properties"] = properties

        self.results.append(result)

    def add_vulnerability_hint(self, hint: Dict):
        """
        Add a vulnerability hint as a SARIF result.

        Args:
            hint: Vulnerability hint dictionary
        """
        # Map severity to SARIF level
        severity_map = {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "note",
        }

        level = severity_map.get(hint.get("severity", "medium"), "warning")
        
        self.add_result(
            rule_id=hint.get("type", "unknown"),
            message=hint.get("description", ""),
            uri=hint.get("url", ""),
            level=level,
            properties={
                "severity": hint.get("severity"),
                "recommendation": hint.get("recommendation"),
                "parameter": hint.get("parameter"),
            }
        )

    def add_secret_finding(self, secret: Dict):
        """
        Add a secret detection as a SARIF result.

        Args:
            secret: Secret dictionary
        """
        severity_map = {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "note",
        }

        level = severity_map.get(secret.get("severity", "high"), "error")

        self.add_result(
            rule_id=f"secret.{secret.get('type', 'unknown')}",
            message=f"{secret.get('description', 'Secret detected')}: {secret.get('value', '')}",
            uri=secret.get("source", ""),
            level=level,
            properties={
                "secret_type": secret.get("type"),
                "context": secret.get("context"),
            }
        )

    def to_sarif(self) -> Dict:
        """
        Convert to SARIF format.

        Returns:
            SARIF dictionary
        """
        return {
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": self.tool_name,
                            "version": self.tool_version,
                            "informationUri": "https://github.com/ZeidMahmoud/xnLinkFinder-Z",
                            "rules": self._generate_rules()
                        }
                    },
                    "results": self.results
                }
            ]
        }

    def _generate_rules(self) -> List[Dict]:
        """
        Generate SARIF rules from results.

        Returns:
            List of rule definitions
        """
        # Extract unique rule IDs
        rule_ids = set(result["ruleId"] for result in self.results)
        
        # Define rules
        rules = []
        for rule_id in rule_ids:
            rules.append({
                "id": rule_id,
                "name": rule_id.replace("_", " ").title(),
                "shortDescription": {
                    "text": f"{rule_id} detected"
                }
            })
        
        return rules

    def to_json(self, indent: int = 2) -> str:
        """
        Convert to JSON string.

        Args:
            indent: JSON indentation

        Returns:
            JSON string
        """
        return json.dumps(self.to_sarif(), indent=indent)

    def save_to_file(self, filepath: str, indent: int = 2):
        """
        Save to SARIF file.

        Args:
            filepath: Output file path
            indent: JSON indentation
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_sarif(), f, indent=indent)


def create_sarif_output(
    vulnerability_hints: List[Dict],
    secrets: List[Dict],
    tool_name: str = "xnLinkFinder-Z",
    tool_version: str = "7.18",
) -> str:
    """
    Convenience function to create SARIF output.

    Args:
        vulnerability_hints: List of vulnerability hints
        secrets: List of detected secrets
        tool_name: Tool name
        tool_version: Tool version

    Returns:
        SARIF JSON string
    """
    formatter = SARIFOutputFormatter(tool_name, tool_version)
    
    # Add vulnerability hints
    for hint in vulnerability_hints:
        formatter.add_vulnerability_hint(hint)
    
    # Add secrets
    for secret in secrets:
        formatter.add_secret_finding(secret)
    
    return formatter.to_json()
