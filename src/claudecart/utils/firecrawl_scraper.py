from typing import Any, Dict

from firecrawl import FirecrawlApp


def scrape_web_page(url: str, firecrawl_api_key: str) -> Dict[str, Any]:
    """
    Scrape content from a web page using Firecrawl.
    
    This function takes a URL and API key, then uses the Firecrawl service
    to extract structured content from the webpage. The content is returned
    in both markdown and HTML formats.
    
    Args:
        url: The URL of the web page to scrape
        firecrawl_api_key: API key for authenticating with Firecrawl
        
    Returns:
        Dictionary containing the scraped content in markdown and HTML formats
    """
    app = FirecrawlApp(api_key=firecrawl_api_key)
    scrape_result = app.scrape_url(url, formats=['markdown', 'html'])
    return scrape_result
