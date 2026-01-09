from bs4 import BeautifulSoup
from .errors import ParsingError

class ResultParser:
    @staticmethod
    def parse_google_results(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        for g in soup.select('div.g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title_elem = g.find('h3')
                title = title_elem.text if title_elem else "No Title"
                snippet_elem = g.select_one('div.VwiC3b')
                snippet = snippet_elem.text if snippet_elem else ""
                if link.startswith('/url?q='):
                    link = link.split('/url?q=')[1].split('&')[0]
                if link.startswith('http'):
                    results.append({"title": title, "link": link, "snippet": snippet, "source": "Google"})
        return results

    @staticmethod
    def parse_bing_results(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        for li in soup.select('li.b_algo'):
            anchor = li.find('a')
            if anchor and anchor.get('href'):
                link = anchor['href']
                title = anchor.text
                snippet_elem = li.select_one('div.b_caption p') or li.select_one('div.b_snippet')
                snippet = snippet_elem.text if snippet_elem else ""
                if link.startswith('http'):
                    results.append({"title": title, "link": link, "snippet": snippet, "source": "Bing"})
        return results
    @staticmethod
    def parse_duckduckgo_results(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        for result in soup.select('div.result'):
            anchor = result.select_one('a.result__a')
            if anchor and anchor.get('href'):
                link = anchor['href']
                title = anchor.text
                snippet_elem = result.select_one('a.result__snippet')
                snippet = snippet_elem.text if snippet_elem else ""
                # DDG sometimes uses proxy links, but html version is usually direct
                if link.startswith('http'):
                    results.append({"title": title, "link": link, "snippet": snippet, "source": "DuckDuckGo"})
        return results
