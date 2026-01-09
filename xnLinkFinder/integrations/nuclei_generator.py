"""
Nuclei Template Auto-Generation for xnLinkFinder-Z.

Automatically generates Nuclei YAML templates for discovered endpoints.
"""

from typing import List, Dict, Optional
import logging
import yaml

logger = logging.getLogger(__name__)


class NucleiGenerator:
    """Generate Nuclei templates from discovered endpoints."""
    
    def __init__(self, output_dir: str = "./nuclei-templates"):
        """
        Initialize Nuclei template generator.
        
        Args:
            output_dir: Directory to save generated templates
        """
        self.output_dir = output_dir
    
    def generate_template(
        self,
        endpoint: str,
        vuln_type: str,
        severity: str = "medium",
        **kwargs
    ) -> Dict:
        """
        Generate a Nuclei template for an endpoint.
        
        Args:
            endpoint: Target endpoint
            vuln_type: Type of vulnerability to test
            severity: Severity level
            **kwargs: Additional template parameters
            
        Returns:
            Dictionary representing Nuclei template
        """
        import hashlib
        # Use hashlib for consistent hashing
        endpoint_hash = hashlib.md5(endpoint.encode()).hexdigest()[:8]
        template = {
            'id': f"xnlinkfinder-{vuln_type}-{endpoint_hash}",
            'info': {
                'name': f"{vuln_type.upper()} Test for {endpoint}",
                'author': 'xnLinkFinder-Z',
                'severity': severity,
                'description': f'Test for {vuln_type} vulnerability on {endpoint}',
                'tags': [vuln_type, 'xnlinkfinder']
            },
            'requests': self._generate_requests(endpoint, vuln_type)
        }
        
        return template
    
    def _generate_requests(self, endpoint: str, vuln_type: str) -> List[Dict]:
        """Generate request specifications based on vulnerability type."""
        requests = []
        
        if vuln_type == 'idor':
            requests.append({
                'method': 'GET',
                'path': [endpoint],
                'matchers': [{
                    'type': 'status',
                    'status': [200]
                }]
            })
        elif vuln_type == 'sqli':
            payloads = ["'", "1' OR '1'='1", "admin'--"]
            for payload in payloads:
                requests.append({
                    'method': 'GET',
                    'path': [f"{endpoint}?id={payload}"],
                    'matchers': [{
                        'type': 'word',
                        'words': ['error', 'syntax', 'mysql', 'sql']
                    }]
                })
        elif vuln_type == 'xss':
            payload = '<script>alert(1)</script>'
            requests.append({
                'method': 'GET',
                'path': [f"{endpoint}?q={payload}"],
                'matchers': [{
                    'type': 'word',
                    'words': [payload]
                }]
            })
        
        return requests
    
    def save_template(self, template: Dict, filename: str):
        """Save template to YAML file."""
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            yaml.dump(template, f, default_flow_style=False)
        
        logger.info(f"Saved Nuclei template: {filepath}")


def generate_nuclei_templates(endpoints: List[str], output_dir: str = "./nuclei-templates") -> List[str]:
    """Generate Nuclei templates for multiple endpoints."""
    generator = NucleiGenerator(output_dir)
    generated_files = []
    
    for endpoint in endpoints:
        template = generator.generate_template(endpoint, 'idor')
        filename = f"idor-{hash(endpoint) & 0xFFFFFFFF}.yaml"
        generator.save_template(template, filename)
        generated_files.append(filename)
    
    return generated_files
