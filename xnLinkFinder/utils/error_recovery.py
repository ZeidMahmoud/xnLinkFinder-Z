"""Error Recovery System"""
import json
from pathlib import Path

class ErrorRecovery:
    def __init__(self, state_file: str = ".xnlinkfinder_state.json"):
        self.state_file = Path(state_file)
    
    def save_state(self, state: dict):
        """Save current state"""
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
    
    def restore_state(self) -> dict:
        """Restore saved state"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def cleanup(self):
        """Clean up state file"""
        if self.state_file.exists():
            self.state_file.unlink()

def resume_scan(scan_id: str) -> dict:
    """Resume interrupted scan"""
    recovery = ErrorRecovery()
    return recovery.restore_state()
