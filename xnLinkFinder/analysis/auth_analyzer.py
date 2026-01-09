"""Authentication flow analyzer."""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class AuthAnalyzer:
    """Analyze authentication flows and mechanisms."""
    
    def analyze(self, endpoints: List[str]) -> Dict:
        """Analyze authentication in endpoints."""
        auth_endpoints = []
        mechanisms = set()
        
        for endpoint in endpoints:
            ep_lower = endpoint.lower()
            if any(kw in ep_lower for kw in ['auth', 'login', 'token', 'oauth', 'saml']):
                auth_endpoints.append(endpoint)
                
                if 'oauth' in ep_lower:
                    mechanisms.add('OAuth')
                if 'saml' in ep_lower:
                    mechanisms.add('SAML')
                if 'jwt' in ep_lower or 'token' in ep_lower:
                    mechanisms.add('JWT')
                if 'basic' in ep_lower:
                    mechanisms.add('Basic Auth')
                if 'api' in ep_lower and 'key' in ep_lower:
                    mechanisms.add('API Key')
        
        return {
            'auth_endpoints': auth_endpoints,
            'mechanisms': list(mechanisms),
            'bypass_opportunities': self._find_bypass_opportunities(auth_endpoints)
        }
    
    def _find_bypass_opportunities(self, endpoints: List[str]) -> List[str]:
        """Identify potential auth bypass opportunities."""
        opportunities = []
        for endpoint in endpoints:
            if 'reset' in endpoint.lower() or 'forgot' in endpoint.lower():
                opportunities.append(f"Password reset flow: {endpoint}")
        return opportunities
