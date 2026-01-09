import asyncio
import httpx
from bs4 import BeautifulSoup
from .utils import get_random_user_agent, setup_logging
from .errors import SearchError, RateLimitError, CaptchaError

logger = setup_logging()

class GoogleSearcher:
    def __init__(self, proxies=None, timeout=10.0):
        self.proxies = proxies
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            proxies=self.proxies,
            timeout=self.timeout,
            follow_redirects=True
        )

    async def search(self, query, pages=1):
        results = []
        for page in range(pages):
            start = page * 10
            url = f"https://www.google.com/search?q={query}&start={start}"
            headers = {"User-Agent": get_random_user_agent()}
            
            try:
                response = await self.client.get(url, headers=headers)
                
                if response.status_code == 429:
                    logger.error(f"Rate limit detected for query: {query}")
                    raise RateLimitError("Google rate limit exceeded")
                
                if "captcha" in response.text.lower() or "not a robot" in response.text.lower():
                    logger.error("Captcha detected!")
                    raise CaptchaError("Google Captcha detected")
                
                response.raise_for_status()
                results.append(response.text)
                
                # Ethical Delay
                await asyncio.sleep(2)
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e}")
                raise SearchError(f"HTTP Error: {e.response.status_code}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
                raise SearchError(f"Unexpected error: {str(e)}")
                
        return results

    async def close(self):
        await self.client.aclose()
