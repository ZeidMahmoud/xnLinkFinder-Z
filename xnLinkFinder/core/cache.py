"""
Caching layer for DNS lookups, static resources, and HTTP responses.
Implements ETag/Last-Modified checking and in-memory caching.
"""

import hashlib
import time
from typing import Optional, Dict, Any, Tuple
from collections import OrderedDict
from datetime import datetime, timedelta
import asyncio


class LRUCache:
    """Thread-safe LRU cache implementation."""

    def __init__(self, max_size: int = 1000):
        """
        Initialize LRU cache.

        Args:
            max_size: Maximum number of items to cache
        """
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        async with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
            return None

    async def set(self, key: str, value: Any) -> None:
        """Set item in cache."""
        async with self.lock:
            if key in self.cache:
                # Update existing
                self.cache.move_to_end(key)
            elif len(self.cache) >= self.max_size:
                # Remove oldest
                self.cache.popitem(last=False)
            self.cache[key] = value

    async def delete(self, key: str) -> None:
        """Delete item from cache."""
        async with self.lock:
            if key in self.cache:
                del self.cache[key]

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self.lock:
            self.cache.clear()

    async def size(self) -> int:
        """Get current cache size."""
        async with self.lock:
            return len(self.cache)


class TTLCache:
    """Time-to-live cache implementation."""

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000):
        """
        Initialize TTL cache.

        Args:
            ttl_seconds: Time-to-live in seconds
            max_size: Maximum number of items to cache
        """
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self.cache: Dict[str, Tuple[Any, float]] = {}
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache if not expired."""
        async with self.lock:
            if key in self.cache:
                value, expiry_time = self.cache[key]
                if time.time() < expiry_time:
                    return value
                else:
                    # Expired, remove it
                    del self.cache[key]
            return None

    async def set(self, key: str, value: Any) -> None:
        """Set item in cache with TTL."""
        async with self.lock:
            expiry_time = time.time() + self.ttl_seconds
            
            # Clean up expired entries if cache is full
            if len(self.cache) >= self.max_size:
                await self._cleanup_expired()
                
                # If still full, remove oldest
                if len(self.cache) >= self.max_size:
                    oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                    del self.cache[oldest_key]
            
            self.cache[key] = (value, expiry_time)

    async def _cleanup_expired(self) -> None:
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if current_time >= expiry
        ]
        for key in expired_keys:
            del self.cache[key]

    async def clear(self) -> None:
        """Clear all cache entries."""
        async with self.lock:
            self.cache.clear()


class CacheManager:
    """Central cache manager for different cache types."""

    def __init__(
        self,
        enable_dns_cache: bool = True,
        enable_resource_cache: bool = True,
        enable_etag_cache: bool = True,
        dns_ttl: int = 3600,
        resource_ttl: int = 1800,
        max_cache_size: int = 1000,
    ):
        """
        Initialize cache manager.

        Args:
            enable_dns_cache: Enable DNS lookup caching
            enable_resource_cache: Enable static resource caching
            enable_etag_cache: Enable ETag/Last-Modified caching
            dns_ttl: DNS cache TTL in seconds
            resource_ttl: Resource cache TTL in seconds
            max_cache_size: Maximum items per cache
        """
        self.enable_dns_cache = enable_dns_cache
        self.enable_resource_cache = enable_resource_cache
        self.enable_etag_cache = enable_etag_cache

        # Initialize caches
        self.dns_cache = TTLCache(ttl_seconds=dns_ttl, max_size=max_cache_size) if enable_dns_cache else None
        self.resource_cache = TTLCache(ttl_seconds=resource_ttl, max_size=max_cache_size) if enable_resource_cache else None
        self.etag_cache = LRUCache(max_size=max_cache_size) if enable_etag_cache else None

        # Stats
        self.stats = {
            "dns_hits": 0,
            "dns_misses": 0,
            "resource_hits": 0,
            "resource_misses": 0,
            "etag_hits": 0,
            "etag_misses": 0,
        }

    def _hash_url(self, url: str) -> str:
        """Generate hash for URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]

    async def get_dns(self, hostname: str) -> Optional[str]:
        """Get cached DNS lookup result."""
        if not self.enable_dns_cache or not self.dns_cache:
            return None

        result = await self.dns_cache.get(hostname)
        if result:
            self.stats["dns_hits"] += 1
        else:
            self.stats["dns_misses"] += 1
        return result

    async def set_dns(self, hostname: str, ip_address: str) -> None:
        """Cache DNS lookup result."""
        if self.enable_dns_cache and self.dns_cache:
            await self.dns_cache.set(hostname, ip_address)

    async def get_resource(self, url: str) -> Optional[Dict[str, Any]]:
        """Get cached resource."""
        if not self.enable_resource_cache or not self.resource_cache:
            return None

        url_hash = self._hash_url(url)
        result = await self.resource_cache.get(url_hash)
        if result:
            self.stats["resource_hits"] += 1
        else:
            self.stats["resource_misses"] += 1
        return result

    async def set_resource(self, url: str, content: bytes, headers: Dict[str, str]) -> None:
        """Cache resource with content and headers."""
        if self.enable_resource_cache and self.resource_cache:
            url_hash = self._hash_url(url)
            await self.resource_cache.set(url_hash, {
                "content": content,
                "headers": headers,
                "cached_at": time.time(),
            })

    async def get_etag_info(self, url: str) -> Optional[Dict[str, str]]:
        """Get cached ETag/Last-Modified info."""
        if not self.enable_etag_cache or not self.etag_cache:
            return None

        url_hash = self._hash_url(url)
        result = await self.etag_cache.get(url_hash)
        if result:
            self.stats["etag_hits"] += 1
        else:
            self.stats["etag_misses"] += 1
        return result

    async def set_etag_info(self, url: str, etag: Optional[str], last_modified: Optional[str]) -> None:
        """Cache ETag and Last-Modified headers."""
        if self.enable_etag_cache and self.etag_cache:
            url_hash = self._hash_url(url)
            info = {}
            if etag:
                info["etag"] = etag
            if last_modified:
                info["last_modified"] = last_modified
            if info:
                await self.etag_cache.set(url_hash, info)

    def should_use_cache(self, url: str, content_type: Optional[str] = None) -> bool:
        """
        Determine if a URL should be cached.

        Args:
            url: URL to check
            content_type: Response content type

        Returns:
            True if should be cached
        """
        if not self.enable_resource_cache:
            return False

        # Cache static resources
        static_extensions = {
            '.js', '.css', '.json', '.xml', '.woff', '.woff2',
            '.ttf', '.eot', '.svg', '.jpg', '.jpeg', '.png', '.gif'
        }
        
        url_lower = url.lower()
        if any(url_lower.endswith(ext) for ext in static_extensions):
            return True

        # Cache based on content type
        if content_type:
            cacheable_types = {
                'application/javascript',
                'text/javascript',
                'application/json',
                'text/css',
                'application/xml',
                'text/xml',
            }
            content_type_lower = content_type.lower().split(';')[0].strip()
            if content_type_lower in cacheable_types:
                return True

        return False

    async def clear_all(self) -> None:
        """Clear all caches."""
        if self.dns_cache:
            await self.dns_cache.clear()
        if self.resource_cache:
            await self.resource_cache.clear()
        if self.etag_cache:
            await self.etag_cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.stats.copy()
