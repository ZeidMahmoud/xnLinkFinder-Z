"""
IDOR Automation

Automated IDOR (Insecure Direct Object Reference) testing:
- ID pattern detection
- Multi-user testing support
- Automated enumeration
"""

import requests
from typing import Dict, List, Optional
import re


class IDORAutomation:
    """Automate IDOR testing"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def test(self, url: str, auth_tokens: List[str],
            id_range: Optional[range] = None) -> List[Dict]:
        """
        Automated IDOR testing
        
        Args:
            url: URL template with {id} placeholder or numeric ID
            auth_tokens: List of authentication tokens for different users
            id_range: Range of IDs to test
            
        Returns:
            List of IDOR vulnerabilities
        """
        vulnerabilities = []
        
        if id_range is None:
            id_range = range(1, 101)  # Default: test 1-100
            
        for test_id in id_range:
            # Replace ID in URL
            if '{id}' in url:
                test_url = url.format(id=test_id)
            else:
                test_url = re.sub(r'/\d+', f'/{test_id}', url)
                
            # Test with each user token
            results = {}
            for i, token in enumerate(auth_tokens):
                try:
                    headers = {'Authorization': f'Bearer {token}'}
                    response = requests.get(
                        test_url, headers=headers,
                        timeout=self.timeout, verify=self.verify_ssl
                    )
                    
                    results[f'user_{i}'] = {
                        'status': response.status_code,
                        'accessible': response.status_code == 200,
                    }
                    
                except requests.RequestException:
                    results[f'user_{i}'] = {'accessible': False}
                    
            # Check if resource is accessible by multiple users
            accessible_count = sum(1 for r in results.values() if r.get('accessible'))
            
            if accessible_count > 1:
                vulnerabilities.append({
                    'url': test_url,
                    'id': test_id,
                    'type': 'IDOR',
                    'severity': 'HIGH',
                    'description': f'Resource {test_id} accessible by {accessible_count} users',
                    'accessible_by': accessible_count,
                })
                
        return vulnerabilities
    
    def detect_id_patterns(self, urls: List[str]) -> Dict[str, str]:
        """Detect ID patterns in URLs"""
        patterns = {}
        
        for url in urls:
            # Numeric IDs
            if re.search(r'/\d+', url):
                patterns[url] = 'numeric'
            # UUID
            elif re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', url, re.I):
                patterns[url] = 'uuid'
            # Base64
            elif re.search(r'[A-Za-z0-9+/=]{16,}', url):
                patterns[url] = 'base64'
            else:
                patterns[url] = 'unknown'
                
        return patterns


def test_idor(urls: List[str], auth_tokens: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """Test multiple URLs for IDOR"""
    automation = IDORAutomation(**kwargs)
    return {url: automation.test(url, auth_tokens, range(1, 11)) for url in urls}
