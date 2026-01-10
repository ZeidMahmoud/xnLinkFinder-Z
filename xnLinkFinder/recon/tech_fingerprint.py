"""
Technology Fingerprinting for xnLinkFinder-Z.

Features:
- Wappalyzer-style detection
- HTTP headers analysis
- JavaScript library detection
- CMS identification
- Framework version detection
- Build detailed technology stack profile
"""

from typing import List, Dict, Optional, Set
import logging
import re

logger = logging.getLogger(__name__)


class TechnologyFingerprinter:
    """Technology stack fingerprinting and identification."""
    
    def __init__(self):
        """Initialize technology fingerprinter."""
        # Technology signatures
        self.tech_signatures = {
            'cms': {
                'WordPress': {
                    'urls': ['/wp-content/', '/wp-includes/', '/wp-admin/'],
                    'headers': {'X-Powered-By': 'WordPress'},
                    'meta': ['wp-content', 'wordpress']
                },
                'Drupal': {
                    'urls': ['/sites/default/', '/misc/drupal.js'],
                    'headers': {'X-Generator': 'Drupal'},
                    'meta': ['drupal']
                },
                'Joomla': {
                    'urls': ['/administrator/', '/components/'],
                    'headers': {},
                    'meta': ['joomla']
                },
            },
            'frameworks': {
                'React': {
                    'indicators': ['react.js', '_react', '__REACT'],
                    'headers': {}
                },
                'Vue.js': {
                    'indicators': ['vue.js', '__VUE__', 'v-bind'],
                    'headers': {}
                },
                'Angular': {
                    'indicators': ['angular.js', 'ng-app', 'ng-controller'],
                    'headers': {}
                },
                'Django': {
                    'indicators': ['csrfmiddlewaretoken', '__admin__'],
                    'headers': {}
                },
                'Flask': {
                    'indicators': ['flask'],
                    'headers': {}
                },
                'Express.js': {
                    'indicators': [],
                    'headers': {'X-Powered-By': 'Express'}
                },
            },
            'servers': {
                'Apache': {
                    'headers': {'Server': 'Apache'}
                },
                'Nginx': {
                    'headers': {'Server': 'nginx'}
                },
                'IIS': {
                    'headers': {'Server': 'Microsoft-IIS'}
                },
            }
        }
    
    def fingerprint_url(self, url: str) -> Dict[str, any]:
        """
        Fingerprint technologies used by a URL.
        
        Args:
            url: Target URL
            
        Returns:
            Detected technologies
        """
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=10, allow_redirects=True)
            
            result = {
                'url': url,
                'technologies': {
                    'cms': [],
                    'frameworks': [],
                    'servers': [],
                    'libraries': [],
                    'analytics': [],
                    'cdn': []
                },
                'headers': dict(response.headers),
                'confidence': {}
            }
            
            # Analyze headers
            headers_lower = {k.lower(): v.lower() for k, v in response.headers.items()}
            
            # Check server
            if 'server' in headers_lower:
                server = headers_lower['server']
                if 'apache' in server:
                    result['technologies']['servers'].append('Apache')
                elif 'nginx' in server:
                    result['technologies']['servers'].append('nginx')
                elif 'iis' in server:
                    result['technologies']['servers'].append('Microsoft IIS')
                elif 'cloudflare' in server:
                    result['technologies']['cdn'].append('Cloudflare')
            
            # Check X-Powered-By
            if 'x-powered-by' in headers_lower:
                powered_by = headers_lower['x-powered-by']
                if 'php' in powered_by:
                    result['technologies']['frameworks'].append('PHP')
                if 'express' in powered_by:
                    result['technologies']['frameworks'].append('Express.js')
                if 'asp.net' in powered_by:
                    result['technologies']['frameworks'].append('ASP.NET')
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check meta tags
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                if meta.get('name') == 'generator':
                    generator = meta.get('content', '').lower()
                    if 'wordpress' in generator:
                        result['technologies']['cms'].append('WordPress')
                    elif 'drupal' in generator:
                        result['technologies']['cms'].append('Drupal')
                    elif 'joomla' in generator:
                        result['technologies']['cms'].append('Joomla')
            
            # Check for JavaScript libraries
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script.get('src', '').lower()
                if 'jquery' in src:
                    result['technologies']['libraries'].append('jQuery')
                if 'react' in src:
                    result['technologies']['frameworks'].append('React')
                if 'vue' in src:
                    result['technologies']['frameworks'].append('Vue.js')
                if 'angular' in src:
                    result['technologies']['frameworks'].append('Angular')
                if 'bootstrap' in src:
                    result['technologies']['libraries'].append('Bootstrap')
                if 'google-analytics' in src or 'gtag' in src:
                    result['technologies']['analytics'].append('Google Analytics')
            
            # Check for CDN
            if any('cloudflare' in str(s) for s in scripts):
                if 'Cloudflare' not in result['technologies']['cdn']:
                    result['technologies']['cdn'].append('Cloudflare')
            
            # Remove duplicates
            for category in result['technologies']:
                result['technologies'][category] = list(set(result['technologies'][category]))
            
            return result
        
        except Exception as e:
            logger.error(f"Error fingerprinting {url}: {e}")
            return {
                'url': url,
                'error': str(e)
            }
    
    def build_tech_stack_profile(self, url: str) -> Dict[str, any]:
        """
        Build comprehensive technology stack profile.
        
        Args:
            url: Target URL
            
        Returns:
            Technology stack profile
        """
        fingerprint = self.fingerprint_url(url)
        
        profile = {
            'url': url,
            'tech_stack': fingerprint.get('technologies', {}),
            'analysis': {
                'total_technologies': sum(len(v) for v in fingerprint.get('technologies', {}).values()),
                'stack_type': self._determine_stack_type(fingerprint),
                'security_concerns': self._identify_security_concerns(fingerprint)
            }
        }
        
        return profile
    
    def _determine_stack_type(self, fingerprint: Dict[str, any]) -> str:
        """Determine the general stack type (LAMP, MEAN, etc.)."""
        technologies = fingerprint.get('technologies', {})
        
        # Check for common stacks
        has_php = 'PHP' in technologies.get('frameworks', [])
        has_apache = 'Apache' in technologies.get('servers', [])
        has_mysql = False  # Would need database detection
        
        has_node = 'Express.js' in technologies.get('frameworks', [])
        has_react = 'React' in technologies.get('frameworks', [])
        has_angular = 'Angular' in technologies.get('frameworks', [])
        
        if has_php and has_apache:
            return 'LAMP-like (PHP/Apache)'
        elif has_node and (has_react or has_angular):
            return 'MEAN/MERN-like (JavaScript full-stack)'
        elif 'ASP.NET' in technologies.get('frameworks', []):
            return '.NET stack'
        else:
            return 'Mixed/Unknown'
    
    def _identify_security_concerns(self, fingerprint: Dict[str, any]) -> List[str]:
        """Identify potential security concerns based on detected technologies."""
        concerns = []
        
        technologies = fingerprint.get('technologies', {})
        
        # Check for outdated or vulnerable technologies
        if 'WordPress' in technologies.get('cms', []):
            concerns.append('WordPress detected - ensure plugins are updated')
        
        if 'jQuery' in technologies.get('libraries', []):
            concerns.append('jQuery detected - check for vulnerable versions')
        
        # Check headers for security issues
        headers = fingerprint.get('headers', {})
        if 'X-Powered-By' in headers:
            concerns.append('X-Powered-By header present - information disclosure')
        
        if 'Server' in headers:
            concerns.append('Server header present - version information disclosure')
        
        return concerns


def fingerprint_technology(url: str) -> Dict[str, any]:
    """
    Convenience function to fingerprint technologies.
    
    Args:
        url: Target URL
        
    Returns:
        Technology fingerprint results
    """
    fingerprinter = TechnologyFingerprinter()
    return fingerprinter.fingerprint_url(url)
