"""JavaScript Library Detector - Detect JS libraries and match CVEs"""
import re
from typing import List, Dict

class JSLibraryDetector:
    def __init__(self):
        self.patterns = {
            'jquery': r'jquery[/-](\d+\.\d+\.\d+)',
            'react': r'react[/-](\d+\.\d+\.\d+)',
            'angular': r'angular[/-](\d+\.\d+\.\d+)',
        }
    
    def detect(self, content: str) -> List[Dict]:
        """Detect JS libraries in content"""
        results = []
        for lib, pattern in self.patterns.items():
            matches = re.findall(pattern, content, re.I)
            for version in matches:
                results.append({'library': lib, 'version': version})
        return results

def detect_js_libraries(content: str) -> List[Dict]:
    detector = JSLibraryDetector()
    return detector.detect(content)
