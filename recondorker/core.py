from .search import MultiSearcher
from .parser import ResultParser
from .report import Reporter
from .utils import setup_logging
from .metadata import MetadataExtractor
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

    async def run_scan(self, queries, pages=1, engines=["google", "bing", "duckduckgo"], progress_callback=None, recursive=False):
        all_results = []
        scanned_domains = {self.target}
        domains_to_scan = [self.target]
        
        while domains_to_scan:
            current_domain = domains_to_scan.pop(0)
            logger.info(f"Scanning domain: {current_domain}")
            
            for engine in engines:
                for dork in queries:
                    query = f"site:{current_domain} {dork}"
                    try:
                        html_pages = await self.searcher.search(query, engine=engine, pages=pages)
                        for html in html_pages:
                            if engine == "google":
                                parsed = ResultParser.parse_google_results(html)
                            elif engine == "bing":
                                parsed = ResultParser.parse_bing_results(html)
                            elif engine == "duckduckgo":
                                parsed = ResultParser.parse_duckduckgo_results(html)
                            else:
                                parsed = []
                            
                            for item in parsed:
                                all_results.append(item)
                                # Metadata extraction for documents
                                if any(item['link'].lower().endswith(ext) for ext in ['.pdf', '.docx']):
                                    item['metadata'] = await MetadataExtractor.extract_from_url(item['link'], client=self.searcher.client)
                                
                                # Subdomain extraction
                                domain_match = re.search(r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+)', item['link'])
                                if domain_match:
                                    found_host = domain_match.group(1)
                                    if found_host.endswith(self.target) and found_host not in scanned_domains:
                                        self.subdomains.add(found_host)
                                        if recursive:
                                            domains_to_scan.append(found_host)
                                            scanned_domains.add(found_host)
                    except Exception as e:
                        logger.error(f"Error scanning {current_domain} with {engine}: {e}")
                    
                    if progress_callback:
                        progress_callback()
            
            if not recursive:
                break
        
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
