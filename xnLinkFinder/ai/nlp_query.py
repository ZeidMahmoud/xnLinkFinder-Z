"""
Natural Language Query Interface for xnLinkFinder-Z.

Ask questions in plain English:
- "find all admin endpoints"
- "show me endpoints with file upload"
- "which endpoints have authentication"
- "list all API endpoints with user ID parameters"
"""

from typing import List, Dict, Optional, Set
import logging
import re

logger = logging.getLogger(__name__)


class NLPQueryEngine:
    """Natural language query interface for endpoints."""
    
    def __init__(self):
        """Initialize NLP query engine."""
        self.endpoints = []
        
        # Define keyword mappings for different query types
        self.keyword_map = {
            'admin': ['admin', 'administrator', 'manage', 'management'],
            'auth': ['auth', 'authentication', 'login', 'signin', 'oauth', 'token'],
            'user': ['user', 'profile', 'account', 'member'],
            'file': ['file', 'upload', 'download', 'document', 'attachment'],
            'api': ['api', 'rest', 'graphql', 'endpoint', 'service'],
            'config': ['config', 'configuration', 'settings', 'preferences'],
            'debug': ['debug', 'test', 'dev', 'development', 'staging'],
            'delete': ['delete', 'remove', 'destroy', 'erase'],
            'create': ['create', 'add', 'new', 'post', 'insert'],
            'update': ['update', 'edit', 'modify', 'patch', 'put'],
            'read': ['read', 'get', 'view', 'show', 'list', 'fetch'],
            'database': ['database', 'db', 'sql', 'query', 'table'],
            'export': ['export', 'download', 'dump', 'backup'],
            'import': ['import', 'upload', 'restore', 'load'],
            'search': ['search', 'find', 'query', 'filter'],
            'payment': ['payment', 'pay', 'checkout', 'billing', 'invoice'],
            'id': ['id', 'identifier', 'uid', 'guid', 'uuid'],
        }
        
        # Query intent patterns
        self.intent_patterns = {
            'find': ['find', 'show', 'list', 'get', 'display', 'which'],
            'filter': ['with', 'having', 'that has', 'that have', 'containing'],
            'count': ['how many', 'count', 'number of'],
            'analyze': ['analyze', 'check', 'inspect', 'examine'],
        }
    
    def load_endpoints(self, endpoints: List[str]):
        """
        Load endpoints for querying.
        
        Args:
            endpoints: List of endpoint URLs/paths
        """
        self.endpoints = endpoints
        logger.info(f"Loaded {len(endpoints)} endpoints for querying")
    
    def parse_query(self, query: str) -> Dict[str, any]:
        """
        Parse a natural language query into structured filters.
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with parsed query components
        """
        query_lower = query.lower()
        
        # Detect intent
        intent = 'find'  # default
        for intent_type, keywords in self.intent_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                intent = intent_type
                break
        
        # Extract keywords
        matched_keywords = set()
        for category, keywords in self.keyword_map.items():
            if any(keyword in query_lower for keyword in keywords):
                matched_keywords.add(category)
        
        # Extract HTTP methods
        methods = []
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
            if method.lower() in query_lower:
                methods.append(method)
        
        # Extract specific patterns
        patterns = []
        
        # Look for quoted strings (exact matches)
        quoted_matches = re.findall(r'"([^"]+)"', query)
        patterns.extend(quoted_matches)
        
        # Look for paths mentioned
        path_matches = re.findall(r'/[\w/\-]+', query)
        patterns.extend(path_matches)
        
        # Look for parameter names
        param_matches = re.findall(r'parameter[s]?\s+(\w+)', query_lower)
        patterns.extend([f'?{p}=' for p in param_matches])
        
        return {
            'intent': intent,
            'keywords': list(matched_keywords),
            'methods': methods,
            'patterns': patterns,
            'original_query': query
        }
    
    def filter_endpoints(self, filters: Dict[str, any]) -> List[str]:
        """
        Filter endpoints based on parsed query.
        
        Args:
            filters: Parsed query filters
            
        Returns:
            List of matching endpoints
        """
        results = self.endpoints.copy()
        
        # Filter by keywords
        if filters['keywords']:
            keyword_results = []
            for endpoint in results:
                endpoint_lower = endpoint.lower()
                if any(keyword in endpoint_lower for keyword in filters['keywords']):
                    keyword_results.append(endpoint)
            results = keyword_results
        
        # Filter by patterns
        if filters['patterns']:
            pattern_results = []
            for endpoint in results:
                if any(pattern in endpoint for pattern in filters['patterns']):
                    pattern_results.append(endpoint)
            results = pattern_results
        
        # Filter by HTTP methods (if methods are part of the endpoint string)
        if filters['methods']:
            method_results = []
            for endpoint in results:
                endpoint_upper = endpoint.upper()
                if any(method in endpoint_upper for method in filters['methods']):
                    method_results.append(endpoint)
            # If no results with method filter, return all results
            if method_results:
                results = method_results
        
        return results
    
    def query(self, query: str) -> Dict[str, any]:
        """
        Execute a natural language query.
        
        Args:
            query: Natural language query string
            
        Returns:
            Dictionary with query results:
            - query: Original query
            - parsed: Parsed query components
            - results: Matching endpoints
            - count: Number of results
        """
        if not self.endpoints:
            logger.warning("No endpoints loaded for querying")
            return {
                'query': query,
                'parsed': {},
                'results': [],
                'count': 0,
                'error': 'No endpoints loaded'
            }
        
        # Parse the query
        parsed = self.parse_query(query)
        
        # Execute based on intent
        if parsed['intent'] == 'count':
            # Filter and count
            results = self.filter_endpoints(parsed)
            return {
                'query': query,
                'parsed': parsed,
                'results': [],
                'count': len(results),
                'summary': f"Found {len(results)} endpoints matching your query"
            }
        elif parsed['intent'] == 'analyze':
            # Filter and provide analysis
            results = self.filter_endpoints(parsed)
            analysis = self._analyze_endpoints(results)
            return {
                'query': query,
                'parsed': parsed,
                'results': results[:10],  # Show sample
                'count': len(results),
                'analysis': analysis
            }
        else:  # find or filter
            # Return matching endpoints
            results = self.filter_endpoints(parsed)
            return {
                'query': query,
                'parsed': parsed,
                'results': results,
                'count': len(results)
            }
    
    def _analyze_endpoints(self, endpoints: List[str]) -> Dict[str, any]:
        """
        Analyze a set of endpoints.
        
        Args:
            endpoints: List of endpoints to analyze
            
        Returns:
            Analysis dictionary
        """
        analysis = {
            'total': len(endpoints),
            'with_params': 0,
            'methods': {},
            'extensions': {},
            'depth_distribution': {},
        }
        
        for endpoint in endpoints:
            # Count parameters
            if '?' in endpoint:
                analysis['with_params'] += 1
            
            # Count path depth
            depth = endpoint.count('/')
            analysis['depth_distribution'][depth] = \
                analysis['depth_distribution'].get(depth, 0) + 1
            
            # Extract extensions
            if '.' in endpoint.split('/')[-1]:
                ext = endpoint.split('.')[-1].split('?')[0]
                analysis['extensions'][ext] = \
                    analysis['extensions'].get(ext, 0) + 1
        
        return analysis
    
    def suggest_queries(self) -> List[str]:
        """
        Suggest example queries based on loaded endpoints.
        
        Returns:
            List of suggested query strings
        """
        suggestions = [
            "find all admin endpoints",
            "show me API endpoints",
            "list endpoints with authentication",
            "which endpoints have file upload",
            "find user management endpoints",
            "show debug or test endpoints",
            "find endpoints with id parameters",
            "list all delete endpoints",
            "show configuration endpoints",
            "find database related endpoints"
        ]
        
        # Add suggestions based on actual endpoint content
        if any('admin' in e.lower() for e in self.endpoints):
            suggestions.insert(0, "find admin endpoints")
        
        if any('api' in e.lower() for e in self.endpoints):
            suggestions.insert(0, "show me all API endpoints")
        
        if any('user' in e.lower() for e in self.endpoints):
            suggestions.insert(0, "list user-related endpoints")
        
        return suggestions[:10]
    
    def fuzzy_search(self, query: str, max_results: int = 50) -> List[str]:
        """
        Perform fuzzy search on endpoints.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of matching endpoints
        """
        query_lower = query.lower()
        results = []
        
        # Exact matches first
        for endpoint in self.endpoints:
            if query_lower in endpoint.lower():
                results.append(endpoint)
        
        # Then fuzzy matches
        if len(results) < max_results:
            query_parts = query_lower.split()
            for endpoint in self.endpoints:
                if endpoint not in results:
                    endpoint_lower = endpoint.lower()
                    if all(part in endpoint_lower for part in query_parts):
                        results.append(endpoint)
        
        return results[:max_results]


def query_endpoints(endpoints: List[str], query: str) -> List[str]:
    """
    Convenience function for natural language querying.
    
    Args:
        endpoints: List of endpoints to query
        query: Natural language query string
        
    Returns:
        List of matching endpoints
    """
    engine = NLPQueryEngine()
    engine.load_endpoints(endpoints)
    result = engine.query(query)
    return result.get('results', [])
