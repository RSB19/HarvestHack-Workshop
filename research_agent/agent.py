"""
Multi-Agent Travel Planning System using Google ADK
Exposed via FastMCP - A comprehensive travel assistant with specialized agents
"""
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent

# ===== SPECIALIZED TRAVEL TOOLS =====

def search_destinations(preferences: str, budget: str = "medium") -> str:
    """
    Searches for travel destinations based on user preferences and budget.
    
    Args:
        preferences: Type of travel (beach, mountains, cultural, adventure, etc.)
        budget: Budget level (low, medium, high)
    
    Returns:
        Destination recommendations with details
    """
    destinations = {
        "beach": [
            {"name": "Maldives", "budget": "high", "highlights": "Crystal clear waters, luxury resorts, snorkeling"},
            {"name": "Bali, Indonesia", "budget": "medium", "highlights": "Beautiful beaches, temples, affordable luxury"},
            {"name": "Goa, India", "budget": "low", "highlights": "Beaches, nightlife, Portuguese culture"}
        ],
        "mountains": [
            {"name": "Swiss Alps", "budget": "high", "highlights": "Skiing, hiking, scenic trains"},
            {"name": "Nepal Himalayas", "budget": "low", "highlights": "Trekking, Mount Everest views, monasteries"},
            {"name": "Rocky Mountains, USA", "budget": "medium", "highlights": "National parks, wildlife, camping"}
        ],
        "cultural": [
            {"name": "Kyoto, Japan", "budget": "medium", "highlights": "Temples, gardens, traditional tea houses"},
            {"name": "Rome, Italy", "budget": "medium", "highlights": "Ancient ruins, Vatican, Italian cuisine"},
            {"name": "Cairo, Egypt", "budget": "low", "highlights": "Pyramids, museums, Nile River"}
        ],
        "adventure": [
            {"name": "New Zealand", "budget": "high", "highlights": "Bungee jumping, hiking, Lord of the Rings tours"},
            {"name": "Costa Rica", "budget": "medium", "highlights": "Zip-lining, surfing, rainforests"},
            {"name": "Peru", "budget": "low", "highlights": "Machu Picchu, Amazon rainforest, hiking"}
        ]
    }
    
    pref_lower = preferences.lower()
    category = next((k for k in destinations.keys() if k in pref_lower), "beach")
    
    results = "🌍 **Destination Recommendations:**\n\n"
    for dest in destinations[category]:
        if budget in dest["budget"] or budget == "medium":
            results += f"📍 **{dest['name']}** (Budget: {dest['budget'].title()})\n"
            results += f"   Highlights: {dest['highlights']}\n\n"
    
    return results


def get_weather_info(destination: str, month: str = "current") -> str:
    """
    Provides weather information and best time to visit a destination.
    
    Args:
        destination: The destination name
        month: Month to check (or "current")
    
    Returns:
        Weather info and travel recommendations
    """
    weather_data = {
        "maldives": {"best_months": "Nov-Apr", "temp": "77-86°F", "condition": "Dry, sunny"},
        "bali": {"best_months": "Apr-Oct", "temp": "75-85°F", "condition": "Dry season, ideal weather"},
        "swiss alps": {"best_months": "Dec-Mar (skiing), Jun-Sep (hiking)", "temp": "Variable", "condition": "Depends on season"},
        "japan": {"best_months": "Mar-May, Sep-Nov", "temp": "50-75°F", "condition": "Cherry blossoms or fall colors"},
        "new zealand": {"best_months": "Dec-Feb", "temp": "60-75°F", "condition": "Summer, best for outdoor activities"},
        "costa rica": {"best_months": "Dec-Apr", "temp": "70-85°F", "condition": "Dry season"},
    }
    
    dest_key = next((k for k in weather_data.keys() if k in destination.lower()), "general")
    
    if dest_key == "general":
        return f"☀️ **Weather Info for {destination}:**\nPlease search for specific destination weather online.\n"
    
    info = weather_data[dest_key]
    return f"""☀️ **Weather Info for {destination}:**
    
Best Time to Visit: {info['best_months']}
Average Temperature: {info['temp']}
Typical Conditions: {info['condition']}

💡 Tip: Book 2-3 months in advance for best prices!
"""


def estimate_budget(destination: str, duration_days: int = 7, travelers: int = 2) -> str:
    """
    Estimates travel budget including flights, accommodation, and activities.
    
    Args:
        destination: The destination name
        duration_days: Trip duration in days
        travelers: Number of travelers
    
    Returns:
        Detailed budget breakdown
    """
    # Base costs per person per day
    base_costs = {
        "maldives": {"flights": 1200, "accommodation": 300, "food": 80, "activities": 150},
        "bali": {"flights": 800, "accommodation": 80, "food": 25, "activities": 50},
        "swiss alps": {"flights": 700, "accommodation": 180, "food": 70, "activities": 120},
        "japan": {"flights": 900, "accommodation": 120, "food": 50, "activities": 80},
        "new zealand": {"flights": 1100, "accommodation": 100, "food": 60, "activities": 100},
        "costa rica": {"flights": 500, "accommodation": 90, "food": 35, "activities": 70},
    }
    
    dest_key = next((k for k in base_costs.keys() if k in destination.lower()), None)
    
    if not dest_key:
        return f"💰 Budget estimation not available for {destination}. Please search online for pricing.\n"
    
    costs = base_costs[dest_key]
    
    flight_total = costs["flights"] * travelers
    accommodation_total = costs["accommodation"] * duration_days * travelers
    food_total = costs["food"] * duration_days * travelers
    activities_total = costs["activities"] * duration_days * travelers
    
    total = flight_total + accommodation_total + food_total + activities_total
    
    return f"""💰 **Budget Estimate for {destination}:**
    
👥 Travelers: {travelers}
📅 Duration: {duration_days} days

📊 **Breakdown:**
✈️  Flights: ${flight_total:,}
🏨 Accommodation: ${accommodation_total:,}
🍽️  Food & Dining: ${food_total:,}
🎯 Activities: ${activities_total:,}

💵 **Total Estimated Cost: ${total:,}**

💡 This is an estimate. Actual costs may vary based on booking time, season, and personal preferences.
"""


def create_itinerary(destination: str, interests: str, days: int = 5) -> str:
    """
    Creates a day-by-day itinerary based on destination and interests.
    
    Args:
        destination: The destination name
        interests: User's interests (sightseeing, food, adventure, relaxation, etc.)
        days: Number of days for the itinerary
    
    Returns:
        Detailed day-by-day itinerary
    """
    itineraries = {
        "bali": {
            "day1": "Arrival in Denpasar → Check-in Ubud → Visit Monkey Forest → Dinner at Ubud Market",
            "day2": "Tegallalang Rice Terraces → Coffee plantation tour → Traditional Balinese massage",
            "day3": "Tanah Lot Temple sunset → Beach day at Seminyak → Seafood dinner",
            "day4": "Water temple visit → Waterfall hiking → Traditional dance performance",
            "day5": "Beach relaxation → Shopping → Departure preparation"
        },
        "japan": {
            "day1": "Arrive Kyoto → Fushimi Inari Shrine → Gion district evening walk",
            "day2": "Kinkaku-ji Temple → Arashiyama Bamboo Grove → Traditional tea ceremony",
            "day3": "Nara day trip → Todai-ji Temple → Feed the deer → Return to Kyoto",
            "day4": "Osaka Castle → Dotonbori food street → Shopping in Shinsaibashi",
            "day5": "Nishiki Market → Souvenir shopping → Departure"
        },
        "new zealand": {
            "day1": "Arrive Queenstown → Lake Wakatipu cruise → Town exploration",
            "day2": "Milford Sound day trip → Scenic flight option",
            "day3": "Bungee jumping or Skydiving → Wine tasting tour",
            "day4": "Gondola ride → Luge → Hiking trails → Sunset views",
            "day5": "Glenorchy scenic drive → Relaxation → Departure prep"
        }
    }
    
    dest_key = next((k for k in itineraries.keys() if k in destination.lower()), None)
    
    if not dest_key:
        return f"📅 Custom itinerary for {destination} - Please research top attractions for detailed planning.\n"
    
    itinerary = itineraries[dest_key]
    
    result = f"📅 **{days}-Day Itinerary for {destination.title()}:**\n\n"
    for i in range(1, min(days + 1, 6)):
        day_key = f"day{i}"
        if day_key in itinerary:
            result += f"**Day {i}:** {itinerary[day_key]}\n\n"
    
    result += "✨ *Itinerary can be customized based on your pace and interests!*\n"
    return result


# ===== SPECIALIZED AGENTS =====

# Agent 1: Destination Discovery Agent
destination_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='destination_discovery_agent',
    description='Finds and recommends travel destinations based on preferences',
    instruction="""You are a Destination Discovery Agent specializing in finding perfect travel spots.

Your responsibilities:
- Use search_destinations to find places matching user preferences and budget
- Use get_weather_info to provide weather insights and best travel times
- Consider user's interests, budget, and travel style
- Provide 2-3 destination options with clear reasoning
- Highlight unique features of each destination

Be enthusiastic but realistic about recommendations!""",
    tools=[search_destinations, get_weather_info],
    output_key="destination_recommendations",
)

# Agent 2: Budget Planning Agent
budget_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='budget_planning_agent',
    description='Creates detailed budget estimates for travel plans',
    instruction="""You are a Budget Planning Agent that helps travelers understand costs.

Your responsibilities:
- Use estimate_budget to calculate trip costs based on destination and duration
- Break down expenses clearly (flights, accommodation, food, activities)
- Provide money-saving tips specific to the destination
- Suggest budget alternatives if costs are high
- Be transparent about what's included and excluded

Help users make informed financial decisions!""",
    tools=[estimate_budget],
    output_key="budget_plan",
)

# Agent 3: Itinerary Builder Agent
itinerary_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='itinerary_builder_agent',
    description='Creates detailed day-by-day travel itineraries',
    instruction="""You are an Itinerary Builder Agent that crafts personalized travel plans.

Your responsibilities:
- Use create_itinerary to build day-by-day schedules
- Balance activities with relaxation time
- Consider travel logistics and timing
- Include must-see attractions and hidden gems
- Provide practical tips for each day

Create realistic, enjoyable itineraries that aren't too packed!""",
    tools=[create_itinerary],
    output_key="detailed_itinerary",
)

# ===== COORDINATOR AGENTS =====

# Parallel Research Agent - Runs destination and budget analysis simultaneously
research_coordinator = ParallelAgent(
    name='travel_research_coordinator',
    sub_agents=[destination_agent, budget_agent],
    description='Simultaneously researches destinations and budget requirements',
)

# Main Travel Planner - Sequential workflow for complete trip planning
root_agent = SequentialAgent(
    name='travel_planning_system',
    sub_agents=[research_coordinator, itinerary_agent],
    description='Complete travel planning system: discovers destinations, estimates budgets, and creates detailed itineraries',
)
