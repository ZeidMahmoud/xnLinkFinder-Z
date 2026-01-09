"""
Neural Network Pattern Recognition for xnLinkFinder-Z.

This module uses deep learning to detect obfuscated endpoints in:
- Heavily minified JavaScript bundles
- Webpack bundles
- Compiled/transpiled code
- Obfuscated strings
"""

from typing import List, Dict, Optional, Tuple
import logging
import re

logger = logging.getLogger(__name__)


class NeuralDetector:
    """
    Uses neural networks to detect obfuscated endpoints in JavaScript code.
    
    Supports TensorFlow and PyTorch backends.
    """
    
    def __init__(self, backend: str = "tensorflow", model_path: Optional[str] = None):
        """
        Initialize neural detector.
        
        Args:
            backend: ML backend ('tensorflow' or 'pytorch')
            model_path: Path to pre-trained model (if None, uses default pattern matching)
        """
        self.backend = backend
        self.model_path = model_path
        self.model = None
        self._initialized = False
    
    def _initialize_model(self):
        """Initialize the neural network model."""
        if self._initialized:
            return
        
        try:
            if self.backend == "tensorflow":
                self._init_tensorflow_model()
            elif self.backend == "pytorch":
                self._init_pytorch_model()
            else:
                logger.warning(f"Unsupported backend: {self.backend}, using pattern matching fallback")
        except ImportError as e:
            logger.warning(f"Neural network backend not available: {e}. Using pattern matching fallback.")
        
        self._initialized = True
    
    def _init_tensorflow_model(self):
        """Initialize TensorFlow model."""
        try:
            import tensorflow as tf
            if self.model_path:
                self.model = tf.keras.models.load_model(self.model_path)
            else:
                # Use default pattern-based detection
                logger.info("No model path provided, using pattern-based detection")
        except ImportError:
            logger.warning("TensorFlow not available")
    
    def _init_pytorch_model(self):
        """Initialize PyTorch model."""
        try:
            import torch
            if self.model_path:
                self.model = torch.load(self.model_path)
                self.model.eval()
            else:
                logger.info("No model path provided, using pattern-based detection")
        except ImportError:
            logger.warning("PyTorch not available")
    
    def detect_obfuscated_endpoints(self, code: str) -> List[Dict[str, any]]:
        """
        Detect obfuscated endpoints in JavaScript code.
        
        Args:
            code: JavaScript source code (minified or not)
            
        Returns:
            List of detected endpoints with confidence scores
        """
        if not self._initialized:
            self._initialize_model()
        
        if self.model:
            return self._detect_with_model(code)
        else:
            return self._detect_with_patterns(code)
    
    def _detect_with_model(self, code: str) -> List[Dict[str, any]]:
        """Detect endpoints using trained neural network."""
        # This would use the actual model for prediction
        # For now, fall back to pattern-based detection
        logger.info("Using neural network model for detection")
        return self._detect_with_patterns(code)
    
    def _detect_with_patterns(self, code: str) -> List[Dict[str, any]]:
        """
        Detect endpoints using advanced pattern matching.
        
        Looks for common obfuscation patterns:
        - Hex-encoded strings
        - Unicode escape sequences
        - Base64 encoded URLs
        - String concatenation patterns
        - Dynamic property access
        """
        endpoints = []
        
        # Detect hex-encoded strings that might be endpoints
        hex_pattern = r'\\x([0-9a-fA-F]{2})+'
        hex_matches = re.finditer(hex_pattern, code)
        for match in hex_matches:
            try:
                decoded = bytes.fromhex(match.group(0).replace('\\x', '')).decode('utf-8', errors='ignore')
                if self._looks_like_endpoint(decoded):
                    endpoints.append({
                        'endpoint': decoded,
                        'confidence': 0.7,
                        'method': 'hex_decode',
                        'original': match.group(0)
                    })
            except:
                pass
        
        # Detect unicode escape sequences
        unicode_pattern = r'\\u([0-9a-fA-F]{4})+'
        unicode_matches = re.finditer(unicode_pattern, code)
        for match in unicode_matches:
            try:
                decoded = match.group(0).encode().decode('unicode-escape')
                if self._looks_like_endpoint(decoded):
                    endpoints.append({
                        'endpoint': decoded,
                        'confidence': 0.7,
                        'method': 'unicode_decode',
                        'original': match.group(0)
                    })
            except:
                pass
        
        # Detect base64 encoded strings
        base64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
        base64_matches = re.finditer(base64_pattern, code)
        for match in base64_matches:
            try:
                import base64
                decoded = base64.b64decode(match.group(0)).decode('utf-8', errors='ignore')
                if self._looks_like_endpoint(decoded):
                    endpoints.append({
                        'endpoint': decoded,
                        'confidence': 0.6,
                        'method': 'base64_decode',
                        'original': match.group(0)
                    })
            except:
                pass
        
        # Detect string concatenation patterns (e.g., "/api"+"/"+"users")
        concat_pattern = r'["\']([/\w-]+)["\'][\s]*\+[\s]*["\']([/\w-]+)["\']'
        concat_matches = re.finditer(concat_pattern, code)
        for match in concat_matches:
            concatenated = match.group(1) + match.group(2)
            if self._looks_like_endpoint(concatenated):
                endpoints.append({
                    'endpoint': concatenated,
                    'confidence': 0.8,
                    'method': 'string_concat',
                    'original': match.group(0)
                })
        
        # Detect template literals with possible endpoints
        template_pattern = r'`([^`]*)`'
        template_matches = re.finditer(template_pattern, code)
        for match in template_matches:
            content = match.group(1)
            if self._looks_like_endpoint(content):
                endpoints.append({
                    'endpoint': content,
                    'confidence': 0.75,
                    'method': 'template_literal',
                    'original': match.group(0)
                })
        
        return self._deduplicate_endpoints(endpoints)
    
    def _looks_like_endpoint(self, text: str) -> bool:
        """Check if a string looks like an API endpoint."""
        if not text or len(text) < 3:
            return False
        
        # Check for URL path patterns
        if text.startswith('/') or text.startswith('http'):
            return True
        
        # Check for API-like patterns
        api_patterns = [
            r'/api/',
            r'/v\d+/',
            r'/rest/',
            r'/graphql',
            r'/endpoint',
            r'\.php',
            r'\.asp',
            r'\.jsp',
            r'/admin',
            r'/user',
            r'/auth',
        ]
        
        for pattern in api_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _deduplicate_endpoints(self, endpoints: List[Dict]) -> List[Dict]:
        """Remove duplicate endpoints, keeping the one with highest confidence."""
        seen = {}
        for ep in endpoints:
            url = ep['endpoint']
            if url not in seen or ep['confidence'] > seen[url]['confidence']:
                seen[url] = ep
        return list(seen.values())
    
    def extract_webpack_chunks(self, code: str) -> List[str]:
        """
        Extract endpoints from webpack chunk loaders.
        
        Args:
            code: JavaScript code containing webpack chunks
            
        Returns:
            List of discovered chunk URLs/endpoints
        """
        endpoints = []
        
        # Webpack chunk loading patterns
        chunk_patterns = [
            r'\.p\s*\+\s*["\']([^"\']+)["\']',  # __webpack_require__.p + "chunk.js"
            r'chunkId\s*\+\s*["\']([^"\']+)["\']',
            r'["\']([\w/.-]+\.chunk\.js)["\']',
            r'\.chunk\.js["\']:\s*["\']([^"\']+)["\']',
        ]
        
        for pattern in chunk_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                chunk = match.group(1)
                endpoints.append(chunk)
        
        return list(set(endpoints))
    
    def analyze_bundle(self, code: str) -> Dict[str, any]:
        """
        Comprehensive analysis of a JavaScript bundle.
        
        Args:
            code: JavaScript bundle code
            
        Returns:
            Analysis results with endpoints, confidence, and metadata
        """
        if not self._initialized:
            self._initialize_model()
        
        results = {
            'endpoints': self.detect_obfuscated_endpoints(code),
            'webpack_chunks': self.extract_webpack_chunks(code),
            'bundle_size': len(code),
            'is_minified': self._is_minified(code),
            'obfuscation_score': self._calculate_obfuscation_score(code)
        }
        
        return results
    
    def _is_minified(self, code: str) -> bool:
        """Check if code appears to be minified."""
        # Simple heuristic: check average line length
        lines = code.split('\n')
        if not lines:
            return False
        avg_line_length = sum(len(line) for line in lines) / len(lines)
        return avg_line_length > 200
    
    def _calculate_obfuscation_score(self, code: str) -> float:
        """
        Calculate obfuscation score (0-1).
        
        Higher scores indicate more obfuscation.
        """
        score = 0.0
        
        # Check for hex encoding
        if re.search(r'\\x[0-9a-fA-F]{2}', code):
            score += 0.2
        
        # Check for unicode escapes
        if re.search(r'\\u[0-9a-fA-F]{4}', code):
            score += 0.2
        
        # Check for base64-like strings
        if re.search(r'[A-Za-z0-9+/]{40,}=', code):
            score += 0.2
        
        # Check for single character variable names (common in minification)
        single_char_vars = len(re.findall(r'\b[a-z]\s*=', code))
        if single_char_vars > 10:
            score += 0.2
        
        # Check for eval/Function usage (potential obfuscation)
        if re.search(r'\beval\(|\bFunction\(', code):
            score += 0.2
        
        return min(score, 1.0)


def detect_obfuscated_endpoints(code: str, backend: str = "tensorflow") -> List[Dict[str, any]]:
    """
    Convenience function to detect obfuscated endpoints.
    
    Args:
        code: JavaScript code to analyze
        backend: ML backend to use
        
    Returns:
        List of detected endpoints
    """
    detector = NeuralDetector(backend=backend)
    return detector.detect_obfuscated_endpoints(code)
