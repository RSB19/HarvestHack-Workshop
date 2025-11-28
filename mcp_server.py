"""
FastMCP Server exposing Google ADK Multi-Agent Travel Planning System
Run with: python mcp_server.py
"""
from fastmcp import FastMCP
from research_agent.agent import (
    search_destinations,
    get_weather_info,
    estimate_budget,
    create_itinerary,
    root_agent
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# Initialize FastMCP server
mcp = FastMCP("Travel Planning Assistant 🌍")

# Initialize ADK runner components
session_service = InMemorySessionService()

# Expose individual tools as MCP tools
@mcp.tool()
def find_destinations(preferences: str, budget: str = "medium") -> str:
    """
    Find travel destinations based on your preferences and budget.
    
    Args:
        preferences: Type of travel (beach, mountains, cultural, adventure)
        budget: Budget level (low, medium, high)
    """
    return search_destinations(preferences, budget)


@mcp.tool()
def check_weather(destination: str, month: str = "current") -> str:
    """
    Get weather information and best time to visit a destination.
    
    Args:
        destination: Name of the destination
        month: Month to check (or "current")
    """
    return get_weather_info(destination, month)


@mcp.tool()
def calculate_budget(destination: str, duration_days: int = 7, travelers: int = 2) -> str:
    """
    Calculate estimated travel budget for a destination.
    
    Args:
        destination: Destination name
        duration_days: Trip duration in days
        travelers: Number of travelers
    """
    return estimate_budget(destination, duration_days, travelers)


@mcp.tool()
def build_itinerary(destination: str, interests: str, days: int = 5) -> str:
    """
    Create a detailed day-by-day travel itinerary.
    
    Args:
        destination: Destination name
        interests: Your interests (sightseeing, food, adventure, relaxation)
        days: Number of days for the itinerary
    """
    return create_itinerary(destination, interests, days)


@mcp.tool()
async def plan_complete_trip(
    preferences: str,
    budget_level: str = "medium",
    duration_days: int = 7,
    travelers: int = 2
) -> str:
    """
    Plan a complete trip using multi-agent system - destinations, budget, and itinerary.
    
    Args:
        preferences: Travel preferences (beach, mountains, cultural, adventure)
        budget_level: Budget level (low, medium, high)
        duration_days: Trip duration in days
        travelers: Number of travelers
    """
    # Create session
    session = await session_service.create_session(
        state={},
        app_name='travel_planning_mcp',
        user_id='mcp_user'
    )
    
    # Create user query
    user_query = f"""Plan a {duration_days}-day trip for {travelers} travelers. 
Preferences: {preferences}
Budget: {budget_level}
Please provide destination recommendations, budget estimates, and a detailed itinerary."""
    
    content = types.Content(
        role='user',
        parts=[types.Part(text=user_query)]
    )
    
    # Initialize runner with root agent
    runner = Runner(
        app_name='travel_planning_mcp',
        agent=root_agent,
        session_service=session_service,
    )
    
    # Collect all events
    result_text = ""
    events_async = runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content
    )
    
    async for event in events_async:
        # Extract text from events
        if hasattr(event, 'content') and hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    result_text += part.text + "\n"
    
    return result_text if result_text else "Travel planning completed. Please check the individual agent outputs."


if __name__ == "__main__":
    print("🚀 Starting Travel Planning FastMCP Server...")
    print("📍 Server provides individual tools AND complete multi-agent trip planning")
    print("\nAvailable tools:")
    print("  - find_destinations: Search for destinations")
    print("  - check_weather: Get weather info")
    print("  - calculate_budget: Estimate costs")
    print("  - build_itinerary: Create day-by-day plans")
    print("  - plan_complete_trip: Full multi-agent planning (ADK)")
    print("\n" + "="*60)
    
    mcp.run()
