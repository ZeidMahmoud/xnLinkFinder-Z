"""
Smart Prioritization Engine for xnLinkFinder-Z.

AI-powered ranking of endpoints by exploitability and vulnerability potential.
"""

from typing import List, Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)


class PriorityEngine:
    """Rank endpoints by exploitability using AI/heuristics."""
    
    def __init__(self, use_ml: bool = False):
        """
        Initialize priority engine.
        
        Args:
            use_ml: Whether to use ML model (if False, uses heuristics)
        """
        self.use_ml = use_ml
        self.model = None
        
        # Vulnerability pattern weights
        self.vuln_patterns = {
            'admin': 0.9,
            'debug': 0.85,
            'test': 0.8,
            'dev': 0.8,
            'internal': 0.85,
            'upload': 0.9,
            'file': 0.85,
            'delete': 0.85,
            'user': 0.7,
            'password': 0.95,
            'auth': 0.8,
            'login': 0.75,
            'api': 0.6,
            'config': 0.9,
            'settings': 0.85,
            'backup': 0.9,
            'export': 0.8,
            'import': 0.85,
            'eval': 0.95,
            'exec': 0.95,
            'command': 0.9,
        }
    
    def prioritize(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Prioritize endpoints by exploitability.
        
        Args:
            endpoints: List of endpoints to prioritize
            
        Returns:
            List of endpoints with priority scores and rankings
        """
        scored_endpoints = []
        
        for endpoint in endpoints:
            score = self._calculate_priority_score(endpoint)
            scored_endpoints.append({
                'endpoint': endpoint,
                'priority_score': score,
                'priority_level': self._score_to_level(score),
                'risk_factors': self._identify_risk_factors(endpoint),
                'vulnerability_hints': self._get_vulnerability_hints(endpoint)
            })
        
        # Sort by priority score (highest first)
        scored_endpoints.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Add ranking
        for rank, item in enumerate(scored_endpoints, 1):
            item['rank'] = rank
        
        return scored_endpoints
    
    def _calculate_priority_score(self, endpoint: str) -> float:
        """
        Calculate priority score for an endpoint (0-1).
        
        Higher scores indicate higher priority/risk.
        """
        score = 0.5  # Base score
        endpoint_lower = endpoint.lower()
        
        # Check for high-risk keywords
        for keyword, weight in self.vuln_patterns.items():
            if keyword in endpoint_lower:
                score = max(score, weight)
        
        # Boost score for parameters (potential for injection)
        if '?' in endpoint or '{' in endpoint:
            score += 0.1
        
        # Boost for numeric IDs (potential IDOR)
        if re.search(r'/\d+(/|$)', endpoint):
            score += 0.15
        
        # Boost for UUIDs (also IDOR potential)
        if re.search(r'/[a-f0-9-]{36}', endpoint, re.I):
            score += 0.1
        
        # Boost for file operations
        if any(ext in endpoint_lower for ext in ['.php', '.asp', '.jsp', '.do', '.action']):
            score += 0.1
        
        # Boost for potential LFI/path traversal
        if '../' in endpoint or '..' in endpoint:
            score += 0.2
        
        # Boost for potential command injection
        if any(char in endpoint for char in ['|', ';', '&', '`', '$']):
            score += 0.15
        
        # Boost for API versioning (older versions may have vulnerabilities)
        version_match = re.search(r'/v(\d+)/', endpoint_lower)
        if version_match:
            version = int(version_match.group(1))
            if version == 1:
                score += 0.1  # v1 APIs often have more vulnerabilities
        
        return min(score, 1.0)
    
    def _score_to_level(self, score: float) -> str:
        """Convert numeric score to priority level."""
        if score >= 0.9:
            return 'Critical'
        elif score >= 0.75:
            return 'High'
        elif score >= 0.6:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_risk_factors(self, endpoint: str) -> List[str]:
        """Identify specific risk factors in an endpoint."""
        factors = []
        endpoint_lower = endpoint.lower()
        
        # Check for each risk category
        if any(kw in endpoint_lower for kw in ['admin', 'administrator']):
            factors.append('Administrative functionality')
        
        if any(kw in endpoint_lower for kw in ['debug', 'test', 'dev']):
            factors.append('Debug/development endpoint')
        
        if any(kw in endpoint_lower for kw in ['upload', 'import']):
            factors.append('File upload capability')
        
        if any(kw in endpoint_lower for kw in ['delete', 'remove', 'drop']):
            factors.append('Destructive operation')
        
        if re.search(r'/\d+(/|$)', endpoint):
            factors.append('Numeric ID (IDOR potential)')
        
        if '?' in endpoint or '=' in endpoint:
            factors.append('Query parameters (injection potential)')
        
        if any(kw in endpoint_lower for kw in ['password', 'passwd', 'pwd']):
            factors.append('Password/credential handling')
        
        if any(kw in endpoint_lower for kw in ['exec', 'eval', 'command', 'cmd']):
            factors.append('Code execution potential')
        
        if any(kw in endpoint_lower for kw in ['export', 'backup', 'dump']):
            factors.append('Data export functionality')
        
        return factors
    
    def _get_vulnerability_hints(self, endpoint: str) -> List[str]:
        """Get specific vulnerability types to test for."""
        hints = []
        endpoint_lower = endpoint.lower()
        
        # IDOR
        if re.search(r'/\d+(/|$)', endpoint) or re.search(r'/[a-f0-9-]{36}', endpoint, re.I):
            hints.append('IDOR (Insecure Direct Object Reference)')
        
        # SQL Injection
        if '?' in endpoint or any(kw in endpoint_lower for kw in ['search', 'query', 'id', 'user']):
            hints.append('SQL Injection')
        
        # XSS
        if '?' in endpoint or any(kw in endpoint_lower for kw in ['search', 'query', 'message', 'comment']):
            hints.append('XSS (Cross-Site Scripting)')
        
        # File Upload vulnerabilities
        if any(kw in endpoint_lower for kw in ['upload', 'import', 'file']):
            hints.append('File Upload vulnerabilities')
        
        # Path Traversal / LFI
        if any(kw in endpoint_lower for kw in ['file', 'download', 'export', 'path']):
            hints.append('Path Traversal / LFI')
        
        # SSRF
        if any(kw in endpoint_lower for kw in ['url', 'redirect', 'proxy', 'fetch']):
            hints.append('SSRF (Server-Side Request Forgery)')
        
        # Authentication/Authorization bypass
        if any(kw in endpoint_lower for kw in ['admin', 'auth', 'login', 'user']):
            hints.append('Authentication/Authorization bypass')
        
        # Command Injection
        if any(kw in endpoint_lower for kw in ['exec', 'command', 'cmd', 'shell', 'ping']):
            hints.append('Command Injection')
        
        # Information Disclosure
        if any(kw in endpoint_lower for kw in ['debug', 'test', 'config', 'env', 'info']):
            hints.append('Information Disclosure')
        
        return hints
    
    def get_top_priority(self, endpoints: List[str], n: int = 10) -> List[Dict[str, any]]:
        """
        Get top N priority endpoints.
        
        Args:
            endpoints: List of endpoints
            n: Number of top endpoints to return
            
        Returns:
            Top N prioritized endpoints
        """
        prioritized = self.prioritize(endpoints)
        return prioritized[:n]
    
    def filter_by_level(self, endpoints: List[str], min_level: str = 'Medium') -> List[Dict[str, any]]:
        """
        Filter endpoints by minimum priority level.
        
        Args:
            endpoints: List of endpoints
            min_level: Minimum priority level ('Critical', 'High', 'Medium', 'Low')
            
        Returns:
            Filtered and prioritized endpoints
        """
        level_values = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        min_value = level_values.get(min_level, 2)
        
        prioritized = self.prioritize(endpoints)
        
        return [ep for ep in prioritized 
                if level_values.get(ep['priority_level'], 0) >= min_value]


def prioritize_endpoints(endpoints: List[str]) -> List[Dict[str, any]]:
    """
    Convenience function to prioritize endpoints.
    
    Args:
        endpoints: List of endpoints to prioritize
        
    Returns:
        Prioritized endpoints with scores and metadata
    """
    engine = PriorityEngine()
    return engine.prioritize(endpoints)
