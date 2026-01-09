"""
FFUF Integration
Generate FFUF-compatible wordlists and configurations
"""

from typing import List, Set, Dict
from pathlib import Path
from urllib.parse import urlparse


class FFUFIntegration:
    """Integrate with FFUF fuzzer"""
    
    def __init__(self):
        self.wordlist = set()
        self.extensions = set()
    
    def extract_paths(self, endpoints: List[str]) -> Set[str]:
        """Extract unique paths from endpoints"""
        paths = set()
        for endpoint in endpoints:
            parsed = urlparse(endpoint)
            path = parsed.path
            if path and path != '/':
                # Add full path
                paths.add(path.strip('/'))
                # Add path segments
                segments = path.strip('/').split('/')
                for segment in segments:
                    if segment:
                        paths.add(segment)
        return paths
    
    def extract_parameters(self, endpoints: List[str]) -> Set[str]:
        """Extract unique parameter names"""
        params = set()
        for endpoint in endpoints:
            parsed = urlparse(endpoint)
            if parsed.query:
                for param in parsed.query.split('&'):
                    if '=' in param:
                        param_name = param.split('=')[0]
                        params.add(param_name)
        return params
    
    def extract_extensions(self, endpoints: List[str]) -> Set[str]:
        """Extract file extensions"""
        extensions = set()
        for endpoint in endpoints:
            parsed = urlparse(endpoint)
            path = parsed.path
            if '.' in path:
                ext = path.rsplit('.', 1)[-1].lower()
                if len(ext) <= 10:  # Reasonable extension length
                    extensions.add(ext)
        return extensions
    
    def generate_wordlist(
        self,
        endpoints: List[str],
        include_paths: bool = True,
        include_params: bool = True,
        include_extensions: bool = False
    ) -> List[str]:
        """Generate comprehensive wordlist"""
        wordlist = set()
        
        if include_paths:
            wordlist.update(self.extract_paths(endpoints))
        
        if include_params:
            wordlist.update(self.extract_parameters(endpoints))
        
        if include_extensions:
            wordlist.update(self.extract_extensions(endpoints))
        
        return sorted(wordlist)
    
    def save_wordlist(
        self,
        endpoints: List[str],
        output_file: str,
        **kwargs
    ) -> Path:
        """Save wordlist to file"""
        wordlist = self.generate_wordlist(endpoints, **kwargs)
        path = Path(output_file)
        path.write_text("\n".join(wordlist))
        return path
    
    def generate_ffuf_config(
        self,
        base_url: str,
        wordlist_file: str,
        output_file: str = "ffuf_config.json"
    ) -> Dict:
        """Generate FFUF configuration"""
        config = {
            "url": f"{base_url}/FUZZ",
            "wordlist": wordlist_file,
            "method": "GET",
            "headers": {
                "User-Agent": "xnLinkFinder-FFUF"
            },
            "follow_redirects": False,
            "recursion": False,
            "recursion_depth": 1,
            "timeout": 10,
            "threads": 40,
            "match_status": [200, 204, 301, 302, 307, 401, 403],
            "filter_size": [],
            "output": {
                "format": "json",
                "file": "ffuf_results.json"
            }
        }
        
        if output_file:
            import json
            Path(output_file).write_text(json.dumps(config, indent=2))
        
        return config
    
    def generate_command(
        self,
        base_url: str,
        wordlist_file: str,
        mode: str = "dir"
    ) -> str:
        """Generate FFUF command"""
        if mode == "dir":
            return f"ffuf -u {base_url}/FUZZ -w {wordlist_file} -mc 200,204,301,302,307,401,403"
        elif mode == "param":
            return f"ffuf -u {base_url}?FUZZ=value -w {wordlist_file} -mc 200"
        elif mode == "subdomain":
            domain = urlparse(base_url).netloc
            return f"ffuf -u http://FUZZ.{domain} -w {wordlist_file} -mc 200"
        else:
            return f"ffuf -u {base_url}/FUZZ -w {wordlist_file}"
