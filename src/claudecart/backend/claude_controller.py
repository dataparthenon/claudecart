import json
import uuid
from typing import Any, Dict, List, Optional

from anthropic import Anthropic

from claudecart.mcp_tools.search_tools import search_competitor_prices, get_price_match_policy
from claudecart.mcp_tools.tool_registry import tool_registry


class ClaudeController:
    """
    Controller for Claude model integration in ClaudeCart retail assistant.
    
    This class handles communication with Anthropic's Claude API, manages
    chat conversations, and provides access to MCP tools for enhanced
    product search and price matching capabilities.
    """
    
    def __init__(
        self,
        api_key: str,
        model_name: str = "claude-3-7-sonnet-latest",
    ) -> None:
        """
        Initialize the Claude controller.
        
        Args:
            api_key: Anthropic API key for authentication
            model_name: Name of the Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model_name = model_name

        # Load tool definitions from schema file
        try:
            with open("mcp_schemas/tools.json", "r") as f:
                self.tool_definitions = json.load(f)["tools"]
        except FileNotFoundError:
            self.tool_definitions = []  # No tools available
        
        # Enhanced system prompt for tool usage
        self.system_prompt = """You are ClaudeCart's price matching assistant.

        When analyzing product information, use these tools:
        1. get_price_match_policy - Check which competitors are allowed for price matching
        2. search_competitor_prices - Search for the product at competitor retailers

        Extract product details from the provided content, then search for competitor prices and provide clear recommendations."""

    def update_model(
        self,
        model_name: str
    ) -> None:
        """
        Update the Claude model being used.
        
        Args:
            model_name: New model name to use for Claude API calls
        """
        self.model_name = model_name
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send messages to Claude and get a response.
        
        This method handles the communication with Claude's API, including
        error handling and response formatting.
        
        Args:
            messages: List of message objects with role and content
            session_id: Optional session identifier for tracking conversations
            
        Returns:
            Dictionary with response content and metadata
        """
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=self.system_prompt,
                messages=messages
            )
            
            return {
                "content": response.content[0].text,
                "success": True,
                "session_id": session_id,
                "model": self.model_name,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        except Exception as e:
            return {
                "content": f"I apologize, but I encountered an error: {str(e)}",
                "success": False,
                "session_id": session_id,
                "error": str(e)
            }
    
    def get_conversation_starter(self) -> str:
        """
        Get a friendly conversation starter for the UI.
        
        Returns:
            Formatted conversation starter message
        """
        return """👋 Hi! I'm ClaudeCart, your intelligent shopping assistant. 
        I can help you with:
        • General product questions and recommendations
        • Shopping advice and comparisons  
        • Store policy information

        🚧 **Coming Soon**: Real-time inventory checks and advanced product search!

        What can I help you with today?"""

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specified MCP tool.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Parameters to pass to the tool
            
        Returns:
            Tool execution results or error information
        """
        # Use tool registry to execute the tool
        return tool_registry.execute_tool(tool_name, tool_input)