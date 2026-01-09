"""API versioning tracker."""
from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)

class APIVersionTracker:
    """Track API versions and deprecated endpoints."""
    
    def analyze(self, endpoints: List[str]) -> Dict:
        """Analyze API versions."""
        versions = {}
        deprecated = []
        
        for endpoint in endpoints:
            version_match = re.search(r'/v(\d+)/', endpoint, re.I)
            if version_match:
                version = int(version_match.group(1))
                if version not in versions:
                    versions[version] = []
                versions[version].append(endpoint)
                
                if version == 1:
                    deprecated.append(endpoint)
        
        return {
            'versions': versions,
            'deprecated': deprecated,
            'latest_version': max(versions.keys()) if versions else None,
            'security_risks': self._analyze_version_risks(versions)
        }
    
    def _analyze_version_risks(self, versions: Dict) -> List[str]:
        """Analyze security risks by version."""
        risks = []
        if 1 in versions:
            risks.append("v1 endpoints may lack modern security controls")
        return risks
