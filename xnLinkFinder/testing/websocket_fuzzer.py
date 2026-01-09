"""
WebSocket Fuzzer

Fuzzes WebSocket connections for vulnerabilities:
- Message format fuzzing
- Injection detection
- Protocol violation testing
"""

from typing import Dict, List, Optional
import json

try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("[!] websocket-client not installed. WebSocket fuzzing unavailable.")


class WebSocketFuzzer:
    """Fuzz WebSocket connections"""
    
    PAYLOADS = [
        '{"test": "' + 'A' * 10000 + '"}',  # Large payload
        '"><script>alert(1)</script>',  # XSS
        "' OR '1'='1",  # SQL injection
        '{{7*7}}',  # Template injection
        '../../../etc/passwd',  # Path traversal
    ]
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.available = WEBSOCKET_AVAILABLE
        
    def fuzz(self, ws_url: str, messages: Optional[List[str]] = None) -> List[Dict]:
        """Fuzz a WebSocket endpoint"""
        if not self.available:
            return [{'error': 'websocket-client not installed'}]
            
        results = []
        test_messages = messages or self.PAYLOADS
        
        try:
            ws = websocket.create_connection(ws_url, timeout=self.timeout)
            
            for payload in test_messages:
                try:
                    ws.send(payload)
                    response = ws.recv()
                    
                    results.append({
                        'payload': payload[:100],
                        'response': response[:100] if response else None,
                        'success': True,
                    })
                except Exception as e:
                    results.append({
                        'payload': payload[:100],
                        'error': str(e),
                        'success': False,
                    })
                    
            ws.close()
            
        except Exception as e:
            results.append({'error': f'Connection failed: {str(e)}'})
            
        return results


def fuzz_websockets(ws_urls: List[str], **kwargs) -> Dict[str, List[Dict]]:
    """Fuzz multiple WebSocket endpoints"""
    fuzzer = WebSocketFuzzer(**kwargs)
    return {url: fuzzer.fuzz(url) for url in ws_urls}
