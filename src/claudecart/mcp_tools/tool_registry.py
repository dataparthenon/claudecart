from typing import Any, Callable, Dict, List
from .search_tools import search_competitor_prices, get_price_match_policy

class ToolRegistry:
    """
    Central registry for all MCP tools used by Claude.
    
    This class manages the registration and execution of tools that can be 
    called by Claude through the Model Control Protocol (MCP). It provides
    a centralized way to dispatch tool calls to their implementations.
    """
    
    def __init__(self):
        """
        Initialize the tool registry with available tools.
        """
        self.tools: Dict[str, Callable] = {
            "search_competitor_prices": search_competitor_prices,
            "get_price_match_policy": get_price_match_policy,
        }
    
    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a tool by name with the provided input parameters.
        
        Args:
            tool_name: Name of the tool to execute
            tool_input: Dictionary of parameters to pass to the tool
            
        Returns:
            Result of the tool execution or error information
        """
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            return self.tools[tool_name](**tool_input)
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def get_available_tools(self) -> List[str]:
        """
        Get list of all available tool names.
        
        Returns:
            List of registered tool names
        """
        return list(self.tools.keys())
    
    def register_tool(self, name: str, function: Callable) -> None:
        """
        Register a new tool with the registry.
        
        Args:
            name: Name to register the tool under
            function: Callable that implements the tool
        """
        self.tools[name] = function

# Global registry instance
tool_registry = ToolRegistry()