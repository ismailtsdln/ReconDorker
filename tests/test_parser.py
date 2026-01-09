import pytest
import asyncio
from recondorker.parser import ResultParser

def test_parse_google_results():
    mock_html = """
    <div class="g">
        <a href="/url?q=https://example.com/target&sa=U"><h3>Example Title</h3></a>
        <div class="VwiC3b">Example snippet for the result.</div>
    </div>
    """
    results = ResultParser.parse_google_results(mock_html)
    assert len(results) == 1
    assert results[0]['link'] == 'https://example.com/target'
    assert results[0]['title'] == 'Example Title'
    assert 'snippet' in results[0]

def test_parse_no_results():
    results = ResultParser.parse_google_results("<html><body>No results</body></html>")
    assert len(results) == 0
