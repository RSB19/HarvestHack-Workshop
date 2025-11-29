# 🎁 Gift Agent System - Quick Reference

## TL;DR
AI-powered gift recommendation system using **Google ADK** + **ChromaDB** with 1,464 Amazon products.

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Run demo (no API key needed)
python demo_gift_tools.py

# 2. Set API key (for agents)
export GOOGLE_API_KEY="your-key"

# 3. Test agents
python test_gift_agent.py
```

---

## 📋 Input Parameters

```python
search_gifts_by_criteria(
    budget=1000,           # ₹ Maximum price
    occasion="birthday",   # Event type
    age_group="teenager",  # Recipient age
    min_rating=4.0,        # 0-5 rating
    min_discount=30,       # % off
    num_results=5          # Results count
)
```

---

## 🤖 Two Agent Modes

### Simple Agent (Recommended)
```python
from gift_agent.agent import simple_gift_agent
# Single intelligent agent - handles all queries
```

### Multi-Agent
```python
from gift_agent.agent import root_gift_agent
# Parallel research + Sequential processing
```

---

## 🛠️ 6 Core Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `initialize_gift_database()` | Setup DB | First call always |
| `search_gifts_by_criteria()` | Multi-search | General queries |
| `find_budget_friendly_gifts()` | Deals | High discounts |
| `find_premium_gifts()` | Quality | Premium items |
| `get_gift_recommendations_by_occasion()` | Events | Birthdays, etc. |
| `get_gift_recommendations_by_age()` | Age-based | Kids, adults |

---

## 💬 Natural Language Examples

```
✅ "Birthday gift for teenager, budget 1000 rupees"
✅ "Find budget-friendly gifts under 500 with 50% off"
✅ "Premium anniversary gifts around 5000"
✅ "Graduation gifts for adults"
```

---

## 📊 Scoring Formula

```
Score = Rating(40%) + Discount(30%) + BudgetFit(30%)
```

Higher score = Better match!

---

## 📁 Key Files

| File | Purpose | Needs API? |
|------|---------|------------|
| `demo_gift_tools.py` | Demo tools | ❌ No |
| `gift_finder.py` | Interactive | ❌ No |
| `test_gift_agent.py` | Test agents | ✅ Yes |
| `gift_mcp_server.py` | MCP server | ✅ Yes |

---

## 🎯 Common Tasks

### Find cheap deals
```python
find_budget_friendly_gifts(max_budget=500, min_discount=50)
```

### Birthday gift
```python
search_gifts_by_criteria(
    budget=1000, occasion="birthday", age_group="teenager"
)
```

### Premium gifts
```python
find_premium_gifts(min_budget=2000, occasion="anniversary")
```

---

## ⚡ Performance

- Products: **1,464**
- Search: **< 100ms**
- Full query: **2-5 sec**
- Accuracy: **High**

---

## 🐛 Troubleshooting

| Error | Solution |
|-------|----------|
| "Missing key inputs" | Set `GOOGLE_API_KEY` |
| Module not found | `pip install -r requirements.txt` |
| No results | Relax filters (rating, discount) |

---

## 📚 Documentation

1. **SYSTEM_SUMMARY.md** ← Full overview
2. **GIFT_AGENT_README.md** ← Agent details
3. **SETUP_INSTRUCTIONS.md** ← Setup guide

---

## ✅ Works Without API Key

- ✓ All 6 tools
- ✓ ChromaDB search
- ✓ `demo_gift_tools.py`
- ✗ AI agents
- ✗ Natural language

---

**Need help? Read SETUP_INSTRUCTIONS.md**
