"""
AI-powered analysis engine (optional feature).
Uses machine learning for semantic similarity and pattern recognition.
"""

from typing import List, Dict, Optional, Set
import re


class AIEngine:
    """
    AI-powered link analysis engine.
    
    Note: This is a placeholder implementation. For production use,
    integrate with scikit-learn or other ML libraries for:
    - Semantic similarity for deduplication
    - Pattern recognition for obfuscated JavaScript
    - Anomaly detection for unusual endpoints
    """

    def __init__(self, enable_ml: bool = False):
        """
        Initialize AI engine.

        Args:
            enable_ml: Enable machine learning features (requires scikit-learn)
        """
        self.enable_ml = enable_ml
        self._ml_available = False
        
        if enable_ml:
            try:
                import sklearn
                self._ml_available = True
            except ImportError:
                pass

    def deduplicate_semantic(self, urls: List[str], threshold: float = 0.9) -> List[str]:
        """
        Deduplicate URLs using semantic similarity.

        Args:
            urls: List of URLs to deduplicate
            threshold: Similarity threshold (0-1)

        Returns:
            Deduplicated list of URLs
        """
        if not self._ml_available or not self.enable_ml:
            # Fallback to simple deduplication
            return list(set(urls))

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            if not urls:
                return []

            # Vectorize URLs
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(urls)

            # Calculate similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)

            # Find duplicates
            unique_indices = []
            for i in range(len(urls)):
                is_duplicate = False
                for j in unique_indices:
                    if similarity_matrix[i][j] > threshold:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    unique_indices.append(i)

            return [urls[i] for i in unique_indices]

        except Exception:
            # Fallback on error
            return list(set(urls))

    def detect_obfuscated_patterns(self, content: str) -> List[Dict[str, any]]:
        """
        Detect obfuscated JavaScript patterns.

        Args:
            content: JavaScript content

        Returns:
            List of detected patterns
        """
        patterns = []

        # Check for common obfuscation indicators
        indicators = [
            (r'eval\s*\(', "eval() usage detected"),
            (r'Function\s*\(', "Function constructor usage detected"),
            (r'atob\s*\(', "base64 decoding detected"),
            (r'String\.fromCharCode', "Character code conversion detected"),
            (r'\[\'\\x[0-9a-f]{2}', "Hex encoding detected"),
            (r'\\u[0-9a-f]{4}', "Unicode escaping detected"),
        ]

        for pattern, description in indicators:
            if re.search(pattern, content, re.IGNORECASE):
                patterns.append({
                    "type": "obfuscation",
                    "indicator": description,
                    "severity": "medium",
                })

        return patterns

    def classify_endpoint_type(self, url: str) -> Dict[str, any]:
        """
        Classify endpoint type using pattern recognition.

        Args:
            url: URL to classify

        Returns:
            Classification result
        """
        # This is a simplified version
        # In production, use trained ML model
        
        classifications = {
            "rest_api": bool(re.search(r'/api/|/v\d+/', url)),
            "graphql": bool(re.search(r'/graphql|/gql', url)),
            "websocket": bool(re.search(r'wss?://', url)),
            "static_resource": bool(re.search(r'\.(js|css|jpg|png|gif|svg)$', url)),
            "authentication": bool(re.search(r'/auth|/login|/signin', url)),
        }

        # Determine primary type
        for type_name, is_match in classifications.items():
            if is_match:
                return {
                    "url": url,
                    "primary_type": type_name,
                    "confidence": 0.8,  # Placeholder confidence
                    "all_types": [k for k, v in classifications.items() if v],
                }

        return {
            "url": url,
            "primary_type": "unknown",
            "confidence": 0.0,
            "all_types": [],
        }

    def predict_parameter_type(self, param_name: str, param_value: Optional[str] = None) -> str:
        """
        Predict parameter type based on name and value.

        Args:
            param_name: Parameter name
            param_value: Optional parameter value

        Returns:
            Predicted type (string, integer, boolean, etc.)
        """
        param_lower = param_name.lower()

        # Pattern-based type inference
        if any(x in param_lower for x in ["id", "count", "limit", "offset", "page"]):
            return "integer"
        elif any(x in param_lower for x in ["email", "mail"]):
            return "email"
        elif any(x in param_lower for x in ["url", "uri", "link"]):
            return "url"
        elif any(x in param_lower for x in ["date", "time", "timestamp"]):
            return "datetime"
        elif any(x in param_lower for x in ["is_", "has_", "enable", "disable"]):
            return "boolean"
        
        # Check value if provided
        if param_value:
            if param_value.lower() in ["true", "false"]:
                return "boolean"
            elif param_value.isdigit():
                return "integer"
            elif re.match(r'^[\d.]+$', param_value):
                return "float"
        
        return "string"

    def get_feature_status(self) -> Dict[str, bool]:
        """
        Get status of AI features.

        Returns:
            Feature availability status
        """
        return {
            "ml_available": self._ml_available,
            "semantic_deduplication": self._ml_available,
            "pattern_recognition": True,  # Basic pattern recognition always available
            "obfuscation_detection": True,
            "endpoint_classification": True,
        }


def create_ai_engine(enable_ml: bool = False) -> AIEngine:
    """
    Create AI engine instance.

    Args:
        enable_ml: Enable ML features

    Returns:
        AIEngine instance
    """
    return AIEngine(enable_ml=enable_ml)
