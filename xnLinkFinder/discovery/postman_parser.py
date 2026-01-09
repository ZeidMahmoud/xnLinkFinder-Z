"""Postman collection parser."""
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class PostmanParser:
    """Parse Postman collections to extract endpoints."""
    
    def parse_collection(self, collection_path: str) -> List[Dict]:
        """Parse Postman collection file."""
        endpoints = []
        try:
            with open(collection_path, 'r') as f:
                data = json.load(f)
            
            if 'item' in data:
                endpoints.extend(self._extract_items(data['item']))
        except Exception as e:
            logger.error(f"Postman parsing failed: {e}")
        return endpoints
    
    def _extract_items(self, items: List[Dict]) -> List[Dict]:
        """Recursively extract request items."""
        endpoints = []
        for item in items:
            if 'request' in item:
                request = item['request']
                if isinstance(request, dict) and 'url' in request:
                    url = request['url']
                    if isinstance(url, dict):
                        url = url.get('raw', '')
                    endpoints.append({
                        'name': item.get('name', 'Unknown'),
                        'method': request.get('method', 'GET'),
                        'url': url
                    })
            if 'item' in item:
                endpoints.extend(self._extract_items(item['item']))
        return endpoints

def parse_postman_collection(collection_path: str) -> List[Dict]:
    """Convenience function to parse Postman collection."""
    parser = PostmanParser()
    return parser.parse_collection(collection_path)
