"""
Gift Recommendation Agent System using Google ADK
Integrates with ChromaDB-based gift recommender to provide intelligent gift suggestions
"""
from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from gift_recommender import GiftRecommender
import re

# Initialize the gift recommender globally
_gift_recommender = None

def initialize_gift_database(csv_path: str) -> str:
    """
    Initialize the ChromaDB gift recommendation database.
    
    Args:
        csv_path: Path to the Amazon products CSV file
    
    Returns:
        Status message about database initialization
    """
    global _gift_recommender
    
    try:
        # Default to amazon.csv if no path provided
        if not csv_path:
            csv_path = "amazon.csv"
        
        if _gift_recommender is None:
            _gift_recommender = GiftRecommender(csv_path)
            _gift_recommender.load_data()
            return "✅ Gift database initialized successfully with 1,464+ products from Amazon!"
        else:
            return "✅ Gift database already initialized and ready to use!"
    except Exception as e:
        return f"❌ Error initializing database: {str(e)}"


def search_gifts_by_criteria(
    budget: float,
    occasion: str,
    age_group: str,
    min_rating: float,
    min_discount: float,
    num_results: int
) -> str:
    """
    Search for gift recommendations based on multiple criteria.
    
    Args:
        budget: Maximum budget in rupees (₹)
        occasion: Gift occasion (birthday, anniversary, festive, graduation, wedding, etc.)
        age_group: Target age group (kid, teenager, adult, senior)
        min_rating: Minimum product rating (0-5 scale)
        min_discount: Minimum discount percentage required
        num_results: Number of recommendations to return
    
    Returns:
        Formatted list of gift recommendations
    """
    global _gift_recommender
    
    if _gift_recommender is None:
        initialize_gift_database("amazon.csv")
    
    # Handle empty strings as defaults
    if not occasion:
        occasion = ""
    if not age_group:
        age_group = ""
    
    try:
        recommendations = _gift_recommender.recommend_gifts(
            budget=budget,
            occasion=occasion,
            age=age_group,
            min_rating=min_rating,
            min_discount=min_discount,
            n_results=num_results
        )
        
        if not recommendations:
            return f"No gifts found matching criteria: Budget ₹{budget}, Occasion: {occasion or 'Any'}, Age: {age_group or 'Any'}, Min Rating: {min_rating}, Min Discount: {min_discount}%. Try relaxing some filters."
        
        result = f"🎁 Found {len(recommendations)} Gift Recommendations:\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. **{rec['product_name'][:100]}**\n"
            result += f"   💰 Price: ₹{rec['price']:.0f} (Save {rec['discount']:.0f}%)\n"
            result += f"   ⭐ Rating: {rec['rating']:.1f}/5.0\n"
            result += f"   📂 Category: {rec['category']}\n"
            
            if rec['about_product']:
                desc = rec['about_product'][:150].replace('\n', ' ').strip()
                result += f"   📝 {desc}...\n"
            
            result += f"   🔗 {rec['product_link']}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error searching gifts: {str(e)}"


def find_budget_friendly_gifts(max_budget: float, min_discount: float) -> str:
    """
    Find highly discounted, budget-friendly gift options.
    
    Args:
        max_budget: Maximum budget in rupees
        min_discount: Minimum discount percentage
    
    Returns:
        List of budget-friendly gift options
    """
    global _gift_recommender
    
    if _gift_recommender is None:
        initialize_gift_database("amazon.csv")
    
    try:
        recommendations = _gift_recommender.recommend_gifts(
            budget=max_budget,
            occasion="",
            age="",
            min_rating=3.8,
            min_discount=min_discount,
            n_results=5
        )
        
        if not recommendations:
            return f"No budget-friendly gifts found under ₹{max_budget} with {min_discount}% discount."
        
        result = f"💸 Budget-Friendly Gifts Under ₹{max_budget} (Min {min_discount}% Off):\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            savings = rec['price'] / (1 - rec['discount']/100) - rec['price']
            result += f"{i}. {rec['product_name'][:80]}\n"
            result += f"   Price: ₹{rec['price']:.0f} (You save: ₹{savings:.0f})\n"
            result += f"   Discount: {rec['discount']:.0f}% | Rating: {rec['rating']:.1f}⭐\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error finding budget gifts: {str(e)}"


def find_premium_gifts(min_budget: float, occasion: str) -> str:
    """
    Find premium, high-quality gift options for special occasions.
    
    Args:
        min_budget: Minimum budget for premium gifts
        occasion: Special occasion (anniversary, wedding, etc.)
    
    Returns:
        List of premium gift recommendations
    """
    global _gift_recommender
    
    if _gift_recommender is None:
        initialize_gift_database("amazon.csv")
    
    # Handle empty occasion string
    if not occasion:
        occasion = ""
    
    try:
        # For premium gifts, we want higher budget items with excellent ratings
        recommendations = _gift_recommender.recommend_gifts(
            budget=min_budget * 3,  # Allow higher range
            occasion=occasion,
            age="adult",
            min_rating=4.2,
            min_discount=15,
            n_results=5
        )
        
        # Filter to only show items above minimum budget
        premium_recs = [r for r in recommendations if r['price'] >= min_budget]
        
        if not premium_recs:
            return f"No premium gifts found above ₹{min_budget}. Try lowering the budget threshold."
        
        result = f"✨ Premium Gifts (Budget ₹{min_budget}+):\n\n"
        
        for i, rec in enumerate(premium_recs[:5], 1):
            result += f"{i}. {rec['product_name'][:80]}\n"
            result += f"   💎 Price: ₹{rec['price']:.0f}\n"
            result += f"   ⭐ Rating: {rec['rating']:.1f}/5.0 | Discount: {rec['discount']:.0f}%\n"
            result += f"   📂 {rec['category']}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error finding premium gifts: {str(e)}"


def get_gift_recommendations_by_occasion(occasion: str, budget: float) -> str:
    """
    Get gift recommendations tailored for a specific occasion.
    
    Args:
        occasion: The occasion (birthday, anniversary, festive, graduation, wedding, etc.)
        budget: Budget in rupees
    
    Returns:
        Occasion-specific gift recommendations
    """
    global _gift_recommender
    
    if _gift_recommender is None:
        initialize_gift_database("amazon.csv")
    
    try:
        recommendations = _gift_recommender.recommend_gifts(
            budget=budget,
            occasion=occasion,
            age="",
            min_rating=4.0,
            min_discount=20,
            n_results=5
        )
        
        if not recommendations:
            return f"No gifts found for {occasion} within budget ₹{budget}."
        
        result = f"🎉 Perfect Gifts for {occasion.title()} (Budget: ₹{budget}):\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. {rec['product_name'][:90]}\n"
            result += f"   ₹{rec['price']:.0f} | {rec['discount']:.0f}% off | {rec['rating']:.1f}⭐\n"
            result += f"   Category: {rec['category']}\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error finding gifts for {occasion}: {str(e)}"


def get_gift_recommendations_by_age(age_group: str, budget: float) -> str:
    """
    Get gift recommendations tailored for a specific age group.
    
    Args:
        age_group: Target age (kid, teenager, adult, senior)
        budget: Budget in rupees
    
    Returns:
        Age-appropriate gift recommendations
    """
    global _gift_recommender
    
    if _gift_recommender is None:
        initialize_gift_database("amazon.csv")
    
    try:
        recommendations = _gift_recommender.recommend_gifts(
            budget=budget,
            occasion="",
            age=age_group,
            min_rating=4.0,
            min_discount=25,
            n_results=5
        )
        
        if not recommendations:
            return f"No gifts found for {age_group} within budget ₹{budget}."
        
        result = f"👤 Perfect Gifts for {age_group.title()} (Budget: ₹{budget}):\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            result += f"{i}. {rec['product_name'][:90]}\n"
            result += f"   ₹{rec['price']:.0f} | Save {rec['discount']:.0f}% | {rec['rating']:.1f}⭐\n\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error finding gifts for {age_group}: {str(e)}"


# ===== SPECIALIZED GIFT AGENTS =====

# Agent 1: Gift Search Agent - Handles general gift searches
gift_search_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    name='gift_search_agent',
    description='Searches for gifts based on budget, occasion, age, and other criteria',
    instruction="""You are a Gift Search Agent that helps users find perfect gifts from the Amazon product database.

Your responsibilities:
- Use initialize_gift_database to set up the database (call this first if not initialized)
- Use search_gifts_by_criteria to find gifts based on user requirements
- Extract budget, occasion, age group, and preferences from user queries
- Provide clear, personalized recommendations
- Explain why each gift is a good match for the criteria

When users ask for gifts:
1. Understand their budget (convert to numeric value)
2. Identify the occasion (birthday, anniversary, festive, etc.)
3. Determine the recipient's age group
4. Call search_gifts_by_criteria with appropriate parameters
5. Present results in a friendly, helpful manner

Be conversational and helpful!""",
    tools=[initialize_gift_database, search_gifts_by_criteria],
    output_key="gift_search_results",
)

# Agent 2: Budget Advisor Agent - Specializes in budget-conscious recommendations
budget_advisor_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    name='budget_advisor_agent',
    description='Finds budget-friendly and premium gift options based on price constraints',
    instruction="""You are a Budget Advisor Agent specializing in finding the best value gifts.

Your responsibilities:
- Use find_budget_friendly_gifts for users looking for deals and discounts
- Use find_premium_gifts for users wanting high-end, quality gifts
- Help users understand pricing and savings
- Suggest budget alternatives when needed

When advising on budget:
1. Determine if the user wants budget-friendly or premium options
2. Identify their price range
3. Call the appropriate tool
4. Highlight savings and value propositions
5. Explain why these gifts offer good value

Focus on helping users maximize their budget!""",
    tools=[find_budget_friendly_gifts, find_premium_gifts],
    output_key="budget_recommendations",
)

# Agent 3: Occasion Specialist Agent - Focuses on occasion-specific recommendations
occasion_specialist_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    name='occasion_specialist_agent',
    description='Provides occasion-specific and age-appropriate gift recommendations',
    instruction="""You are an Occasion Specialist Agent that understands the nuances of different celebrations.

Your responsibilities:
- Use get_gift_recommendations_by_occasion for event-specific gifts
- Use get_gift_recommendations_by_age for age-appropriate selections
- Consider cultural and social context of occasions
- Provide thoughtful recommendations that match the event

When helping with occasions:
1. Identify the specific occasion or recipient age
2. Understand the relationship and context
3. Call the appropriate tool
4. Explain why each gift suits the occasion/age group
5. Provide additional gifting tips

Make every occasion special with perfect gift matches!""",
    tools=[get_gift_recommendations_by_occasion, get_gift_recommendations_by_age],
    output_key="occasion_recommendations",
)

# ===== COORDINATOR AGENTS =====

# Parallel Gift Research Agent - Runs search and budget analysis simultaneously
gift_research_coordinator = ParallelAgent(
    name='gift_research_coordinator',
    sub_agents=[gift_search_agent, budget_advisor_agent],
    description='Simultaneously searches for gifts and analyzes budget options',
)

# Main Gift Assistant - Sequential workflow for complete gift recommendation
root_gift_agent = SequentialAgent(
    name='gift_assistant_system',
    sub_agents=[gift_research_coordinator, occasion_specialist_agent],
    description='Complete gift recommendation system: searches products, analyzes budgets, and provides occasion-specific suggestions',
)

# Alternative: Simple single-agent approach for direct queries
simple_gift_agent = LlmAgent(
    model='gemini-2.0-flash-exp',
    name='smart_gift_assistant',
    description='Intelligent gift recommendation assistant with access to ChromaDB product database',
    instruction="""You are a Smart Gift Assistant powered by a comprehensive Amazon product database.

Your capabilities:
- Search gifts by budget, occasion, age, rating, and discount criteria
- Find budget-friendly options with high discounts
- Recommend premium gifts for special occasions
- Provide occasion-specific and age-appropriate suggestions

How to help users:
1. FIRST: Always initialize the database using initialize_gift_database()
2. Understand what the user is looking for (occasion, recipient, budget)
3. Choose the most appropriate tool based on their needs:
   - search_gifts_by_criteria: General searches with multiple criteria
   - find_budget_friendly_gifts: When they want deals and discounts
   - find_premium_gifts: For high-end, quality gifts
   - get_gift_recommendations_by_occasion: For specific events
   - get_gift_recommendations_by_age: For age-specific gifts
4. Present results clearly with key details (price, rating, discount)
5. Explain why each recommendation is a good match
6. Offer to refine search if needed

Be friendly, helpful, and make gift-giving easy and enjoyable!""",
    tools=[
        initialize_gift_database,
        search_gifts_by_criteria,
        find_budget_friendly_gifts,
        find_premium_gifts,
        get_gift_recommendations_by_occasion,
        get_gift_recommendations_by_age
    ],
)

# Alias for ADK web server compatibility
root_agent = root_gift_agent
