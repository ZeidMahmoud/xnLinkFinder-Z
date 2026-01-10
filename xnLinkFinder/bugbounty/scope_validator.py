"""
Scope Validator for Bug Bounty Programs.

Features:
- Auto-check if target is in scope
- Parse program policies
- Wildcard scope handling
- Out-of-scope warnings
- Rate limit policy detection
"""

from typing import List, Dict, Optional, Set, Tuple
import logging
import re
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ScopeValidator:
    """Validate targets against bug bounty program scopes."""
    
    def __init__(self):
        """Initialize scope validator."""
        self.wildcard_patterns = {}
    
    def parse_scope(self, scope_definition: List[str]) -> Dict[str, List[str]]:
        """
        Parse scope definition into structured format.
        
        Args:
            scope_definition: List of scope entries (domains, IPs, wildcards)
            
        Returns:
            Dictionary with categorized scope entries
        """
        parsed = {
            'domains': [],
            'wildcards': [],
            'ip_ranges': [],
            'specific_urls': [],
            'out_of_scope': []
        }
        
        for entry in scope_definition:
            entry = entry.strip()
            
            if not entry or entry.startswith('#'):
                continue
            
            # Check for out-of-scope marker
            if entry.startswith('!') or entry.lower().startswith('out of scope'):
                parsed['out_of_scope'].append(entry.lstrip('!').strip())
                continue
            
            # Wildcard domain
            if entry.startswith('*.'):
                parsed['wildcards'].append(entry)
            # IP range
            elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$', entry):
                parsed['ip_ranges'].append(entry)
            # Full URL
            elif entry.startswith('http://') or entry.startswith('https://'):
                parsed['specific_urls'].append(entry)
            # Plain domain
            else:
                parsed['domains'].append(entry)
        
        return parsed
    
    def is_in_scope(self, target: str, scope: Dict[str, List[str]]) -> Dict[str, any]:
        """
        Check if a target is in scope.
        
        Args:
            target: Target URL or domain
            scope: Parsed scope definition
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'target': target,
            'in_scope': False,
            'match_type': None,
            'matched_entry': None,
            'warnings': []
        }
        
        # Parse target
        if target.startswith('http://') or target.startswith('https://'):
            parsed = urlparse(target)
            domain = parsed.netloc
            full_url = target
        else:
            domain = target
            full_url = None
        
        # Check if out of scope
        for oos_entry in scope.get('out_of_scope', []):
            if self._matches_pattern(domain, oos_entry):
                result['in_scope'] = False
                result['match_type'] = 'out_of_scope'
                result['matched_entry'] = oos_entry
                result['warnings'].append(f"Target matches out-of-scope entry: {oos_entry}")
                return result
        
        # Check exact domain matches
        for scope_domain in scope.get('domains', []):
            if domain == scope_domain or domain.endswith('.' + scope_domain):
                result['in_scope'] = True
                result['match_type'] = 'exact_domain'
                result['matched_entry'] = scope_domain
                return result
        
        # Check wildcard matches
        for wildcard in scope.get('wildcards', []):
            if self._matches_wildcard(domain, wildcard):
                result['in_scope'] = True
                result['match_type'] = 'wildcard'
                result['matched_entry'] = wildcard
                return result
        
        # Check specific URL matches
        if full_url:
            for scope_url in scope.get('specific_urls', []):
                if full_url.startswith(scope_url):
                    result['in_scope'] = True
                    result['match_type'] = 'specific_url'
                    result['matched_entry'] = scope_url
                    return result
        
        # Check IP ranges (simplified)
        for ip_range in scope.get('ip_ranges', []):
            # Would need proper IP range checking here
            result['warnings'].append(f"IP range checking not fully implemented: {ip_range}")
        
        return result
    
    def _matches_pattern(self, domain: str, pattern: str) -> bool:
        """Check if domain matches a pattern (with wildcard support)."""
        # Remove wildcards for simple matching
        pattern = pattern.replace('*.', '')
        return domain == pattern or domain.endswith('.' + pattern)
    
    def _matches_wildcard(self, domain: str, wildcard: str) -> bool:
        """
        Check if domain matches wildcard pattern.
        
        Args:
            domain: Target domain
            wildcard: Wildcard pattern (e.g., *.example.com)
            
        Returns:
            True if matches
        """
        if wildcard.startswith('*.'):
            base_domain = wildcard[2:]
            return domain.endswith('.' + base_domain) or domain == base_domain
        return domain == wildcard
    
    def validate_batch(self, targets: List[str], scope: Dict[str, List[str]]) -> Dict[str, any]:
        """
        Validate multiple targets against scope.
        
        Args:
            targets: List of target URLs/domains
            scope: Parsed scope definition
            
        Returns:
            Batch validation results
        """
        results = {
            'total_targets': len(targets),
            'in_scope': [],
            'out_of_scope': [],
            'warnings': []
        }
        
        for target in targets:
            validation = self.is_in_scope(target, scope)
            
            if validation['in_scope']:
                results['in_scope'].append({
                    'target': target,
                    'match': validation['matched_entry']
                })
            else:
                results['out_of_scope'].append({
                    'target': target,
                    'reason': validation.get('match_type', 'no_match')
                })
            
            if validation['warnings']:
                results['warnings'].extend(validation['warnings'])
        
        results['in_scope_count'] = len(results['in_scope'])
        results['out_of_scope_count'] = len(results['out_of_scope'])
        
        return results
    
    def detect_rate_limits(self, policy_text: str) -> Dict[str, any]:
        """
        Detect rate limit policies from program text.
        
        Args:
            policy_text: Program policy text
            
        Returns:
            Detected rate limit information
        """
        rate_limits = {
            'detected': False,
            'requests_per_second': None,
            'requests_per_minute': None,
            'requests_per_hour': None,
            'notes': []
        }
        
        policy_lower = policy_text.lower()
        
        # Look for rate limit mentions
        if any(term in policy_lower for term in ['rate limit', 'throttle', 'requests per']):
            rate_limits['detected'] = True
            
            # Try to extract specific numbers
            # Pattern: "X requests per Y"
            patterns = [
                (r'(\d+)\s*requests?\s*per\s*second', 'requests_per_second'),
                (r'(\d+)\s*requests?\s*per\s*minute', 'requests_per_minute'),
                (r'(\d+)\s*requests?\s*per\s*hour', 'requests_per_hour'),
            ]
            
            for pattern, key in patterns:
                match = re.search(pattern, policy_lower)
                if match:
                    rate_limits[key] = int(match.group(1))
        
        # Look for testing guidelines
        if 'slow' in policy_lower or 'gentle' in policy_lower:
            rate_limits['notes'].append('Use gentle/slow scanning as requested')
        
        if 'no automated' in policy_lower or 'manual only' in policy_lower:
            rate_limits['notes'].append('Automated testing may be restricted')
        
        return rate_limits
    
    def extract_prohibited_activities(self, policy_text: str) -> List[str]:
        """
        Extract prohibited activities from policy.
        
        Args:
            policy_text: Program policy text
            
        Returns:
            List of prohibited activities
        """
        prohibited = []
        
        policy_lower = policy_text.lower()
        
        # Common prohibited activities
        checks = {
            'DoS/DDoS attacks': ['dos', 'ddos', 'denial of service'],
            'Social engineering': ['social engineering', 'phishing'],
            'Physical security testing': ['physical', 'building'],
            'Network attacks': ['network', 'mitm', 'man in the middle'],
            'Data destruction': ['destroy', 'delete data', 'corruption'],
            'Automated scanning without permission': ['automated', 'scanner'],
        }
        
        for activity, keywords in checks.items():
            if any(keyword in policy_lower for keyword in keywords):
                prohibited.append(activity)
        
        return prohibited
    
    def generate_scope_report(self, scope_definition: List[str]) -> str:
        """
        Generate a human-readable scope report.
        
        Args:
            scope_definition: List of scope entries
            
        Returns:
            Formatted scope report
        """
        parsed = self.parse_scope(scope_definition)
        
        report_lines = [
            "=" * 60,
            "BUG BOUNTY SCOPE REPORT",
            "=" * 60,
            ""
        ]
        
        if parsed['domains']:
            report_lines.append(f"In-Scope Domains ({len(parsed['domains'])}):")
            for domain in parsed['domains']:
                report_lines.append(f"  ✓ {domain}")
            report_lines.append("")
        
        if parsed['wildcards']:
            report_lines.append(f"Wildcard Scopes ({len(parsed['wildcards'])}):")
            for wildcard in parsed['wildcards']:
                report_lines.append(f"  ✓ {wildcard}")
            report_lines.append("")
        
        if parsed['specific_urls']:
            report_lines.append(f"Specific URLs ({len(parsed['specific_urls'])}):")
            for url in parsed['specific_urls']:
                report_lines.append(f"  ✓ {url}")
            report_lines.append("")
        
        if parsed['out_of_scope']:
            report_lines.append(f"Out of Scope ({len(parsed['out_of_scope'])}):")
            for oos in parsed['out_of_scope']:
                report_lines.append(f"  ✗ {oos}")
            report_lines.append("")
        
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)


def validate_scope(target: str, scope_definition: List[str]) -> bool:
    """
    Convenience function to validate a single target.
    
    Args:
        target: Target URL or domain
        scope_definition: List of scope entries
        
    Returns:
        True if in scope, False otherwise
    """
    validator = ScopeValidator()
    parsed_scope = validator.parse_scope(scope_definition)
    result = validator.is_in_scope(target, parsed_scope)
    return result['in_scope']
