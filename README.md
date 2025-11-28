# HarvestHack-Workshop
This repository contains the resources and other tools for the workshop session during HarvestHack. It will cover topics mainly about agentic AI development via Google ADK, MCP, and other relevant technologies. 

Google Agent Development Kit - 
https://google.github.io/adk-docs/

Fast MCP - 
https://gofastmcp.com/getting-started/welcome

---

# Multi-Agent Research Assistant Demo

A workshop demonstration of multi-agent systems using **Google ADK** and **MCP (Model Context Protocol)**.

## 🎯 Overview

This demo showcases a multi-agent research system where different AI agents collaborate to:
1. **Research Agent**: Gathers information using custom tools
2. **Summarizer Agent**: Analyzes and synthesizes findings
3. **Coordinator Agent**: Orchestrates the workflow using Sequential execution

## 📁 Project Structure

```
HarvestHack-Workshop/
├── research_agent/
│   ├── __init__.py
│   └── agent.py           # Multi-agent definitions with tools
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
└── README.md             # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip for installing packages
- Google API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 1. Create Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- `google-adk` - Google Agent Development Kit (latest version)
- `python-dotenv` - Environment variable management
- `mcp` - Model Context Protocol library

### 3. Configure Environment Variables

Edit the `.env` file and add your Google API key:

```
GOOGLE_API_KEY="your_actual_google_api_key_here"
```

**Get your API key from:** https://aistudio.google.com/app/apikey

## 🎮 Running the Demo

### Run with ADK Web Interface

The primary way to run this demo is using the ADK web interface:

```bash
# Make sure you're in the project root directory
adk web
```

This will:
1. Start the ADK web server (typically at http://localhost:8000)
2. Open your browser automatically
3. Show all available agents in the dropdown

### Using the Web Interface

1. **Select Agent**: Choose `research_coordinator` from the dropdown
2. **Enter Query**: Try queries like:
   - "Research artificial intelligence in healthcare"
   - "Tell me about quantum computing"
   - "What is machine learning and its applications?"
3. **Watch the Workflow**: See agents collaborate in real-time

### Run with CLI (Alternative)

You can also run agents via command line:

```bash
adk run research_agent
```

## 🔧 How It Works

### Agent Architecture

```
User Query
    ↓
Coordinator (SequentialAgent)
    ↓
Research Agent → Uses search_topic() & get_topic_facts()
    ↓
Summarizer Agent → Uses analyze_sentiment()
    ↓
Final Response to User
```

### Available Tools

1. **search_topic(query, max_results)**
   - Searches for information on topics
   - Returns formatted search results
   
2. **get_topic_facts(topic)**
   - Retrieves key facts about topics
   - Returns bullet-pointed facts

3. **analyze_sentiment(text)**
   - Analyzes sentiment of text
   - Returns positive/negative/neutral assessment

## 🎓 Workshop Learning Points

1. **Multi-Agent Architecture**: How to structure collaborative AI agents using ADK
2. **Google ADK Integration**: Using LlmAgent and SequentialAgent
3. **Tool Integration**: Creating and using custom function tools
4. **Agent Orchestration**: Coordinating workflows between specialized agents
5. **System Instructions**: Crafting effective agent personas and roles
6. **ADK Web Interface**: Using the built-in web UI for testing

## 🛠️ Extending the Demo

### Add More Agents

```python
new_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    name='new_agent',
    description='Your agent description',
    instruction='Your agent instructions',
    tools=[your_tools],
)
```

### Add Custom Tools

```python
def your_custom_tool(param: str) -> str:
    """Tool description"""
    # Your implementation
    return result
```

### Use MCP Servers

To integrate external MCP servers:

```python
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', '/path/to/folder'],
        ),
    ),
)
```

## 📚 Resources

- **Google ADK Docs**: https://google.github.io/adk-docs/
- **ADK Python Quickstart**: https://google.github.io/adk-docs/get-started/python/
- **MCP Documentation**: https://modelcontextprotocol.io/
- **MCP Tools in ADK**: https://google.github.io/adk-docs/tools-custom/mcp-tools/
- **Gemini API**: https://ai.google.dev/

## 🐛 Troubleshooting

**API Key Error**: 
- Ensure your `.env` file has the correct Google API key
- Make sure the `.env` file is in the project root directory

**Import Errors**: 
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're using Python 3.10 or higher

**ADK Command Not Found**:
- Make sure you've activated your virtual environment
- Reinstall google-adk: `pip install google-adk`

**Agent Not Showing in Web UI**:
- Ensure `__init__.py` exists in the `research_agent/` directory
- Check that you're running `adk web` from the project root (parent of `research_agent/`)

## 🎉 Next Steps

After the workshop, try:
- Adding more specialized agents (fact-checker, translator, etc.)
- Integrating real MCP servers (filesystem, Google Maps, etc.)
- Building custom MCP tools
- Implementing agent memory and state management
- Deploying to Cloud Run or Vertex AI Agent Engine
- Creating parallel agent workflows using `ParallelAgent`

## 📝 Additional Notes

### Agent Types in ADK

- **LlmAgent**: Single AI agent with tools
- **SequentialAgent**: Executes agents in sequence
- **ParallelAgent**: Executes agents in parallel
- **LoopAgent**: Executes agents in a loop

### Models Available

- `gemini-2.0-flash-exp` - Latest experimental Flash model
- `gemini-2.0-flash` - Stable Flash model
- `gemini-1.5-pro` - Pro model for complex tasks

---

**Workshop Created For**: HarvestHack 2025
**Technology Stack**: Google ADK, Python, MCP
**License**: Educational Use
