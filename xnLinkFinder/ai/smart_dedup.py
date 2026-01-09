"""
AI-powered duplicate detection using semantic similarity.

Features:
- Sentence transformers for embeddings
- Cluster similar endpoints
- Identify near-duplicates (e.g., /api/v1/users vs /api/v2/users)
- Configurable similarity threshold
"""

from typing import List, Dict, Set, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)


class SmartDeduplicator:
    """Advanced deduplication using AI and pattern matching."""
    
    def __init__(self, 
                 similarity_threshold: float = 0.85,
                 use_semantic: bool = True,
                 model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize smart deduplicator.
        
        Args:
            similarity_threshold: Threshold for considering endpoints similar (0-1)
            use_semantic: Whether to use semantic similarity (requires sentence-transformers)
            model_name: Sentence transformer model name
        """
        self.similarity_threshold = similarity_threshold
        self.use_semantic = use_semantic
        self.model_name = model_name
        self.model = None
        self._initialized = False
    
    def _initialize_model(self):
        """Lazy-load the sentence transformer model."""
        if self._initialized or not self.use_semantic:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self._initialized = True
            logger.info(f"Loaded sentence transformer model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not available, using pattern-based deduplication")
            self.use_semantic = False
            self._initialized = True
    
    def normalize_endpoint(self, endpoint: str) -> str:
        """
        Normalize an endpoint for comparison.
        
        Args:
            endpoint: Endpoint URL or path
            
        Returns:
            Normalized endpoint
        """
        # Remove protocol and domain
        normalized = re.sub(r'^https?://[^/]+', '', endpoint)
        
        # Remove trailing slashes
        normalized = normalized.rstrip('/')
        
        # Normalize parameter values (replace with placeholder)
        normalized = re.sub(r'=([^&]+)', '={value}', normalized)
        
        # Normalize numeric IDs
        normalized = re.sub(r'/\d+', '/{id}', normalized)
        
        # Normalize UUIDs
        normalized = re.sub(
            r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            '/{uuid}',
            normalized,
            flags=re.IGNORECASE
        )
        
        # Normalize version numbers
        normalized = re.sub(r'/v\d+', '/v{n}', normalized, flags=re.IGNORECASE)
        
        return normalized
    
    def extract_pattern(self, endpoint: str) -> str:
        """
        Extract a generalized pattern from an endpoint.
        
        Args:
            endpoint: Endpoint URL or path
            
        Returns:
            Pattern string
        """
        pattern = self.normalize_endpoint(endpoint)
        
        # Remove query parameters for pattern matching
        if '?' in pattern:
            path, params = pattern.split('?', 1)
            # Count parameters
            param_count = params.count('&') + 1
            pattern = f"{path}?params={param_count}"
        
        return pattern
    
    def find_near_duplicates(self, endpoints: List[str]) -> Dict[str, List[str]]:
        """
        Find near-duplicate endpoints (similar patterns with minor differences).
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Dictionary mapping pattern -> list of matching endpoints
        """
        pattern_groups = {}
        
        for endpoint in endpoints:
            pattern = self.extract_pattern(endpoint)
            
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(endpoint)
        
        # Filter out single-element groups
        near_duplicates = {k: v for k, v in pattern_groups.items() if len(v) > 1}
        
        return near_duplicates
    
    def deduplicate_semantic(self, endpoints: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Deduplicate using semantic similarity.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Tuple of (unique_endpoints, clusters)
        """
        if not self._initialized:
            self._initialize_model()
        
        if not self.model or len(endpoints) == 0:
            return endpoints, {}
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Encode all endpoints
            embeddings = self.model.encode(endpoints)
            
            # Compute pairwise similarities
            similarities = cosine_similarity(embeddings)
            
            # Cluster similar endpoints
            clusters = {}
            processed = set()
            unique_endpoints = []
            
            for i, endpoint in enumerate(endpoints):
                if i in processed:
                    continue
                
                # Find all similar endpoints
                similar_indices = [
                    j for j in range(len(endpoints))
                    if similarities[i][j] >= self.similarity_threshold and j != i
                ]
                
                if similar_indices:
                    # This endpoint represents a cluster
                    cluster_members = [endpoints[j] for j in similar_indices]
                    clusters[endpoint] = cluster_members
                    processed.update(similar_indices)
                
                unique_endpoints.append(endpoint)
                processed.add(i)
            
            return unique_endpoints, clusters
        
        except Exception as e:
            logger.error(f"Error in semantic deduplication: {e}")
            return endpoints, {}
    
    def deduplicate_pattern(self, endpoints: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Deduplicate using pattern matching.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Tuple of (unique_endpoints, pattern_groups)
        """
        pattern_groups = self.find_near_duplicates(endpoints)
        
        # Keep one representative from each pattern group
        unique_endpoints = []
        seen_patterns = set()
        
        for endpoint in endpoints:
            pattern = self.extract_pattern(endpoint)
            
            if pattern not in seen_patterns:
                unique_endpoints.append(endpoint)
                seen_patterns.add(pattern)
        
        return unique_endpoints, pattern_groups
    
    def deduplicate(self, endpoints: List[str]) -> Tuple[List[str], Dict[str, any]]:
        """
        Deduplicate endpoints using the configured method.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Tuple of (unique_endpoints, metadata) where metadata contains:
            - original_count: Original number of endpoints
            - unique_count: Number of unique endpoints
            - duplicate_count: Number of duplicates found
            - clusters: Groups of similar endpoints
        """
        original_count = len(endpoints)
        
        if self.use_semantic and not self._initialized:
            self._initialize_model()
        
        # First pass: pattern-based deduplication
        unique_pattern, pattern_groups = self.deduplicate_pattern(endpoints)
        
        # Second pass: semantic deduplication (if enabled)
        if self.use_semantic and self.model:
            unique_final, semantic_clusters = self.deduplicate_semantic(unique_pattern)
        else:
            unique_final = unique_pattern
            semantic_clusters = {}
        
        metadata = {
            'original_count': original_count,
            'unique_count': len(unique_final),
            'duplicate_count': original_count - len(unique_final),
            'pattern_groups': pattern_groups,
            'semantic_clusters': semantic_clusters,
            'reduction_percentage': round(
                (1 - len(unique_final) / original_count) * 100, 2
            ) if original_count > 0 else 0.0
        }
        
        logger.info(
            f"Deduplicated {original_count} endpoints to {len(unique_final)} "
            f"({metadata['reduction_percentage']}% reduction)"
        )
        
        return unique_final, metadata
    
    def identify_api_versions(self, endpoints: List[str]) -> Dict[str, List[str]]:
        """
        Identify and group different versions of the same API endpoint.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Dictionary mapping base_path -> list of versions
        """
        version_groups = {}
        
        for endpoint in endpoints:
            # Remove version information to get base path
            base = re.sub(r'/v\d+/', '/', endpoint, flags=re.IGNORECASE)
            base = re.sub(r'/version[_-]?\d+/', '/', base, flags=re.IGNORECASE)
            
            if base not in version_groups:
                version_groups[base] = []
            
            if endpoint not in version_groups[base]:
                version_groups[base].append(endpoint)
        
        # Filter out single-element groups
        version_groups = {k: v for k, v in version_groups.items() if len(v) > 1}
        
        return version_groups
    
    def find_parameter_variations(self, endpoints: List[str]) -> Dict[str, List[str]]:
        """
        Find endpoints that are the same except for parameters.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Dictionary mapping base_url -> list of parameter variations
        """
        param_groups = {}
        
        for endpoint in endpoints:
            # Split at query string
            if '?' in endpoint:
                base, params = endpoint.split('?', 1)
            else:
                base = endpoint
                params = ''
            
            if base not in param_groups:
                param_groups[base] = []
            
            param_groups[base].append(endpoint)
        
        # Filter out single-element groups
        param_groups = {k: v for k, v in param_groups.items() if len(v) > 1}
        
        return param_groups


def deduplicate_endpoints(endpoints: List[str],
                          threshold: float = 0.85,
                          use_semantic: bool = True) -> List[str]:
    """
    Convenience function for smart deduplication.
    
    Args:
        endpoints: List of endpoints to deduplicate
        threshold: Similarity threshold (0-1)
        use_semantic: Whether to use semantic similarity
        
    Returns:
        Deduplicated list of endpoints
    """
    deduplicator = SmartDeduplicator(
        similarity_threshold=threshold,
        use_semantic=use_semantic
    )
    unique, _ = deduplicator.deduplicate(endpoints)
    return unique
