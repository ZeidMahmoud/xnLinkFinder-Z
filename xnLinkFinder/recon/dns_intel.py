"""
DNS Intelligence gathering for xnLinkFinder-Z.

Features:
- Zone transfer detection (AXFR)
- DNS record enumeration (A, AAAA, CNAME, MX, TXT, NS)
- DNSSEC validation
- DNS history lookup
- Subdomain brute-forcing with smart wordlists
"""

from typing import List, Dict, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)


class DNSIntelligence:
    """DNS intelligence gathering and analysis."""
    
    def __init__(self):
        """Initialize DNS intelligence module."""
        self.common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'ns2',
            'webdisk', 'ns', 'cpanel', 'whm', 'autodiscover', 'autoconfig',
            'api', 'dev', 'staging', 'test', 'admin', 'portal', 'app',
            'mobile', 'blog', 'shop', 'store', 'support', 'help', 'secure',
            'vpn', 'remote', 'ssh', 'git', 'gitlab', 'github', 'jenkins',
            'dashboard', 'analytics', 'monitoring', 'logs', 'status'
        ]
    
    def query_dns_record(self, domain: str, record_type: str) -> List[str]:
        """
        Query DNS records of a specific type.
        
        Args:
            domain: Target domain
            record_type: DNS record type (A, AAAA, MX, TXT, NS, CNAME, etc.)
            
        Returns:
            List of record values
        """
        try:
            import dns.resolver
            
            answers = dns.resolver.resolve(domain, record_type)
            results = [str(rdata) for rdata in answers]
            
            logger.info(f"Found {len(results)} {record_type} records for {domain}")
            return results
        
        except dns.resolver.NXDOMAIN:
            logger.debug(f"Domain {domain} does not exist")
            return []
        except dns.resolver.NoAnswer:
            logger.debug(f"No {record_type} records found for {domain}")
            return []
        except Exception as e:
            logger.error(f"Error querying {record_type} records for {domain}: {e}")
            return []
    
    def enumerate_dns_records(self, domain: str) -> Dict[str, List[str]]:
        """
        Enumerate all common DNS record types.
        
        Args:
            domain: Target domain
            
        Returns:
            Dictionary mapping record type to list of values
        """
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'SRV']
        
        results = {}
        for record_type in record_types:
            records = self.query_dns_record(domain, record_type)
            if records:
                results[record_type] = records
        
        return results
    
    def attempt_zone_transfer(self, domain: str) -> Dict[str, any]:
        """
        Attempt DNS zone transfer (AXFR).
        
        Args:
            domain: Target domain
            
        Returns:
            Zone transfer results or error information
        """
        try:
            import dns.resolver
            import dns.zone
            import dns.query
            
            # Get nameservers
            ns_records = self.query_dns_record(domain, 'NS')
            
            if not ns_records:
                return {
                    'success': False,
                    'error': 'No nameservers found'
                }
            
            results = {
                'success': False,
                'nameservers_tested': [],
                'vulnerable_nameservers': [],
                'records': []
            }
            
            # Try zone transfer on each nameserver
            for ns in ns_records:
                ns = ns.rstrip('.')
                results['nameservers_tested'].append(ns)
                
                try:
                    # Resolve nameserver IP
                    ns_ips = self.query_dns_record(ns, 'A')
                    if not ns_ips:
                        continue
                    
                    ns_ip = ns_ips[0]
                    
                    # Attempt zone transfer
                    zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain))
                    
                    # If we get here, zone transfer succeeded
                    results['success'] = True
                    results['vulnerable_nameservers'].append(ns)
                    
                    # Extract all records
                    for name, node in zone.nodes.items():
                        for rdataset in node.rdatasets:
                            for rdata in rdataset:
                                results['records'].append({
                                    'name': str(name),
                                    'type': dns.rdatatype.to_text(rdataset.rdtype),
                                    'value': str(rdata)
                                })
                    
                    logger.warning(f"Zone transfer successful on {ns} for {domain}!")
                
                except Exception as e:
                    logger.debug(f"Zone transfer failed on {ns}: {e}")
                    continue
            
            if not results['success']:
                results['error'] = 'Zone transfer not allowed on any nameserver'
            
            return results
        
        except Exception as e:
            logger.error(f"Error attempting zone transfer for {domain}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def brute_force_subdomains(self, domain: str, wordlist: Optional[List[str]] = None,
                               threads: int = 10) -> List[str]:
        """
        Brute-force subdomain discovery.
        
        Args:
            domain: Target domain
            wordlist: Custom subdomain wordlist (uses default if None)
            threads: Number of concurrent threads
            
        Returns:
            List of discovered subdomains
        """
        if wordlist is None:
            wordlist = self.common_subdomains
        
        discovered = []
        
        for subdomain in wordlist:
            full_domain = f"{subdomain}.{domain}"
            
            # Try A record
            records = self.query_dns_record(full_domain, 'A')
            if records:
                discovered.append(full_domain)
                logger.info(f"Discovered subdomain: {full_domain} -> {records[0]}")
        
        return discovered
    
    def check_dnssec(self, domain: str) -> Dict[str, any]:
        """
        Check DNSSEC validation status.
        
        Args:
            domain: Target domain
            
        Returns:
            DNSSEC status information
        """
        try:
            import dns.resolver
            import dns.dnssec
            
            result = {
                'domain': domain,
                'dnssec_enabled': False,
                'dnskey_records': [],
                'ds_records': []
            }
            
            # Check for DNSKEY records
            try:
                dnskey_records = self.query_dns_record(domain, 'DNSKEY')
                if dnskey_records:
                    result['dnssec_enabled'] = True
                    result['dnskey_records'] = dnskey_records
            except Exception:
                pass
            
            # Check for DS records
            try:
                ds_records = self.query_dns_record(domain, 'DS')
                if ds_records:
                    result['ds_records'] = ds_records
            except Exception:
                pass
            
            return result
        
        except Exception as e:
            logger.error(f"Error checking DNSSEC for {domain}: {e}")
            return {
                'domain': domain,
                'error': str(e)
            }
    
    def analyze_dns(self, domain: str) -> Dict[str, any]:
        """
        Comprehensive DNS analysis.
        
        Args:
            domain: Target domain
            
        Returns:
            Complete DNS analysis results
        """
        logger.info(f"Starting comprehensive DNS analysis for {domain}")
        
        analysis = {
            'domain': domain,
            'records': self.enumerate_dns_records(domain),
            'zone_transfer': self.attempt_zone_transfer(domain),
            'dnssec': self.check_dnssec(domain),
            'discovered_subdomains': []
        }
        
        # Try subdomain brute-force (limited for performance)
        analysis['discovered_subdomains'] = self.brute_force_subdomains(domain)
        
        # Extract IPs
        ips = set()
        if 'A' in analysis['records']:
            ips.update(analysis['records']['A'])
        if 'AAAA' in analysis['records']:
            ips.update(analysis['records']['AAAA'])
        
        analysis['ip_addresses'] = list(ips)
        analysis['mail_servers'] = analysis['records'].get('MX', [])
        analysis['nameservers'] = analysis['records'].get('NS', [])
        
        return analysis
    
    def find_dns_history(self, domain: str) -> Dict[str, any]:
        """
        Look up historical DNS records (requires external API).
        
        Args:
            domain: Target domain
            
        Returns:
            Historical DNS information
        """
        # This would typically use an external service like SecurityTrails, DNSHistory, etc.
        # For now, return current records as baseline
        return {
            'domain': domain,
            'current_records': self.enumerate_dns_records(domain),
            'note': 'Historical DNS lookup requires external API integration'
        }


def enumerate_dns(domain: str) -> Dict[str, List[str]]:
    """
    Convenience function to enumerate DNS records.
    
    Args:
        domain: Target domain
        
    Returns:
        Dictionary of DNS records by type
    """
    intel = DNSIntelligence()
    return intel.enumerate_dns_records(domain)


def discover_subdomains(domain: str, wordlist: Optional[List[str]] = None) -> List[str]:
    """
    Convenience function to discover subdomains.
    
    Args:
        domain: Target domain
        wordlist: Optional custom wordlist
        
    Returns:
        List of discovered subdomains
    """
    intel = DNSIntelligence()
    return intel.brute_force_subdomains(domain, wordlist=wordlist)
