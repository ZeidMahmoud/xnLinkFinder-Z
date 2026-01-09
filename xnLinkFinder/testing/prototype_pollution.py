"""
Prototype Pollution Scanner

Detects JavaScript prototype pollution:
- DOM-based pollution
- Server-side pollution detection
- Payload generation
"""

import requests
from typing import Dict, List, Optional


class PrototypePollutionScanner:
    """Scanner for prototype pollution vulnerabilities"""
    
    PAYLOADS = [
        {'__proto__[test]': 'polluted'},
        {'constructor[prototype][test]': 'polluted'},
        {'__proto__.test': 'polluted'},
    ]
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def scan(self, url: str, params: Optional[Dict] = None) -> List[Dict]:
        """Scan for prototype pollution"""
        vulnerabilities = []
        
        for payload in self.PAYLOADS:
            vuln = self._test_payload(url, payload, params)
            if vuln:
                vulnerabilities.append(vuln)
                
        return vulnerabilities
    
    def _test_payload(self, url: str, payload: Dict,
                     params: Optional[Dict]) -> Optional[Dict]:
        """Test a pollution payload"""
        test_params = params.copy() if params else {}
        test_params.update(payload)
        
        try:
            response = requests.get(
                url, params=test_params,
                timeout=self.timeout, verify=self.verify_ssl
            )
            
            # Check for pollution indicators
            if 'polluted' in response.text or 'test' in response.headers:
                return {
                    'url': url,
                    'payload': payload,
                    'type': 'PROTOTYPE_POLLUTION',
                    'severity': 'HIGH',
                    'description': 'Potential prototype pollution detected',
                }
                
        except requests.RequestException:
            pass
            
        return None


def scan_prototype_pollution(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """Scan multiple URLs"""
    scanner = PrototypePollutionScanner(**kwargs)
    return {url: scanner.scan(url) for url in urls}
