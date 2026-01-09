"""Diff comparison report generator."""
from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)

class DiffReporter:
    """Compare scans and generate diff reports."""
    
    def compare(self, old_endpoints: List[str], new_endpoints: List[str]) -> Dict:
        """Compare two endpoint lists."""
        old_set = set(old_endpoints)
        new_set = set(new_endpoints)
        
        return {
            'added': list(new_set - old_set),
            'removed': list(old_set - new_set),
            'unchanged': list(old_set & new_set),
            'total_old': len(old_set),
            'total_new': len(new_set)
        }
    
    def generate_report(self, diff: Dict, output_path: str):
        """Generate diff report."""
        with open(output_path, 'w') as f:
            f.write("# Endpoint Diff Report\n\n")
            f.write(f"## Added ({len(diff['added'])})\n")
            for ep in diff['added']:
                f.write(f"+ {ep}\n")
            f.write(f"\n## Removed ({len(diff['removed'])})\n")
            for ep in diff['removed']:
                f.write(f"- {ep}\n")
