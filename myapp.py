import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Print Python executable path to debug environment issues
st.sidebar.info(f"Using Python: {sys.executable}")

# Import LLM
from langchain_groq import ChatGroq

# Import utilities and tools
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper, GoogleSearchAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
# Fixed import for GoogleSearchRun
from langchain_community.tools.google_search.tool import GoogleSearchRun

# Import agent components
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Import decorator for custom tools
from langchain.tools import tool

# For chat history and memory
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()

## Arxiv and wikipedia Tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# Set up Google Search
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Create a single search tool - either Google Search or a placeholder
if GOOGLE_API_KEY and GOOGLE_CSE_ID:
    search_wrapper = GoogleSearchAPIWrapper(google_api_key=GOOGLE_API_KEY, google_cse_id=GOOGLE_CSE_ID)
    search = GoogleSearchRun(api_wrapper=search_wrapper)
    st.sidebar.success("✅ Google Search API configured")
else:
    # Fallback to placeholder search tool if API keys are missing
    @tool
    def search(query: str) -> str:
        """Search the web for the given query and return relevant results."""
        return f"Here are search results for: {query} (Note: This is a placeholder. Add Google API keys to enable real search)"
    st.sidebar.warning("⚠️ Using placeholder search tool - add Google API keys for real search")


st.title("🔎 LangChain - Chat with search")
st.markdown("""
This app demonstrates a conversational agent that can search the web, Wikipedia, and Arxiv.
It uses LangChain with Groq LLM to create a powerful search experience with memory.
""")

## Sidebar for settings
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Add more settings
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
model_name = st.sidebar.selectbox("Model", ["Llama3-8b-8192", "Mixtral-8x7b-32768", "Gemma-7b-it"], index=0)

# Add a button to clear chat history
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    st.experimental_rerun()

# Initialize conversation memory if not already done
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize message history if not already done
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm an AI research assistant. I can search the web, Wikipedia, and arXiv to help answer your questions. What would you like to know?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input(placeholder="Ask me anything..."):
    # Don't process empty inputs
    if not prompt.strip():
        st.stop()
        
    # Validate API key
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
        st.stop()
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Set up the LLM with user-selected parameters
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        streaming=True
    )
    # Create the tools list
    tools = [search, arxiv, wiki]
    
    # Create the agent with memory
    memory = st.session_state.memory
    
    # Display assistant message with spinner while processing
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Create a callback handler to display agent thoughts
            st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            
            # Create the agent
            search_agent = initialize_agent(
                tools,
                llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                memory=memory,
                handle_parsing_errors=True
            )
            
            # Run the agent and get the response
            try:
                response = search_agent.run(input=prompt, callbacks=[st_callback])
                
                # Add the response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Display the final answer
                st.markdown(response)
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": f"I encountered an error: {error_msg}"})
    
    # Store the updated conversation in memory
    memory.chat_memory.add_user_message(prompt)
    memory.chat_memory.add_ai_message(response)

