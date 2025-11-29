# 🎁 Gift Recommendation Agent System

An intelligent gift recommendation system powered by **Google ADK (Agentic Development Kit)** and **ChromaDB** vector database. This system uses AI agents to understand natural language queries and provide personalized gift recommendations from the Amazon product dataset.

## 🌟 Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Query (Natural Language)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Google ADK Agent System                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Simple Gift Agent (Single Agent)                        │  │
│  │  - Understands natural language                          │  │
│  │  - Routes to appropriate tools                           │  │
│  │  - Gemini 2.0 Flash Exp                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                          OR                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Multi-Agent System (Complex Queries)                    │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Parallel Research Coordinator                     │  │  │
│  │  │  ├─ Gift Search Agent                              │  │  │
│  │  │  └─ Budget Advisor Agent                           │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │                      ▼                                       │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Occasion Specialist Agent                         │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Gift Recommendation Tools                     │
│  • search_gifts_by_criteria()                                   │
│  • find_budget_friendly_gifts()                                 │
│  • find_premium_gifts()                                         │
│  • get_gift_recommendations_by_occasion()                       │
│  • get_gift_recommendations_by_age()                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              ChromaDB Vector Database                            │
│  • 1,464+ Amazon Products                                        │
│  • Semantic Embeddings (all-MiniLM-L6-v2)                       │
│  • Metadata: price, rating, discount, category                  │
│  • Vector Similarity Search                                      │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Agent Roles

### 1. **Simple Gift Agent** (Recommended)
- Single intelligent agent using Gemini 2.0 Flash Exp
- Understands natural language queries
- Access to all tools
- Best for straightforward queries

### 2. **Multi-Agent System** (Complex Queries)

#### **Gift Search Agent**
- Handles general gift searches
- Processes budget, occasion, age criteria
- Extracts user requirements from queries

#### **Budget Advisor Agent**
- Specializes in budget optimization
- Finds deals and high-discount items
- Recommends premium options

#### **Occasion Specialist Agent**
- Focuses on occasion-specific gifts
- Age-appropriate recommendations
- Contextual understanding of events

#### **Gift Research Coordinator** (Parallel)
- Runs Search + Budget agents simultaneously
- Faster response times
- Comprehensive analysis

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install google-adk chromadb pandas fastmcp

# Or use requirements.txt
pip install -r requirements.txt
```

### Test the Agent System

```bash
python test_gift_agent.py
```

### Run FastMCP Server

```bash
python gift_mcp_server.py
```

## 💡 Usage Examples

### Example 1: Simple Agent (Natural Language)

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from gift_agent.agent import simple_gift_agent
import asyncio

async def ask_gift_agent():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        state={}, app_name='gift_app', user_id='user1'
    )
    
    runner = Runner(
        app_name='gift_app',
        agent=simple_gift_agent,
        session_service=session_service
    )
    
    query = "Find me a birthday gift for a teenager, budget 1000 rupees"
    content = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    
    async for event in runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content
    ):
        if hasattr(event, 'content'):
            for part in event.content.parts:
                if hasattr(part, 'text'):
                    print(part.text)

asyncio.run(ask_gift_agent())
```

### Example 2: Direct Tool Usage

```python
from gift_agent.agent import search_gifts_by_criteria, initialize_gift_database

# Initialize database first
initialize_gift_database()

# Search for gifts
results = search_gifts_by_criteria(
    budget=2000,
    occasion="anniversary",
    age_group="adult",
    min_rating=4.2,
    min_discount=25,
    num_results=5
)

print(results)
```

### Example 3: FastMCP Server

Once the server is running, you can use it via MCP protocol:

```python
# Using smart_gift_assistant tool
response = await client.call_tool(
    "smart_gift_assistant",
    user_query="I need premium gifts for wedding, budget 5000"
)
```

## 🛠️ Available Tools

### Core Tools

1. **initialize_gift_database()**
   - Sets up ChromaDB with Amazon products
   - Must be called before using other tools

2. **search_gifts_by_criteria()**
   - Multi-criteria search
   - Parameters: budget, occasion, age_group, min_rating, min_discount, num_results

3. **find_budget_friendly_gifts()**
   - High-discount deals
   - Parameters: max_budget, min_discount

4. **find_premium_gifts()**
   - Premium quality items
   - Parameters: min_budget, occasion

5. **get_gift_recommendations_by_occasion()**
   - Occasion-specific gifts
   - Parameters: occasion, budget

6. **get_gift_recommendations_by_age()**
   - Age-appropriate gifts
   - Parameters: age_group, budget

## 📊 Natural Language Query Examples

The agent understands queries like:

```
✅ "I need a birthday gift for a teenager, budget 1000 rupees"
✅ "Find me budget-friendly gifts with high discounts under 500"
✅ "Show premium anniversary gifts around 5000"
✅ "What are good graduation gifts for adults?"
✅ "I want festive gifts with at least 40% discount"
✅ "Suggest wedding gifts for a couple, budget 3000-4000"
```

## 🎯 Agent Selection Guide

| Query Type | Recommended Agent | Why |
|------------|------------------|-----|
| Simple searches | Simple Gift Agent | Faster, direct tool access |
| "Find gifts under X" | Simple Gift Agent | Single-step query |
| Complex requirements | Multi-Agent System | Parallel processing |
| "Compare budget vs premium" | Multi-Agent System | Needs multiple perspectives |
| Occasion + Age + Budget | Multi-Agent System | Comprehensive analysis |

## 📁 File Structure

```
HarvestHack-Workshop/
├── gift_agent/
│   ├── __init__.py              # Package initialization
│   └── agent.py                 # Agent definitions and tools
├── gift_recommender.py          # ChromaDB recommendation engine
├── gift_mcp_server.py           # FastMCP server
├── test_gift_agent.py           # Test suite
├── GIFT_AGENT_README.md         # This file
└── amazon.csv                   # Product dataset
```

## 🔧 Customization

### Add New Tools

```python
def custom_gift_tool(param: str) -> str:
    """Your custom logic"""
    # Access the global recommender
    global _gift_recommender
    # Your implementation
    return results

# Add to agent
custom_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    tools=[custom_gift_tool, ...],
    # ...
)
```

### Modify Agent Instructions

Edit the `instruction` parameter in agent definitions to change behavior:

```python
simple_gift_agent = LlmAgent(
    instruction="""Your custom instructions here...""",
    # ...
)
```

## 🧪 Testing

Run the test suite:

```bash
python test_gift_agent.py
```

Tests include:
- Simple agent with natural language
- Multi-agent system with complex queries
- All tool functionality

## 🚀 Deployment

### As FastMCP Server

```bash
# Production mode
python gift_mcp_server.py
```

### Integration with Existing Systems

```python
from gift_agent.agent import simple_gift_agent
# Integrate with your ADK application
```

## 📈 Performance

- **Database Size**: 1,464 products
- **Embedding Model**: all-MiniLM-L6-v2
- **LLM**: Gemini 2.0 Flash Exp
- **Average Query Time**: 2-5 seconds (includes embedding search + LLM)
- **Vector Search**: < 100ms

## 🤝 Contributing

Enhance the system by:
- Adding more specialized agents
- Improving query understanding
- Expanding tool capabilities
- Optimizing search algorithms

## 📝 License

Educational project for HarvestHack Workshop.

---

**Happy Gift Finding with AI Agents! 🎁🤖✨**
