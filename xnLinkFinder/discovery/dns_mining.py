"""DNS record mining for endpoint discovery."""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DNSMiner:
    """Mine endpoints from DNS records."""
    
    def __init__(self):
        pass
    
    def mine_txt_records(self, domain: str) -> List[str]:
        """Extract endpoints from TXT records."""
        endpoints = []
        try:
            import dns.resolver
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                for txt_string in rdata.strings:
                    endpoints.append(txt_string.decode('utf-8'))
        except Exception as e:
            logger.error(f"DNS TXT mining failed: {e}")
        return endpoints
    
    def enumerate_subdomains(self, domain: str) -> List[str]:
        """Enumerate subdomains via DNS."""
        subdomains = []
        common_subs = ['www', 'api', 'dev', 'staging', 'test', 'admin', 'mail']
        try:
            import dns.resolver
            for sub in common_subs:
                try:
                    dns.resolver.resolve(f'{sub}.{domain}', 'A')
                    subdomains.append(f'{sub}.{domain}')
                except:
                    pass
        except Exception as e:
            logger.error(f"Subdomain enumeration failed: {e}")
        return subdomains

def mine_dns_endpoints(domain: str) -> Dict[str, List[str]]:
    """Convenience function for DNS mining."""
    miner = DNSMiner()
    return {
        'txt_records': miner.mine_txt_records(domain),
        'subdomains': miner.enumerate_subdomains(domain)
    }
