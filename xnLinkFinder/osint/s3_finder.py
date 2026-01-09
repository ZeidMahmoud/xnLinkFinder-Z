"""S3 Bucket Finder - Brute-force S3 bucket discovery"""
import requests
from typing import List, Dict

class S3Finder:
    def __init__(self):
        self.common_names = ['dev', 'prod', 'test', 'backup', 'assets']
    
    def find_buckets(self, base_name: str) -> List[Dict]:
        """Find S3 buckets using permutations"""
        results = []
        for name in self.common_names:
            bucket = f"{base_name}-{name}"
            url = f"https://{bucket}.s3.amazonaws.com"
            try:
                resp = requests.head(url, timeout=5)
                if resp.status_code != 404:
                    results.append({'bucket': bucket, 'url': url, 'status': resp.status_code})
            except:
                pass
        return results

def find_s3_buckets(base_name: str) -> List[Dict]:
    finder = S3Finder()
    return finder.find_buckets(base_name)
