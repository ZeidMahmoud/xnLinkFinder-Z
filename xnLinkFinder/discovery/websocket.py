"""
WebSocket endpoint enumeration and discovery module.
"""

import re
from typing import List, Dict, Optional, Set


class WebSocketDiscovery:
    """WebSocket endpoint discovery."""

    # Common WebSocket URL patterns
    WS_PATTERNS = [
        r'wss?://[^\s\'"<>]+',
        r'["\'](wss?://[^"\']+)["\']',
        r'new\s+WebSocket\s*\(\s*["\']([^"\']+)["\']',
        r'io\s*\(\s*["\']([^"\']+)["\']',  # Socket.io
    ]

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize WebSocket discovery.

        Args:
            base_url: Base URL for resolving relative WebSocket URLs
        """
        self.base_url = base_url
        self.discovered_endpoints: Set[str] = set()

    def extract_from_content(self, content: str) -> List[str]:
        """
        Extract WebSocket URLs from content.

        Args:
            content: Text content to analyze

        Returns:
            List of discovered WebSocket URLs
        """
        discovered = set()

        for pattern in self.WS_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get the URL from the appropriate capture group
                if match.lastindex and match.lastindex > 0:
                    url = match.group(1)
                else:
                    url = match.group(0)

                # Clean up the URL
                url = url.strip().strip('"').strip("'")

                if url.startswith("ws://") or url.startswith("wss://"):
                    discovered.add(url)
                    self.discovered_endpoints.add(url)

        return list(discovered)

    def extract_socket_io_paths(self, content: str) -> List[str]:
        """
        Extract Socket.io specific paths.

        Args:
            content: JavaScript content to analyze

        Returns:
            List of Socket.io paths
        """
        paths = set()

        # Socket.io connection patterns
        patterns = [
            r'io\.connect\s*\(\s*["\']([^"\']+)["\']',
            r'io\s*\(\s*["\']([^"\']+)["\']',
            r'socket\.io\s*\(\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                path = match.group(1).strip()
                paths.add(path)

        return list(paths)

    def extract_sockjs_paths(self, content: str) -> List[str]:
        """
        Extract SockJS specific paths.

        Args:
            content: JavaScript content to analyze

        Returns:
            List of SockJS paths
        """
        paths = set()

        # SockJS connection patterns
        patterns = [
            r'new\s+SockJS\s*\(\s*["\']([^"\']+)["\']',
            r'SockJS\s*\(\s*["\']([^"\']+)["\']',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                path = match.group(1).strip()
                paths.add(path)

        return list(paths)

    def analyze_content(self, content: str) -> Dict[str, any]:
        """
        Perform full WebSocket analysis on content.

        Args:
            content: Content to analyze

        Returns:
            Analysis results
        """
        ws_urls = self.extract_from_content(content)
        socketio_paths = self.extract_socket_io_paths(content)
        sockjs_paths = self.extract_sockjs_paths(content)

        return {
            "websocket_urls": ws_urls,
            "socketio_paths": socketio_paths,
            "sockjs_paths": sockjs_paths,
            "total_count": len(ws_urls) + len(socketio_paths) + len(sockjs_paths),
        }

    def check_common_endpoints(self, base_url: str) -> List[str]:
        """
        Generate common WebSocket endpoint paths to check.

        Args:
            base_url: Base URL

        Returns:
            List of potential WebSocket endpoints
        """
        # Convert HTTP(S) to WS(S)
        ws_base = base_url.replace("https://", "wss://").replace("http://", "ws://")

        common_paths = [
            "/ws",
            "/websocket",
            "/socket",
            "/socket.io",
            "/sockjs",
            "/api/ws",
            "/api/websocket",
            "/live",
            "/stream",
            "/realtime",
            "/chat",
            "/notifications",
            "/updates",
            "/events",
        ]

        return [f"{ws_base}{path}" for path in common_paths]


def discover_websockets(content: str, base_url: Optional[str] = None) -> Dict[str, any]:
    """
    Convenience function for WebSocket discovery.

    Args:
        content: Content to analyze
        base_url: Optional base URL

    Returns:
        Discovery results
    """
    discovery = WebSocketDiscovery(base_url)
    results = discovery.analyze_content(content)

    if base_url:
        results["common_endpoints"] = discovery.check_common_endpoints(base_url)

    return results
