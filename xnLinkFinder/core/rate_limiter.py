"""
Smart rate limiting with adaptive backoff.
Handles 429/503 responses and adjusts request rate automatically.
"""

import time
import asyncio
from typing import Dict, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:
    """Smart rate limiter with adaptive backoff and per-domain limiting."""

    def __init__(
        self,
        requests_per_second: float = 10.0,
        per_domain: bool = True,
        adaptive: bool = True,
        backoff_429: float = 60.0,
        backoff_503: float = 30.0,
    ):
        """
        Initialize the rate limiter.

        Args:
            requests_per_second: Base rate limit (requests per second)
            per_domain: Apply rate limiting per domain
            adaptive: Enable adaptive rate limiting based on response times
            backoff_429: Backoff time in seconds for 429 responses
            backoff_503: Backoff time in seconds for 503 responses
        """
        self.base_rate = requests_per_second
        self.per_domain = per_domain
        self.adaptive = adaptive
        self.backoff_429 = backoff_429
        self.backoff_503 = backoff_503

        # Per-domain tracking
        self._domain_limits: Dict[str, float] = defaultdict(lambda: requests_per_second)
        self._domain_last_request: Dict[str, float] = {}
        self._domain_backoff_until: Dict[str, float] = {}
        self._domain_response_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10))

        # Global tracking
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc or "global"

    def _calculate_adaptive_rate(self, domain: str) -> float:
        """Calculate adaptive rate based on recent response times."""
        if not self.adaptive or domain not in self._domain_response_times:
            return self._domain_limits[domain]

        response_times = list(self._domain_response_times[domain])
        if not response_times:
            return self._domain_limits[domain]

        # Calculate average response time
        avg_response_time = sum(response_times) / len(response_times)

        # Adjust rate based on response time
        # Slower response = lower rate
        if avg_response_time > 2.0:
            # Slow responses, reduce rate
            adjusted_rate = max(1.0, self._domain_limits[domain] * 0.5)
        elif avg_response_time > 1.0:
            adjusted_rate = max(2.0, self._domain_limits[domain] * 0.7)
        elif avg_response_time < 0.2:
            # Fast responses, can increase rate slightly
            adjusted_rate = min(50.0, self._domain_limits[domain] * 1.2)
        else:
            adjusted_rate = self._domain_limits[domain]

        return adjusted_rate

    async def acquire(self, url: str) -> None:
        """
        Acquire permission to make a request.

        Args:
            url: URL to request
        """
        async with self._lock:
            domain = self._extract_domain(url) if self.per_domain else "global"

            # Check if domain is in backoff period
            if domain in self._domain_backoff_until:
                backoff_until = self._domain_backoff_until[domain]
                if time.time() < backoff_until:
                    wait_time = backoff_until - time.time()
                    await asyncio.sleep(wait_time)
                else:
                    del self._domain_backoff_until[domain]

            # Calculate current rate and wait time
            current_rate = self._calculate_adaptive_rate(domain)
            min_interval = 1.0 / current_rate if current_rate > 0 else 0

            # Check time since last request for this domain
            last_request = self._domain_last_request.get(domain, 0)
            time_since_last = time.time() - last_request

            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)

            # Update last request time
            self._domain_last_request[domain] = time.time()

    def record_response(
        self,
        url: str,
        status_code: int,
        response_time: float
    ) -> None:
        """
        Record response for adaptive rate limiting.

        Args:
            url: URL that was requested
            status_code: HTTP status code
            response_time: Response time in seconds
        """
        domain = self._extract_domain(url) if self.per_domain else "global"

        # Record response time for adaptive limiting
        if self.adaptive:
            self._domain_response_times[domain].append(response_time)

        # Handle rate limit responses
        if status_code == 429:
            # Too Many Requests - apply backoff
            self._domain_backoff_until[domain] = time.time() + self.backoff_429
            # Also reduce rate for this domain
            self._domain_limits[domain] = max(1.0, self._domain_limits[domain] * 0.5)
        elif status_code == 503:
            # Service Unavailable - apply shorter backoff
            self._domain_backoff_until[domain] = time.time() + self.backoff_503
            self._domain_limits[domain] = max(1.0, self._domain_limits[domain] * 0.7)

    def get_domain_stats(self, url: str) -> Dict[str, any]:
        """
        Get rate limiting stats for a domain.

        Args:
            url: URL to check

        Returns:
            Dictionary with domain stats
        """
        domain = self._extract_domain(url) if self.per_domain else "global"
        
        return {
            "domain": domain,
            "current_rate": self._calculate_adaptive_rate(domain),
            "base_rate": self._domain_limits[domain],
            "in_backoff": domain in self._domain_backoff_until,
            "backoff_until": self._domain_backoff_until.get(domain),
            "avg_response_time": (
                sum(self._domain_response_times[domain]) / len(self._domain_response_times[domain])
                if domain in self._domain_response_times and self._domain_response_times[domain]
                else None
            ),
        }

    def reset_domain(self, url: str) -> None:
        """
        Reset rate limiting for a specific domain.

        Args:
            url: URL whose domain to reset
        """
        domain = self._extract_domain(url) if self.per_domain else "global"
        
        if domain in self._domain_limits:
            self._domain_limits[domain] = self.base_rate
        if domain in self._domain_backoff_until:
            del self._domain_backoff_until[domain]
        if domain in self._domain_response_times:
            self._domain_response_times[domain].clear()
