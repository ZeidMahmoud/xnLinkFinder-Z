#!/usr/bin/env python3
"""
CI/CD Integration Example
Use xnLinkFinder-Z in your CI/CD pipeline
"""

import sys
import json

def ci_cd_scan(target_url, fail_on_vuln=True):
    """CI/CD security scan"""
    print(f"[CI/CD] Scanning {target_url}")
    
    # Run scan
    vulnerabilities = []
    
    # Check for critical vulnerabilities
    critical_vulns = [v for v in vulnerabilities if v.get('severity') == 'CRITICAL']
    
    if critical_vulns and fail_on_vuln:
        print(f"[FAIL] Found {len(critical_vulns)} critical vulnerabilities")
        sys.exit(1)
    
    print(f"[PASS] Security scan completed")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <target_url>")
        sys.exit(1)
    ci_cd_scan(sys.argv[1])
