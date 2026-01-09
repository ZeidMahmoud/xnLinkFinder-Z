"""
Achievement System for xnLinkFinder-Z.

Track progress and reward accomplishments with badges and achievements.
"""

from typing import Dict, List, Optional, Set
import logging
import json
import os
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class Achievement:
    """Represents a single achievement."""
    
    def __init__(self, id: str, name: str, description: str, 
                 category: str, points: int = 10):
        """
        Initialize achievement.
        
        Args:
            id: Unique achievement ID
            name: Achievement name
            description: Achievement description
            category: Achievement category
            points: Points awarded
        """
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.points = points
        self.unlocked = False
        self.unlock_date = None


class AchievementSystem:
    """Manage achievements and track progress."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize achievement system.
        
        Args:
            data_dir: Directory to store achievement data
        """
        self.data_dir = data_dir or os.path.expanduser("~/.xnlinkfinder/achievements")
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        self.achievements = self._define_achievements()
        self.stats = self._load_stats()
        self.unlocked = self._load_unlocked()
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all available achievements."""
        achievements = {
            # Discovery achievements
            'first_blood': Achievement(
                'first_blood',
                '🎯 First Blood',
                'Find your first endpoint',
                'discovery',
                10
            ),
            'centurion': Achievement(
                'centurion',
                '💯 Centurion',
                'Discover 100 endpoints in one scan',
                'discovery',
                50
            ),
            'millennium': Achievement(
                'millennium',
                '🏆 Millennium',
                'Discover 1000 endpoints total',
                'discovery',
                100
            ),
            'mega_discovery': Achievement(
                'mega_discovery',
                '🌟 Mega Discovery',
                'Discover 10000 endpoints total',
                'discovery',
                500
            ),
            
            # Vulnerability hunting achievements
            'critical_hunter': Achievement(
                'critical_hunter',
                '🔥 Critical Hunter',
                'Find a critical severity endpoint',
                'vulnerability',
                75
            ),
            'api_master': Achievement(
                'api_master',
                '🔌 API Master',
                'Discover 50 API endpoints',
                'vulnerability',
                50
            ),
            'admin_finder': Achievement(
                'admin_finder',
                '👑 Admin Finder',
                'Discover 10 admin endpoints',
                'vulnerability',
                50
            ),
            
            # Technical achievements
            'js_ninja': Achievement(
                'js_ninja',
                '⚡ JS Ninja',
                'Extract endpoints from 100 JS files',
                'technical',
                75
            ),
            'speed_demon': Achievement(
                'speed_demon',
                '🚀 Speed Demon',
                'Complete scan in under 60 seconds',
                'technical',
                25
            ),
            'deep_diver': Achievement(
                'deep_diver',
                '🤿 Deep Diver',
                'Scan with depth level 5 or higher',
                'technical',
                50
            ),
            
            # Persistence achievements
            'persistent': Achievement(
                'persistent',
                '💪 Persistent',
                'Run 100 scans',
                'persistence',
                100
            ),
            'marathon': Achievement(
                'marathon',
                '🏃 Marathon',
                'Run 1000 scans',
                'persistence',
                500
            ),
            'night_owl': Achievement(
                'night_owl',
                '🦉 Night Owl',
                'Run a scan after midnight',
                'persistence',
                25
            ),
            'early_bird': Achievement(
                'early_bird',
                '🐦 Early Bird',
                'Run a scan before 6 AM',
                'persistence',
                25
            ),
            
            # Exploration achievements
            'explorer': Achievement(
                'explorer',
                '🗺️ Explorer',
                'Scan 10 different domains',
                'exploration',
                50
            ),
            'world_traveler': Achievement(
                'world_traveler',
                '🌍 World Traveler',
                'Scan 100 different domains',
                'exploration',
                200
            ),
            'jack_of_trades': Achievement(
                'jack_of_trades',
                '🎭 Jack of All Trades',
                'Use 5 different output formats',
                'exploration',
                50
            ),
            
            # Special achievements
            'bug_bounty_pro': Achievement(
                'bug_bounty_pro',
                '💰 Bug Bounty Pro',
                'Use bug bounty integration features',
                'special',
                100
            ),
            'ai_enthusiast': Achievement(
                'ai_enthusiast',
                '🤖 AI Enthusiast',
                'Use AI-powered analysis features',
                'special',
                75
            ),
            'perfectionist': Achievement(
                'perfectionist',
                '✨ Perfectionist',
                'Complete a scan with 0 errors',
                'special',
                50
            ),
        }
        
        return achievements
    
    def _load_stats(self) -> Dict[str, int]:
        """Load statistics from disk."""
        stats_file = os.path.join(self.data_dir, 'stats.json')
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading stats: {e}")
        
        # Default stats
        return {
            'total_endpoints_discovered': 0,
            'total_scans_run': 0,
            'total_domains_scanned': 0,
            'total_js_files_analyzed': 0,
            'total_api_endpoints': 0,
            'total_admin_endpoints': 0,
            'critical_findings': 0,
            'fastest_scan_time': float('inf'),
            'output_formats_used': set(),
        }
    
    def _save_stats(self):
        """Save statistics to disk."""
        stats_file = os.path.join(self.data_dir, 'stats.json')
        
        try:
            # Convert sets to lists for JSON serialization
            stats_copy = self.stats.copy()
            for key, value in stats_copy.items():
                if isinstance(value, set):
                    stats_copy[key] = list(value)
            
            with open(stats_file, 'w') as f:
                json.dump(stats_copy, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving stats: {e}")
    
    def _load_unlocked(self) -> Set[str]:
        """Load unlocked achievements from disk."""
        unlocked_file = os.path.join(self.data_dir, 'unlocked.json')
        
        if os.path.exists(unlocked_file):
            try:
                with open(unlocked_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('unlocked', []))
            except Exception as e:
                logger.error(f"Error loading unlocked achievements: {e}")
        
        return set()
    
    def _save_unlocked(self):
        """Save unlocked achievements to disk."""
        unlocked_file = os.path.join(self.data_dir, 'unlocked.json')
        
        try:
            with open(unlocked_file, 'w') as f:
                json.dump({'unlocked': list(self.unlocked)}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving unlocked achievements: {e}")
    
    def update_stats(self, **kwargs):
        """
        Update statistics.
        
        Args:
            **kwargs: Stat updates (e.g., endpoints_discovered=50)
        """
        for key, value in kwargs.items():
            if key in self.stats:
                if isinstance(self.stats[key], set):
                    self.stats[key].add(value)
                elif isinstance(self.stats[key], int):
                    self.stats[key] += value
                elif key == 'fastest_scan_time':
                    self.stats[key] = min(self.stats[key], value)
        
        self._save_stats()
        self._check_achievements()
    
    def _check_achievements(self):
        """Check if any new achievements should be unlocked."""
        newly_unlocked = []
        
        for ach_id, achievement in self.achievements.items():
            if ach_id in self.unlocked:
                continue  # Already unlocked
            
            should_unlock = False
            
            # Check conditions for each achievement
            if ach_id == 'first_blood' and self.stats.get('total_endpoints_discovered', 0) >= 1:
                should_unlock = True
            elif ach_id == 'centurion' and self.stats.get('total_endpoints_discovered', 0) >= 100:
                should_unlock = True
            elif ach_id == 'millennium' and self.stats.get('total_endpoints_discovered', 0) >= 1000:
                should_unlock = True
            elif ach_id == 'mega_discovery' and self.stats.get('total_endpoints_discovered', 0) >= 10000:
                should_unlock = True
            elif ach_id == 'critical_hunter' and self.stats.get('critical_findings', 0) >= 1:
                should_unlock = True
            elif ach_id == 'api_master' and self.stats.get('total_api_endpoints', 0) >= 50:
                should_unlock = True
            elif ach_id == 'admin_finder' and self.stats.get('total_admin_endpoints', 0) >= 10:
                should_unlock = True
            elif ach_id == 'js_ninja' and self.stats.get('total_js_files_analyzed', 0) >= 100:
                should_unlock = True
            elif ach_id == 'persistent' and self.stats.get('total_scans_run', 0) >= 100:
                should_unlock = True
            elif ach_id == 'marathon' and self.stats.get('total_scans_run', 0) >= 1000:
                should_unlock = True
            elif ach_id == 'explorer' and self.stats.get('total_domains_scanned', 0) >= 10:
                should_unlock = True
            elif ach_id == 'world_traveler' and self.stats.get('total_domains_scanned', 0) >= 100:
                should_unlock = True
            elif ach_id == 'jack_of_trades' and len(self.stats.get('output_formats_used', set())) >= 5:
                should_unlock = True
            
            if should_unlock:
                self.unlock_achievement(ach_id)
                newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    def unlock_achievement(self, achievement_id: str):
        """
        Unlock an achievement.
        
        Args:
            achievement_id: ID of achievement to unlock
        """
        if achievement_id in self.unlocked:
            return  # Already unlocked
        
        if achievement_id not in self.achievements:
            logger.warning(f"Unknown achievement: {achievement_id}")
            return
        
        self.unlocked.add(achievement_id)
        achievement = self.achievements[achievement_id]
        achievement.unlocked = True
        achievement.unlock_date = datetime.now().isoformat()
        
        self._save_unlocked()
        
        # Display unlock message
        logger.info(f"🎉 Achievement Unlocked: {achievement.name}")
        logger.info(f"   {achievement.description}")
        logger.info(f"   +{achievement.points} points")
    
    def get_progress(self) -> Dict[str, any]:
        """
        Get achievement progress summary.
        
        Returns:
            Progress dictionary
        """
        total_achievements = len(self.achievements)
        unlocked_count = len(self.unlocked)
        total_points = sum(a.points for a in self.achievements.values() if a.id in self.unlocked)
        max_points = sum(a.points for a in self.achievements.values())
        
        return {
            'unlocked': unlocked_count,
            'total': total_achievements,
            'percentage': round((unlocked_count / total_achievements) * 100, 1),
            'points': total_points,
            'max_points': max_points,
            'stats': self.stats,
            'achievements': {
                ach_id: {
                    'name': ach.name,
                    'description': ach.description,
                    'unlocked': ach.id in self.unlocked,
                    'points': ach.points
                }
                for ach_id, ach in self.achievements.items()
            }
        }
    
    def display_progress(self):
        """Display progress in a nice format."""
        progress = self.get_progress()
        
        print("\n" + "=" * 60)
        print("🏆 ACHIEVEMENT PROGRESS")
        print("=" * 60)
        print(f"Unlocked: {progress['unlocked']}/{progress['total']} ({progress['percentage']}%)")
        print(f"Points: {progress['points']}/{progress['max_points']}")
        print()
        
        # Group by category
        categories = {}
        for ach_id, ach in self.achievements.items():
            if ach.category not in categories:
                categories[ach.category] = []
            categories[ach.category].append((ach_id, ach))
        
        for category, achievements in sorted(categories.items()):
            print(f"\n{category.upper()}:")
            for ach_id, ach in achievements:
                status = "✅" if ach_id in self.unlocked else "⬜"
                print(f"  {status} {ach.name} - {ach.description} ({ach.points} pts)")
        
        print("\n" + "=" * 60)


# Global achievement system instance
_achievement_system = None


def get_achievement_system() -> AchievementSystem:
    """Get or create the global achievement system instance."""
    global _achievement_system
    if _achievement_system is None:
        _achievement_system = AchievementSystem()
    return _achievement_system


def track_endpoint_discovery(count: int, critical: int = 0, api: int = 0, admin: int = 0):
    """
    Convenience function to track endpoint discovery.
    
    Args:
        count: Number of endpoints discovered
        critical: Number of critical findings
        api: Number of API endpoints
        admin: Number of admin endpoints
    """
    system = get_achievement_system()
    system.update_stats(
        total_endpoints_discovered=count,
        critical_findings=critical,
        total_api_endpoints=api,
        total_admin_endpoints=admin
    )
