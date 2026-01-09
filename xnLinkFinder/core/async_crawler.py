"""
Async HTTP crawler for efficient concurrent processing.
Replaces basic multiprocessing with async/await using aiohttp.
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Optional, Callable, Any
from urllib.parse import urlparse


class AsyncCrawler:
    """Asynchronous HTTP crawler with connection pooling and rate limiting."""

    def __init__(
        self,
        max_concurrent: int = 25,
        timeout: int = 10,
        rate_limit: float = 0,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        verify_ssl: bool = True,
        proxy: Optional[str] = None,
    ):
        """
        Initialize the async crawler.

        Args:
            max_concurrent: Maximum number of concurrent requests
            timeout: Request timeout in seconds
            rate_limit: Maximum requests per second (0 = no limit)
            headers: Custom HTTP headers
            cookies: HTTP cookies
            verify_ssl: Whether to verify SSL certificates
            proxy: Proxy URL (e.g., http://127.0.0.1:8080)
        """
        self.max_concurrent = max_concurrent
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.rate_limit = rate_limit
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.verify_ssl = verify_ssl
        self.proxy = proxy
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None
        self._last_request_time = 0.0
        self._rate_limit_lock = asyncio.Lock()

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        """Start the crawler session."""
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            ssl=self.verify_ssl,
            force_close=False,
            enable_cleanup_closed=True,
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout,
            headers=self.headers,
            cookies=self.cookies,
        )
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

    async def close(self):
        """Close the crawler session."""
        if self.session:
            await self.session.close()

    async def _apply_rate_limit(self):
        """Apply rate limiting between requests."""
        if self.rate_limit <= 0:
            return

        async with self._rate_limit_lock:
            current_time = time.time()
            time_since_last = current_time - self._last_request_time
            min_interval = 1.0 / self.rate_limit

            if time_since_last < min_interval:
                await asyncio.sleep(min_interval - time_since_last)

            self._last_request_time = time.time()

    async def fetch(
        self,
        url: str,
        method: str = "GET",
        data: Optional[Any] = None,
        max_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Fetch a single URL.

        Args:
            url: URL to fetch
            method: HTTP method
            data: Request body data
            max_size: Maximum response size in bytes

        Returns:
            Dictionary with status, headers, content, and error information
        """
        if not self.session:
            raise RuntimeError("Crawler not started. Use 'async with' or call start()")

        await self._apply_rate_limit()

        result = {
            "url": url,
            "status": None,
            "headers": {},
            "content": None,
            "error": None,
            "size": 0,
        }

        try:
            async with self.semaphore:
                async with self.session.request(
                    method,
                    url,
                    data=data,
                    proxy=self.proxy,
                    allow_redirects=True,
                ) as response:
                    result["status"] = response.status
                    result["headers"] = dict(response.headers)

                    # Check size if max_size is specified
                    content_length = response.headers.get("Content-Length")
                    if max_size and content_length:
                        if int(content_length) > max_size:
                            result["error"] = f"Response too large: {content_length} bytes"
                            return result

                    # Read content in chunks if max_size is specified
                    if max_size:
                        chunks = []
                        total_size = 0
                        async for chunk in response.content.iter_chunked(8192):
                            total_size += len(chunk)
                            if total_size > max_size:
                                result["error"] = f"Response exceeded max size: {max_size} bytes"
                                return result
                            chunks.append(chunk)
                        result["content"] = b"".join(chunks)
                    else:
                        result["content"] = await response.read()

                    result["size"] = len(result["content"])

        except asyncio.TimeoutError:
            result["error"] = "Timeout"
        except aiohttp.ClientError as e:
            result["error"] = f"Client error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"

        return result

    async def fetch_many(
        self,
        urls: List[str],
        callback: Optional[Callable] = None,
        max_size: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch multiple URLs concurrently.

        Args:
            urls: List of URLs to fetch
            callback: Optional callback function called for each result
            max_size: Maximum response size in bytes

        Returns:
            List of result dictionaries
        """
        tasks = [self.fetch(url, max_size=max_size) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "url": "unknown",
                    "status": None,
                    "headers": {},
                    "content": None,
                    "error": str(result),
                    "size": 0,
                })
            else:
                processed_results.append(result)
                if callback:
                    try:
                        callback(result)
                    except Exception:
                        pass  # Ignore callback errors

        return processed_results


async def crawl_urls(
    urls: List[str],
    max_concurrent: int = 25,
    timeout: int = 10,
    rate_limit: float = 0,
    **kwargs
) -> List[Dict[str, Any]]:
    """
    Convenience function to crawl multiple URLs.

    Args:
        urls: List of URLs to crawl
        max_concurrent: Maximum concurrent connections
        timeout: Request timeout in seconds
        rate_limit: Maximum requests per second
        **kwargs: Additional arguments passed to AsyncCrawler

    Returns:
        List of result dictionaries
    """
    async with AsyncCrawler(
        max_concurrent=max_concurrent,
        timeout=timeout,
        rate_limit=rate_limit,
        **kwargs
    ) as crawler:
        return await crawler.fetch_many(urls)
