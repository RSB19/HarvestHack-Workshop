# 🎁 Gift Recommendation Agentic System

> **An intelligent gift finder powered by Google ADK and ChromaDB** - Recommends perfect products from 1,464 Amazon items using AI agents and semantic search.

---

## 🌟 Overview

This project demonstrates an advanced **agentic AI system** that:

1. **Stores** product data in a **ChromaDB vector database**
2. **Uses Google ADK agents** for intelligent query understanding
3. **Recommends gifts** based on budget, occasion, age, rating, and discount
4. **Responds naturally** to conversational queries

### Key Technologies
- 🤖 **Google ADK (Agentic Development Kit)** - Multi-agent orchestration
- 🗄️ **ChromaDB** - Vector database with semantic search
- 🧠 **Gemini 2.0 Flash Exp** - LLM for natural language understanding
- 📊 **1,464 Amazon Products** - Real product dataset

---

## 🏗️ System Architecture

```
User Query → Google ADK Agents → Gift Tools → ChromaDB → Results
              (Simple/Multi)      (6 tools)   (Vector DB)
```

### Two Agent Approaches

**1. Simple Gift Agent** (Single Agent)
- Best for: Direct queries
- Gemini 2.0 Flash Exp
- All tools available
- Faster responses

**2. Multi-Agent System** (Parallel + Sequential)
- Best for: Complex queries
- Parallel Research (Search + Budget)
- Sequential Occasion Analysis
- Comprehensive results

---

## 🚀 Quick Start

### Run Without API Key (ChromaDB Tools)

```bash
# Install dependencies
pip install chromadb pandas

# Run demo
python demo_gift_tools.py
```

**Output**: Gift recommendations using ChromaDB search!

### Run With Google API (Full Agent System)

```bash
# Set API key
export GOOGLE_API_KEY="your-api-key"

# Install all dependencies
pip install google-adk chromadb pandas fastmcp

# Test agents
python test_gift_agent.py

# Or run MCP server
python gift_mcp_server.py
```

---

## 💡 Usage Examples

### Example 1: Direct Tool Call

```python
from gift_agent.agent import initialize_gift_database, search_gifts_by_criteria

# Initialize database
initialize_gift_database()

# Search for gifts
results = search_gifts_by_criteria(
    budget=1000,
    occasion="birthday",
    age_group="teenager",
    min_rating=4.0,
    min_discount=30,
    num_results=5
)

print(results)
```

**Output:**
```
🎁 Found 5 Gift Recommendations:

1. **BAJAJ Mini Fan**
   💰 Price: ₹948 (Save 41%)
   ⭐ Rating: 4.1/5.0
   
2. **Note Pad with Sticky Notes**
   💰 Price: ₹198 (Save 75%)
   ⭐ Rating: 4.1/5.0
...
```

### Example 2: Natural Language Query (Requires API Key)

```python
from google.adk.runners import Runner
from gift_agent.agent import simple_gift_agent
# ... (see GIFT_AGENT_README.md for full code)

query = "Find me a birthday gift for a teenager, budget 1000 rupees"
# Agent understands and extracts: budget=1000, occasion=birthday, age=teenager
```

### Example 3: Interactive CLI

```bash
python gift_finder.py
```

Enter criteria interactively and get recommendations!

---

## 📊 Input Criteria

The system accepts 6 input parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| **budget** | float | Maximum price (₹) | 1000, 5000 |
| **occasion** | string | Gift occasion | birthday, anniversary, festive |
| **age_group** | string | Recipient age | kid, teenager, adult, senior |
| **min_rating** | float | Minimum rating (0-5) | 4.0, 4.2 |
| **min_discount** | float | Minimum discount % | 20, 50 |
| **num_results** | int | Number of results | 5, 10 |

---

## 🛠️ Available Tools

### 1. `initialize_gift_database()`
Sets up ChromaDB with Amazon products (call first!)

### 2. `search_gifts_by_criteria()`
Multi-criteria semantic search - most versatile

### 3. `find_budget_friendly_gifts()`
High-discount deals under budget

### 4. `find_premium_gifts()`
Premium quality items above price threshold

### 5. `get_gift_recommendations_by_occasion()`
Occasion-specific recommendations

### 6. `get_gift_recommendations_by_age()`
Age-appropriate gift suggestions

---

## 🎯 How It Works

### 1. Data Loading
```python
# Reads amazon.csv (1,464 products)
# Parses: price, discount, rating, category, description
```

### 2. Embedding Creation
```python
# Creates semantic embeddings using all-MiniLM-L6-v2
# Combines: name, category, price, rating, description
```

### 3. ChromaDB Storage
```python
# Stores embeddings + metadata in vector database
# Enables semantic similarity search
```

### 4. Query Processing
```python
# User query → Agent understands intent → Calls appropriate tool
# Tool builds search query + applies filters
```

### 5. Ranking
```python
# Composite Score = Rating(40%) + Discount(30%) + BudgetFit(30%)
# Higher score = Better match
```

### 6. Results
```python
# Returns top N products with details
# Includes: name, price, discount, rating, link
```

---

## 🤖 Agent System Details

### Simple Gift Agent
- **Model**: gemini-2.0-flash-exp
- **Tools**: All 6 tools
- **Instruction**: Understands natural language, routes to tools
- **Best for**: Single queries, fast responses

### Multi-Agent System

**Gift Search Agent**
- Handles general searches
- Extracts criteria from queries

**Budget Advisor Agent**
- Specializes in budget optimization
- Finds deals and premium options

**Occasion Specialist Agent**
- Occasion-specific recommendations
- Age-appropriate selections

**Gift Research Coordinator** (Parallel)
- Runs Search + Budget simultaneously
- Faster comprehensive analysis

---

## 📁 Project Structure

```
HarvestHack-Workshop/
│
├── 📂 gift_agent/               # Google ADK agents
│   ├── __init__.py
│   └── agent.py                 # Agent definitions + tools
│
├── 📄 gift_recommender.py       # ChromaDB engine
├── 📄 gift_finder.py            # Interactive CLI
├── 📄 gift_mcp_server.py        # FastMCP server
│
├── 📄 demo_gift_tools.py        # ✅ Demo (no API key)
├── 📄 test_gift_agent.py        # Test agents (needs key)
│
├── 📂 research_agent/           # Travel agent (separate)
│   ├── __init__.py
│   └── agent.py
│
├── 📄 mcp_server.py             # Travel MCP server
│
├── 📊 amazon.csv                # Product dataset
│
├── 📚 Documentation/
│   ├── SYSTEM_SUMMARY.md        # Complete overview
│   ├── GIFT_AGENT_README.md     # Agent details
│   ├── GIFT_FINDER_README.md    # ChromaDB details
│   ├── SETUP_INSTRUCTIONS.md    # Setup guide
│   ├── QUICK_REFERENCE.md       # Quick ref
│   └── README.md                # This file
│
└── 📄 requirements.txt          # Dependencies
```

---

## 🎓 Natural Language Queries

The agents understand conversational queries:

```
✅ "I need a birthday gift for a teenager, budget 1000 rupees"
✅ "Find me budget-friendly gifts with high discounts under 500"
✅ "Show premium anniversary gifts around 5000"
✅ "What are good graduation gifts for adults?"
✅ "I want festive gifts with at least 40% discount"
✅ "Suggest wedding gifts for a couple, budget 3000-4000"
```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| Products in Database | 1,464 |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Gemini 2.0 Flash Exp |
| Vector Search Time | < 100ms |
| Full Query (with Agent) | 2-5 seconds |
| Accuracy | High (semantic + filters) |

---

## ✅ What Works Without API Key

**ChromaDB Tools** (Fully functional):
- ✓ All 6 gift recommendation tools
- ✓ Vector semantic search
- ✓ Metadata filtering
- ✓ Composite scoring
- ✓ `demo_gift_tools.py`
- ✓ `gift_finder.py` (interactive)

**Requires Google API Key**:
- ✗ Google ADK agents
- ✗ Natural language understanding
- ✗ Multi-agent orchestration
- ✗ `test_gift_agent.py`
- ✗ Agent endpoints in MCP server

---

## 🔧 Setup

### Quick Setup (No API Key)

```bash
pip install chromadb pandas
python demo_gift_tools.py
```

### Full Setup (With Agents)

```bash
# Install dependencies
pip install google-adk chromadb pandas fastmcp python-dotenv

# Get API key from: https://makersuite.google.com/app/apikey

# Set API key
export GOOGLE_API_KEY="your-api-key"
# OR create .env file:
echo "GOOGLE_API_KEY=your-key" > .env

# Test
python test_gift_agent.py
```

---

## 📚 Documentation Guide

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Overview & quick start | Everyone |
| **QUICK_REFERENCE.md** | Cheat sheet | Developers |
| **SYSTEM_SUMMARY.md** | Complete architecture | Technical |
| **GIFT_AGENT_README.md** | Agent system details | AI Engineers |
| **GIFT_FINDER_README.md** | ChromaDB details | Data Scientists |
| **SETUP_INSTRUCTIONS.md** | Setup & troubleshooting | DevOps |

---

## 🎁 Sample Results

**Query**: Birthday gift for teenager, budget ₹1000, min 30% discount

**Results**:
1. 🌀 BAJAJ Mini Fan - ₹948 (41% off) ⭐4.1
2. 📒 Note Pad Set - ₹198 (75% off) ⭐4.1  
3. 📝 3M Post-it Cube - ₹90 (49% off) ⭐4.4
4. 🔌 Travel Adaptor - ₹99 (42% off) ⭐4.5
5. 📓 Notebook - ₹125 (31% off) ⭐4.4

---

## 🚀 Advanced Features

### Composite Scoring
```python
score = rating/5 * 0.4 + discount/100 * 0.3 + price_fit * 0.3
```

### Semantic Search
Understands context: "gift for tech-savvy teenager" finds electronics

### Parallel Processing
Multi-agent runs search + budget analysis simultaneously

### Metadata Filtering
Hard filters on price, rating, discount before semantic search

---

## 🤝 Contributing

Enhance the system:
- Add more product categories
- Improve scoring algorithm
- Add user preference learning
- Implement category filtering
- Multi-language support

---

## 📝 License

Educational project for HarvestHack Workshop.

---

## 🎯 Next Steps

1. **Try the demo**: `python demo_gift_tools.py`
2. **Read docs**: Start with QUICK_REFERENCE.md
3. **Get API key**: [Google AI Studio](https://makersuite.google.com/app/apikey)
4. **Test agents**: `python test_gift_agent.py`
5. **Deploy**: `python gift_mcp_server.py`

---

## 💬 Questions?

- **Setup issues?** → SETUP_INSTRUCTIONS.md
- **How agents work?** → GIFT_AGENT_README.md
- **ChromaDB details?** → GIFT_FINDER_README.md
- **Quick reference?** → QUICK_REFERENCE.md

---

**Built with ❤️ using Google ADK and ChromaDB**

**Happy Gift Finding! 🎁✨**
