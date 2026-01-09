from .search import GoogleSearcher
from .parser import ResultParser
from .report import Reporter
from .utils import setup_logging
import asyncio

logger = setup_logging()

class ReconDorker:
    def __init__(self, target, proxies=None):
        self.target = target
        self.proxies = proxies
        self.searcher = GoogleSearcher(proxies=proxies)
        self.results = []

    async def run_scan(self, queries, pages=1):
        logger.info(f"Starting scan for target: [bold cyan]{self.target}[/bold cyan]")
        
        all_results = []
        for dork in queries:
            query = f"site:{self.target} {dork}"
            logger.info(f"Running query: [yellow]{query}[/yellow]")
            try:
                html_pages = await self.searcher.search(query, pages=pages)
                for html in html_pages:
                    parsed = ResultParser.parse_google_results(html)
                    all_results.extend(parsed)
            except Exception as e:
                logger.error(f"Failed to run query {query}: {e}")
        
        # Deduplicate results by link
        unique_results = {res['link']: res for res in all_results}.values()
        self.results = list(unique_results)
        
        logger.info(f"Scan completed. Found [bold green]{len(self.results)}[/bold green] unique results.")
        return self.results

    def export(self, format='json', output_file=None):
        if not output_file:
            output_file = f"report_{self.target}.{format}"
            
        if format == 'json':
            Reporter.to_json(self.results, output_file)
        elif format == 'csv':
            Reporter.to_csv(self.results, output_file)
        elif format == 'html':
            Reporter.to_html(self.target, self.results, output_file)
        
        logger.info(f"Report saved to: [bold blue]{output_file}[/bold blue]")

    async def close(self):
        await self.searcher.close()
