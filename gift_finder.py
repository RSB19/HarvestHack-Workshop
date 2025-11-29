"""
Interactive Gift Finder
Run this script to get personalized gift recommendations based on your criteria
"""
from gift_recommender import GiftRecommender


def main():
    print("\n" + "="*100)
    print("🎁 AMAZON GIFT FINDER - Powered by ChromaDB 🎁")
    print("="*100)
    
    # Initialize and load data
    print("\n⏳ Initializing the gift recommendation system...")
    recommender = GiftRecommender("amazon.csv")
    recommender.load_data()
    
    print("\n✅ System ready! Let's find the perfect gift!\n")
    
    while True:
        print("\n" + "-"*100)
        print("Enter your gift criteria:")
        print("-"*100)
        
        # Get user inputs
        try:
            budget = float(input("💰 Maximum budget (in ₹): "))
        except ValueError:
            print("❌ Invalid budget. Please enter a number.")
            continue
        
        occasion = input("🎉 Occasion (birthday/anniversary/festive/graduation/wedding/any): ").strip()
        age = input("👤 Age group (kid/teenager/adult/senior/any): ").strip()
        
        try:
            min_rating = float(input("⭐ Minimum rating (0-5, recommended 4.0): ") or "4.0")
        except ValueError:
            min_rating = 4.0
        
        try:
            min_discount = float(input("🏷️  Minimum discount percentage (0-100, recommended 20): ") or "20")
        except ValueError:
            min_discount = 20
        
        try:
            n_results = int(input("📊 Number of recommendations (default 5): ") or "5")
        except ValueError:
            n_results = 5
        
        # Get recommendations
        recommendations = recommender.recommend_gifts(
            budget=budget,
            occasion=occasion if occasion.lower() != 'any' else '',
            age=age if age.lower() != 'any' else '',
            min_rating=min_rating,
            min_discount=min_discount,
            n_results=n_results
        )
        
        # Display results
        recommender.display_recommendations(recommendations)
        
        # Ask to continue
        print("\n" + "="*100)
        continue_search = input("\n🔄 Search for more gifts? (yes/no): ").strip().lower()
        if continue_search not in ['yes', 'y']:
            print("\n👋 Thank you for using Amazon Gift Finder! Happy gifting! 🎁\n")
            break


if __name__ == "__main__":
    main()
