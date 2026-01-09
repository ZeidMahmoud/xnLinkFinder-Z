"""
Rate Limit Tester

Tests API rate limiting effectiveness:
- Identifies rate limit thresholds
- Tests bypass techniques
- Measures rate limit windows
"""

import requests
import time
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class RateLimitTester:
    """Test API rate limiting"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        """
        Initialize rate limit tester
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.lock = threading.Lock()
        
    def test(self, url: str, max_requests: int = 100, 
             threads: int = 10, headers: Optional[Dict] = None) -> Dict:
        """
        Test rate limiting on an endpoint
        
        Args:
            url: Target URL to test
            max_requests: Maximum number of requests to send
            threads: Number of concurrent threads
            headers: Optional headers to include
            
        Returns:
            Rate limit test results
        """
        results = {
            'url': url,
            'total_requests': 0,
            'successful_requests': 0,
            'rate_limited': 0,
            'errors': 0,
            'response_codes': {},
            'start_time': time.time(),
            'end_time': None,
            'requests_per_second': 0,
        }
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for i in range(max_requests):
                future = executor.submit(
                    self._make_request, url, headers, i
                )
                futures.append(future)
                
            for future in as_completed(futures):
                try:
                    response_data = future.result()
                    
                    with self.lock:
                        results['total_requests'] += 1
                        
                        if response_data['success']:
                            results['successful_requests'] += 1
                        elif response_data['status_code'] == 429:
                            results['rate_limited'] += 1
                        else:
                            results['errors'] += 1
                            
                        code = response_data['status_code']
                        results['response_codes'][code] = \
                            results['response_codes'].get(code, 0) + 1
                            
                except Exception as e:
                    with self.lock:
                        results['errors'] += 1
                        
        results['end_time'] = time.time()
        duration = results['end_time'] - results['start_time']
        results['requests_per_second'] = results['total_requests'] / duration if duration > 0 else 0
        
        return results
    
    def _make_request(self, url: str, headers: Optional[Dict], 
                     request_num: int) -> Dict:
        """Make a single request"""
        try:
            response = requests.get(
                url,
                headers=headers or {},
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=False
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'request_num': request_num,
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'status_code': 0,
                'request_num': request_num,
                'error': str(e),
            }
    
    def test_bypass_techniques(self, url: str, 
                              headers: Optional[Dict] = None) -> List[Dict]:
        """
        Test common rate limit bypass techniques
        
        Args:
            url: Target URL
            headers: Optional headers
            
        Returns:
            List of bypass attempts and results
        """
        bypass_results = []
        
        # Test with different IP headers
        ip_headers = [
            {'X-Forwarded-For': '127.0.0.1'},
            {'X-Forwarded-For': f'192.168.1.{i}'}
            for i in range(1, 11)
        ]
        
        for bypass_header in ip_headers[:5]:  # Test first 5
            combined_headers = headers.copy() if headers else {}
            combined_headers.update(bypass_header)
            
            try:
                response = requests.get(
                    url,
                    headers=combined_headers,
                    timeout=self.timeout,
                    verify=self.verify_ssl
                )
                
                bypass_results.append({
                    'technique': 'IP_HEADER_BYPASS',
                    'header': bypass_header,
                    'status_code': response.status_code,
                    'bypassed': response.status_code != 429,
                })
                
            except requests.RequestException:
                pass
                
        return bypass_results
    
    def analyze_rate_limit_headers(self, url: str, 
                                   headers: Optional[Dict] = None) -> Dict:
        """
        Analyze rate limit headers in response
        
        Args:
            url: Target URL
            headers: Optional headers
            
        Returns:
            Rate limit header information
        """
        try:
            response = requests.get(
                url,
                headers=headers or {},
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            rate_limit_headers = {}
            
            # Common rate limit headers
            header_patterns = [
                'X-RateLimit-Limit',
                'X-RateLimit-Remaining',
                'X-RateLimit-Reset',
                'X-Rate-Limit-Limit',
                'X-Rate-Limit-Remaining',
                'X-Rate-Limit-Reset',
                'RateLimit-Limit',
                'RateLimit-Remaining',
                'RateLimit-Reset',
                'Retry-After',
            ]
            
            for header in header_patterns:
                if header in response.headers:
                    rate_limit_headers[header] = response.headers[header]
                    
            return {
                'url': url,
                'rate_limit_headers': rate_limit_headers,
                'has_rate_limiting': len(rate_limit_headers) > 0,
            }
            
        except requests.RequestException:
            return {'error': 'Failed to fetch headers'}


def test_rate_limits(urls: List[str], **kwargs) -> Dict[str, Dict]:
    """
    Convenience function to test multiple URLs
    
    Args:
        urls: List of URLs to test
        **kwargs: Additional arguments for RateLimitTester
        
    Returns:
        Dictionary mapping URLs to test results
    """
    tester = RateLimitTester(**kwargs)
    results = {}
    
    for url in urls:
        try:
            result = tester.test(url, max_requests=50)
            results[url] = result
        except Exception as e:
            print(f"[!] Error testing {url}: {str(e)}")
            
    return results
