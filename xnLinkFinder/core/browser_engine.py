"""
Headless browser integration using Playwright for dynamic JavaScript analysis.
Intercepts network requests and extracts endpoints from JavaScript execution context.
"""

from typing import List, Dict, Optional, Set, Callable
import asyncio


class BrowserEngine:
    """Playwright-based browser engine for dynamic analysis."""

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 30000,
        user_agent: Optional[str] = None,
        proxy: Optional[str] = None,
    ):
        """
        Initialize browser engine.

        Args:
            headless: Run browser in headless mode
            timeout: Page load timeout in milliseconds
            user_agent: Custom user agent
            proxy: Proxy URL
        """
        self.headless = headless
        self.timeout = timeout
        self.user_agent = user_agent
        self.proxy = proxy
        
        self.playwright = None
        self.browser = None
        self.context = None
        
        self.discovered_urls: Set[str] = set()
        self.network_requests: List[Dict] = []

    async def __aenter__(self):
        """Context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def start(self):
        """Start the browser."""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            raise ImportError(
                "Playwright not installed. Install with: pip install playwright && playwright install"
            )

        self.playwright = await async_playwright().start()
        
        # Browser launch options
        launch_options = {
            "headless": self.headless,
        }
        
        # Context options
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "ignore_https_errors": True,
        }
        
        if self.user_agent:
            context_options["user_agent"] = self.user_agent
        
        if self.proxy:
            context_options["proxy"] = {"server": self.proxy}
        
        # Launch browser
        self.browser = await self.playwright.chromium.launch(**launch_options)
        self.context = await self.browser.new_context(**context_options)
        
        # Set default timeout
        self.context.set_default_timeout(self.timeout)

    async def close(self):
        """Close the browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def analyze_url(
        self,
        url: str,
        wait_for_network_idle: bool = True,
        extract_heap: bool = False,
        javascript_to_execute: Optional[str] = None,
    ) -> Dict[str, any]:
        """
        Analyze a URL with the browser.

        Args:
            url: URL to analyze
            wait_for_network_idle: Wait for network to be idle
            extract_heap: Extract URLs from heap snapshot
            javascript_to_execute: Custom JavaScript to execute

        Returns:
            Dictionary with discovered URLs and metadata
        """
        if not self.context:
            raise RuntimeError("Browser not started")

        page = await self.context.new_page()
        
        # Track network requests
        page_requests = []
        page_responses = []

        def handle_request(request):
            page_requests.append({
                "url": request.url,
                "method": request.method,
                "headers": request.headers,
                "resource_type": request.resource_type,
            })

        def handle_response(response):
            page_responses.append({
                "url": response.url,
                "status": response.status,
                "headers": response.headers,
            })

        page.on("request", handle_request)
        page.on("response", handle_response)

        try:
            # Navigate to URL
            if wait_for_network_idle:
                await page.goto(url, wait_until="networkidle")
            else:
                await page.goto(url, wait_until="domcontentloaded")

            # Execute custom JavaScript if provided
            js_results = None
            if javascript_to_execute:
                js_results = await page.evaluate(javascript_to_execute)

            # Extract URLs from page content
            links = await page.evaluate("""
                () => {
                    const urls = new Set();
                    
                    // Extract from <a> tags
                    document.querySelectorAll('a[href]').forEach(a => {
                        urls.add(a.href);
                    });
                    
                    // Extract from <script> tags
                    document.querySelectorAll('script[src]').forEach(script => {
                        urls.add(script.src);
                    });
                    
                    // Extract from <link> tags
                    document.querySelectorAll('link[href]').forEach(link => {
                        urls.add(link.href);
                    });
                    
                    // Extract from <img> tags
                    document.querySelectorAll('img[src]').forEach(img => {
                        urls.add(img.src);
                    });
                    
                    // Extract from inline scripts (fetch, XMLHttpRequest, etc.)
                    const scriptContent = Array.from(document.querySelectorAll('script:not([src])')).map(s => s.textContent).join('\\n');
                    const urlPattern = /(?:https?:\\/\\/|\\/)[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)/g;
                    const matches = scriptContent.match(urlPattern) || [];
                    matches.forEach(match => urls.add(match));
                    
                    return Array.from(urls);
                }
            """)

            # Extract from heap snapshot if requested
            heap_urls = []
            if extract_heap:
                heap_urls = await self._extract_heap_urls(page)

            # Combine all discovered URLs
            all_urls = set(links + heap_urls)
            all_urls.update([req["url"] for req in page_requests])

            result = {
                "url": url,
                "discovered_urls": list(all_urls),
                "network_requests": page_requests,
                "network_responses": page_responses,
                "javascript_results": js_results,
            }

        finally:
            await page.close()

        return result

    async def _extract_heap_urls(self, page) -> List[str]:
        """
        Extract URLs from browser heap snapshot.

        Args:
            page: Playwright page object

        Returns:
            List of URLs found in heap
        """
        # This is a simplified implementation
        # Full heap snapshot analysis would require CDP (Chrome DevTools Protocol)
        try:
            heap_content = await page.evaluate("""
                () => {
                    const urls = [];
                    
                    // Try to access global variables that might contain URLs
                    try {
                        const globals = Object.keys(window);
                        globals.forEach(key => {
                            const value = window[key];
                            if (typeof value === 'string' && (value.startsWith('http') || value.startsWith('/'))) {
                                urls.push(value);
                            }
                        });
                    } catch (e) {}
                    
                    return urls;
                }
            """)
            return heap_content
        except Exception:
            return []

    async def intercept_api_calls(
        self,
        url: str,
        duration_seconds: int = 10,
        actions: Optional[List[Callable]] = None,
    ) -> List[Dict[str, any]]:
        """
        Intercept API calls made by the page during interaction.

        Args:
            url: URL to visit
            duration_seconds: How long to observe the page
            actions: Optional list of actions to perform (e.g., click buttons)

        Returns:
            List of API calls intercepted
        """
        if not self.context:
            raise RuntimeError("Browser not started")

        page = await self.context.new_page()
        api_calls = []

        def handle_route(route, request):
            # Check if it's an API call (XHR or Fetch)
            if request.resource_type in ["xhr", "fetch"]:
                api_calls.append({
                    "url": request.url,
                    "method": request.method,
                    "headers": request.headers,
                    "post_data": request.post_data,
                })
            route.continue_()

        # Intercept all requests
        await page.route("**/*", handle_route)

        try:
            await page.goto(url, wait_until="domcontentloaded")
            
            # Perform custom actions if provided
            if actions:
                for action in actions:
                    try:
                        await action(page)
                    except Exception:
                        pass  # Continue even if action fails
            
            # Wait for the specified duration
            await asyncio.sleep(duration_seconds)

        finally:
            await page.close()

        return api_calls


async def analyze_with_browser(
    urls: List[str],
    headless: bool = True,
    extract_heap: bool = False,
    **kwargs
) -> List[Dict[str, any]]:
    """
    Convenience function to analyze URLs with browser.

    Args:
        urls: List of URLs to analyze
        headless: Run in headless mode
        extract_heap: Extract URLs from heap
        **kwargs: Additional arguments for BrowserEngine

    Returns:
        List of analysis results
    """
    async with BrowserEngine(headless=headless, **kwargs) as engine:
        tasks = [
            engine.analyze_url(url, extract_heap=extract_heap)
            for url in urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        return [r for r in results if not isinstance(r, Exception)]
