# 🧪 Test Queries for Travel Planning System

## 🎯 Using ADK Web Interface (`adk web`)

### Query 1: Beach Vacation (Basic)
```
I want to plan a beach vacation with a medium budget
```

**What to watch:**
- Destination agent finds beach destinations
- Budget agent calculates costs in parallel
- Itinerary agent creates day plans sequentially

---

### Query 2: Adventure Trip (Detailed)
```
Plan a 7-day adventure trip to New Zealand for 2 people with a high budget
```

**What to watch:**
- Parallel execution of destination + budget research
- Specific itinerary for New Zealand with adventure activities
- Complete budget breakdown

---

### Query 3: Cultural Exploration (Budget-Conscious)
```
I want a cultural experience in Asia for 5 days, low budget, solo traveler
```

**What to watch:**
- Budget-aware destination recommendations
- Solo traveler budget calculation
- Cultural activity-focused itinerary

---

### Query 4: Mountain Getaway
```
Suggest a mountain destination for hiking and relaxation, 10 days, 3 travelers
```

**What to watch:**
- Mountain-specific destinations
- Extended itinerary (10 days)
- Budget for multiple travelers

---

### Query 5: Comparison Request
```
Compare beach vs mountain destinations for a couple with medium budget
```

**What to watch:**
- Multiple destination types analyzed
- Comparative budget analysis
- Pros/cons of each option

---

## 🔧 Using FastMCP Server (Advanced)

### Setup
```bash
# Terminal 1: Start FastMCP server
python mcp_server.py

# Terminal 2: Test with Python client (see test_mcp_client.py)
```

### Individual Tool Tests

**Test 1: Find Destinations**
```python
await client.call_tool(
    name="find_destinations",
    arguments={"preferences": "beach vacation", "budget": "medium"}
)
```

**Test 2: Check Weather**
```python
await client.call_tool(
    name="check_weather",
    arguments={"destination": "Bali", "month": "current"}
)
```

**Test 3: Calculate Budget**
```python
await client.call_tool(
    name="calculate_budget",
    arguments={
        "destination": "Maldives",
        "duration_days": 7,
        "travelers": 2
    }
)
```

**Test 4: Build Itinerary**
```python
await client.call_tool(
    name="build_itinerary",
    arguments={
        "destination": "Japan",
        "interests": "cultural and food",
        "days": 5
    }
)
```

**Test 5: Complete Trip Planning (Multi-Agent)**
```python
await client.call_tool(
    name="plan_complete_trip",
    arguments={
        "preferences": "adventure in mountains",
        "budget_level": "high",
        "duration_days": 10,
        "travelers": 2
    }
)
```

---

## 🎪 Demo Flow for Workshop

### Demo 1: Quick Start (5 min)
1. Run `adk web`
2. Use Query 1: "I want to plan a beach vacation with a medium budget"
3. Show the agent workflow in real-time
4. Highlight parallel vs sequential execution

### Demo 2: Detailed Planning (10 min)
1. Use Query 2: "Plan a 7-day adventure trip to New Zealand..."
2. Walk through each agent's contribution:
   - Destination Discovery Agent findings
   - Budget Planning Agent calculations
   - Itinerary Builder Agent day-by-day plan
3. Show how agents pass data via `output_key`

### Demo 3: MCP Integration (Advanced - 10 min)
1. Start FastMCP server: `python mcp_server.py`
2. Show individual tool usage
3. Demonstrate complete multi-agent planning via MCP
4. Explain how ADK agents are exposed as MCP tools

---

## 🌟 Expected Behaviors

### Parallel Execution
- **Destination Agent** + **Budget Agent** run simultaneously
- Faster response time for initial research
- Both complete before itinerary building starts

### Sequential Flow
1. Research Coordinator (Parallel: Destination + Budget)
2. Itinerary Builder (uses outputs from research)
3. Final combined response

### Data Flow
```
User Query
    ↓
[Parallel] Destination Discovery Agent → destination_recommendations
[Parallel] Budget Planning Agent → budget_plan
    ↓
Itinerary Builder Agent → detailed_itinerary
    ↓
Complete Travel Plan
```

---

## 💡 Customization Ideas

After basic demo, try modifying:
1. Add more destinations to the tool databases
2. Create a "Flight Search Agent" 
3. Add a "Accommodation Booking Agent"
4. Include real API integrations (weather, flights, hotels)
5. Add user preference memory across sessions

---

## 🐛 Troubleshooting

**If agents don't use tools:**
- Check agent instructions mention tool usage
- Verify tools are in the `tools` list
- Try more explicit queries

**If parallel execution isn't visible:**
- Check the ADK web UI event stream
- Both agents should show "running" status simultaneously

**If MCP server fails:**
- Ensure FastMCP is installed: `pip install fastmcp`
- Check imports from research_agent.agent work
- Verify `.env` has GOOGLE_API_KEY

---

**Ready to test! Start with `adk web` and Query 1! 🚀**
