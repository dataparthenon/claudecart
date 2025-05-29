import uuid
from datetime import datetime

import streamlit as st
from arize.otel import register
from openinference.instrumentation.anthropic import AnthropicInstrumentor

from claudecart.backend import ClaudeController
from claudecart.utils.firecrawl_scraper import scrape_web_page


def init_tracing():
    """Initialize tracing for monitoring Claude interactions."""
    if "tracing_initialized" not in st.session_state:
        _tracer_provider = register(
            space_id=st.secrets["secrets"]["ARIZE_SPACE_ID"],
            api_key=st.secrets["secrets"]["ARIZE_API_KEY"],
            project_name="claude-cart",
        )
        AnthropicInstrumentor().instrument(tracer_provider=_tracer_provider)
        st.session_state.tracing_initialized = True


def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())


@st.cache_resource
def get_claude_controller(api_key: str, model_name: str):
    """Create and cache Claude controller instance."""
    return ClaudeController(api_key=api_key, model_name=model_name)


def setup_ui():
    """Configure the Streamlit UI layout."""
    st.set_page_config(
        page_title="ClaudeCart",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def create_sidebar(claude_controller):
    """Create sidebar with model selection and price match tool."""
    model_name = st.sidebar.selectbox(
        "Claude",
        options=[
            "claude-opus-4-0",
            "claude-sonnet-4-0",
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-5-haiku-latest",
            "claude-3-opus-latest",
        ],
        index=2
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Price Match Assistant")

    product_url = st.sidebar.text_input(
        "Product URL",
        placeholder="https://www.bestbuy.com/site/product...",
        help="Paste a product link to check competitor prices"
    )

    if st.sidebar.button("Check Price Match", type="primary"):
        handle_price_match(product_url, claude_controller)
    
    return model_name


def handle_price_match(product_url, claude_controller):
    """Process a price match request for a product URL."""
    if not product_url:
        st.sidebar.error("Please enter a product URL first")
        return
        
    with st.sidebar:
        with st.spinner("Scraping product information..."):
            scrape_result = scrape_web_page(
                product_url, 
                st.secrets["secrets"]["FIRECRAWL_API_KEY"]
            )
                    
            # Create message with scraped content
            scraped_content = str(scrape_result.markdown)
            
            # Add price match message to chat
            st.session_state.messages.append({
                "role": "user", 
                "content": f"Can you analyze this product for price matching? I found this information from {product_url}:\n\n{scraped_content[:1000]}..."
            })

            response = claude_controller.chat(
                messages=st.session_state.messages,
            )
                    
            if response["success"]:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response["content"]
                })
                st.success("Product analyzed! Check the chat.")
            else:
                st.error(f"Error from Claude: {response.get('error')}")
                    
            st.rerun()


def display_chat_ui(claude_controller):
    """Display the main chat interface."""
    st.title("🛒 ClaudeCart")
    st.markdown("""ClaudeCart is a multimodal, agent-based retail assistant 
                that uses Claude + MCP to route user queries between SQL-based
                inventory lookup and RAG-based product discovery.
                It runs as a Streamlit Cloud application with an embedded vector store 
                and a lightweight SQLite product database.""")

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    query = st.chat_input("Ask a question...")

    if query and claude_controller:
        handle_user_query(query, claude_controller)
    elif query and not claude_controller:
        st.error("ClaudeCart is not properly initialized. Please check your configuration.")


def handle_user_query(query, claude_controller):
    """Process a user query and display the response."""
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = claude_controller.chat(
                messages=st.session_state.messages,
            )
            if response["success"]:
                # Display the response
                st.markdown(response["content"])
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response["content"]
                })
            else:
                error_msg = f"Error: {response['error']}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })


def display_debug_info(model_name, claude_controller):
    """Display debugging information in an expander."""
    with st.expander("Debug Information"):
        st.write("Session ID:", st.session_state.session_id)
        st.write("Model:", model_name)
        st.write("Current Time:", datetime.now().isoformat())
        if claude_controller:
            st.write("ClaudeCart: Initialized")
            st.write("Available Tools:", claude_controller.tool_definitions)
        else:
            st.write("ClaudeCart: Not initialized")


def main():
    """Main application entry point."""
    # Setup
    init_tracing()
    setup_ui()
    init_session_state()

    claude_controller = get_claude_controller(
        st.secrets["secrets"]["ANTHROPIC_API_KEY"],
        "claude-3-7-sonnet-latest"  # Default model
    )

    model_name = create_sidebar(claude_controller)
     
    # Initialize Claude controller with selected model
    claude_controller = get_claude_controller(
        st.secrets["secrets"]["ANTHROPIC_API_KEY"],
        model_name
    )
    
    # Display main chat interface
    display_chat_ui(claude_controller)
    
    # Display debug information
    display_debug_info(model_name, claude_controller)
    
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit, Anthropic Claude, and LanceDB")


if __name__ == "__main__":
    main()