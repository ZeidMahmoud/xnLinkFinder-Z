"""Role-Based Access Control detector."""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class RBACDetector:
    """Detect role-based access issues."""
    
    def analyze(self, endpoints: List[str]) -> Dict:
        """Analyze endpoints for RBAC issues."""
        role_endpoints = []
        admin_endpoints = []
        
        for endpoint in endpoints:
            ep_lower = endpoint.lower()
            if 'admin' in ep_lower:
                admin_endpoints.append(endpoint)
                role_endpoints.append({'endpoint': endpoint, 'role': 'admin', 'risk': 'high'})
            elif 'user' in ep_lower:
                role_endpoints.append({'endpoint': endpoint, 'role': 'user', 'risk': 'medium'})
            elif any(kw in ep_lower for kw in ['moderator', 'manager']):
                role_endpoints.append({'endpoint': endpoint, 'role': 'privileged', 'risk': 'high'})
        
        return {
            'role_endpoints': role_endpoints,
            'admin_endpoints': admin_endpoints,
            'privilege_escalation_risks': self._find_escalation_risks(role_endpoints)
        }
    
    def _find_escalation_risks(self, role_endpoints: List[Dict]) -> List[str]:
        """Identify privilege escalation risks."""
        risks = []
        for ep in role_endpoints:
            if ep['risk'] == 'high':
                risks.append(f"High-privilege endpoint: {ep['endpoint']}")
        return risks
