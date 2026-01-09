import asyncio
import httpx
import re
from bs4 import BeautifulSoup
from .utils import get_random_user_agent, setup_logging
from .errors import SearchError, RateLimitError, CaptchaError

logger = setup_logging()

class MultiSearcher:
    def __init__(self, proxies=None, timeout=15.0):
        self.proxies = proxies
        self.timeout = timeout
        self.proxy_list = []
        if isinstance(proxies, list):
            self.proxy_list = proxies
            self.current_proxy_idx = 0
            
        self.client = self._create_client()

    def _create_client(self):
        proxy_url = None
        if self.proxy_list:
            proxy_url = self.proxy_list[self.current_proxy_idx]
            self.current_proxy_idx = (self.current_proxy_idx + 1) % len(self.proxy_list)
        elif isinstance(self.proxies, dict):
            proxy_url = self.proxies.get("http://") or self.proxies.get("https://")
        elif isinstance(self.proxies, str):
            proxy_url = self.proxies

        return httpx.AsyncClient(
            proxy=proxy_url,
            timeout=self.timeout,
            follow_redirects=True,
            headers={"User-Agent": get_random_user_agent()}
        )

    async def rotate_proxy(self):
        if self.proxy_list:
            await self.client.aclose()
            self.client = self._create_client()

    async def search_google(self, query, pages=1):
        results = []
        for page in range(pages):
            start = page * 10
            url = f"https://www.google.com/search?q={query}&start={start}"
            try:
                response = await self.client.get(url)
                if response.status_code == 429:
                    raise RateLimitError("Google rate limit exceeded")
                if "captcha" in response.text.lower() or "not a robot" in response.text.lower():
                    raise CaptchaError("Google Captcha detected")
                response.raise_for_status()
                results.append(response.text)
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Google search error: {e}")
        return results

    async def search_bing(self, query, pages=1):
        results = []
        for page in range(pages):
            first = (page * 10) + 1
            url = f"https://www.bing.com/search?q={query}&first={first}"
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                results.append(response.text)
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f"Bing search error: {e}")
        return results

    async def search_duckduckgo(self, query, pages=1):
        results = []
        url = "https://html.duckduckgo.com/html/"
        # Note: DDG HTML version doesn't support easy pagination via URL for all cases, 
        # but for OSINT, the first page is often enough.
        for page in range(pages):
            try:
                data = {'q': query}
                response = await self.client.post(url, data=data)
                response.raise_for_status()
                results.append(response.text)
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"DuckDuckGo search error: {e}")
        return results

    async def search(self, query, engine="google", pages=1):
        if engine == "google":
            return await self.search_google(query, pages)
        elif engine == "bing":
            return await self.search_bing(query, pages)
        elif engine == "duckduckgo":
            return await self.search_duckduckgo(query, pages)
        return []

    async def close(self):
        await self.client.aclose()
