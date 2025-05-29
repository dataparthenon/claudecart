# 🛒 ClaudeCart

ClaudeCart is a multimodal, agent-based retail assistant that uses Claude + MCP to provide intelligent shopping assistance. The application routes user queries between SQL-based inventory lookup and RAG-based product discovery. It runs as a Streamlit Cloud application with product information management capabilities.

## Features

- **Intelligent Chat Interface**: Conversational assistant powered by Claude AI models
- **Price Matching**: Scrape external product information and analyze competitor pricing
- **Product Database**: Sample product data with detailed specifications across categories
- **Policy Information**: Store policies for returns, warranty, shipping, and price matching

## Tech Stack

- **Frontend**: Streamlit for interactive UI
- **AI**: Anthropic's Claude models via their Python SDK
- **Web Scraping**: Firecrawl for product information retrieval
- **Search**: Tavily for competitive price searching
- **Observability**: Arize and OpenInference for tracing

## Setup and Run

```bash
# Development environment setup
./dev.sh

# Or manually:
uv venv
uv pip install -e .
source .venv/bin/activate
streamlit run app.py
```

## Project Structure

- `/app.py` - Main Streamlit application entry point
- `/src/claudecart/` - Core application code
  - `/backend/` - Claude controller logic
  - `/database/` - Database managers (SQLite and vector store)
  - `/mcp_tools/` - Model control protocol tools for Claude
  - `/utils/` - Utility functions and external API clients
- `/data/` - Sample product and policy data
- `/mcp_schemas/` - JSON schemas for MCP tools

## To-Do

- **Database Implementation**:
  - Complete SQLite manager for product database
  - Implement vector store for semantic search
- **MCP Tool Enhancements**: 
  - Implement inventory tools
  - Complete search tool functionality
  - Fix the Tavily client import in search_tools.py
- **Claude Controller Updates**:
  - Add full MCP tool registration and routing
  - Implement structured tool responses
- **Additional Features**:
  - User account functionality
  - Shopping cart persistence
  - Order history tracking
  - Product recommendations
  - Complete price matching implementation
