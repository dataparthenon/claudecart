from typing import List, Dict, Any, Optional

from tavily import TavilyClient


class TavilySearchClient:
    """
    Client for interacting with Tavily search API for product information.
    
    This class provides a wrapper around the Tavily API client to simplify
    searching for product information and competitor pricing.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Tavily search client.
        
        Args:
            api_key: API key for authenticating with Tavily
        """
        self.client = TavilyClient(api_key=api_key)
    
    def search_product(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for product information using Tavily.
        
        This method performs a web search using Tavily's API to find
        information about products, including pricing and availability.
        
        Args:
            query: Search query string for the product
            max_results: Maximum number of results to return
            
        Returns:
            List of search results containing product information
        """
        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=max_results
            )
            return response.get("results", [])
        except Exception as e:
            return []
