# AI Search Engine with LangChain

This Streamlit application integrates multiple search sources (Google, Wikipedia, and ArXiv) with a LLM-powered conversational interface using LangChain and Groq LLM.

![Search Engine Demo](https://via.placeholder.com/800x400?text=AI+Search+Engine+Demo)

## Features

- 🔍 **Multi-source search**: Query Google, Wikipedia, and ArXiv academic papers
- 💬 **Conversational interface**: Chat-like experience with memory of previous interactions
- 🤖 **AI-powered responses**: Uses Groq's powerful language models to generate human-like responses
- ⚙️ **Customizable settings**: Adjust temperature and select different models
- 📝 **Chat history management**: Save, export, and clear conversation history
- 📊 **Performance insights**: View response time and model details
- 🔒 **Error handling**: Robust error handling and prevention of concurrent requests

## Requirements

- Python 3.8+
- Groq API key
- Google API key and Custom Search Engine ID (for Google Search functionality)

## Installation

1. Clone the repository or navigate to the project directory:

```bash
cd "d:\Desktop\GenAI\LangChain\5-Search Engine"
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_google_custom_search_engine_id_here
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run myapp.py
```

2. Enter your Groq API key in the sidebar settings if not already provided in the `.env` file.

3. Adjust the temperature and select your preferred model from the sidebar.

4. Start chatting! Ask questions about any topic, and the AI will search the web, Wikipedia, and ArXiv to provide informative answers.

5. Use the chat management options in the sidebar:
   - "Clear Chat History" to start a fresh conversation
   - "Export Chat History" to save your conversation as a JSON file

6. View performance metrics and response details by expanding the "Response Details" section after each answer.

## How It Works

This application uses LangChain's agent framework to:

1. Process user queries using Groq's language models
2. Determine which search tools (Google, Wikipedia, ArXiv) to use for each query
3. Execute searches and gather information from different sources
4. Synthesize the information into a coherent, human-like response
5. Maintain conversation context through memory mechanisms

The agent utilizes a ZERO_SHOT_REACT_DESCRIPTION approach, which allows it to reason through the steps needed to answer a query without requiring specific examples.

## Troubleshooting

- **Missing Google Search Results**: Ensure you've added valid Google API key and Custom Search Engine ID in the `.env` file or sidebar.
- **Memory Issues**: If the conversation seems to forget context, try adjusting the memory settings or clear the chat history to start fresh.
- **Performance**: If responses are slow, try using a smaller model like "Llama3-8b-8192" which offers a good balance of speed and quality.
- **Concurrent Requests**: The app prevents multiple concurrent requests to avoid confusion. If you see a "Please wait" message, let the current request complete.
- **Export Errors**: If you can't export chat history, ensure you have at least one exchange in the conversation.

## License

This project is provided as an educational resource and is available under the MIT License.

## Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the framework
- [Groq](https://groq.com/) for the LLM API
- [Streamlit](https://streamlit.io/) for the web interface
