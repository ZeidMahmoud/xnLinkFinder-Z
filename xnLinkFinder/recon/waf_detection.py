"""
WAF Detection and Bypass for xnLinkFinder-Z.

Features:
- Identify WAF vendor (Cloudflare, Akamai, AWS WAF, etc.)
- Test common bypass techniques
- Suggest bypass payloads
- Rate limit detection
"""

from typing import List, Dict, Optional, Set, Tuple
import logging
import re

logger = logging.getLogger(__name__)


class WAFDetector:
    """WAF detection and bypass suggestion engine."""
    
    def __init__(self):
        """Initialize WAF detector."""
        # WAF signatures (headers, cookies, response patterns)
        self.waf_signatures = {
            'Cloudflare': {
                'headers': ['cf-ray', 'cf-cache-status', '__cfduid'],
                'cookies': ['__cfduid', '__cfruid'],
                'server': ['cloudflare'],
                'blocked_codes': [403, 429, 503],
                'blocked_text': ['attention required', 'cloudflare', 'ray id']
            },
            'AWS WAF': {
                'headers': ['x-amzn-requestid', 'x-amz-cf-id'],
                'cookies': [],
                'server': ['awselb', 'amazon'],
                'blocked_codes': [403],
                'blocked_text': ['aws', 'request blocked']
            },
            'Akamai': {
                'headers': ['akamai-origin-hop', 'akamai-x-cache'],
                'cookies': ['ak_bmsc', 'bm_sv'],
                'server': ['akamaighost'],
                'blocked_codes': [403, 405],
                'blocked_text': ['akamai', 'reference']
            },
            'Imperva (Incapsula)': {
                'headers': ['x-cdn', 'x-iinfo'],
                'cookies': ['incap_ses', 'visid_incap'],
                'server': ['incapsula'],
                'blocked_codes': [403],
                'blocked_text': ['incapsula incident id', 'client ip']
            },
            'Sucuri': {
                'headers': ['x-sucuri-id', 'x-sucuri-cache'],
                'cookies': [],
                'server': ['sucuri'],
                'blocked_codes': [403],
                'blocked_text': ['sucuri', 'access denied']
            },
            'ModSecurity': {
                'headers': ['x-mod-sec-rule'],
                'cookies': [],
                'server': ['mod_security', 'modsecurity'],
                'blocked_codes': [403, 406],
                'blocked_text': ['mod_security', 'not acceptable']
            },
            'F5 BIG-IP': {
                'headers': ['x-waf-event-info'],
                'cookies': ['bigipserver', 'f5_cspm', 'ts'],
                'server': ['big-ip', 'bigip'],
                'blocked_codes': [403],
                'blocked_text': []
            },
            'Barracuda': {
                'headers': ['x-barracuda-url'],
                'cookies': ['barra_counter_session'],
                'server': ['barracuda'],
                'blocked_codes': [403],
                'blocked_text': ['barracuda']
            },
        }
    
    def detect_waf(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, any]:
        """
        Detect WAF presence and identify vendor.
        
        Args:
            url: Target URL
            headers: Optional custom headers for request
            
        Returns:
            WAF detection results
        """
        try:
            import requests
            
            # Make initial request
            response = requests.get(url, headers=headers or {}, timeout=10, allow_redirects=True)
            
            result = {
                'url': url,
                'waf_detected': False,
                'waf_vendor': None,
                'confidence': 0,
                'indicators': [],
                'response_code': response.status_code,
                'server': response.headers.get('Server', 'Unknown')
            }
            
            response_headers_lower = {k.lower(): v for k, v in response.headers.items()}
            cookies = response.cookies.get_dict()
            response_text = response.text[:1000].lower()  # First 1000 chars
            
            # Check each WAF signature
            matches = {}
            for waf_name, signature in self.waf_signatures.items():
                score = 0
                indicators = []
                
                # Check headers
                for header in signature['headers']:
                    if header.lower() in response_headers_lower:
                        score += 3
                        indicators.append(f"Header: {header}")
                
                # Check cookies
                for cookie in signature['cookies']:
                    if cookie.lower() in [c.lower() for c in cookies.keys()]:
                        score += 3
                        indicators.append(f"Cookie: {cookie}")
                
                # Check server header
                server_header = response.headers.get('Server', '').lower()
                for server_pattern in signature['server']:
                    if server_pattern in server_header:
                        score += 2
                        indicators.append(f"Server: {server_pattern}")
                
                # Check response text
                for text_pattern in signature['blocked_text']:
                    if text_pattern in response_text:
                        score += 1
                        indicators.append(f"Body text: {text_pattern}")
                
                if score > 0:
                    matches[waf_name] = {'score': score, 'indicators': indicators}
            
            # Determine best match
            if matches:
                best_match = max(matches.items(), key=lambda x: x[1]['score'])
                result['waf_detected'] = True
                result['waf_vendor'] = best_match[0]
                result['confidence'] = min(100, best_match[1]['score'] * 10)
                result['indicators'] = best_match[1]['indicators']
            
            return result
        
        except Exception as e:
            logger.error(f"Error detecting WAF for {url}: {e}")
            return {
                'url': url,
                'error': str(e)
            }
    
    def test_bypass_techniques(self, url: str, waf_vendor: Optional[str] = None) -> Dict[str, any]:
        """
        Test common WAF bypass techniques.
        
        Args:
            url: Target URL
            waf_vendor: Known WAF vendor (optional)
            
        Returns:
            Bypass test results
        """
        bypass_techniques = {
            'case_variation': 'sElEcT * fRoM users',
            'url_encoding': '%53%45%4C%45%43%54',
            'double_encoding': '%2553%2545%254C',
            'unicode_encoding': '\\u0053\\u0045\\u004C',
            'hex_encoding': '0x53454C454354',
            'null_byte': 'SELECT%00FROM',
            'comment_injection': 'SEL/**/ECT',
            'whitespace_variation': 'SELECT%09FROM',
            'mixed_case_headers': {'X-Forwarded-For': '127.0.0.1'},
            'user_agent_variation': {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)'}
        }
        
        results = {
            'url': url,
            'waf_vendor': waf_vendor,
            'techniques_tested': [],
            'potential_bypasses': []
        }
        
        try:
            import requests
            
            # Get baseline response
            baseline = requests.get(url, timeout=10)
            baseline_code = baseline.status_code
            
            # Test each bypass technique
            for technique_name, test_payload in bypass_techniques.items():
                try:
                    if isinstance(test_payload, dict):
                        # Header-based bypass
                        response = requests.get(url, headers=test_payload, timeout=10)
                    else:
                        # Parameter-based bypass
                        test_url = f"{url}?test={test_payload}"
                        response = requests.get(test_url, timeout=10)
                    
                    results['techniques_tested'].append(technique_name)
                    
                    # Check if response differs from baseline (potential bypass)
                    if response.status_code != baseline_code:
                        results['potential_bypasses'].append({
                            'technique': technique_name,
                            'response_code': response.status_code,
                            'note': 'Response code differs from baseline'
                        })
                
                except Exception as e:
                    logger.debug(f"Error testing {technique_name}: {e}")
                    continue
            
            return results
        
        except Exception as e:
            logger.error(f"Error testing bypass techniques for {url}: {e}")
            return {
                'url': url,
                'error': str(e)
            }
    
    def suggest_bypass_payloads(self, waf_vendor: str) -> List[Dict[str, str]]:
        """
        Suggest bypass payloads specific to a WAF vendor.
        
        Args:
            waf_vendor: WAF vendor name
            
        Returns:
            List of suggested bypass payloads
        """
        # Generic bypasses that work on many WAFs
        generic_bypasses = [
            {
                'technique': 'HTTP Parameter Pollution',
                'payload': '?id=1&id=2',
                'description': 'Send duplicate parameters'
            },
            {
                'technique': 'HTTP Method Override',
                'payload': 'X-HTTP-Method-Override: PUT',
                'description': 'Use method override headers'
            },
            {
                'technique': 'Case Manipulation',
                'payload': 'sElEcT/**/fRoM/**/users',
                'description': 'Mix case and comments'
            },
            {
                'technique': 'Content-Type Confusion',
                'payload': 'Content-Type: application/json',
                'description': 'Change content type'
            },
        ]
        
        # WAF-specific bypasses
        vendor_specific = {
            'Cloudflare': [
                {
                    'technique': 'Origin IP Access',
                    'payload': 'Direct IP access bypassing Cloudflare',
                    'description': 'Find origin IP and access directly'
                },
                {
                    'technique': 'IPv6 Access',
                    'payload': 'Use IPv6 address',
                    'description': 'Cloudflare may not protect IPv6'
                },
            ],
            'AWS WAF': [
                {
                    'technique': 'Rate Limit Bypass',
                    'payload': 'X-Forwarded-For: 1.2.3.4',
                    'description': 'Spoof source IP'
                },
            ],
            'ModSecurity': [
                {
                    'technique': 'Unicode Normalization',
                    'payload': '\\u0053\\u0045\\u004C\\u0045\\u0043\\u0054',
                    'description': 'Use Unicode encoding'
                },
            ],
        }
        
        bypasses = generic_bypasses.copy()
        if waf_vendor in vendor_specific:
            bypasses.extend(vendor_specific[waf_vendor])
        
        return bypasses
    
    def detect_rate_limiting(self, url: str, num_requests: int = 20) -> Dict[str, any]:
        """
        Detect rate limiting behavior.
        
        Args:
            url: Target URL
            num_requests: Number of requests to send
            
        Returns:
            Rate limiting analysis
        """
        try:
            import requests
            import time
            
            results = {
                'url': url,
                'requests_sent': 0,
                'blocked_at': None,
                'rate_limit_detected': False,
                'response_codes': [],
                'rate_limit_headers': {}
            }
            
            for i in range(num_requests):
                try:
                    response = requests.get(url, timeout=10)
                    results['requests_sent'] += 1
                    results['response_codes'].append(response.status_code)
                    
                    # Check for rate limit indicators
                    if response.status_code in [429, 503]:
                        results['rate_limit_detected'] = True
                        results['blocked_at'] = i + 1
                        
                        # Capture rate limit headers
                        for header in ['X-RateLimit-Limit', 'X-RateLimit-Remaining', 
                                     'X-RateLimit-Reset', 'Retry-After']:
                            if header in response.headers:
                                results['rate_limit_headers'][header] = response.headers[header]
                        
                        break
                    
                    time.sleep(0.1)  # Small delay between requests
                
                except Exception as e:
                    logger.debug(f"Request {i+1} failed: {e}")
                    continue
            
            return results
        
        except Exception as e:
            logger.error(f"Error detecting rate limiting for {url}: {e}")
            return {
                'url': url,
                'error': str(e)
            }
    
    def comprehensive_waf_analysis(self, url: str) -> Dict[str, any]:
        """
        Perform comprehensive WAF analysis.
        
        Args:
            url: Target URL
            
        Returns:
            Complete WAF analysis
        """
        logger.info(f"Starting comprehensive WAF analysis for {url}")
        
        # Detect WAF
        waf_detection = self.detect_waf(url)
        
        analysis = {
            'url': url,
            'waf_detection': waf_detection,
            'bypass_tests': {},
            'rate_limiting': {},
            'recommendations': []
        }
        
        # If WAF detected, test bypasses
        if waf_detection.get('waf_detected'):
            waf_vendor = waf_detection.get('waf_vendor')
            analysis['bypass_tests'] = self.test_bypass_techniques(url, waf_vendor)
            analysis['suggested_payloads'] = self.suggest_bypass_payloads(waf_vendor)
            
            analysis['recommendations'].append(
                f"WAF detected: {waf_vendor}. Consider testing suggested bypass techniques."
            )
        else:
            analysis['recommendations'].append("No WAF detected. Proceed with normal testing.")
        
        # Detect rate limiting
        analysis['rate_limiting'] = self.detect_rate_limiting(url, num_requests=10)
        
        if analysis['rate_limiting'].get('rate_limit_detected'):
            analysis['recommendations'].append(
                "Rate limiting detected. Implement request throttling in your testing."
            )
        
        return analysis


def detect_waf(url: str) -> Dict[str, any]:
    """
    Convenience function to detect WAF.
    
    Args:
        url: Target URL
        
    Returns:
        WAF detection results
    """
    detector = WAFDetector()
    return detector.detect_waf(url)
