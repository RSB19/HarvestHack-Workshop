"""
Test script for Gift Recommendation Agent System
Demonstrates Google ADK integration with ChromaDB
"""
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
from gift_agent.agent import simple_gift_agent, root_gift_agent

# Load environment variables from .env file
load_dotenv()


async def test_simple_agent():
    """Test the simple gift agent with natural language queries"""
    print("\n" + "="*100)
    print("TEST 1: Simple Gift Agent (Single Agent)")
    print("="*100)
    
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create session
    session = await session_service.create_session(
        state={},
        app_name='gift_test_simple',
        user_id='test_user'
    )
    
    # Test queries
    test_queries = [
        "I need a birthday gift for a teenager with a budget of 1000 rupees",
        "Find me budget-friendly gifts with at least 50% discount under 500 rupees",
        "Show me premium anniversary gifts around 5000 rupees"
    ]
    
    runner = Runner(
        app_name='gift_test_simple',
        agent=simple_gift_agent,
        session_service=session_service,
    )
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─'*100}")
        print(f"Query {i}: {query}")
        print('─'*100)
        
        content = types.Content(
            role='user',
            parts=[types.Part(text=query)]
        )
        
        # Run agent and collect responses
        events_async = runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=content
        )
        
        async for event in events_async:
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(part.text)
        
        print("\n")


async def test_multi_agent():
    """Test the multi-agent system (parallel + sequential)"""
    print("\n" + "="*100)
    print("TEST 2: Multi-Agent System (Parallel Research + Occasion Specialist)")
    print("="*100)
    
    # Initialize session service
    session_service = InMemorySessionService()
    
    # Create session
    session = await session_service.create_session(
        state={},
        app_name='gift_test_multi',
        user_id='test_user'
    )
    
    # Complex query for multi-agent
    complex_query = """
    I'm looking for a meaningful wedding gift for my best friend. My budget is around 3000-4000 rupees.
    I want something high-quality with good ratings and decent discount. 
    They're adults who love technology and home gadgets.
    """
    
    print(f"\n{'─'*100}")
    print(f"Complex Query: {complex_query.strip()}")
    print('─'*100)
    
    runner = Runner(
        app_name='gift_test_multi',
        agent=root_gift_agent,
        session_service=session_service,
    )
    
    content = types.Content(
        role='user',
        parts=[types.Part(text=complex_query)]
    )
    
    # Run multi-agent system
    events_async = runner.run_async(
        session_id=session.id,
        user_id=session.user_id,
        new_message=content
    )
    
    async for event in events_async:
        if hasattr(event, 'content') and hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    print(part.text)
    
    print("\n")


async def main():
    """Run all tests"""
    print("\n🎁 GIFT RECOMMENDATION AGENT SYSTEM - TEST SUITE 🎁\n")
    
    # Test simple agent
    await test_simple_agent()
    
    # Wait a moment between tests
    await asyncio.sleep(2)
    
    # Test multi-agent system
    await test_multi_agent()
    
    print("\n" + "="*100)
    print("✅ All tests completed!")
    print("="*100)


if __name__ == "__main__":
    asyncio.run(main())
