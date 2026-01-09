"""
Semantic Similarity Deduplication for xnLinkFinder-Z.

Uses sentence embeddings to group similar endpoints intelligently
instead of simple string matching.
"""

from typing import List, Dict, Set, Tuple
import logging

logger = logging.getLogger(__name__)


class SemanticDeduplicator:
    """Deduplicate endpoints using semantic similarity."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", similarity_threshold: float = 0.85):
        """
        Initialize semantic deduplicator.
        
        Args:
            model_name: Sentence transformer model name
            similarity_threshold: Threshold for considering endpoints similar (0-1)
        """
        self.model_name = model_name
        self.similarity_threshold = similarity_threshold
        self.model = None
        self._initialized = False
    
    def _initialize_model(self):
        """Lazy-load the sentence transformer model."""
        if self._initialized:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            self._initialized = True
            logger.info(f"Loaded sentence transformer model: {self.model_name}")
        except ImportError:
            logger.warning("sentence-transformers not available, using basic deduplication")
            self._initialized = True
    
    def deduplicate(self, endpoints: List[str]) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Deduplicate endpoints using semantic similarity.
        
        Args:
            endpoints: List of endpoint URLs/paths
            
        Returns:
            Tuple of (unique_endpoints, clusters) where clusters maps representative -> similar endpoints
        """
        if not self._initialized:
            self._initialize_model()
        
        if not self.model or len(endpoints) == 0:
            return endpoints, {}
        
        # Encode all endpoints
        embeddings = self.model.encode(endpoints)
        
        # Compute pairwise similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(embeddings)
        
        # Cluster similar endpoints
        clusters = {}
        processed = set()
        unique_endpoints = []
        
        for i, endpoint in enumerate(endpoints):
            if i in processed:
                continue
            
            # Find all similar endpoints
            similar_indices = [j for j in range(len(endpoints)) 
                             if similarities[i][j] >= self.similarity_threshold and j != i]
            
            if similar_indices:
                # This endpoint represents a cluster
                cluster_members = [endpoints[j] for j in similar_indices]
                clusters[endpoint] = cluster_members
                processed.update(similar_indices)
            
            unique_endpoints.append(endpoint)
            processed.add(i)
        
        return unique_endpoints, clusters
    
    def group_by_similarity(self, endpoints: List[str], num_clusters: int = 10) -> Dict[int, List[str]]:
        """
        Group endpoints into clusters by similarity.
        
        Args:
            endpoints: List of endpoints
            num_clusters: Number of clusters to create
            
        Returns:
            Dictionary mapping cluster_id -> list of endpoints
        """
        if not self._initialized:
            self._initialize_model()
        
        if not self.model or len(endpoints) == 0:
            return {0: endpoints}
        
        # Encode endpoints
        embeddings = self.model.encode(endpoints)
        
        # Use KMeans clustering
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=min(num_clusters, len(endpoints)), random_state=42)
        labels = kmeans.fit_predict(embeddings)
        
        # Group by cluster
        clusters = {}
        for endpoint, label in zip(endpoints, labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(endpoint)
        
        return clusters


def deduplicate_endpoints(endpoints: List[str], threshold: float = 0.85) -> List[str]:
    """
    Convenience function for semantic deduplication.
    
    Args:
        endpoints: List of endpoints to deduplicate
        threshold: Similarity threshold
        
    Returns:
        Deduplicated list of endpoints
    """
    deduplicator = SemanticDeduplicator(similarity_threshold=threshold)
    unique, _ = deduplicator.deduplicate(endpoints)
    return unique
