"""GitHub/GitLab code search for exposed endpoints."""
from typing import List, Dict, Optional
import requests
import logging

logger = logging.getLogger(__name__)

class GitSearch:
    """Search GitHub/GitLab for exposed endpoints and secrets."""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.github_api = "https://api.github.com"
    
    def search_github(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search GitHub code for endpoints."""
        results = []
        try:
            headers = {'Authorization': f'token {self.github_token}'} if self.github_token else {}
            params = {'q': query, 'per_page': min(max_results, 100)}
            response = requests.get(f"{self.github_api}/search/code", headers=headers, params=params)
            if response.status_code == 200:
                results = response.json().get('items', [])
        except Exception as e:
            logger.error(f"GitHub search failed: {e}")
        return results

def search_github_for_endpoints(domain: str, github_token: Optional[str] = None) -> List[Dict]:
    """Search GitHub for endpoints related to a domain."""
    searcher = GitSearch(github_token)
    return searcher.search_github(f'{domain} path:*.js')
