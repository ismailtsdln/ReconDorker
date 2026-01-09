import click
import asyncio
import sys
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from .core import ReconDorker
from .utils import BANNER, console, setup_logging, load_dorks

@click.command()
@click.option('--target', '-t', required=True, help='Target domain (e.g., example.com)')
@click.option('--pages', '-p', default=1, help='Number of pages to search per dork')
@click.option('--output', '-o', default='report', help='Output filename (without extension)')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html']), default='html', help='Output format')
@click.option('--proxy', default=None, help='Proxy URL (e.g., http://user:pass@host:port)')
@click.option('--category', '-c', multiple=True, help='Dork categories to run (general, config_files, sensitive_data, leaks, admin_panels)')
def main(target, pages, output, format, proxy, category):
    """ReconDorker - Advanced OSINT & Google Dorking Tool"""
    console.print(BANNER)
    
    setup_logging()
    
    proxies = {"http://": proxy, "https://": proxy} if proxy else None
    
    dorks_config = load_dorks()
    selected_categories = category if category else dorks_config.keys()
    
    queries = []
    for cat in selected_categories:
        if cat in dorks_config:
            queries.extend(dorks_config[cat])
    
    if not queries:
        console.print("[error]No dorks found for selected categories.[/error]")
        return

    recon = ReconDorker(target, proxies=proxies)
    
    console.print(Panel(f"[info]Starting scan for:[/info] [target]{target}[/target]\n"
                        f"[info]Categories:[/info] [highlight]{', '.join(selected_categories)}[/highlight]\n"
                        f"[info]Total Dorks:[/info] [highlight]{len(queries)}[/highlight]",
                        title="Scan Configuration", border_style="blue"))

    try:
        loop = asyncio.get_event_loop()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            scan_task = progress.add_task("[cyan]Scanning...", total=len(queries))
            results = loop.run_until_complete(recon.run_scan(queries, pages=pages, progress_callback=lambda: progress.update(scan_task, advance=1)))
        
        output_file = f"{output}_{target.replace('.', '_')}.{format}"
        recon.export(format=format, output_file=output_file)
        
        console.print(f"\n[success]✨ Scan completed successfully![/success]")
        console.print(f"[info]Total Findings:[/info] [bold green]{len(results)}[/bold green]")
        console.print(f"[info]Report saved to:[/info] [bold blue]{output_file}[/bold blue]")
        
    except KeyboardInterrupt:
        console.print("\n[error]Scan interrupted by user.[/error]")
    except Exception as e:
        console.print(f"\n[error]Critical Error: {e}[/error]")
    finally:
        loop.run_until_complete(recon.close())

if __name__ == '__main__':
    main()
