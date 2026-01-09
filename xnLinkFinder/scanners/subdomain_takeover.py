"""
Subdomain Takeover Checker

Detects vulnerable subdomains that may be taken over including:
- Dangling DNS records (CNAME, A)
- Vulnerable cloud services (S3, Azure, Heroku, GitHub Pages, etc.)
- Service fingerprinting
"""

import requests
import socket
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print("[!] dnspython not installed. Subdomain takeover checking will be limited.")


class SubdomainTakeoverChecker:
    """Check for subdomain takeover vulnerabilities"""
    
    # Fingerprints for common vulnerable services
    FINGERPRINTS = {
        'github': {
            'cname': 'github.io',
            'response': ['There isn\'t a GitHub Pages site here', 'For root URLs'],
            'severity': 'HIGH'
        },
        'heroku': {
            'cname': 'herokuapp.com',
            'response': ['No such app', 'There\'s nothing here, yet'],
            'severity': 'HIGH'
        },
        'aws_s3': {
            'cname': 's3.amazonaws.com',
            'response': ['NoSuchBucket', 'The specified bucket does not exist'],
            'severity': 'HIGH'
        },
        'azure': {
            'cname': 'azurewebsites.net',
            'response': ['404 Web Site not found', 'Error 404'],
            'severity': 'HIGH'
        },
        'shopify': {
            'cname': 'myshopify.com',
            'response': ['Sorry, this shop is currently unavailable'],
            'severity': 'HIGH'
        },
        'fastly': {
            'cname': 'fastly.net',
            'response': ['Fastly error: unknown domain'],
            'severity': 'HIGH'
        },
        'pantheon': {
            'cname': 'pantheonsite.io',
            'response': ['404 error unknown site'],
            'severity': 'HIGH'
        },
        'tumblr': {
            'cname': 'tumblr.com',
            'response': ['Whatever you were looking for doesn\'t currently exist'],
            'severity': 'HIGH'
        },
        'wordpress': {
            'cname': 'wordpress.com',
            'response': ['Do you want to register'],
            'severity': 'HIGH'
        },
        'ghost': {
            'cname': 'ghost.io',
            'response': ['The thing you were looking for is no longer here'],
            'severity': 'MEDIUM'
        },
    }
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = False):
        """
        Initialize subdomain takeover checker
        
        Args:
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
    def check(self, domain: str) -> Optional[Dict]:
        """
        Check a domain for subdomain takeover vulnerability
        
        Args:
            domain: Domain/subdomain to check
            
        Returns:
            Vulnerability details if found, None otherwise
        """
        # Get CNAME records
        cnames = self._get_cname_records(domain)
        
        if not cnames:
            return None
            
        # Check each CNAME for known vulnerable patterns
        for cname in cnames:
            vuln = self._check_cname(domain, cname)
            if vuln:
                return vuln
                
        return None
    
    def _get_cname_records(self, domain: str) -> List[str]:
        """Get CNAME records for a domain"""
        cnames = []
        
        if not DNS_AVAILABLE:
            return cnames
            
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout
            
            answers = resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                cnames.append(str(rdata.target).rstrip('.'))
                
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, 
                dns.resolver.NoNameservers, dns.exception.Timeout):
            pass
        except Exception as e:
            print(f"[!] DNS error for {domain}: {str(e)}")
            
        return cnames
    
    def _check_cname(self, domain: str, cname: str) -> Optional[Dict]:
        """Check if CNAME points to a vulnerable service"""
        # Check against known fingerprints
        for service_name, fingerprint in self.FINGERPRINTS.items():
            if fingerprint['cname'] in cname:
                # Try to verify by fetching the page
                if self._verify_vulnerability(domain, fingerprint['response']):
                    return {
                        'domain': domain,
                        'type': 'SUBDOMAIN_TAKEOVER',
                        'service': service_name,
                        'cname': cname,
                        'severity': fingerprint['severity'],
                        'description': f'Subdomain pointing to unclaimed {service_name} resource',
                    }
                    
        return None
    
    def _verify_vulnerability(self, domain: str, 
                             response_patterns: List[str]) -> bool:
        """Verify vulnerability by checking HTTP response"""
        try:
            # Try both HTTP and HTTPS
            for protocol in ['https', 'http']:
                try:
                    url = f"{protocol}://{domain}"
                    response = requests.get(
                        url,
                        timeout=self.timeout,
                        verify=self.verify_ssl,
                        allow_redirects=True
                    )
                    
                    content = response.text.lower()
                    
                    # Check if any response pattern matches
                    for pattern in response_patterns:
                        if pattern.lower() in content:
                            return True
                            
                except requests.RequestException:
                    continue
                    
        except Exception:
            pass
            
        return False


def check_subdomains(domains: List[str], **kwargs) -> Dict[str, Dict]:
    """
    Convenience function to check multiple subdomains
    
    Args:
        domains: List of domains to check
        **kwargs: Additional arguments for SubdomainTakeoverChecker
        
    Returns:
        Dictionary mapping domains to vulnerabilities
    """
    checker = SubdomainTakeoverChecker(**kwargs)
    results = {}
    
    for domain in domains:
        try:
            vuln = checker.check(domain)
            if vuln:
                results[domain] = vuln
        except Exception as e:
            print(f"[!] Error checking {domain}: {str(e)}")
            
    return results
