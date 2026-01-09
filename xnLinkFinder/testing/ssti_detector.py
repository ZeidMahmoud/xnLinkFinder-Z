"""
SSTI (Server-Side Template Injection) Detector

Detects template injection vulnerabilities:
- Multiple template engines (Jinja2, Twig, Freemarker, etc.)
- Polyglot payload generation
- Context-aware detection
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urlencode


class SSTIDetector:
    """Detect Server-Side Template Injection"""
    
    # Polyglot and engine-specific payloads
    PAYLOADS = {
        'jinja2': ['{{7*7}}', '{{config}}', '{{self}}'],
        'twig': ['{{7*7}}', '{{_self}}', '{{app}}'],
        'freemarker': ['${7*7}', '#{7*7}', '<#assign ex="freemarker">'],
        'velocity': ['#set($x=7*7)$x', '$class.inspect'],
        'smarty': ['{7*7}', '{$smarty.version}'],
        'erb': ['<%= 7*7 %>', '<%= File.open(\'/etc/passwd\').read %>'],
        'polyglot': ['{{7*\'7\'}}', '${7*7}', '#{7*7}', '<%= 7*7 %>'],
    }
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def detect(self, url: str, params: Optional[Dict] = None) -> List[Dict]:
        """Detect SSTI vulnerabilities"""
        vulnerabilities = []
        
        if not params:
            return vulnerabilities
            
        for param in params:
            for engine, payloads in self.PAYLOADS.items():
                for payload in payloads:
                    vuln = self._test_payload(url, param, payload, engine, params)
                    if vuln:
                        vulnerabilities.append(vuln)
                        break  # Move to next engine
                        
        return vulnerabilities
    
    def _test_payload(self, url: str, param: str, payload: str,
                     engine: str, params: Dict) -> Optional[Dict]:
        """Test a single SSTI payload"""
        test_params = params.copy()
        test_params[param] = payload
        
        try:
            response = requests.get(
                url, params=test_params,
                timeout=self.timeout, verify=self.verify_ssl
            )
            
            # Check if payload was executed
            if self._check_execution(response.text, payload):
                return {
                    'url': url,
                    'parameter': param,
                    'payload': payload,
                    'engine': engine,
                    'type': 'SSTI',
                    'severity': 'CRITICAL',
                    'description': f'Server-Side Template Injection ({engine})',
                }
                
        except requests.RequestException:
            pass
            
        return None
    
    def _check_execution(self, response: str, payload: str) -> bool:
        """Check if template was executed"""
        # Check for mathematical operation results
        if '49' in response and ('7*7' in payload or "7*'7'" in payload):
            return True
        # Check for specific markers
        if 'freemarker' in response.lower() and 'freemarker' in payload.lower():
            return True
        return False


def detect_ssti(urls: List[str], params: Optional[Dict] = None, **kwargs) -> Dict[str, List[Dict]]:
    """Detect SSTI on multiple URLs"""
    detector = SSTIDetector(**kwargs)
    return {url: detector.detect(url, params) for url in urls}
