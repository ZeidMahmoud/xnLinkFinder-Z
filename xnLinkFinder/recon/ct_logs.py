"""
Certificate Transparency Logs integration for xnLinkFinder-Z.

Features:
- Query crt.sh, Google CT, Facebook CT
- Discover subdomains from certificates
- Historical certificate analysis
- Wildcard detection
"""

from typing import List, Dict, Optional, Set
import logging
import re

logger = logging.getLogger(__name__)


class CTLogsScanner:
    """Certificate Transparency logs scanner for subdomain discovery."""
    
    def __init__(self):
        """Initialize CT logs scanner."""
        self.sources = {
            'crt.sh': 'https://crt.sh/?q={domain}&output=json',
            'certspotter': 'https://api.certspotter.com/v1/issuances?domain={domain}&include_subdomains=true&expand=dns_names'
        }
    
    def search_crtsh(self, domain: str) -> List[Dict[str, any]]:
        """
        Search crt.sh for certificates.
        
        Args:
            domain: Target domain
            
        Returns:
            List of certificate entries
        """
        try:
            import requests
            
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                certificates = response.json()
                logger.info(f"Found {len(certificates)} certificates for {domain} on crt.sh")
                return certificates
            else:
                logger.warning(f"crt.sh returned status {response.status_code}")
                return []
        
        except Exception as e:
            logger.error(f"Error querying crt.sh for {domain}: {e}")
            return []
    
    def extract_subdomains(self, certificates: List[Dict[str, any]], base_domain: str) -> Set[str]:
        """
        Extract unique subdomains from certificate data.
        
        Args:
            certificates: List of certificate entries
            base_domain: Base domain to filter results
            
        Returns:
            Set of discovered subdomains
        """
        subdomains = set()
        
        for cert in certificates:
            # Extract from name_value field
            if 'name_value' in cert:
                names = cert['name_value'].split('\n')
                for name in names:
                    name = name.strip().lower()
                    
                    # Skip wildcards and invalid entries
                    if name.startswith('*'):
                        name = name[2:]  # Remove *.
                    
                    # Check if it's a subdomain of base_domain
                    if name.endswith(base_domain) and name != base_domain:
                        subdomains.add(name)
            
            # Also check common_name
            if 'common_name' in cert:
                name = cert['common_name'].strip().lower()
                if name.startswith('*'):
                    name = name[2:]
                if name.endswith(base_domain) and name != base_domain:
                    subdomains.add(name)
        
        return subdomains
    
    def find_wildcards(self, certificates: List[Dict[str, any]]) -> Set[str]:
        """
        Find wildcard certificates.
        
        Args:
            certificates: List of certificate entries
            
        Returns:
            Set of wildcard patterns
        """
        wildcards = set()
        
        for cert in certificates:
            if 'name_value' in cert:
                names = cert['name_value'].split('\n')
                for name in names:
                    if name.strip().startswith('*'):
                        wildcards.add(name.strip())
            
            if 'common_name' in cert and cert['common_name'].startswith('*'):
                wildcards.add(cert['common_name'])
        
        return wildcards
    
    def analyze_certificates(self, domain: str) -> Dict[str, any]:
        """
        Comprehensive certificate analysis for a domain.
        
        Args:
            domain: Target domain
            
        Returns:
            Analysis dictionary with subdomains, wildcards, and statistics
        """
        # Search for certificates
        certificates = self.search_crtsh(domain)
        
        if not certificates:
            return {
                'domain': domain,
                'certificates_found': 0,
                'subdomains': [],
                'wildcards': [],
                'error': 'No certificates found or API error'
            }
        
        # Extract subdomains
        subdomains = self.extract_subdomains(certificates, domain)
        wildcards = self.find_wildcards(certificates)
        
        # Analyze certificate issuers
        issuers = {}
        for cert in certificates:
            issuer = cert.get('issuer_name', 'Unknown')
            issuers[issuer] = issuers.get(issuer, 0) + 1
        
        # Sort by issuance count
        top_issuers = sorted(issuers.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'domain': domain,
            'certificates_found': len(certificates),
            'unique_subdomains': len(subdomains),
            'subdomains': sorted(list(subdomains)),
            'wildcards': sorted(list(wildcards)),
            'top_issuers': [{'name': name, 'count': count} for name, count in top_issuers]
        }
    
    def historical_analysis(self, domain: str) -> Dict[str, any]:
        """
        Perform historical certificate analysis.
        
        Args:
            domain: Target domain
            
        Returns:
            Historical analysis with timeline information
        """
        certificates = self.search_crtsh(domain)
        
        if not certificates:
            return {
                'domain': domain,
                'error': 'No certificates found'
            }
        
        # Parse dates
        from datetime import datetime
        
        timeline = []
        for cert in certificates:
            try:
                entry_timestamp = cert.get('entry_timestamp', '')
                not_before = cert.get('not_before', '')
                not_after = cert.get('not_after', '')
                
                timeline.append({
                    'entry_timestamp': entry_timestamp,
                    'not_before': not_before,
                    'not_after': not_after,
                    'issuer': cert.get('issuer_name', 'Unknown'),
                    'name_value': cert.get('name_value', '').split('\n')[0]
                })
            except Exception as e:
                logger.debug(f"Error parsing certificate date: {e}")
                continue
        
        # Sort by entry timestamp
        timeline.sort(key=lambda x: x['entry_timestamp'], reverse=True)
        
        return {
            'domain': domain,
            'total_certificates': len(certificates),
            'timeline': timeline[:20],  # Most recent 20
            'first_seen': timeline[-1]['entry_timestamp'] if timeline else None,
            'last_seen': timeline[0]['entry_timestamp'] if timeline else None
        }
    
    def discover_infrastructure(self, domain: str) -> Dict[str, any]:
        """
        Discover infrastructure patterns from certificates.
        
        Args:
            domain: Target domain
            
        Returns:
            Infrastructure discovery results
        """
        result = self.analyze_certificates(domain)
        
        subdomains = result.get('subdomains', [])
        
        # Categorize subdomains
        categories = {
            'development': [],
            'staging': [],
            'production': [],
            'api': [],
            'admin': [],
            'mail': [],
            'cdn': [],
            'cloud': [],
            'other': []
        }
        
        for subdomain in subdomains:
            lower = subdomain.lower()
            
            if any(keyword in lower for keyword in ['dev', 'devel', 'development']):
                categories['development'].append(subdomain)
            elif any(keyword in lower for keyword in ['stag', 'staging', 'test', 'qa']):
                categories['staging'].append(subdomain)
            elif any(keyword in lower for keyword in ['api', 'rest', 'graphql']):
                categories['api'].append(subdomain)
            elif any(keyword in lower for keyword in ['admin', 'manage', 'control']):
                categories['admin'].append(subdomain)
            elif any(keyword in lower for keyword in ['mail', 'smtp', 'imap', 'pop']):
                categories['mail'].append(subdomain)
            elif any(keyword in lower for keyword in ['cdn', 'static', 'assets', 'media']):
                categories['cdn'].append(subdomain)
            elif any(keyword in lower for keyword in ['aws', 'azure', 's3', 'cloudfront', 'gcp']):
                categories['cloud'].append(subdomain)
            elif any(keyword in lower for keyword in ['www', 'prod', 'app']):
                categories['production'].append(subdomain)
            else:
                categories['other'].append(subdomain)
        
        return {
            'domain': domain,
            'total_subdomains': len(subdomains),
            'categories': {k: v for k, v in categories.items() if v},  # Only non-empty
            'high_value_targets': categories['admin'] + categories['api'] + categories['development']
        }


def scan_ct_logs(domain: str) -> Dict[str, any]:
    """
    Convenience function to scan CT logs for a domain.
    
    Args:
        domain: Target domain
        
    Returns:
        Certificate analysis results
    """
    scanner = CTLogsScanner()
    return scanner.analyze_certificates(domain)


def discover_subdomains_from_ct(domain: str) -> List[str]:
    """
    Convenience function to discover subdomains from CT logs.
    
    Args:
        domain: Target domain
        
    Returns:
        List of discovered subdomains
    """
    scanner = CTLogsScanner()
    result = scanner.analyze_certificates(domain)
    return result.get('subdomains', [])
