"""
Nuclei Template Generator
Auto-generate Nuclei templates from discovered endpoints
"""

import yaml
from typing import List, Dict, Any
from pathlib import Path


class NucleiTemplateGenerator:
    """Generate Nuclei templates for discovered endpoints"""
    
    def __init__(self, output_dir: str = "nuclei-templates"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_info_disclosure_template(self, endpoints: List[str], name: str = "info-disclosure") -> str:
        """Generate template for information disclosure"""
        template = {
            'id': f'{name}-endpoints',
            'info': {
                'name': f'{name.replace("-", " ").title()} Detection',
                'author': 'xnLinkFinder-Z',
                'severity': 'info',
                'description': f'Detects {name} endpoints',
                'tags': ['disclosure', 'info']
            },
            'requests': [{
                'method': 'GET',
                'path': endpoints[:20],  # Limit to first 20
                'matchers': [{
                    'type': 'status',
                    'status': [200]
                }]
            }]
        }
        return yaml.dump(template, sort_keys=False)
    
    def generate_sqli_template(self, endpoints: List[str]) -> str:
        """Generate SQL injection test template"""
        template = {
            'id': 'sqli-detection',
            'info': {
                'name': 'SQL Injection Detection',
                'author': 'xnLinkFinder-Z',
                'severity': 'high',
                'description': 'Tests for SQL injection vulnerabilities',
                'tags': ['sqli', 'injection']
            },
            'requests': [{
                'method': 'GET',
                'path': [f"{ep}?id=1'" for ep in endpoints[:10]],
                'matchers': [{
                    'type': 'word',
                    'words': ['SQL syntax', 'mysql_fetch', 'syntax error', 'ORA-']
                }]
            }]
        }
        return yaml.dump(template, sort_keys=False)
    
    def generate_xss_template(self, endpoints: List[str]) -> str:
        """Generate XSS test template"""
        template = {
            'id': 'xss-detection',
            'info': {
                'name': 'Cross-Site Scripting Detection',
                'author': 'xnLinkFinder-Z',
                'severity': 'medium',
                'description': 'Tests for XSS vulnerabilities',
                'tags': ['xss', 'injection']
            },
            'requests': [{
                'method': 'GET',
                'path': [f"{ep}?q=<script>alert(1)</script>" for ep in endpoints[:10]],
                'matchers': [{
                    'type': 'word',
                    'words': ['<script>alert(1)</script>'],
                    'part': 'body'
                }]
            }]
        }
        return yaml.dump(template, sort_keys=False)
    
    def generate_idor_template(self, endpoints: List[str]) -> str:
        """Generate IDOR test template"""
        # Filter endpoints with ID patterns
        id_endpoints = [ep for ep in endpoints if any(x in ep.lower() for x in ['id=', '/id/', 'user/', 'account/'])]
        
        template = {
            'id': 'idor-detection',
            'info': {
                'name': 'IDOR Detection',
                'author': 'xnLinkFinder-Z',
                'severity': 'high',
                'description': 'Tests for Insecure Direct Object Reference',
                'tags': ['idor', 'access-control']
            },
            'requests': [{
                'method': 'GET',
                'path': id_endpoints[:10],
                'matchers': [{
                    'type': 'status',
                    'status': [200, 301, 302]
                }]
            }]
        }
        return yaml.dump(template, sort_keys=False)
    
    def generate_auth_bypass_template(self, endpoints: List[str]) -> str:
        """Generate authentication bypass template"""
        # Filter admin/auth endpoints
        auth_endpoints = [ep for ep in endpoints if any(x in ep.lower() for x in ['admin', 'auth', 'login', 'panel'])]
        
        template = {
            'id': 'auth-bypass-detection',
            'info': {
                'name': 'Authentication Bypass Detection',
                'author': 'xnLinkFinder-Z',
                'severity': 'critical',
                'description': 'Tests for authentication bypass vulnerabilities',
                'tags': ['auth', 'bypass']
            },
            'requests': [{
                'method': 'GET',
                'path': auth_endpoints[:10],
                'headers': {
                    'X-Forwarded-For': '127.0.0.1',
                    'X-Original-URL': '/admin'
                },
                'matchers': [{
                    'type': 'status',
                    'status': [200]
                }]
            }]
        }
        return yaml.dump(template, sort_keys=False)
    
    def generate_all_templates(self, endpoints: List[str]) -> Dict[str, str]:
        """Generate all template types"""
        templates = {
            'info-disclosure': self.generate_info_disclosure_template(endpoints),
            'sqli': self.generate_sqli_template(endpoints),
            'xss': self.generate_xss_template(endpoints),
            'idor': self.generate_idor_template(endpoints),
            'auth-bypass': self.generate_auth_bypass_template(endpoints)
        }
        return templates
    
    def save_templates(self, endpoints: List[str]) -> List[Path]:
        """Save all generated templates to files"""
        templates = self.generate_all_templates(endpoints)
        saved_files = []
        
        for name, content in templates.items():
            file_path = self.output_dir / f"{name}.yaml"
            file_path.write_text(content)
            saved_files.append(file_path)
        
        return saved_files
