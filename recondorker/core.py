from .search import MultiSearcher
from .parser import ResultParser
from .report import Reporter
from .utils import setup_logging
import asyncio
import re

logger = setup_logging()

class ReconDorker:
    def __init__(self, target, proxies=None):
        self.target = target
        self.proxies = proxies
        self.searcher = MultiSearcher(proxies=proxies)
        self.results = []
        self.subdomains = set()

    async def run_scan(self, queries, pages=1, engines=["google", "bing"], progress_callback=None):
        all_results = []
        for engine in engines:
            for dork in queries:
                query = f"site:{self.target} {dork}"
                try:
                    html_pages = await self.searcher.search(query, engine=engine, pages=pages)
                    for html in html_pages:
                        if engine == "google":
                            parsed = ResultParser.parse_google_results(html)
                        else:
                            parsed = ResultParser.parse_bing_results(html)
                        
                        for item in parsed:
                            all_results.append(item)
                            # Simple subdomain extraction
                            domain_match = re.search(r'https?://([a-zA-Z0-9.-]+\.' + re.escape(self.target) + r')', item['link'])
                            if domain_match:
                                self.subdomains.add(domain_match.group(1))
                except Exception:
                    pass
                
                if progress_callback:
                    progress_callback()
        
        unique_results = {res['link']: res for res in all_results}.values()
        self.results = list(unique_results)
        return self.results

    def export(self, format='json', output_file=None):
        if not output_file:
            output_file = f"report_{self.target.replace('.', '_')}.{format}"
            
        if format == 'json':
            Reporter.to_json(self.results, output_file)
        elif format == 'csv':
            Reporter.to_csv(self.results, output_file)
        elif format == 'html':
            Reporter.to_html(self.target, self.results, output_file)

    async def close(self):
        await self.searcher.close()
