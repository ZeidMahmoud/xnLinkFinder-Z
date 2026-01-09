"""
Anomaly Detection for xnLinkFinder-Z.

Detect unusual patterns in endpoints:
- Unusual parameter names
- Suspicious file extensions
- Debug/test endpoints in production
- Hidden admin interfaces
"""

from typing import List, Dict, Optional, Set, Tuple
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect unusual and suspicious patterns in endpoints."""
    
    def __init__(self):
        """Initialize anomaly detector."""
        # Known suspicious patterns
        self.suspicious_keywords = {
            'debug', 'test', 'dev', 'development', 'staging',
            'admin', 'root', 'internal', 'private', 'hidden',
            'backup', 'old', 'temp', 'tmp', 'bak',
            'config', 'conf', 'configuration', 'settings',
            'password', 'passwd', 'pwd', 'secret', 'key',
            'token', 'api_key', 'apikey', 'access',
            'shell', 'cmd', 'exec', 'eval', 'system',
            'database', 'db', 'sql', 'query'
        }
        
        # Suspicious file extensions
        self.suspicious_extensions = {
            '.bak', '.old', '.backup', '.save', '.tmp',
            '.sql', '.db', '.sqlite', '.mdb',
            '.log', '.trace', '.dump',
            '.config', '.conf', '.cfg', '.ini', '.env',
            '.key', '.pem', '.crt', '.cer',
            '.zip', '.tar', '.gz', '.7z', '.rar',
            '.git', '.svn', '.hg', '.DS_Store',
            '.php~', '.php.bak', '.asp.bak'
        }
        
        # Debug/test indicators
        self.debug_indicators = {
            'debug', 'test', 'dev', 'phpinfo', 'info.php',
            'test.php', 'debug.js', 'console', 'stacktrace',
            'error', 'exception', 'trace'
        }
        
        # Unusual parameter names
        self.unusual_params = {
            'cmd', 'exec', 'command', 'shell', 'system',
            'eval', 'code', 'script', 'function',
            'file', 'path', 'dir', 'folder',
            'url', 'uri', 'redirect', 'goto',
            'template', 'page', 'view', 'include',
            'query', 'sql', 'statement'
        }
    
    def detect_all(self, endpoints: List[str]) -> Dict[str, List[Dict[str, any]]]:
        """
        Run all anomaly detection checks.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Dictionary of anomaly type -> list of findings
        """
        anomalies = {
            'suspicious_keywords': self.detect_suspicious_keywords(endpoints),
            'suspicious_extensions': self.detect_suspicious_extensions(endpoints),
            'debug_endpoints': self.detect_debug_endpoints(endpoints),
            'hidden_admin': self.detect_hidden_admin(endpoints),
            'unusual_params': self.detect_unusual_parameters(endpoints),
            'encoding_anomalies': self.detect_encoding_anomalies(endpoints),
            'path_anomalies': self.detect_path_anomalies(endpoints),
            'version_leaks': self.detect_version_leaks(endpoints)
        }
        
        # Count total anomalies
        total = sum(len(findings) for findings in anomalies.values())
        logger.info(f"Detected {total} anomalies across {len(endpoints)} endpoints")
        
        return anomalies
    
    def detect_suspicious_keywords(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect endpoints containing suspicious keywords.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            endpoint_lower = endpoint.lower()
            matched_keywords = [
                kw for kw in self.suspicious_keywords
                if kw in endpoint_lower
            ]
            
            if matched_keywords:
                findings.append({
                    'endpoint': endpoint,
                    'keywords': matched_keywords,
                    'severity': self._calculate_keyword_severity(matched_keywords),
                    'description': f"Contains suspicious keywords: {', '.join(matched_keywords)}"
                })
        
        return findings
    
    def detect_suspicious_extensions(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect endpoints with suspicious file extensions.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            endpoint_lower = endpoint.lower()
            for ext in self.suspicious_extensions:
                if endpoint_lower.endswith(ext) or ext in endpoint_lower:
                    findings.append({
                        'endpoint': endpoint,
                        'extension': ext,
                        'severity': 'high' if ext in ['.bak', '.sql', '.db', '.env'] else 'medium',
                        'description': f"Suspicious file extension: {ext}"
                    })
                    break  # Only report once per endpoint
        
        return findings
    
    def detect_debug_endpoints(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect debug/test endpoints that shouldn't be in production.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            endpoint_lower = endpoint.lower()
            matched_indicators = [
                ind for ind in self.debug_indicators
                if ind in endpoint_lower
            ]
            
            if matched_indicators:
                findings.append({
                    'endpoint': endpoint,
                    'indicators': matched_indicators,
                    'severity': 'high',
                    'description': f"Debug/test endpoint detected: {', '.join(matched_indicators)}"
                })
        
        return findings
    
    def detect_hidden_admin(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect hidden or obfuscated admin interfaces.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        # Patterns for hidden admin panels
        patterns = [
            r'/[a-z0-9]{32}/',  # MD5-like path
            r'/[a-f0-9]{40}/',  # SHA1-like path
            r'/\d{8,}/',  # Long numeric path
            r'/[a-z]{1,3}\d{3,}/',  # Short prefix + numbers
            r'/_[a-z]+/',  # Underscore prefix
            r'/\.well-known/',  # Well-known paths
        ]
        
        admin_keywords = ['admin', 'administrator', 'manage', 'panel', 'console', 'control']
        
        for endpoint in endpoints:
            endpoint_lower = endpoint.lower()
            
            # Check for obfuscated paths with admin keywords
            for pattern in patterns:
                if re.search(pattern, endpoint_lower):
                    if any(kw in endpoint_lower for kw in admin_keywords):
                        findings.append({
                            'endpoint': endpoint,
                            'pattern': pattern,
                            'severity': 'high',
                            'description': 'Potentially hidden admin interface with obfuscated path'
                        })
                        break
            
            # Check for admin panels in unusual locations
            if any(kw in endpoint_lower for kw in admin_keywords):
                path_parts = endpoint_lower.split('/')
                if len(path_parts) > 3:  # Deep nested admin
                    findings.append({
                        'endpoint': endpoint,
                        'severity': 'medium',
                        'description': 'Admin interface in deep nested path'
                    })
        
        return findings
    
    def detect_unusual_parameters(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect endpoints with unusual parameter names.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            if '?' not in endpoint:
                continue
            
            # Extract parameter names
            query_string = endpoint.split('?', 1)[1]
            params = re.findall(r'(\w+)=', query_string)
            
            unusual = [p for p in params if p.lower() in self.unusual_params]
            
            if unusual:
                findings.append({
                    'endpoint': endpoint,
                    'parameters': unusual,
                    'severity': self._calculate_param_severity(unusual),
                    'description': f"Unusual parameters detected: {', '.join(unusual)}"
                })
        
        return findings
    
    def detect_encoding_anomalies(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect unusual encoding patterns (possible evasion attempts).
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            anomalies = []
            
            # URL encoding
            if re.search(r'%[0-9a-f]{2}', endpoint, re.IGNORECASE):
                anomalies.append('url_encoded')
            
            # Double encoding
            if re.search(r'%25[0-9a-f]{2}', endpoint, re.IGNORECASE):
                anomalies.append('double_encoded')
            
            # Unicode encoding
            if re.search(r'\\u[0-9a-f]{4}', endpoint, re.IGNORECASE):
                anomalies.append('unicode_encoded')
            
            # Excessive encoding (multiple encoded chars)
            encoded_count = len(re.findall(r'%[0-9a-f]{2}', endpoint, re.IGNORECASE))
            if encoded_count > 5:
                anomalies.append('excessive_encoding')
            
            if anomalies:
                findings.append({
                    'endpoint': endpoint,
                    'anomalies': anomalies,
                    'severity': 'medium' if 'double_encoded' in anomalies else 'low',
                    'description': f"Encoding anomalies detected: {', '.join(anomalies)}"
                })
        
        return findings
    
    def detect_path_anomalies(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect unusual path patterns.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        for endpoint in endpoints:
            anomalies = []
            
            # Path traversal sequences
            if '..' in endpoint or '..\\' in endpoint:
                anomalies.append('path_traversal')
            
            # Excessive path depth
            depth = endpoint.count('/')
            if depth > 10:
                anomalies.append('excessive_depth')
            
            # Mixed slashes
            if '/' in endpoint and '\\' in endpoint:
                anomalies.append('mixed_slashes')
            
            # Null bytes
            if '%00' in endpoint or '\\x00' in endpoint:
                anomalies.append('null_byte')
            
            # Multiple consecutive slashes
            if '//' in endpoint.replace('://', ''):  # Ignore protocol
                anomalies.append('double_slashes')
            
            if anomalies:
                findings.append({
                    'endpoint': endpoint,
                    'anomalies': anomalies,
                    'severity': 'high' if 'path_traversal' in anomalies or 'null_byte' in anomalies else 'medium',
                    'description': f"Path anomalies detected: {', '.join(anomalies)}"
                })
        
        return findings
    
    def detect_version_leaks(self, endpoints: List[str]) -> List[Dict[str, any]]:
        """
        Detect endpoints that might leak version information.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            List of findings
        """
        findings = []
        
        version_patterns = [
            (r'/v\d+/', 'api_version'),
            (r'/version\d+/', 'version_path'),
            (r'\?v=\d+', 'version_param'),
            (r'/\d+\.\d+\.\d+/', 'semver'),
            (r'/changelog', 'changelog'),
            (r'/release', 'release_info'),
            (r'/version\.txt', 'version_file'),
        ]
        
        for endpoint in endpoints:
            endpoint_lower = endpoint.lower()
            
            for pattern, leak_type in version_patterns:
                if re.search(pattern, endpoint_lower):
                    findings.append({
                        'endpoint': endpoint,
                        'leak_type': leak_type,
                        'pattern': pattern,
                        'severity': 'low',
                        'description': f"Potential version information leak: {leak_type}"
                    })
                    break  # Only report once per endpoint
        
        return findings
    
    def _calculate_keyword_severity(self, keywords: List[str]) -> str:
        """Calculate severity based on matched keywords."""
        critical_keywords = {'password', 'passwd', 'secret', 'key', 'exec', 'eval', 'shell', 'cmd'}
        high_keywords = {'admin', 'root', 'config', 'database', 'sql', 'backup'}
        
        if any(kw in critical_keywords for kw in keywords):
            return 'critical'
        elif any(kw in high_keywords for kw in keywords):
            return 'high'
        else:
            return 'medium'
    
    def _calculate_param_severity(self, params: List[str]) -> str:
        """Calculate severity based on unusual parameters."""
        critical_params = {'cmd', 'exec', 'command', 'shell', 'eval', 'code'}
        high_params = {'file', 'path', 'dir', 'url', 'redirect', 'template', 'sql'}
        
        if any(p.lower() in critical_params for p in params):
            return 'critical'
        elif any(p.lower() in high_params for p in params):
            return 'high'
        else:
            return 'medium'
    
    def generate_report(self, anomalies: Dict[str, List[Dict[str, any]]]) -> str:
        """
        Generate a human-readable report of detected anomalies.
        
        Args:
            anomalies: Dictionary of anomaly findings
            
        Returns:
            Formatted report string
        """
        report_lines = ["=" * 60, "ANOMALY DETECTION REPORT", "=" * 60, ""]
        
        for anomaly_type, findings in anomalies.items():
            if not findings:
                continue
            
            report_lines.append(f"\n{anomaly_type.replace('_', ' ').title()}: {len(findings)} found")
            report_lines.append("-" * 60)
            
            # Group by severity
            by_severity = {}
            for finding in findings:
                severity = finding.get('severity', 'low')
                if severity not in by_severity:
                    by_severity[severity] = []
                by_severity[severity].append(finding)
            
            for severity in ['critical', 'high', 'medium', 'low']:
                if severity in by_severity:
                    report_lines.append(f"\n  {severity.upper()}: {len(by_severity[severity])}")
                    for finding in by_severity[severity][:5]:  # Show first 5
                        report_lines.append(f"    - {finding['endpoint']}")
                        report_lines.append(f"      {finding['description']}")
        
        report_lines.append("\n" + "=" * 60)
        return "\n".join(report_lines)


def detect_anomalies(endpoints: List[str]) -> Dict[str, List[Dict[str, any]]]:
    """
    Convenience function for anomaly detection.
    
    Args:
        endpoints: List of endpoints to analyze
        
    Returns:
        Dictionary of anomaly findings
    """
    detector = AnomalyDetector()
    return detector.detect_all(endpoints)
