import logging
import random
from rich.console import Console
from rich.logging import RichHandler

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger("recondorker")

console = Console()

BANNER = """
[bold blue]
  _____                     _____             _               
 |  __ \                   |  __ \           | |              
 | |__) |___  ___ ___  _ __| |  | | ___  _ __| | _____ _ __  
 |  _  // _ \/ __/ _ \| '_ \ |  | |/ _ \| '__| |/ / _ \ '__| 
 | | \ \  __/ (_| (_) | | | | |__| | (_) | |  |   <  __/ |    
 |_|  \_\___|\___\___/|_| |_|_____/ \___/|_|  |_|\_\___|_|    
[/bold blue]
[bold cyan]    OSINT & Google Dorking Reconnaissance Tool[/bold cyan]
"""

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    return random.choice(user_agents)
