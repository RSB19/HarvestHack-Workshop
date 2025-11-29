"""
FastMCP Server exposing Google ADK Gift Recommendation Agent System
Integrates ChromaDB-based gift finder with conversational AI
Run with: python gift_mcp_server.py
"""
from fastmcp import FastMCP
from gift_agent.agent import (
    simple_gift_agent,
    root_gift_agent,
    initialize_gift_database,
    search_gifts_by_criteria,
    find_budget_friendly_gifts,
    find_premium_gifts,
    get_gift_recommendations_by_occasion,
    get_gift_recommendations_by_age
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

# Initialize FastMCP server
mcp = FastMCP("Gift Recommendation Assistant 🎁")

# Initialize ADK runner components
session_service = InMemorySessionService()

# Expose individual tools as MCP tools
@mcp.tool()
def initialize_database() -> str:
    """Initialize the ChromaDB gift recommendation database with Amazon products."""
    return initialize_gift_database("amazon.csv")


@mcp.tool()
def search_gifts(
    budget: float,
    occasion: str,
    age_group: str,
    min_rating: float,
    min_discount: float,
    num_results: int
) -> str:
    """
    Search for gift recommendations based on criteria.
    
    Args:
        budget: Maximum budget in rupees (₹)
        occasion: Gift occasion (birthday, anniversary, festive, etc.)
        age_group: Target age group (kid, teenager, adult, senior)
        min_rating: Minimum product rating (0-5)
        min_discount: Minimum discount percentage
        num_results: Number of recommendations
    """
    return search_gifts_by_criteria(budget, occasion, age_group, min_rating, min_discount, num_results)


@mcp.tool()
def find_deals(max_budget: float, min_discount: float) -> str:
    """
    Find budget-friendly gifts with high discounts.
    
    Args:
        max_budget: Maximum budget in rupees
        min_discount: Minimum discount percentage
    """
    return find_budget_friendly_gifts(max_budget, min_discount)


@mcp.tool()
def find_premium(min_budget: float, occasion: str) -> str:
    """
    Find premium, high-quality gifts.
    
    Args:
        min_budget: Minimum budget for premium gifts
        occasion: Special occasion
    """
    return find_premium_gifts(min_budget, occasion)


@mcp.tool()
def gifts_by_occasion(occasion: str, budget: float) -> str:
    """
    Get occasion-specific gift recommendations.
    
    Args:
        occasion: The occasion (birthday, anniversary, festive, etc.)
        budget: Budget in rupees
    """
    return get_gift_recommendations_by_occasion(occasion, budget)


@mcp.tool()
def gifts_by_age(age_group: str, budget: float) -> str:
    """
    Get age-appropriate gift recommendations.
    
    Args:
        age_group: Target age (kid, teenager, adult, senior)
        budget: Budget in rupees
    """
    return get_gift_recommendations_by_age(age_group, budget)


@mcp.tool()
async def smart_gift_assistant(user_query: str) -> str:
    """
    Intelligent gift assistant that understands natural language queries.
    Ask for gift recommendations in plain English!
    
    Args:
        user_query: Your gift request in natural language
        
    Examples:
        - "I need a birthday gift for a teenager, budget 1000 rupees"
        - "Find me premium anniversary gifts"
        - "Show budget-friendly festive gifts with high discounts"
    """
    # Create session
    session = await session_service.create_session(
        state={},
        app_name='gift_assistant_mcp',
        user_id='mcp_user'
    )
    
    # Create user query content
    content = types.Content(
        role='user',
        parts=[types.Part(text=user_query)]
    )
    
    # Initialize runner with simple gift agent
    runner = Runner(
        app_name='gift_assistant_mcp',
        agent=simple_gift_agent,
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
    
    return result_text if result_text else "I apologize, but I couldn't process your request. Please try again."


@mcp.tool()
async def complete_gift_recommendation(
    user_request: str
) -> str:
    """
    Complete multi-agent gift recommendation system.
    Uses parallel search, budget analysis, and occasion-specific recommendations.
    
    Args:
        user_request: Detailed description of your gift requirements
        
    Example:
        "I need to find a meaningful anniversary gift for my wife. Budget is 5000 rupees. 
         She likes technology and gadgets. Looking for something with good ratings."
    """
    # Create session
    session = await session_service.create_session(
        state={},
        app_name='gift_multi_agent_mcp',
        user_id='mcp_user'
    )
    
    # Create user query content
    content = types.Content(
        role='user',
        parts=[types.Part(text=user_request)]
    )
    
    # Initialize runner with root agent (multi-agent system)
    runner = Runner(
        app_name='gift_multi_agent_mcp',
        agent=root_gift_agent,
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
    
    return result_text if result_text else "Gift recommendation completed. Please check the search results."


if __name__ == "__main__":
    print("🚀 Starting Gift Recommendation FastMCP Server...")
    print("🎁 Server integrates Google ADK with ChromaDB for intelligent gift recommendations")
    print("\nAvailable tools:")
    print("  - initialize_database: Set up the product database")
    print("  - search_gifts: Multi-criteria gift search")
    print("  - find_deals: Budget-friendly high-discount gifts")
    print("  - find_premium: Premium quality gifts")
    print("  - gifts_by_occasion: Occasion-specific recommendations")
    print("  - gifts_by_age: Age-appropriate suggestions")
    print("  - smart_gift_assistant: Natural language gift queries (ADK Single Agent)")
    print("  - complete_gift_recommendation: Full multi-agent analysis (ADK Multi-Agent)")
    print("\n" + "="*80)
    
    mcp.run()
