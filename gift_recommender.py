"""
Gift Recommendation System using ChromaDB
Recommends products from Amazon dataset based on budget, occasion, age, rating, and discount
"""
import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import List, Dict
import re


class GiftRecommender:
    def __init__(self, csv_path: str = "amazon.csv"):
        """Initialize the gift recommender with ChromaDB"""
        self.csv_path = csv_path
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        self.collection = None
        self.df = None
        
    def parse_price(self, price_str: str) -> float:
        """Convert price string to float (handles ₹ symbol and commas)"""
        if pd.isna(price_str) or price_str == '':
            return 0.0
        # Remove ₹ symbol and commas
        price_clean = re.sub(r'[₹,]', '', str(price_str))
        try:
            return float(price_clean)
        except:
            return 0.0
    
    def parse_discount(self, discount_str: str) -> float:
        """Convert discount percentage to float"""
        if pd.isna(discount_str) or discount_str == '':
            return 0.0
        # Remove % symbol
        discount_clean = re.sub(r'%', '', str(discount_str))
        try:
            return float(discount_clean)
        except:
            return 0.0
    
    def parse_rating(self, rating_str: str) -> float:
        """Convert rating to float"""
        if pd.isna(rating_str) or rating_str == '':
            return 0.0
        try:
            return float(rating_str)
        except:
            return 0.0
    
    def load_data(self):
        """Load CSV data and create ChromaDB collection"""
        print("📊 Loading Amazon product data...")
        self.df = pd.read_csv(self.csv_path)
        
        # Parse numeric columns
        self.df['discounted_price_num'] = self.df['discounted_price'].apply(self.parse_price)
        self.df['actual_price_num'] = self.df['actual_price'].apply(self.parse_price)
        self.df['discount_num'] = self.df['discount_percentage'].apply(self.parse_discount)
        self.df['rating_num'] = self.df['rating'].apply(self.parse_rating)
        
        # Filter out products with invalid data
        self.df = self.df[
            (self.df['discounted_price_num'] > 0) & 
            (self.df['rating_num'] > 0)
        ].copy()
        
        print(f"✅ Loaded {len(self.df)} valid products")
        
        # Create or get collection
        try:
            self.client.delete_collection(name="amazon_products")
        except:
            pass
        
        self.collection = self.client.create_collection(
            name="amazon_products",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Prepare documents for embedding
        print("🔄 Creating embeddings and storing in ChromaDB...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in self.df.iterrows():
            # Create rich text representation for embedding
            doc_text = f"""
            Product: {row['product_name']}
            Category: {row['category']}
            Price: ₹{row['discounted_price_num']:.0f}
            Discount: {row['discount_num']:.0f}%
            Rating: {row['rating_num']:.1f}/5
            Description: {str(row['about_product'])[:500]}
            """
            
            documents.append(doc_text)
            
            # Store metadata for filtering and retrieval
            metadatas.append({
                'product_id': str(row['product_id']),
                'product_name': str(row['product_name'])[:500],
                'category': str(row['category'])[:200],
                'price': float(row['discounted_price_num']),
                'discount': float(row['discount_num']),
                'rating': float(row['rating_num']),
                'about_product': str(row['about_product'])[:1000] if pd.notna(row['about_product']) else '',
                'product_link': str(row['product_link']) if pd.notna(row['product_link']) else ''
            })
            
            ids.append(f"product_{idx}")
            
            # Add in batches to avoid memory issues
            if len(documents) >= 100:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                documents = []
                metadatas = []
                ids = []
        
        # Add remaining documents
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
        
        print("✅ Data loaded into ChromaDB successfully!")
    
    def recommend_gifts(
        self,
        budget: float,
        occasion: str = "",
        age: str = "",
        min_rating: float = 3.5,
        min_discount: float = 0,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Recommend top gifts based on criteria
        
        Args:
            budget: Maximum price willing to pay
            occasion: Occasion for the gift (birthday, anniversary, festive, etc.)
            age: Age group (kid, teenager, adult, senior)
            min_rating: Minimum rating filter
            min_discount: Minimum discount percentage
            n_results: Number of recommendations to return
        
        Returns:
            List of recommended products with details
        """
        if self.collection is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Build search query from inputs
        query_parts = []
        
        if occasion:
            query_parts.append(f"gift for {occasion}")
        if age:
            query_parts.append(f"suitable for {age}")
        
        # Add some context about gift-giving
        query_parts.append("gift present quality popular recommended")
        
        query_text = " ".join(query_parts)
        
        # Search with filters
        # ChromaDB filtering: price <= budget, rating >= min_rating, discount >= min_discount
        where_filter = {
            "$and": [
                {"price": {"$lte": budget}},
                {"rating": {"$gte": min_rating}},
                {"discount": {"$gte": min_discount}}
            ]
        }
        
        print(f"\n🔍 Searching for gifts with:")
        print(f"   💰 Budget: ₹{budget}")
        print(f"   🎉 Occasion: {occasion if occasion else 'Any'}")
        print(f"   👤 Age Group: {age if age else 'Any'}")
        print(f"   ⭐ Min Rating: {min_rating}")
        print(f"   🏷️  Min Discount: {min_discount}%")
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=min(n_results * 3, 50),  # Get more to filter further
                where=where_filter
            )
            
            if not results['metadatas'][0]:
                print("\n❌ No products found matching the criteria. Try relaxing some filters.")
                return []
            
            # Process and rank results
            recommendations = []
            seen_products = set()
            
            for i, metadata in enumerate(results['metadatas'][0]):
                # Avoid duplicates
                product_id = metadata['product_id']
                if product_id in seen_products:
                    continue
                seen_products.add(product_id)
                
                # Calculate a composite score for ranking
                # Factors: rating, discount, price fit (closer to budget is better)
                rating_score = metadata['rating'] / 5.0  # Normalize to 0-1
                discount_score = metadata['discount'] / 100.0  # Normalize to 0-1
                price_fit_score = 1 - (abs(budget - metadata['price']) / budget)  # Closer to budget is better
                
                # Weighted composite score
                composite_score = (
                    rating_score * 0.4 +
                    discount_score * 0.3 +
                    price_fit_score * 0.3
                )
                
                recommendations.append({
                    'product_name': metadata['product_name'],
                    'category': metadata['category'],
                    'price': metadata['price'],
                    'discount': metadata['discount'],
                    'rating': metadata['rating'],
                    'about_product': metadata['about_product'],
                    'product_link': metadata['product_link'],
                    'score': composite_score
                })
                
                if len(recommendations) >= n_results:
                    break
            
            # Sort by composite score
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            return recommendations[:n_results]
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return []
    
    def display_recommendations(self, recommendations: List[Dict]):
        """Display recommendations in a nice format"""
        if not recommendations:
            print("\n😞 No recommendations found. Try adjusting your criteria.")
            return
        
        print(f"\n🎁 Top {len(recommendations)} Gift Recommendations:\n")
        print("=" * 100)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n#{i} - {rec['product_name'][:80]}")
            print(f"   📂 Category: {rec['category']}")
            print(f"   💰 Price: ₹{rec['price']:.0f}")
            print(f"   🏷️  Discount: {rec['discount']:.0f}%")
            print(f"   ⭐ Rating: {rec['rating']:.1f}/5.0")
            print(f"   📊 Match Score: {rec['score']:.2f}")
            
            # Show brief description
            if rec['about_product']:
                desc = rec['about_product'][:200].replace('\n', ' ').strip()
                print(f"   📝 About: {desc}...")
            
            if rec['product_link']:
                print(f"   🔗 Link: {rec['product_link']}")
            
            print("-" * 100)


def main():
    """Example usage"""
    # Initialize recommender
    recommender = GiftRecommender("amazon.csv")
    
    # Load data into ChromaDB
    recommender.load_data()
    
    # Example 1: Birthday gift for teenager, budget ₹1000
    print("\n" + "="*100)
    print("EXAMPLE 1: Birthday Gift for Teenager")
    print("="*100)
    recommendations = recommender.recommend_gifts(
        budget=1000,
        occasion="birthday",
        age="teenager",
        min_rating=4.0,
        min_discount=30
    )
    recommender.display_recommendations(recommendations)
    
    # Example 2: Anniversary gift, higher budget
    print("\n\n" + "="*100)
    print("EXAMPLE 2: Anniversary Gift")
    print("="*100)
    recommendations = recommender.recommend_gifts(
        budget=5000,
        occasion="anniversary",
        age="adult",
        min_rating=4.2,
        min_discount=20
    )
    recommender.display_recommendations(recommendations)
    
    # Example 3: Budget-friendly gift with high discount
    print("\n\n" + "="*100)
    print("EXAMPLE 3: Budget Gift with High Discount")
    print("="*100)
    recommendations = recommender.recommend_gifts(
        budget=500,
        occasion="festive",
        age="any",
        min_rating=3.8,
        min_discount=50
    )
    recommender.display_recommendations(recommendations)


if __name__ == "__main__":
    main()
