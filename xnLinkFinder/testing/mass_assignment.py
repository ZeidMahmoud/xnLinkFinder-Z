"""
Mass Assignment Detector

Detects mass assignment vulnerabilities:
- Hidden parameter discovery
- Parameter binding testing
- Privilege escalation detection
"""

import requests
from typing import Dict, List, Optional


class MassAssignmentDetector:
    """Detect mass assignment vulnerabilities"""
    
    # Common privileged parameters
    PRIVILEGED_PARAMS = [
        'admin', 'is_admin', 'isAdmin', 'role', 'user_role', 'privilege',
        'is_superuser', 'isSuperuser', 'permissions', 'access_level',
    ]
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def detect(self, url: str, method: str = 'POST',
              data: Optional[Dict] = None) -> List[Dict]:
        """Detect mass assignment vulnerabilities"""
        vulnerabilities = []
        
        for param in self.PRIVILEGED_PARAMS:
            vuln = self._test_parameter(url, method, param, data)
            if vuln:
                vulnerabilities.append(vuln)
                
        return vulnerabilities
    
    def _test_parameter(self, url: str, method: str, param: str,
                       data: Optional[Dict]) -> Optional[Dict]:
        """Test a privileged parameter"""
        test_data = data.copy() if data else {}
        test_data[param] = 'true'  # or 1, 'admin', etc.
        
        try:
            if method.upper() == 'POST':
                response = requests.post(
                    url, json=test_data,
                    timeout=self.timeout, verify=self.verify_ssl
                )
            else:
                response = requests.put(
                    url, json=test_data,
                    timeout=self.timeout, verify=self.verify_ssl
                )
                
            # Check if parameter was accepted
            if response.status_code in [200, 201, 204]:
                return {
                    'url': url,
                    'parameter': param,
                    'type': 'MASS_ASSIGNMENT',
                    'severity': 'HIGH',
                    'description': f'Privileged parameter {param} accepted',
                }
                
        except requests.RequestException:
            pass
            
        return None


def detect_mass_assignment(urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """Detect mass assignment on multiple URLs"""
    detector = MassAssignmentDetector(**kwargs)
    return {url: detector.detect(url) for url in urls}
