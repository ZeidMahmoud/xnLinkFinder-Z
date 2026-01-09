"""
Race Condition Tester

Tests for race condition vulnerabilities:
- Concurrent request testing
- TOCTOU (Time-of-check to time-of-use) detection
- Double-spend issues
"""

import requests
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class RaceConditionTester:
    """Test for race condition vulnerabilities"""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = True):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.results = []
        self.lock = threading.Lock()
        
    def test(self, url: str, method: str = 'GET', 
             data: Optional[Dict] = None, headers: Optional[Dict] = None,
             num_requests: int = 10) -> Dict:
        """
        Test for race conditions by sending concurrent requests
        
        Args:
            url: Target URL
            method: HTTP method
            data: Request data
            headers: Request headers
            num_requests: Number of concurrent requests
            
        Returns:
            Test results
        """
        responses = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [
                executor.submit(
                    self._make_request, url, method, data, headers
                )
                for _ in range(num_requests)
            ]
            
            for future in as_completed(futures):
                try:
                    resp_data = future.result()
                    responses.append(resp_data)
                except Exception as e:
                    print(f"[!] Request error: {str(e)}")
                    
        end_time = time.time()
        
        # Analyze responses for race condition indicators
        status_codes = [r['status_code'] for r in responses]
        unique_responses = set(r.get('content_hash') for r in responses)
        
        return {
            'url': url,
            'num_requests': num_requests,
            'duration': end_time - start_time,
            'responses': len(responses),
            'unique_status_codes': len(set(status_codes)),
            'unique_responses': len(unique_responses),
            'status_codes': status_codes,
            'potential_race_condition': len(unique_responses) > 1,
        }
    
    def _make_request(self, url: str, method: str, 
                     data: Optional[Dict], headers: Optional[Dict]) -> Dict:
        """Make a single HTTP request"""
        try:
            if method.upper() == 'POST':
                response = requests.post(
                    url, json=data, headers=headers or {},
                    timeout=self.timeout, verify=self.verify_ssl
                )
            else:
                response = requests.get(
                    url, headers=headers or {},
                    timeout=self.timeout, verify=self.verify_ssl
                )
                
            return {
                'status_code': response.status_code,
                'content_hash': hash(response.text[:1000]),
                'response_time': response.elapsed.total_seconds(),
            }
            
        except requests.RequestException as e:
            return {
                'status_code': 0,
                'error': str(e),
            }


def test_race_conditions(urls: List[str], **kwargs) -> Dict[str, Dict]:
    """Test multiple URLs for race conditions"""
    tester = RaceConditionTester(**kwargs)
    return {url: tester.test(url) for url in urls}
