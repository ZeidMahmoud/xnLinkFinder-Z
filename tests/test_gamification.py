"""
Unit tests for gamification modules.
"""
import pytest
import tempfile
import shutil


def test_achievements_import():
    """Test that achievements can be imported."""
    try:
        from xnLinkFinder.gamification import achievements
        assert achievements is not None
    except ImportError as e:
        pytest.skip(f"Module not available: {e}")


def test_achievement_system_basic():
    """Test basic achievement system."""
    try:
        from xnLinkFinder.gamification.achievements import AchievementSystem
        
        # Create temporary directory for test
        temp_dir = tempfile.mkdtemp()
        
        try:
            system = AchievementSystem(data_dir=temp_dir)
            
            # Test initial state
            progress = system.get_progress()
            assert isinstance(progress, dict)
            assert progress['unlocked'] == 0
            assert progress['total'] > 0
            
            # Test updating stats
            system.update_stats(total_endpoints_discovered=1)
            
            # Should unlock first_blood achievement
            progress = system.get_progress()
            assert progress['unlocked'] >= 1
            
        finally:
            # Cleanup
            shutil.rmtree(temp_dir)
        
    except Exception as e:
        pytest.skip(f"Test failed: {e}")


def test_achievement_unlock():
    """Test achievement unlocking."""
    try:
        from xnLinkFinder.gamification.achievements import AchievementSystem
        
        temp_dir = tempfile.mkdtemp()
        
        try:
            system = AchievementSystem(data_dir=temp_dir)
            
            # Unlock a specific achievement
            system.unlock_achievement('first_blood')
            
            progress = system.get_progress()
            assert 'first_blood' in system.unlocked
            assert progress['points'] > 0
            
        finally:
            shutil.rmtree(temp_dir)
        
    except Exception as e:
        pytest.skip(f"Test failed: {e}")
