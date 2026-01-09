#!/usr/bin/env python3
"""
Bug Bounty Workflow Example
Automated recon and scanning for bug bounty hunting
"""

from xnLinkFinder.sdk import XnLinkFinderClient

def bug_bounty_scan(target_domain):
    """Complete bug bounty workflow"""
    print(f"[*] Starting bug bounty scan for {target_domain}")
    
    client = XnLinkFinderClient()
    
    # Phase 1: Endpoint Discovery
    print("[*] Phase 1: Discovering endpoints...")
    scan = client.scan(
        target_domain,
        depth=3,
        include_wayback=True,
        include_github=True
    )
    
    # Phase 2: Security Scanning
    print("[*] Phase 2: Security scanning...")
    security_scan = client.scan(
        target_domain,
        scan_cors=True,
        scan_jwt=True,
        scan_open_redirect=True,
        test_ssrf=True
    )
    
    # Phase 3: Report Generation
    print("[*] Phase 3: Generating report...")
    results = client.get_results(scan['scan_id'])
    
    print(f"[+] Found {len(results.get('endpoints', []))} endpoints")
    print(f"[+] Found {len(results.get('vulnerabilities', []))} potential vulnerabilities")
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <target_domain>")
        sys.exit(1)
    
    bug_bounty_scan(sys.argv[1])
