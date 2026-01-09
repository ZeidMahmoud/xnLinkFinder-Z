"""
Cloud service integration detection module.
Automatically identifies cloud provider endpoints (AWS, Azure, GCP, Firebase).
"""

import re
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse


class CloudServiceDetector:
    """Detector for cloud service endpoints and resources."""

    # AWS patterns
    AWS_PATTERNS = {
        "s3_bucket": [
            r'https?://([a-z0-9][a-z0-9\-]*[a-z0-9])\.s3\.([a-z0-9\-]+)\.amazonaws\.com',
            r'https?://s3\.([a-z0-9\-]+)\.amazonaws\.com/([a-z0-9][a-z0-9\-]*[a-z0-9])',
            r'https?://([a-z0-9][a-z0-9\-]*[a-z0-9])\.s3\.amazonaws\.com',
            r's3://([a-z0-9][a-z0-9\-]*[a-z0-9])',
        ],
        "lambda": [
            r'https?://([a-z0-9\-]+)\.lambda-url\.([a-z0-9\-]+)\.on\.aws',
            r'https?://([a-z0-9\-]+)\.lambda\.([a-z0-9\-]+)\.amazonaws\.com',
        ],
        "api_gateway": [
            r'https?://([a-z0-9]+)\.execute-api\.([a-z0-9\-]+)\.amazonaws\.com',
        ],
        "cloudfront": [
            r'https?://([a-z0-9]+)\.cloudfront\.net',
        ],
        "dynamodb": [
            r'https?://dynamodb\.([a-z0-9\-]+)\.amazonaws\.com',
        ],
        "cognito": [
            r'https?://([a-z0-9\-]+)\.auth\.([a-z0-9\-]+)\.amazoncognito\.com',
        ],
        "elasticbeanstalk": [
            r'https?://([a-z0-9\-]+)\.([a-z0-9\-]+)\.elasticbeanstalk\.com',
        ],
    }

    # Azure patterns
    AZURE_PATTERNS = {
        "blob_storage": [
            r'https?://([a-z0-9]+)\.blob\.core\.windows\.net',
        ],
        "functions": [
            r'https?://([a-z0-9\-]+)\.azurewebsites\.net/api',
        ],
        "app_service": [
            r'https?://([a-z0-9\-]+)\.azurewebsites\.net',
        ],
        "cosmos_db": [
            r'https?://([a-z0-9\-]+)\.documents\.azure\.com',
        ],
        "api_management": [
            r'https?://([a-z0-9\-]+)\.azure-api\.net',
        ],
    }

    # GCP patterns
    GCP_PATTERNS = {
        "cloud_storage": [
            r'https?://storage\.googleapis\.com/([a-z0-9][a-z0-9_\-\.]*[a-z0-9])',
            r'https?://([a-z0-9][a-z0-9_\-\.]*[a-z0-9])\.storage\.googleapis\.com',
            r'gs://([a-z0-9][a-z0-9_\-\.]*[a-z0-9])',
        ],
        "cloud_functions": [
            r'https?://([a-z0-9\-]+)-([a-z0-9]+)\.cloudfunctions\.net',
            r'https?://([a-z0-9\-]+)\.([a-z0-9\-]+)\.run\.app',
        ],
        "app_engine": [
            r'https?://([a-z0-9\-]+)\.appspot\.com',
        ],
        "firebase": [
            r'https?://([a-z0-9\-]+)\.firebaseapp\.com',
            r'https?://([a-z0-9\-]+)\.web\.app',
        ],
    }

    # Firebase patterns (separate for clarity)
    FIREBASE_PATTERNS = {
        "hosting": [
            r'https?://([a-z0-9\-]+)\.firebaseapp\.com',
            r'https?://([a-z0-9\-]+)\.web\.app',
        ],
        "database": [
            r'https?://([a-z0-9\-]+)\.firebaseio\.com',
        ],
        "storage": [
            r'https?://firebasestorage\.googleapis\.com/v0/b/([a-z0-9\-_\.]+)',
        ],
        "functions": [
            r'https?://([a-z0-9\-]+)-([a-z0-9]+)\.cloudfunctions\.net',
        ],
    }

    def __init__(self):
        """Initialize cloud service detector."""
        self.detected_services: Dict[str, List[Dict]] = {
            "aws": [],
            "azure": [],
            "gcp": [],
            "firebase": [],
        }

    def detect_aws_services(self, content: str) -> List[Dict[str, str]]:
        """
        Detect AWS services in content.

        Args:
            content: Text content to analyze

        Returns:
            List of detected AWS services
        """
        detected = []

        for service_type, patterns in self.AWS_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    detected.append({
                        "provider": "aws",
                        "service": service_type,
                        "url": match.group(0),
                        "resource": match.group(1) if match.lastindex >= 1 else None,
                        "region": match.group(2) if match.lastindex >= 2 else None,
                    })

        return detected

    def detect_azure_services(self, content: str) -> List[Dict[str, str]]:
        """
        Detect Azure services in content.

        Args:
            content: Text content to analyze

        Returns:
            List of detected Azure services
        """
        detected = []

        for service_type, patterns in self.AZURE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    detected.append({
                        "provider": "azure",
                        "service": service_type,
                        "url": match.group(0),
                        "resource": match.group(1) if match.lastindex >= 1 else None,
                    })

        return detected

    def detect_gcp_services(self, content: str) -> List[Dict[str, str]]:
        """
        Detect GCP services in content.

        Args:
            content: Text content to analyze

        Returns:
            List of detected GCP services
        """
        detected = []

        for service_type, patterns in self.GCP_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    detected.append({
                        "provider": "gcp",
                        "service": service_type,
                        "url": match.group(0),
                        "resource": match.group(1) if match.lastindex >= 1 else None,
                        "region": match.group(2) if match.lastindex >= 2 else None,
                    })

        return detected

    def detect_firebase_services(self, content: str) -> List[Dict[str, str]]:
        """
        Detect Firebase services in content.

        Args:
            content: Text content to analyze

        Returns:
            List of detected Firebase services
        """
        detected = []

        for service_type, patterns in self.FIREBASE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    detected.append({
                        "provider": "firebase",
                        "service": service_type,
                        "url": match.group(0),
                        "resource": match.group(1) if match.lastindex >= 1 else None,
                    })

        return detected

    def detect_all(self, content: str) -> Dict[str, List[Dict]]:
        """
        Detect all cloud services in content.

        Args:
            content: Text content to analyze

        Returns:
            Dictionary with detected services by provider
        """
        results = {
            "aws": self.detect_aws_services(content),
            "azure": self.detect_azure_services(content),
            "gcp": self.detect_gcp_services(content),
            "firebase": self.detect_firebase_services(content),
        }

        return results

    def get_unique_resources(self, detections: Dict[str, List[Dict]]) -> Dict[str, Set[str]]:
        """
        Get unique resources from detections.

        Args:
            detections: Detection results

        Returns:
            Dictionary of unique resources per provider
        """
        unique = {}

        for provider, services in detections.items():
            unique[provider] = set()
            for service in services:
                if service.get("resource"):
                    unique[provider].add(service["resource"])

        return unique

    def analyze_urls(self, urls: List[str]) -> Dict[str, List[Dict]]:
        """
        Analyze a list of URLs for cloud services.

        Args:
            urls: List of URLs to analyze

        Returns:
            Detection results
        """
        # Combine all URLs into a single string for analysis
        content = "\n".join(urls)
        return self.detect_all(content)

    def get_summary(self, detections: Dict[str, List[Dict]]) -> Dict[str, int]:
        """
        Get summary of detections.

        Args:
            detections: Detection results

        Returns:
            Summary with counts per provider
        """
        summary = {}

        for provider, services in detections.items():
            summary[provider] = len(services)

            # Count by service type
            service_counts = {}
            for service in services:
                service_type = service.get("service", "unknown")
                service_counts[service_type] = service_counts.get(service_type, 0) + 1

            if service_counts:
                summary[f"{provider}_by_service"] = service_counts

        return summary


def detect_cloud_services(content: str) -> Dict[str, List[Dict]]:
    """
    Convenience function to detect cloud services.

    Args:
        content: Content to analyze

    Returns:
        Detection results
    """
    detector = CloudServiceDetector()
    return detector.detect_all(content)
