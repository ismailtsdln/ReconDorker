import click
import asyncio
import sys
from .core import ReconDorker
from .utils import BANNER, console, setup_logging

DEFAULT_DORKS = [
    "intitle:index.of",
    "ext:php",
    "ext:log",
    "ext:sql",
    "ext:env",
    "inurl:admin",
    "inurl:login",
    "ext:pdf",
    "ext:txt"
]

@click.command()
@click.option('--target', '-t', required=True, help='Target domain (e.g., example.com)')
@click.option('--pages', '-p', default=1, help='Number of pages to search per dork')
@click.option('--output', '-o', default='report', help='Output filename (without extension)')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html']), default='json', help='Output format')
@click.option('--proxy', default=None, help='Proxy URL (e.g., http://user:pass@host:port)')
def main(target, pages, output, format, proxy):
    """ReconDorker - OSINT & Google Dorking Tool"""
    console.print(BANNER)
    
    setup_logging()
    
    proxies = {"http://": proxy, "https://": proxy} if proxy else None
    
    recon = ReconDorker(target, proxies=proxies)
    
    try:
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(recon.run_scan(DEFAULT_DORKS, pages=pages))
        
        output_file = f"{output}.{format}"
        recon.export(format=format, output_file=output_file)
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Scan interrupted by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
    finally:
        loop.run_until_complete(recon.close())

if __name__ == '__main__':
    main()
