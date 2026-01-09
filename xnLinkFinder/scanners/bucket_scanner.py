"""
Cloud Bucket Scanner

Scans for open or misconfigured cloud storage buckets:
- AWS S3 buckets
- Azure Blob Storage
- Google Cloud Storage (GCP)
- Tests for listing, read, and write permissions
"""

import requests
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse
import re


class BucketScanner:
    """Scanner for cloud storage bucket misconfigurations"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize bucket scanner
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.found_buckets = set()
        
    def scan_s3(self, bucket_name: str, region: str = 'us-east-1') -> Optional[Dict]:
        """
        Scan an S3 bucket for misconfigurations
        
        Args:
            bucket_name: Name of the S3 bucket
            region: AWS region (default: us-east-1)
            
        Returns:
            Vulnerability details if found
        """
        urls = [
            f"https://{bucket_name}.s3.amazonaws.com",
            f"https://s3.amazonaws.com/{bucket_name}",
            f"https://{bucket_name}.s3-{region}.amazonaws.com",
            f"https://s3-{region}.amazonaws.com/{bucket_name}",
        ]
        
        for url in urls:
            try:
                response = requests.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=False
                )
                
                if response.status_code == 200:
                    # Check if we can list contents
                    if self._is_s3_listing(response.text):
                        return {
                            'bucket': bucket_name,
                            'type': 'S3_BUCKET_LISTING',
                            'url': url,
                            'severity': 'HIGH',
                            'description': 'S3 bucket allows public listing',
                            'permissions': ['LIST', 'READ'],
                        }
                elif response.status_code == 403:
                    # Bucket exists but access denied
                    return {
                        'bucket': bucket_name,
                        'type': 'S3_BUCKET_EXISTS',
                        'url': url,
                        'severity': 'INFO',
                        'description': 'S3 bucket exists but is not publicly accessible',
                    }
                    
            except requests.RequestException:
                continue
                
        return None
    
    def scan_azure_blob(self, account_name: str, 
                        container_name: str = None) -> Optional[Dict]:
        """
        Scan Azure Blob Storage for misconfigurations
        
        Args:
            account_name: Azure storage account name
            container_name: Optional container name
            
        Returns:
            Vulnerability details if found
        """
        if container_name:
            url = f"https://{account_name}.blob.core.windows.net/{container_name}?restype=container&comp=list"
        else:
            url = f"https://{account_name}.blob.core.windows.net/?comp=list"
            
        try:
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    'account': account_name,
                    'container': container_name,
                    'type': 'AZURE_BLOB_LISTING',
                    'url': url,
                    'severity': 'HIGH',
                    'description': 'Azure Blob Storage allows public listing',
                    'permissions': ['LIST', 'READ'],
                }
            elif response.status_code == 403:
                return {
                    'account': account_name,
                    'container': container_name,
                    'type': 'AZURE_BLOB_EXISTS',
                    'url': url,
                    'severity': 'INFO',
                    'description': 'Azure Blob Storage exists but is not publicly accessible',
                }
                
        except requests.RequestException:
            pass
            
        return None
    
    def scan_gcp_bucket(self, bucket_name: str) -> Optional[Dict]:
        """
        Scan a Google Cloud Storage bucket
        
        Args:
            bucket_name: GCP bucket name
            
        Returns:
            Vulnerability details if found
        """
        url = f"https://storage.googleapis.com/{bucket_name}"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                # Check if we can list contents
                if self._is_gcp_listing(response.text):
                    return {
                        'bucket': bucket_name,
                        'type': 'GCP_BUCKET_LISTING',
                        'url': url,
                        'severity': 'HIGH',
                        'description': 'GCP bucket allows public listing',
                        'permissions': ['LIST', 'READ'],
                    }
            elif response.status_code == 403:
                return {
                    'bucket': bucket_name,
                    'type': 'GCP_BUCKET_EXISTS',
                    'url': url,
                    'severity': 'INFO',
                    'description': 'GCP bucket exists but is not publicly accessible',
                }
                
        except requests.RequestException:
            pass
            
        return None
    
    def extract_bucket_names(self, text: str) -> Set[str]:
        """
        Extract potential bucket names from text
        
        Args:
            text: Text to search for bucket names
            
        Returns:
            Set of potential bucket names
        """
        buckets = set()
        
        # S3 patterns
        s3_patterns = [
            r'https?://([a-z0-9\-\.]+)\.s3\.amazonaws\.com',
            r'https?://s3\.amazonaws\.com/([a-z0-9\-\.]+)',
            r'https?://([a-z0-9\-\.]+)\.s3-[a-z0-9\-]+\.amazonaws\.com',
            r's3://([a-z0-9\-\.]+)',
        ]
        
        for pattern in s3_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            buckets.update(matches)
            
        # Azure patterns
        azure_pattern = r'https?://([a-z0-9]+)\.blob\.core\.windows\.net'
        matches = re.findall(azure_pattern, text, re.IGNORECASE)
        buckets.update(matches)
        
        # GCP patterns
        gcp_pattern = r'https?://storage\.googleapis\.com/([a-z0-9\-\_\.]+)'
        matches = re.findall(gcp_pattern, text, re.IGNORECASE)
        buckets.update(matches)
        
        return buckets
    
    def _is_s3_listing(self, content: str) -> bool:
        """Check if content is an S3 bucket listing"""
        return '<ListBucketResult' in content or '<Contents>' in content
    
    def _is_gcp_listing(self, content: str) -> bool:
        """Check if content is a GCP bucket listing"""
        return '<ListBucketResult' in content or 'storage.googleapis.com' in content


def scan_buckets(bucket_names: List[str], 
                 cloud_provider: str = 'auto', 
                 **kwargs) -> Dict[str, Dict]:
    """
    Convenience function to scan multiple buckets
    
    Args:
        bucket_names: List of bucket names to scan
        cloud_provider: 's3', 'azure', 'gcp', or 'auto' (default)
        **kwargs: Additional arguments for BucketScanner
        
    Returns:
        Dictionary mapping bucket names to vulnerabilities
    """
    scanner = BucketScanner(**kwargs)
    results = {}
    
    for bucket_name in bucket_names:
        try:
            if cloud_provider == 'auto' or cloud_provider == 's3':
                vuln = scanner.scan_s3(bucket_name)
                if vuln:
                    results[bucket_name] = vuln
                    continue
                    
            if cloud_provider == 'auto' or cloud_provider == 'gcp':
                vuln = scanner.scan_gcp_bucket(bucket_name)
                if vuln:
                    results[bucket_name] = vuln
                    continue
                    
        except Exception as e:
            print(f"[!] Error scanning bucket {bucket_name}: {str(e)}")
            
    return results
