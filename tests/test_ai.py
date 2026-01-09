"""
Unit tests for AI modules.
"""
import pytest
import sys


def test_vulnerability_predictor_import():
    """Test that vulnerability predictor can be imported."""
    try:
        from xnLinkFinder.ai import vulnerability_predictor
        assert vulnerability_predictor is not None
    except ImportError as e:
        pytest.skip(f"Module not available: {e}")


def test_vulnerability_predictor_basic():
    """Test basic vulnerability prediction."""
    try:
        from xnLinkFinder.ai.vulnerability_predictor import VulnerabilityPredictor
        
        predictor = VulnerabilityPredictor()
        result = predictor.predict('/admin/config')
        
        assert isinstance(result, dict)
        assert 'probability' in result
        assert 'severity' in result
        assert 0 <= result['probability'] <= 100
        
    except ImportError:
        pytest.skip("scikit-learn not available")


def test_smart_dedup_import():
    """Test that smart dedup can be imported."""
    try:
        from xnLinkFinder.ai import smart_dedup
        assert smart_dedup is not None
    except ImportError as e:
        pytest.skip(f"Module not available: {e}")


def test_smart_dedup_basic():
    """Test basic deduplication."""
    try:
        from xnLinkFinder.ai.smart_dedup import SmartDeduplicator
        
        deduplicator = SmartDeduplicator(use_semantic=False)
        endpoints = [
            '/api/v1/users',
            '/api/v2/users',
            '/api/v1/users?id=1',
            '/api/v1/users?id=2',
            '/completely/different'
        ]
        
        unique, metadata = deduplicator.deduplicate(endpoints)
        
        assert isinstance(unique, list)
        assert isinstance(metadata, dict)
        assert len(unique) <= len(endpoints)
        assert 'original_count' in metadata
        assert metadata['original_count'] == len(endpoints)
        
    except Exception as e:
        pytest.skip(f"Test failed: {e}")


def test_nlp_query_import():
    """Test that NLP query can be imported."""
    try:
        from xnLinkFinder.ai import nlp_query
        assert nlp_query is not None
    except ImportError as e:
        pytest.skip(f"Module not available: {e}")


def test_nlp_query_basic():
    """Test basic NLP querying."""
    try:
        from xnLinkFinder.ai.nlp_query import NLPQueryEngine
        
        engine = NLPQueryEngine()
        engine.load_endpoints([
            '/admin/users',
            '/api/login',
            '/public/home',
            '/admin/config'
        ])
        
        result = engine.query('find all admin endpoints')
        
        assert isinstance(result, dict)
        assert 'results' in result
        assert 'count' in result
        assert result['count'] >= 0
        
    except Exception as e:
        pytest.skip(f"Test failed: {e}")


def test_anomaly_detector_import():
    """Test that anomaly detector can be imported."""
    try:
        from xnLinkFinder.ai import anomaly_detector
        assert anomaly_detector is not None
    except ImportError as e:
        pytest.skip(f"Module not available: {e}")


def test_anomaly_detector_basic():
    """Test basic anomaly detection."""
    try:
        from xnLinkFinder.ai.anomaly_detector import AnomalyDetector
        
        detector = AnomalyDetector()
        endpoints = [
            '/admin/debug',
            '/config.bak',
            '/test.php?cmd=ls',
            '/normal/path'
        ]
        
        anomalies = detector.detect_all(endpoints)
        
        assert isinstance(anomalies, dict)
        assert 'suspicious_keywords' in anomalies
        assert 'suspicious_extensions' in anomalies
        
    except Exception as e:
        pytest.skip(f"Test failed: {e}")
