import logging
import random
import json
import os
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

# Custom Theme for premium look
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "banner": "bold blue",
    "target": "bold cyan",
})

console = Console(theme=custom_theme)

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )
    return logging.getLogger("recondorker")

BANNER = """
[banner]
  _____                     _____             _               
 |  __ \                   |  __ \           | |              
 | |__) |___  ___ ___  _ __| |  | | ___  _ __| | _____ _ __  
 |  _  // _ \/ __/ _ \| '_ \ |  | |/ _ \| '__| |/ / _ \ '__| 
 | | \ \  __/ (_| (_) | | | | |__| | (_) | |  |   <  __/ |    
 |_|  \_\___|\___\___/|_| |_|_____/ \___/|_|  |_|\_\___|_|    
[/banner]
[bold cyan]    Advanced OSINT & Google Dorking Reconnaissance Tool[/bold cyan]
[dim]           Created by Deepmind Antigravity v1.0[/dim]
"""

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def load_dorks():
    config_path = os.path.join(os.path.dirname(__file__), 'data', 'dorks.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[error]Failed to load dorks: {e}[/error]")
        return {"general": ["intitle:index.of"]}
