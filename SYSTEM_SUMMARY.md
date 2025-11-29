# 🎁 Gift Recommendation Agentic System - Complete Summary

## Project Overview

A sophisticated **AI-powered gift recommendation system** that combines:
- **ChromaDB** vector database for semantic product search
- **Google ADK (Agentic Development Kit)** for intelligent agent orchestration
- **Natural language understanding** for conversational queries
- **1,464 Amazon products** with rich metadata

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACES                           │
│  • Natural Language Queries                                  │
│  • FastMCP Server API                                        │
│  • Direct Tool Calls                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              GOOGLE ADK AGENT LAYER                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Option 1: Simple Gift Agent (Gemini 2.0 Flash)      │  │
│  │  • Single intelligent agent                          │  │
│  │  • All tools available                               │  │
│  │  • Best for direct queries                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                          OR                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Option 2: Multi-Agent System                        │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Parallel Research Coordinator                  │ │  │
│  │  │  • Gift Search Agent                            │ │  │
│  │  │  • Budget Advisor Agent                         │ │  │
│  │  │  (Run simultaneously)                           │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  │                      ↓                                │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │  Occasion Specialist Agent                      │ │  │
│  │  │  (Sequential processing)                        │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              TOOL/FUNCTION LAYER                             │
│  • initialize_gift_database()                                │
│  • search_gifts_by_criteria()                                │
│  • find_budget_friendly_gifts()                              │
│  • find_premium_gifts()                                      │
│  • get_gift_recommendations_by_occasion()                    │
│  • get_gift_recommendations_by_age()                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           ChromaDB VECTOR DATABASE                           │
│  • Embedding Model: all-MiniLM-L6-v2                         │
│  • 1,464 Amazon Products                                     │
│  • Semantic Search with Metadata Filtering                   │
│  • Composite Scoring Algorithm                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Input Criteria

The system accepts multiple gift-finding criteria:

| Criterion | Type | Description | Example |
|-----------|------|-------------|---------|
| **Budget** | Float | Maximum price (₹) | 1000, 5000 |
| **Occasion** | String | Event type | birthday, anniversary, festive |
| **Age Group** | String | Recipient age | kid, teenager, adult, senior |
| **Min Rating** | Float | Minimum rating (0-5) | 4.0, 4.2 |
| **Min Discount** | Float | Minimum discount % | 20, 50 |
| **Num Results** | Integer | Results to return | 5, 10 |

---

## 🤖 Agent Components

### 1. **Simple Gift Agent** (Recommended)
- **Model**: Gemini 2.0 Flash Exp
- **Type**: Single LLM Agent
- **Capabilities**:
  - Natural language understanding
  - Intelligent tool selection
  - Contextual responses
- **Use Cases**: Direct queries, simple searches

### 2. **Multi-Agent System**

#### **Gift Search Agent**
- Handles general searches
- Extracts criteria from queries
- Provides personalized recommendations

#### **Budget Advisor Agent**
- Specializes in value optimization
- Finds deals and discounts
- Premium gift suggestions

#### **Occasion Specialist Agent**
- Occasion-specific recommendations
- Age-appropriate selections
- Contextual understanding

#### **Gift Research Coordinator** (Parallel Agent)
- Coordinates Search + Budget agents
- Runs simultaneously for faster results
- Comprehensive analysis

---

## 🛠️ Core Tools

### 1. `initialize_gift_database()`
**Purpose**: Set up ChromaDB with Amazon products

```python
initialize_gift_database("amazon.csv")
# Returns: "✅ Gift database initialized successfully with 1,464+ products"
```

### 2. `search_gifts_by_criteria()`
**Purpose**: Multi-criteria semantic search

```python
search_gifts_by_criteria(
    budget=1000,
    occasion="birthday",
    age_group="teenager",
    min_rating=4.0,
    min_discount=30,
    num_results=5
)
```

### 3. `find_budget_friendly_gifts()`
**Purpose**: High-discount deals

```python
find_budget_friendly_gifts(
    max_budget=500,
    min_discount=50
)
```

### 4. `find_premium_gifts()`
**Purpose**: Premium quality items

```python
find_premium_gifts(
    min_budget=2000,
    occasion="anniversary"
)
```

### 5. `get_gift_recommendations_by_occasion()`
**Purpose**: Occasion-specific gifts

```python
get_gift_recommendations_by_occasion(
    occasion="wedding",
    budget=3000
)
```

### 6. `get_gift_recommendations_by_age()`
**Purpose**: Age-appropriate gifts

```python
get_gift_recommendations_by_age(
    age_group="adult",
    budget=1500
)
```

---

## 🎯 Scoring Algorithm

Products are ranked using a **composite score**:

```python
composite_score = (
    (rating / 5.0) * 0.4 +           # Rating weight: 40%
    (discount / 100.0) * 0.3 +       # Discount weight: 30%
    price_fit_score * 0.3             # Budget fit: 30%
)

where:
price_fit_score = 1 - abs(budget - price) / budget
```

**Key Features**:
- Higher ratings = better score
- Better discounts = better score
- Closer to budget = better score
- Products ranked by composite score

---

## 📁 File Structure

```
HarvestHack-Workshop/
├── gift_agent/
│   ├── __init__.py                 # Package exports
│   └── agent.py                    # Agent definitions + tools
│
├── gift_recommender.py             # ChromaDB engine
├── gift_finder.py                  # Interactive CLI
├── gift_mcp_server.py              # FastMCP server
│
├── demo_gift_tools.py              # Demo (no API key needed) ✓
├── test_gift_agent.py              # Test agents (needs API key)
│
├── amazon.csv                      # Product dataset (1,464 items)
│
├── GIFT_AGENT_README.md            # Agent system docs
├── GIFT_FINDER_README.md           # ChromaDB docs
└── SETUP_INSTRUCTIONS.md           # Setup guide
```

---

## 🚀 Usage Examples

### Example 1: Direct Tool Usage (No API Key Required)

```python
from gift_agent.agent import initialize_gift_database, search_gifts_by_criteria

# Initialize
initialize_gift_database()

# Search
results = search_gifts_by_criteria(
    budget=1000,
    occasion="birthday",
    age_group="teenager",
    min_rating=4.0,
    min_discount=30
)
print(results)
```

**Output**: Top 5 birthday gifts for teenagers under ₹1000

### Example 2: Simple Agent (Requires API Key)

```python
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from gift_agent.agent import simple_gift_agent
import asyncio

async def ask_agent():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        state={}, app_name='gift_app', user_id='user1'
    )
    
    runner = Runner(
        app_name='gift_app',
        agent=simple_gift_agent,
        session_service=session_service
    )
    
    query = "I need a birthday gift for a teenager, budget 1000 rupees"
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    async for event in runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content
    ):
        if hasattr(event, 'content'):
            for part in event.content.parts:
                if hasattr(part, 'text'):
                    print(part.text)

asyncio.run(ask_agent())
```

### Example 3: FastMCP Server

Start server:
```bash
python gift_mcp_server.py
```

Use tools:
```python
# Via MCP protocol
await client.call_tool("smart_gift_assistant", 
    user_query="Find premium anniversary gifts around 5000 rupees")
```

---

## 🎓 Natural Language Query Examples

The agent understands queries like:

✅ **"I need a birthday gift for a teenager, budget 1000 rupees"**
- Extracts: budget=1000, occasion=birthday, age=teenager

✅ **"Find me budget-friendly gifts with high discounts under 500"**
- Routes to: find_budget_friendly_gifts()

✅ **"Show premium anniversary gifts around 5000"**
- Routes to: find_premium_gifts()

✅ **"What are good graduation gifts for adults?"**
- Routes to: get_gift_recommendations_by_occasion()

✅ **"I want festive gifts with at least 40% discount"**
- Combines: occasion=festive, min_discount=40

---

## ✅ What Works WITHOUT Google API Key

**ChromaDB Tools** (All functional):
- ✓ `initialize_gift_database()`
- ✓ `search_gifts_by_criteria()`
- ✓ `find_budget_friendly_gifts()`
- ✓ `find_premium_gifts()`
- ✓ `get_gift_recommendations_by_occasion()`
- ✓ `get_gift_recommendations_by_age()`
- ✓ Run `demo_gift_tools.py`

**Requires API Key**:
- ✗ Google ADK agents
- ✗ Natural language understanding
- ✗ Multi-agent coordination
- ✗ `test_gift_agent.py`
- ✗ FastMCP agent endpoints

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Products in DB | 1,464 |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Gemini 2.0 Flash Exp |
| Vector Search Time | < 100ms |
| Full Query Time | 2-5 seconds |
| Accuracy | High (semantic + metadata) |

---

## 🔑 Key Innovations

1. **Hybrid Search**: Combines vector similarity with metadata filtering
2. **Composite Scoring**: Multi-factor ranking (rating + discount + price)
3. **Agent Orchestration**: Parallel + Sequential processing
4. **Natural Language**: Understands conversational queries
5. **Tool Specialization**: Each tool optimized for specific use cases

---

## 🎯 Use Cases

| Scenario | Best Approach |
|----------|---------------|
| "Find gifts under ₹1000" | `search_gifts_by_criteria()` |
| "I need a birthday gift for mom" | Simple Gift Agent |
| "Compare budget vs premium options" | Multi-Agent System |
| "High discount deals" | `find_budget_friendly_gifts()` |
| Complex multi-criteria | Multi-Agent System |

---

## 🚀 Quick Start Commands

```bash
# 1. Demo tools (no API key needed)
python demo_gift_tools.py

# 2. Interactive CLI
python gift_finder.py

# 3. Test agents (needs GOOGLE_API_KEY)
export GOOGLE_API_KEY="your-key"
python test_gift_agent.py

# 4. Run MCP server
python gift_mcp_server.py
```

---

## 📚 Documentation Files

1. **GIFT_AGENT_README.md** - Agent system architecture
2. **GIFT_FINDER_README.md** - ChromaDB implementation
3. **SETUP_INSTRUCTIONS.md** - Setup & troubleshooting
4. **This file** - Complete system overview

---

## 🎁 Sample Results

**Query**: "Birthday gift for teenager, budget ₹1000"

**Results**:
1. BAJAJ Mini Fan - ₹948 (41% off) ⭐4.1
2. Note Pad with Sticky Notes - ₹198 (75% off) ⭐4.1
3. 3M Post-it Cube - ₹90 (49% off) ⭐4.4
4. Universal Travel Adaptor - ₹99 (42% off) ⭐4.5
5. Luxor Notebook - ₹125 (31% off) ⭐4.4

---

## 💡 Future Enhancements

- Add user preferences learning
- Category-based filtering
- Price range recommendations
- Multi-language support
- Product image analysis
- Review sentiment analysis

---

**Built with ❤️ using Google ADK and ChromaDB**
