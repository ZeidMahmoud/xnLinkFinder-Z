"""
BOLA/BFLA Detector

Tests for authorization vulnerabilities:
- Broken Object Level Authorization (BOLA)
- Broken Function Level Authorization (BFLA)
- ID enumeration
"""

import requests
from typing import Dict, List, Optional
import re


class BOLABFLADetector:
    """Detect BOLA and BFLA vulnerabilities"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def test_bola(self, url: str, user_tokens: List[str],
                 test_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Test for BOLA by accessing resources with different user tokens
        
        Args:
            url: API endpoint with ID parameter
            user_tokens: List of authentication tokens for different users
            test_ids: Optional list of IDs to test
            
        Returns:
            List of BOLA vulnerabilities found
        """
        vulnerabilities = []
        
        if not test_ids:
            test_ids = self._extract_ids(url) or ['1', '2', '100']
            
        for resource_id in test_ids:
            # Replace ID in URL
            test_url = re.sub(r'/\d+', f'/{resource_id}', url)
            
            responses = {}
            for i, token in enumerate(user_tokens):
                try:
                    headers = {'Authorization': f'Bearer {token}'}
                    response = requests.get(
                        test_url, headers=headers,
                        timeout=self.timeout, verify=self.verify_ssl
                    )
                    responses[f'user_{i}'] = {
                        'status': response.status_code,
                        'content_length': len(response.text),
                    }
                except requests.RequestException:
                    pass
                    
            # Check if multiple users can access same resource
            if len([r for r in responses.values() if r['status'] == 200]) > 1:
                vulnerabilities.append({
                    'url': test_url,
                    'resource_id': resource_id,
                    'type': 'BOLA',
                    'severity': 'HIGH',
                    'description': 'Multiple users can access same resource',
                    'responses': responses,
                })
                
        return vulnerabilities
    
    def test_bfla(self, privileged_endpoints: List[str],
                 regular_token: str) -> List[Dict]:
        """
        Test for BFLA by accessing privileged endpoints with regular user
        
        Args:
            privileged_endpoints: List of admin/privileged endpoints
            regular_token: Regular user authentication token
            
        Returns:
            List of BFLA vulnerabilities
        """
        vulnerabilities = []
        
        for endpoint in privileged_endpoints:
            try:
                headers = {'Authorization': f'Bearer {regular_token}'}
                response = requests.get(
                    endpoint, headers=headers,
                    timeout=self.timeout, verify=self.verify_ssl
                )
                
                if response.status_code == 200:
                    vulnerabilities.append({
                        'url': endpoint,
                        'type': 'BFLA',
                        'severity': 'CRITICAL',
                        'description': 'Regular user can access privileged endpoint',
                        'status_code': response.status_code,
                    })
                    
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _extract_ids(self, url: str) -> Optional[List[str]]:
        """Extract numeric IDs from URL"""
        ids = re.findall(r'/(\d+)', url)
        return ids if ids else None


def test_authorization(urls: List[str], user_tokens: List[str], **kwargs) -> Dict:
    """Test multiple URLs for authorization issues"""
    detector = BOLABFLADetector(**kwargs)
    results = {'bola': {}, 'bfla': {}}
    
    for url in urls:
        bola_vulns = detector.test_bola(url, user_tokens)
        if bola_vulns:
            results['bola'][url] = bola_vulns
            
    return results
