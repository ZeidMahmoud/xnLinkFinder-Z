"""
Scope Intelligence Engine
Auto-detect and parse scope from various sources
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse, urljoin
import re


class ScopeIntelligenceEngine:
    """Intelligent scope detection from multiple sources"""
    
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.scope = set()
        self.robots_txt_paths = []
        self.sitemap_urls = []
        self.security_contacts = []
    
    def fetch_robots_txt(self) -> Optional[str]:
        """Fetch and parse robots.txt"""
        try:
            url = f"{self.base_url}/robots.txt"
            response = requests.get(url, timeout=self.timeout, verify=False)
            if response.status_code == 200:
                return response.text
        except Exception:
            pass
        return None
    
    def parse_robots_txt(self, content: str) -> List[str]:
        """Parse robots.txt for interesting paths"""
        paths = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('Disallow:') or line.startswith('Allow:'):
                path = line.split(':', 1)[1].strip()
                if path and path != '/':
                    paths.append(path)
            elif line.startswith('Sitemap:'):
                sitemap_url = line.split(':', 1)[1].strip()
                self.sitemap_urls.append(sitemap_url)
        return paths
    
    def fetch_sitemap(self, sitemap_url: Optional[str] = None) -> Optional[str]:
        """Fetch sitemap.xml"""
        try:
            url = sitemap_url or f"{self.base_url}/sitemap.xml"
            response = requests.get(url, timeout=self.timeout, verify=False)
            if response.status_code == 200:
                return response.text
        except Exception:
            pass
        return None
    
    def parse_sitemap(self, content: str) -> List[str]:
        """Parse sitemap.xml for URLs"""
        urls = []
        try:
            root = ET.fromstring(content)
            # Handle both sitemap index and urlset
            for elem in root.iter():
                if elem.tag.endswith('loc'):
                    url = elem.text
                    if url:
                        urls.append(url)
        except Exception:
            # Fallback to regex parsing
            urls = re.findall(r'<loc>(.*?)</loc>', content)
        return urls
    
    def fetch_security_txt(self) -> Optional[str]:
        """Fetch security.txt"""
        for path in ['/.well-known/security.txt', '/security.txt']:
            try:
                url = f"{self.base_url}{path}"
                response = requests.get(url, timeout=self.timeout, verify=False)
                if response.status_code == 200:
                    return response.text
            except Exception:
                continue
        return None
    
    def parse_security_txt(self, content: str) -> Dict[str, List[str]]:
        """Parse security.txt"""
        data = {
            'contacts': [],
            'policy': [],
            'acknowledgments': []
        }
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('Contact:'):
                data['contacts'].append(line.split(':', 1)[1].strip())
            elif line.startswith('Policy:'):
                data['policy'].append(line.split(':', 1)[1].strip())
            elif line.startswith('Acknowledgments:'):
                data['acknowledgments'].append(line.split(':', 1)[1].strip())
        return data
    
    def fetch_well_known(self) -> Dict[str, str]:
        """Fetch common .well-known files"""
        well_known_files = [
            'security.txt',
            'change-password',
            'openid-configuration',
            'assetlinks.json',
            'apple-app-site-association'
        ]
        results = {}
        for file in well_known_files:
            try:
                url = f"{self.base_url}/.well-known/{file}"
                response = requests.get(url, timeout=self.timeout, verify=False)
                if response.status_code == 200:
                    results[file] = response.text
            except Exception:
                continue
        return results
    
    def expand_wildcards(self, paths: List[str]) -> List[str]:
        """Expand wildcard patterns"""
        expanded = []
        for path in paths:
            if '*' in path:
                # Remove wildcards for basic expansion
                expanded.append(path.replace('*', ''))
                # Add common patterns
                if path.endswith('/*'):
                    base = path[:-2]
                    expanded.extend([
                        f"{base}/admin",
                        f"{base}/api",
                        f"{base}/v1",
                        f"{base}/v2"
                    ])
            else:
                expanded.append(path)
        return expanded
    
    def get_unified_scope(self) -> Dict[str, any]:
        """Get unified scope from all sources"""
        scope_data = {
            'base_url': self.base_url,
            'robots_paths': [],
            'sitemap_urls': [],
            'security_info': {},
            'well_known_files': [],
            'all_paths': set()
        }
        
        # Fetch robots.txt
        robots_content = self.fetch_robots_txt()
        if robots_content:
            scope_data['robots_paths'] = self.parse_robots_txt(robots_content)
            scope_data['all_paths'].update(scope_data['robots_paths'])
        
        # Fetch sitemaps
        sitemap_content = self.fetch_sitemap()
        if sitemap_content:
            scope_data['sitemap_urls'] = self.parse_sitemap(sitemap_content)
            # Extract paths from sitemap URLs
            for url in scope_data['sitemap_urls']:
                parsed = urlparse(url)
                scope_data['all_paths'].add(parsed.path)
        
        # Fetch security.txt
        security_content = self.fetch_security_txt()
        if security_content:
            scope_data['security_info'] = self.parse_security_txt(security_content)
        
        # Fetch .well-known files
        well_known = self.fetch_well_known()
        scope_data['well_known_files'] = list(well_known.keys())
        
        # Expand wildcards
        expanded_paths = self.expand_wildcards(list(scope_data['all_paths']))
        scope_data['all_paths'] = set(expanded_paths)
        
        return scope_data
    
    def save_scope(self, output_file: str) -> None:
        """Save scope to file"""
        scope_data = self.get_unified_scope()
        with open(output_file, 'w') as f:
            f.write(f"# Scope for {self.base_url}\n\n")
            f.write("## Paths from robots.txt\n")
            for path in scope_data['robots_paths']:
                f.write(f"{path}\n")
            f.write("\n## URLs from sitemap\n")
            for url in scope_data['sitemap_urls'][:50]:  # Limit output
                f.write(f"{url}\n")
            f.write("\n## All unique paths\n")
            for path in sorted(scope_data['all_paths']):
                f.write(f"{path}\n")
