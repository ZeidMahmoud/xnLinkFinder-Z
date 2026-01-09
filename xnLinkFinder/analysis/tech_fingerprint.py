"""Technology stack fingerprinting."""
from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)

class TechFingerprinter:
    """Deep analysis of frameworks and tech stack."""
    
    def fingerprint(self, endpoints: List[str]) -> Dict:
        """Fingerprint technology stack."""
        frameworks = set()
        languages = set()
        
        for endpoint in endpoints:
            ep_lower = endpoint.lower()
            
            # Framework detection
            if '.php' in ep_lower:
                languages.add('PHP')
            if '.asp' in ep_lower or '.aspx' in ep_lower:
                languages.add('ASP.NET')
            if '.jsp' in ep_lower:
                languages.add('Java/JSP')
            if '.do' in ep_lower or '.action' in ep_lower:
                frameworks.add('Struts')
            if '/api/v' in ep_lower:
                frameworks.add('REST API')
            if 'graphql' in ep_lower:
                frameworks.add('GraphQL')
        
        return {
            'frameworks': list(frameworks),
            'languages': list(languages),
            'known_vulnerabilities': self._check_vulnerabilities(frameworks)
        }
    
    def _check_vulnerabilities(self, frameworks: Set[str]) -> List[str]:
        """Check for known framework vulnerabilities."""
        vulns = []
        if 'Struts' in frameworks:
            vulns.append("Apache Struts - Check for CVE-2017-5638")
        return vulns
