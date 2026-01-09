"""
Nuclei Integration
Direct integration with Nuclei scanner
"""

import subprocess
import json
from typing import List, Dict, Optional
from pathlib import Path


class NucleiIntegration:
    """Integrate with Nuclei for scanning discovered endpoints"""
    
    def __init__(self, nuclei_path: str = "nuclei"):
        self.nuclei_path = nuclei_path
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Nuclei is available"""
        try:
            result = subprocess.run(
                [self.nuclei_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def scan_endpoints(
        self,
        endpoints: List[str],
        templates: Optional[List[str]] = None,
        severity: Optional[List[str]] = None,
        output_file: Optional[str] = None
    ) -> Dict:
        """Scan endpoints with Nuclei"""
        if not self.available:
            raise RuntimeError("Nuclei is not available")
        
        # Create temporary file with endpoints
        endpoints_file = Path("/tmp/xnlinkfinder_endpoints.txt")
        endpoints_file.write_text("\n".join(endpoints))
        
        # Build Nuclei command
        cmd = [self.nuclei_path, "-l", str(endpoints_file), "-json"]
        
        if templates:
            for template in templates:
                cmd.extend(["-t", template])
        
        if severity:
            cmd.extend(["-severity", ",".join(severity)])
        
        if output_file:
            cmd.extend(["-o", output_file])
        
        # Run Nuclei
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse results
            results = []
            if result.stdout:
                for line in result.stdout.split("\n"):
                    if line.strip():
                        try:
                            results.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
            
            return {
                "success": result.returncode == 0,
                "results": results,
                "count": len(results)
            }
        finally:
            # Cleanup
            if endpoints_file.exists():
                endpoints_file.unlink()
    
    def scan_with_custom_templates(
        self,
        endpoints: List[str],
        template_dir: str,
        output_file: Optional[str] = None
    ) -> Dict:
        """Scan with custom template directory"""
        return self.scan_endpoints(
            endpoints=endpoints,
            templates=[template_dir],
            output_file=output_file
        )
