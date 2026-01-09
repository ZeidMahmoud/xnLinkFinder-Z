"""
Payout Estimator for Bug Bounty Programs.

Features:
- Estimate potential bounty based on finding
- Historical payout data
- Severity-based estimation
- Program-specific adjustments
"""

from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class PayoutEstimator:
    """Estimate bug bounty payouts based on vulnerability details."""
    
    def __init__(self):
        """Initialize payout estimator."""
        # Historical average payouts by severity (in USD)
        self.base_payouts = {
            'critical': {'min': 5000, 'max': 50000, 'avg': 15000},
            'high': {'min': 1000, 'max': 10000, 'avg': 3000},
            'medium': {'min': 250, 'max': 2500, 'avg': 750},
            'low': {'min': 50, 'max': 500, 'avg': 150},
            'info': {'min': 0, 'max': 100, 'avg': 25}
        }
        
        # Program type multipliers
        self.program_multipliers = {
            'public': 1.0,
            'private': 1.3,
            'vdp': 0.5,  # Vulnerability Disclosure Program (often no payout)
        }
        
        # Vulnerability type multipliers
        self.vuln_multipliers = {
            'rce': 2.0,
            'authentication_bypass': 1.8,
            'sqli': 1.5,
            'privilege_escalation': 1.5,
            'idor': 1.2,
            'xss_stored': 1.2,
            'ssrf': 1.3,
            'xxe': 1.4,
            'xss_reflected': 1.0,
            'csrf': 0.9,
            'open_redirect': 0.7,
            'info_disclosure': 0.6,
        }
    
    def estimate_payout(self,
                       severity: str,
                       vulnerability_type: str,
                       program_type: str = 'public',
                       asset_type: str = 'web') -> Dict[str, any]:
        """
        Estimate payout for a vulnerability.
        
        Args:
            severity: Vulnerability severity (critical/high/medium/low/info)
            vulnerability_type: Type of vulnerability (e.g., 'xss', 'sqli')
            program_type: Type of program (public/private/vdp)
            asset_type: Type of asset (web/mobile/api)
            
        Returns:
            Payout estimation dictionary
        """
        severity_lower = severity.lower()
        if severity_lower not in self.base_payouts:
            logger.warning(f"Unknown severity: {severity}, defaulting to 'low'")
            severity_lower = 'low'
        
        # Get base payout
        base = self.base_payouts[severity_lower].copy()
        
        # Apply program type multiplier
        program_mult = self.program_multipliers.get(program_type.lower(), 1.0)
        
        # Apply vulnerability type multiplier
        vuln_type_lower = vulnerability_type.lower().replace(' ', '_')
        vuln_mult = self.vuln_multipliers.get(vuln_type_lower, 1.0)
        
        # Calculate adjusted payouts
        min_payout = int(base['min'] * program_mult * vuln_mult)
        max_payout = int(base['max'] * program_mult * vuln_mult)
        avg_payout = int(base['avg'] * program_mult * vuln_mult)
        
        return {
            'severity': severity,
            'vulnerability_type': vulnerability_type,
            'program_type': program_type,
            'estimated_payout': {
                'min': min_payout,
                'max': max_payout,
                'average': avg_payout,
                'currency': 'USD'
            },
            'factors': {
                'base_payout': base['avg'],
                'program_multiplier': program_mult,
                'vulnerability_multiplier': vuln_mult
            },
            'confidence': 'medium',  # Could be enhanced with ML
            'notes': self._generate_notes(severity_lower, vulnerability_type, program_type)
        }
    
    def _generate_notes(self, severity: str, vuln_type: str, program_type: str) -> List[str]:
        """Generate helpful notes about the estimation."""
        notes = []
        
        if program_type == 'vdp':
            notes.append("VDP programs often don't offer monetary rewards")
        
        if severity == 'critical':
            notes.append("Critical vulnerabilities can sometimes exceed the estimated range")
        
        if 'rce' in vuln_type.lower():
            notes.append("RCE vulnerabilities typically command premium payouts")
        
        if severity == 'info':
            notes.append("Informational findings may not qualify for rewards in many programs")
        
        return notes
    
    def compare_programs(self, severity: str, programs: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Compare estimated payouts across multiple programs.
        
        Args:
            severity: Vulnerability severity
            programs: List of program details (each with name, type, etc.)
            
        Returns:
            List of programs with estimated payouts, sorted by average
        """
        results = []
        
        for program in programs:
            estimate = self.estimate_payout(
                severity=severity,
                vulnerability_type=program.get('vuln_type', 'xss'),
                program_type=program.get('type', 'public')
            )
            
            results.append({
                'program_name': program.get('name', 'Unknown'),
                'estimate': estimate
            })
        
        # Sort by average payout (descending)
        results.sort(key=lambda x: x['estimate']['estimated_payout']['average'], reverse=True)
        
        return results


def estimate_payout(severity: str, vulnerability_type: str) -> Dict[str, any]:
    """
    Convenience function to estimate payout.
    
    Args:
        severity: Vulnerability severity
        vulnerability_type: Type of vulnerability
        
    Returns:
        Payout estimation
    """
    estimator = PayoutEstimator()
    return estimator.estimate_payout(severity, vulnerability_type)
