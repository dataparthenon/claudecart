import json
import os
from typing import List, Dict, Any, Optional

import streamlit as st


class TavilySearchClient:
    """Client for interacting with Tavily search API."""

    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)
    
    def search_product(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for product information using Tavily.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
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


def search_competitor_prices(
    product_name: str,
    retailers: Optional[List[str]] = ["Target", "Walmart", "BestBuy"], 
    brand: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search for product prices at competitor retailers.
    
    Args:
        product_name: Name of the product to search for
        retailers: List of retailer names to search
        brand: Optional product brand/manufacturer to narrow search
        
    Returns:
        List of search results from retailers with price information
    """
    tavily_client = TavilySearchClient(api_key=st.secrets["secrets"]["TAVILY_API_KEY"])
    results = []
    
    for retailer in retailers:
        query = f"{product_name} {retailer}"
        if brand:
            query = f"{brand} {query}"
            
        result = tavily_client.search_product(query=query)
        results.append(result)
        
    return results
    
    
def get_price_match_policy(retailer: str) -> Dict[str, Any]:
    """
    Get price matching policy for a specific retailer.
    
    Args:
        retailer: Retailer name to get policy for
        
    Returns:
        Dictionary containing price match policy details
    """
    try:
        # Load policy data from JSON file
        with open("data/sample_policies.json", "r") as f:
            policies = json.load(f)
            
        # Return price match policy if available
        if "policies" in policies and "price_match" in policies["policies"]:
            return policies["policies"]["price_match"]
    except:
        pass
        
    # Return default policy if not found or error occurs
    return {
        "title": "Price Match Guarantee",
        "content": "We'll match the price of identical items found at major competitors.",
        "details": {
            "time_limit": "Must be requested at time of purchase",
            "conditions": [
                "Item must be identical (same model, brand, specifications)",
                "Competitor must be authorized retailer"
            ],
            "exceptions": [
                "Marketplace sellers",
                "Clearance or limited-time offers"
            ]
        }
    }