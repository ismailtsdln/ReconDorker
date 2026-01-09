import click
import asyncio
import sys
import os
import webbrowser
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from .core import ReconDorker
from .utils import BANNER, console, setup_logging, load_dorks

async def run_scan_async(target, queries, pages, format, output, proxies, engines, recursive, open_report):
    recon = ReconDorker(target, proxies=proxies)
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            scan_task = progress.add_task("[cyan]Scanning...", total=len(queries) * len(engines))
            results = await recon.run_scan(
                queries, 
                pages=pages, 
                engines=engines,
                recursive=recursive,
                progress_callback=lambda: progress.update(scan_task, advance=1)
            )
        
        output_file = f"{output}_{target.replace('.', '_')}.{format}"
        recon.export(format=format, output_file=output_file)
        
        console.print(f"\n[success]✨ Scan completed successfully![/success]")
        console.print(f"[info]Total Findings:[/info] [bold green]{len(results)}[/bold green]")
        console.print(f"[info]Report saved to:[/info] [bold blue]{output_file}[/bold blue]")
        
        if open_report:
            report_path = os.path.abspath(output_file)
            webbrowser.open(f"file://{report_path}")
            
        return results
    finally:
        await recon.close()

@click.command()
@click.version_option(version="0.1.0")
@click.option('--target', '-t', required=True, help='Target domain (e.g., example.com)')
@click.option('--pages', '-p', default=1, help='Number of pages to search per dork')
@click.option('--output', '-o', default='report', help='Output filename (without extension)')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html']), default='html', help='Output format')
@click.option('--proxy', default=None, help='Proxy URL (e.g., http://user:pass@host:port)')
@click.option('--proxy-file', help='Path to a file containing a list of proxies (one per line)')
@click.option('--category', '-c', multiple=True, help='Dork categories to run (general, config_files, sensitive_data, leaks, admin_panels)')
@click.option('--engines', '-e', multiple=True, default=['google', 'bing', 'duckduckgo'], help='Search engines to use')
@click.option('--recursive', '-r', is_flag=True, help='Recursively dork discovered subdomains')
@click.option('--open', 'open_report', is_flag=True, help='Automatically open the HTML report after scan')
def main(target, pages, output, format, proxy, proxy_file, category, engines, recursive, open_report):
    """ReconDorker - Advanced OSINT & Google Dorking Tool"""
    console.print(BANNER)
    
    setup_logging()
    
    # Handle proxies
    proxies = None
    if proxy_file:
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        else:
            console.print(f"[error]Proxy file not found: {proxy_file}[/error]")
            return
    elif proxy:
        proxies = {"http://": proxy, "https://": proxy}
    
    dorks_config = load_dorks()
    selected_categories = category if category else dorks_config.keys()
    
    queries = []
    for cat in selected_categories:
        if cat in dorks_config:
            queries.extend(dorks_config[cat])
    
    if not queries:
        console.print("[error]No dorks found for selected categories.[/error]")
        return

    console.print(Panel(f"[info]Target Domain:[/info] [target]{target}[/target]\n"
                        f"[info]Categories:[/info] [highlight]{', '.join(selected_categories)}[/highlight]\n"
                        f"[info]Engines:[/info] [highlight]{', '.join(engines)}[/highlight]\n"
                        f"[info]Recursive:[/info] [highlight]{'Yes' if recursive else 'No'}[/highlight]\n"
                        f"[info]Total Dorks:[/info] [highlight]{len(queries)}[/highlight]",
                        title="Scan Configuration", border_style="blue"))

    try:
        asyncio.run(run_scan_async(target, queries, pages, format, output, proxies, list(engines), recursive, open_report))
    except KeyboardInterrupt:
        console.print("\n[error]Scan interrupted by user.[/error]")
    except Exception as e:
        console.print(f"\n[error]Critical Error: {e}[/error]")

if __name__ == '__main__':
    main()
