"""
Predictive Endpoint Discovery for xnLinkFinder-Z.

Uses machine learning to predict likely hidden endpoints based on discovered patterns.
"""

from typing import List, Dict, Set, Optional
import logging
import re

logger = logging.getLogger(__name__)


class PredictiveDiscovery:
    """Predict hidden endpoints based on patterns in discovered endpoints."""
    
    def __init__(self):
        """Initialize predictive discovery engine."""
        self.known_endpoints = set()
        self.patterns = []
        self.model = None
    
    def learn_from_endpoints(self, endpoints: List[str]):
        """
        Learn patterns from discovered endpoints.
        
        Args:
            endpoints: List of discovered endpoints
        """
        self.known_endpoints.update(endpoints)
        self.patterns = self._extract_patterns(endpoints)
    
    def predict_endpoints(self, max_predictions: int = 50) -> List[Dict[str, any]]:
        """
        Predict likely hidden endpoints.
        
        Args:
            max_predictions: Maximum number of predictions to generate
            
        Returns:
            List of predicted endpoints with confidence scores
        """
        predictions = []
        
        # Generate predictions based on patterns
        for pattern in self.patterns:
            predicted = self._generate_from_pattern(pattern)
            predictions.extend(predicted)
        
        # Filter out known endpoints
        predictions = [p for p in predictions if p['endpoint'] not in self.known_endpoints]
        
        # Sort by confidence and limit
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        return predictions[:max_predictions]
    
    def _extract_patterns(self, endpoints: List[str]) -> List[Dict]:
        """Extract common patterns from endpoints."""
        patterns = []
        
        # Pattern 1: Versioned APIs (e.g., /api/v1/users -> /api/v2/users)
        version_pattern = r'(/api/v)(\d+)(/.*)'
        for endpoint in endpoints:
            match = re.search(version_pattern, endpoint)
            if match:
                patterns.append({
                    'type': 'versioned_api',
                    'prefix': match.group(1),
                    'version': int(match.group(2)),
                    'suffix': match.group(3)
                })
        
        # Pattern 2: CRUD operations
        crud_verbs = ['list', 'get', 'create', 'update', 'delete', 'search']
        for endpoint in endpoints:
            for verb in crud_verbs:
                if verb in endpoint.lower():
                    # Extract resource name
                    parts = endpoint.split('/')
                    for part in parts:
                        if part and part != verb and len(part) > 2:
                            patterns.append({
                                'type': 'crud',
                                'resource': part,
                                'found_verb': verb
                            })
        
        # Pattern 3: ID parameters
        id_pattern = r'/(\w+)/(\d+|[a-f0-9-]{36})'
        for endpoint in endpoints:
            match = re.search(id_pattern, endpoint)
            if match:
                patterns.append({
                    'type': 'resource_with_id',
                    'resource': match.group(1),
                    'id_type': 'uuid' if '-' in match.group(2) else 'numeric'
                })
        
        return self._deduplicate_patterns(patterns)
    
    def _generate_from_pattern(self, pattern: Dict) -> List[Dict]:
        """Generate endpoint predictions from a pattern."""
        predictions = []
        
        if pattern['type'] == 'versioned_api':
            # Predict other versions
            for v in range(1, pattern['version'] + 3):
                if v != pattern['version']:
                    predicted_url = f"{pattern['prefix']}{v}{pattern['suffix']}"
                    predictions.append({
                        'endpoint': predicted_url,
                        'confidence': 0.8 if abs(v - pattern['version']) == 1 else 0.6,
                        'reasoning': f"Predicted API version {v} based on v{pattern['version']}"
                    })
        
        elif pattern['type'] == 'crud':
            # Predict missing CRUD operations
            crud_verbs = ['list', 'get', 'create', 'update', 'delete', 'search', 'patch']
            resource = pattern['resource']
            
            for verb in crud_verbs:
                if verb != pattern['found_verb']:
                    # Generate multiple possible URL patterns
                    possible_urls = [
                        f"/api/{resource}/{verb}",
                        f"/api/{verb}/{resource}",
                        f"/{resource}/{verb}",
                        f"/{verb}/{resource}",
                    ]
                    for url in possible_urls:
                        predictions.append({
                            'endpoint': url,
                            'confidence': 0.7,
                            'reasoning': f"Predicted {verb} operation for {resource} resource"
                        })
        
        elif pattern['type'] == 'resource_with_id':
            # Predict common actions on resources
            resource = pattern['resource']
            common_actions = ['edit', 'delete', 'update', 'view', 'details', 'export', 'duplicate']
            
            for action in common_actions:
                id_placeholder = '{id}' if pattern['id_type'] == 'numeric' else '{uuid}'
                predictions.append({
                    'endpoint': f"/{resource}/{id_placeholder}/{action}",
                    'confidence': 0.65,
                    'reasoning': f"Predicted {action} action for {resource}"
                })
        
        return predictions
    
    def _deduplicate_patterns(self, patterns: List[Dict]) -> List[Dict]:
        """Remove duplicate patterns."""
        seen = set()
        unique = []
        for pattern in patterns:
            key = tuple(sorted(pattern.items()))
            if key not in seen:
                seen.add(key)
                unique.append(pattern)
        return unique
    
    def suggest_parameter_variations(self, endpoint: str) -> List[Dict[str, any]]:
        """
        Suggest parameter variations for an endpoint.
        
        Args:
            endpoint: Base endpoint URL
            
        Returns:
            List of suggested parameter variations
        """
        suggestions = []
        
        # Common query parameters
        common_params = {
            'pagination': ['page', 'limit', 'offset', 'per_page', 'size'],
            'filtering': ['filter', 'search', 'q', 'query', 'where'],
            'sorting': ['sort', 'order', 'orderBy', 'sortBy'],
            'selection': ['fields', 'select', 'include', 'expand'],
            'format': ['format', 'output', 'type'],
            'auth': ['token', 'api_key', 'key', 'auth'],
        }
        
        for category, params in common_params.items():
            for param in params:
                suggestions.append({
                    'endpoint': f"{endpoint}?{param}={{value}}",
                    'parameter': param,
                    'category': category,
                    'confidence': 0.6
                })
        
        return suggestions


def predict_hidden_endpoints(known_endpoints: List[str], max_predictions: int = 50) -> List[Dict]:
    """
    Convenience function to predict hidden endpoints.
    
    Args:
        known_endpoints: List of known/discovered endpoints
        max_predictions: Maximum predictions to generate
        
    Returns:
        List of predicted endpoints with metadata
    """
    discovery = PredictiveDiscovery()
    discovery.learn_from_endpoints(known_endpoints)
    return discovery.predict_endpoints(max_predictions)
