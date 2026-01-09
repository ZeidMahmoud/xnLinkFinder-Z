"""Mobile app analysis for endpoint extraction."""
from typing import List, Dict
import logging
import subprocess
import os

logger = logging.getLogger(__name__)

class MobileAnalyzer:
    """Analyze mobile apps to extract endpoints."""
    
    def analyze_apk(self, apk_path: str) -> List[str]:
        """Extract endpoints from Android APK."""
        endpoints = []
        try:
            import os
            # Validate path to prevent command injection
            if not os.path.isfile(apk_path):
                logger.error(f"APK file not found: {apk_path}")
                return endpoints
            
            # Simple string extraction (requires strings in PATH)
            result = subprocess.run(
                ['strings', apk_path],
                capture_output=True,
                text=True,
                timeout=60,
                check=False
            )
            for line in result.stdout.split('\n'):
                if 'http' in line.lower() or 'api' in line.lower():
                    endpoints.append(line.strip())
        except Exception as e:
            logger.error(f"APK analysis failed: {e}")
        return endpoints
    
    def analyze_ipa(self, ipa_path: str) -> List[str]:
        """Extract endpoints from iOS IPA."""
        endpoints = []
        try:
            import os
            # Validate path to prevent command injection
            if not os.path.isfile(ipa_path):
                logger.error(f"IPA file not found: {ipa_path}")
                return endpoints
            
            result = subprocess.run(
                ['strings', ipa_path],
                capture_output=True,
                text=True,
                timeout=60,
                check=False
            )
            for line in result.stdout.split('\n'):
                if 'http' in line.lower() or 'api' in line.lower():
                    endpoints.append(line.strip())
        except Exception as e:
            logger.error(f"IPA analysis failed: {e}")
        return endpoints

def analyze_mobile_app(app_path: str) -> List[str]:
    """Analyze mobile app and extract endpoints."""
    analyzer = MobileAnalyzer()
    if app_path.endswith('.apk'):
        return analyzer.analyze_apk(app_path)
    elif app_path.endswith('.ipa'):
        return analyzer.analyze_ipa(app_path)
    return []
