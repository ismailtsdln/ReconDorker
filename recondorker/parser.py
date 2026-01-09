from bs4 import BeautifulSoup
from .errors import ParsingError

class ResultParser:
    @staticmethod
    def parse_google_results(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # Google search result blocks are usually in 'div.g'
        for g in soup.select('div.g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title_elem = g.find('h3')
                title = title_elem.text if title_elem else "No Title"
                
                # Snippet is usually in div.VwiC3b or similar
                snippet_elem = g.select_one('div.VwiC3b')
                snippet = snippet_elem.text if snippet_elem else ""
                
                if link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                
                if link.startswith('http'):
                    results.append({
                        "title": title,
                        "link": link,
                        "snippet": snippet
                    })
        
        return results
