# 🎁 Amazon Gift Recommendation System

A smart gift finder that uses **ChromaDB** and semantic search to recommend the perfect products from the Amazon dataset based on your criteria.

## 🌟 Features

- **Semantic Search**: Uses AI-powered embeddings to understand gift context
- **Multi-Criteria Filtering**: Filter by budget, occasion, age, rating, and discount
- **Smart Ranking**: Products ranked by composite score considering:
  - Product rating (40% weight)
  - Discount percentage (30% weight)  
  - Price fit to budget (30% weight)
- **ChromaDB Integration**: Efficient vector storage and similarity search

## 📋 Criteria Inputs

The system accepts the following inputs:

1. **Budget** (₹): Maximum price you're willing to pay
2. **Occasion**: birthday, anniversary, festive, graduation, wedding, etc.
3. **Age Group**: kid, teenager, adult, senior
4. **Min Rating**: Minimum product rating (0-5 scale)
5. **Min Discount**: Minimum discount percentage required

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install chromadb pandas

# Or use the requirements file
pip install -r requirements.txt
```

### Run Interactive Gift Finder

```bash
python gift_finder.py
```

This will start an interactive session where you can enter your criteria and get personalized recommendations.

### Run Demo Examples

```bash
python gift_recommender.py
```

This runs pre-configured examples showing different use cases.

## 💡 Usage Examples

### Example 1: Birthday Gift for Teenager (Budget ₹1000)

```python
from gift_recommender import GiftRecommender

recommender = GiftRecommender("amazon.csv")
recommender.load_data()

recommendations = recommender.recommend_gifts(
    budget=1000,
    occasion="birthday",
    age="teenager",
    min_rating=4.0,
    min_discount=30,
    n_results=5
)

recommender.display_recommendations(recommendations)
```

### Example 2: Anniversary Gift (Budget ₹5000)

```python
recommendations = recommender.recommend_gifts(
    budget=5000,
    occasion="anniversary",
    age="adult",
    min_rating=4.2,
    min_discount=20
)
```

### Example 3: High Discount Budget Gift (Budget ₹500)

```python
recommendations = recommender.recommend_gifts(
    budget=500,
    occasion="festive",
    age="any",
    min_rating=3.8,
    min_discount=50
)
```

## 🔧 How It Works

1. **Data Loading**: Reads Amazon product CSV and parses prices, ratings, and discounts
2. **Embedding Creation**: Creates semantic embeddings for each product using product name, category, price, and description
3. **ChromaDB Storage**: Stores embeddings and metadata in ChromaDB collection
4. **Query Processing**: Builds search query from user inputs (occasion + age + gift context)
5. **Filtering**: Applies hard filters (budget, min rating, min discount)
6. **Ranking**: Calculates composite score and ranks results
7. **Results**: Returns top N products matching criteria

## 📊 Composite Scoring Formula

```
composite_score = (rating/5.0) * 0.4 
                + (discount/100.0) * 0.3 
                + price_fit_score * 0.3

where:
  price_fit_score = 1 - abs(budget - price) / budget
```

Products closer to the budget with higher ratings and better discounts score higher.

## 📁 File Structure

```
HarvestHack-Workshop/
├── amazon.csv                  # Amazon product dataset
├── gift_recommender.py         # Core recommendation system
├── gift_finder.py              # Interactive CLI interface
├── GIFT_FINDER_README.md       # This file
└── requirements.txt            # Python dependencies
```

## 🎯 CSV Columns Used

- `product_name`: Product title
- `category`: Product category
- `discounted_price`: Current selling price
- `actual_price`: Original price
- `discount_percentage`: Discount %
- `rating`: Product rating (0-5)
- `about_product`: Product description
- `product_link`: Amazon product URL

## 🛠️ Customization

### Adjust Scoring Weights

Edit the `recommend_gifts()` method in `gift_recommender.py`:

```python
composite_score = (
    rating_score * 0.4 +      # Rating weight
    discount_score * 0.3 +    # Discount weight
    price_fit_score * 0.3     # Budget fit weight
)
```

### Add More Filters

You can extend the ChromaDB filter:

```python
where_filter = {
    "$and": [
        {"price": {"$lte": budget}},
        {"rating": {"$gte": min_rating}},
        {"discount": {"$gte": min_discount}},
        # Add more filters here
    ]
}
```

## 🤝 Contributing

Feel free to enhance the system by:
- Adding more intelligent occasion mapping
- Implementing category-based filtering
- Adding price range recommendations
- Improving the scoring algorithm

## 📝 License

This project is for educational purposes as part of HarvestHack Workshop.

---

**Happy Gift Finding! 🎁✨**
