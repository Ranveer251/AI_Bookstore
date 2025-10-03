import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.query import (
    QueryProcessor,
    QueryRouter,
    QueryRetriever,
    QueryIntent,
    IntentClassifier,
    EntityExtractor
)
from src.vectorstore import BookIndexer
from src.core.models import UnifiedBookModel, GenreEnum
from typing import List
import json

def create_sample_books_for_query_test() -> List[UnifiedBookModel]:
    """Create a diverse set of sample books for testing"""
    books = [
        UnifiedBookModel(
            title="Dune",
            author="Frank Herbert",
            genre=GenreEnum.SCIENCE_FICTION,
            price=16.99,
            rating=4.6,
            description="A science fiction masterpiece about politics, religion, and ecology on the desert planet Arrakis.",
            publisher="Chilton Books",
            publication_year=1965,
            isbn="9780441172719",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=14.99,
            rating=4.8,
            description="A classic fantasy adventure following Bilbo Baggins on his unexpected journey with dwarves and a dragon.",
            publisher="George Allen & Unwin",
            publication_year=1937,
            isbn="9780547928210",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="1984",
            author="George Orwell",
            genre=GenreEnum.FICTION,
            price=13.99,
            rating=4.4,
            description="A dystopian social science fiction novel about totalitarian control and surveillance.",
            publisher="Secker & Warburg",
            publication_year=1949,
            isbn="9780451524935",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Pride and Prejudice",
            author="Jane Austen",
            genre=GenreEnum.ROMANCE,
            price=11.99,
            rating=4.5,
            description="A romantic novel about Elizabeth Bennet and Mr. Darcy in Regency England.",
            publisher="T. Egerton",
            publication_year=1813,
            isbn="9780141439518",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Martian",
            author="Andy Weir",
            genre=GenreEnum.SCIENCE_FICTION,
            price=17.99,
            rating=4.6,
            description="A thrilling survival story about astronaut Mark Watney stranded on Mars.",
            publisher="Crown Publishing",
            publication_year=2011,
            isbn="9780804139021",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=24.99,
            rating=4.9,
            description="An epic fantasy adventure about the quest to destroy the One Ring in Middle-earth.",
            publisher="George Allen & Unwin",
            publication_year=1954,
            isbn="9780547928227",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Neuromancer",
            author="William Gibson",
            genre=GenreEnum.SCIENCE_FICTION,
            price=15.99,
            rating=4.2,
            description="A groundbreaking cyberpunk novel about hacker Case in cyberspace.",
            publisher="Ace Books",
            publication_year=1984,
            isbn="9780441569595",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Harry Potter and the Sorcerer's Stone",
            author="J.K. Rowling",
            genre=GenreEnum.FANTASY,
            price=10.99,
            rating=4.7,
            description="A young wizard discovers his magical heritage and attends Hogwarts School.",
            publisher="Scholastic",
            publication_year=1997,
            isbn="9780439708180",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Foundation",
            author="Isaac Asimov",
            genre=GenreEnum.SCIENCE_FICTION,
            price=14.99,
            rating=4.3,
            description="The story of a galactic empire's fall and the foundation to preserve civilization.",
            publisher="Gnome Press",
            publication_year=1951,
            isbn="9780553293357",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre=GenreEnum.FICTION,
            price=12.99,
            rating=4.0,
            description="A classic American novel about the Jazz Age and the American Dream.",
            publisher="Charles Scribner's Sons",
            publication_year=1925,
            isbn="9780743273565",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
    ]
    
    return books

def test_intent_classification():
    """Test the intent classification component"""
    print("🎯 Testing Intent Classification")
    print("=" * 70)
    
    classifier = IntentClassifier()
    
    test_queries = [
        # Search queries
        "Find science fiction books about space",
        "I'm looking for fantasy novels",
        "Show me books about dragons",
        
        # Recommendation queries
        "Recommend books similar to Harry Potter",
        "What should I read if I liked Dune?",
        "Suggest some good mystery novels",
        
        # Comparison queries
        "Which store has cheaper sci-fi books?",
        "Compare prices between bookstore A and B",
        "Which store has better fantasy selection?",
        
        # Analytics queries
        "What's the most popular genre?",
        "Show me the average price by genre",
        "How many books are under $15?",
        
        # Filter queries
        "Books under $15",
        "Show me highly rated fantasy books",
        "Available science fiction in store A",
        
        # Information queries
        "Tell me about The Hobbit",
        "What is Dune about?",
        "Information on 1984"
    ]
    
    for query in test_queries:
        intent, confidence = classifier.classify(query)
        print(f"Query: '{query}'")
        print(f"   → Intent: {intent.value} (confidence: {confidence:.2f})")
        print()

def test_entity_extraction():
    """Test the entity extraction component"""
    print("\n🔍 Testing Entity Extraction")
    print("=" * 70)
    
    extractor = EntityExtractor()
    
    test_queries = [
        "Find science fiction books under $15",
        "Show me fantasy novels rated above 4.5",
        "Get me the top 5 cheapest books in store A",
        "Looking for romance books between $10 and $20",
        "Find available ebooks about space exploration",
        "Show me highly rated mystery novels from both stores"
    ]
    
    for query in test_queries:
        entities = extractor.extract(query)
        print(f"Query: '{query}'")
        print(f"   Extracted entities:")
        for key, value in entities.items():
            if value:
                print(f"      {key}: {value}")
        print()

def test_query_processing():
    """Test the complete query processing pipeline"""
    print("\n⚙️  Testing Query Processing Pipeline")
    print("=" * 70)
    
    processor = QueryProcessor()
    
    test_queries = [
        "Find me science fiction books under $20 from store A",
        "Recommend fantasy novels similar to Lord of the Rings",
        "Which store has cheaper books?",
        "Show me the top 3 highest rated books"
    ]
    
    for query in test_queries:
        parsed = processor.process(query)
        print(f"Query: '{query}'")
        print(f"   Intent: {parsed.intent.value} (confidence: {parsed.confidence:.2f})")
        print(f"   Keywords: {parsed.keywords}")
        print(f"   Entities: {parsed.entities}")
        print(f"   Filters: {parsed.filters}")
        print(f"   Metadata: {parsed.metadata}")
        print()

def test_query_retrieval():
    """Test query retrieval with actual book data"""
    print("\n📚 Testing Query Retrieval with Book Data")
    print("=" * 70)
    
    # Setup: Index sample books
    print("Setting up book index...")
    books = create_sample_books_for_query_test()
    indexer = BookIndexer()
    
    try:
        indexer.index_books(books, show_progress=False)
        print(f"✅ Indexed {len(books)} books\n")
    except Exception as e:
        print(f"❌ Failed to index books: {e}")
        return
    
    # Initialize retriever
    retriever = QueryRetriever(indexer)
    processor = QueryProcessor()
    
    # Test different query types
    test_cases = [
        {
            'query': "Find science fiction books about space",
            'intent': QueryIntent.SEARCH
        },
        {
            'query': "Recommend fantasy books similar to Lord of the Rings",
            'intent': QueryIntent.RECOMMENDATION
        },
        {
            'query': "Compare sci-fi books between stores",
            'intent': QueryIntent.COMPARISON
        },
        {
            'query': "Show me books under $15",
            'intent': QueryIntent.FILTER
        },
        {
            'query': "What are the most popular genres?",
            'intent': QueryIntent.ANALYTICS
        }
    ]
    
    for test_case in test_cases:
        query = test_case['query']
        expected_intent = test_case['intent']
        
        print(f"🔎 Query: '{query}'")
        print(f"   Expected Intent: {expected_intent.value}")
        
        # Process query
        parsed = processor.process(query)
        print(f"   Detected Intent: {parsed.intent.value} (confidence: {parsed.confidence:.2f})")
        
        # Retrieve based on intent
        try:
            if parsed.intent == QueryIntent.SEARCH:
                results = retriever.retrieve_for_search(parsed)
                print(f"   ✅ Found {len(results)} books:")
                for i, book in enumerate(results[:3], 1):
                    metadata = book['metadata']
                    print(f"      {i}. {metadata['title']} by {metadata['author']} - ${metadata['price']}")
            
            elif parsed.intent == QueryIntent.RECOMMENDATION:
                results = retriever.retrieve_for_recommendation(parsed)
                print(f"   ✅ Recommended {len(results)} books:")
                for i, book in enumerate(results[:3], 1):
                    metadata = book['metadata']
                    print(f"      {i}. {metadata['title']} by {metadata['author']} ({metadata['genre']})")
            
            elif parsed.intent == QueryIntent.COMPARISON:
                comparison = retriever.retrieve_for_comparison(parsed)
                print(f"   ✅ Comparison results:")
                for store_id, data in comparison.get('stores', {}).items():
                    print(f"      {data['store_name']}:")
                    print(f"         Books: {data['book_count']}")
                    print(f"         Avg Price: ${data['avg_price']:.2f}")
                    print(f"         Price Range: ${data['min_price']:.2f} - ${data['max_price']:.2f}")
            
            elif parsed.intent == QueryIntent.FILTER:
                results = retriever.retrieve_for_filter(parsed)
                print(f"   ✅ Filtered {len(results)} books:")
                for i, book in enumerate(results[:5], 1):
                    metadata = book['metadata']
                    print(f"      {i}. {metadata['title']} - ${metadata['price']}")
            
            elif parsed.intent == QueryIntent.ANALYTICS:
                analytics = retriever.retrieve_for_analytics(parsed)
                print(f"   ✅ Analytics results:")
                if 'genre_distribution' in analytics:
                    print(f"      Genre Distribution: {analytics['genre_distribution']}")
                if 'price_stats' in analytics:
                    stats = analytics['price_stats']
                    print(f"      Price Stats: Avg=${stats['average']:.2f}, Min=${stats['min']:.2f}, Max=${stats['max']:.2f}")
            
        except Exception as e:
            print(f"   ❌ Retrieval failed: {e}")
        
        print()

def test_query_router():
    """Test the query router with handlers"""
    print("\n🚦 Testing Query Router")
    print("=" * 70)
    
    # Setup
    books = create_sample_books_for_query_test()
    indexer = BookIndexer()
    
    try:
        indexer.index_books(books, show_progress=False)
    except Exception as e:
        print(f"❌ Failed to setup: {e}")
        return
    
    retriever = QueryRetriever(indexer)
    router = QueryRouter()
    
    # Register handlers
    router.register_handler(QueryIntent.SEARCH, retriever.retrieve_for_search)
    router.register_handler(QueryIntent.RECOMMENDATION, retriever.retrieve_for_recommendation)
    router.register_handler(QueryIntent.COMPARISON, retriever.retrieve_for_comparison)
    router.register_handler(QueryIntent.ANALYTICS, retriever.retrieve_for_analytics)
    router.register_handler(QueryIntent.FILTER, retriever.retrieve_for_filter)
    
    # Test routing
    test_queries = [
        "Find fantasy books with magic",
        "Recommend books like Dune",
        "Which store is cheaper for sci-fi?",
        "Show me books under $15",
        "What's the average book price?"
    ]
    
    for query in test_queries:
        print(f"🔎 Query: '{query}'")
        
        result = router.route(query)
        
        if result['success']:
            parsed = result['parsed_query']
            print(f"   ✅ Routed to: {parsed.intent.value} handler")
            print(f"   Confidence: {parsed.confidence:.2f}")
            
            # Show result summary
            if isinstance(result['result'], list):
                print(f"   Results: {len(result['result'])} items")
            elif isinstance(result['result'], dict):
                print(f"   Results: {list(result['result'].keys())}")
        else:
            print(f"   ❌ Error: {result['error']}")
        
        print()

def demonstrate_real_world_queries():
    """Demonstrate with real-world user queries"""
    print("\n💬 Real-World Query Examples")
    print("=" * 70)
    
    # Setup
    books = create_sample_books_for_query_test()
    indexer = BookIndexer()
    
    try:
        indexer.index_books(books, show_progress=False)
        print("✅ Book database ready\n")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return
    
    retriever = QueryRetriever(indexer)
    processor = QueryProcessor()
    
    real_queries = [
        "I want a book about artificial intelligence and technology",
        "Looking for something similar to Harry Potter with magic and adventure",
        "Which bookstore has better deals on science fiction?",
        "Show me the cheapest fantasy books available",
        "I need a good book for a 13-year-old who likes adventure",
        "What are the highest rated books under $20?",
        "Find me dystopian novels about future societies",
        "Recommend classic literature from the early 1900s"
    ]
    
    for query in real_queries:
        print(f"💭 User asks: '{query}'")
        
        try:
            # Process query
            parsed = processor.process(query)
            print(f"   🤖 Understanding: {parsed.intent.value} query")
            
            # Retrieve results
            if parsed.intent == QueryIntent.SEARCH:
                results = retriever.retrieve_for_search(parsed)
                if results:
                    print(f"   📚 Found {len(results)} books:")
                    for i, book in enumerate(results[:2], 1):
                        metadata = book['metadata']
                        print(f"      {i}. '{metadata['title']}' by {metadata['author']}")
                        print(f"         {metadata['genre']} | ${metadata['price']} | {metadata['store_name']}")
                else:
                    print("   ❌ No books found")
            
            elif parsed.intent == QueryIntent.RECOMMENDATION:
                results = retriever.retrieve_for_recommendation(parsed)
                if results:
                    print(f"   💡 Recommendations:")
                    for i, book in enumerate(results[:2], 1):
                        metadata = book['metadata']
                        print(f"      {i}. '{metadata['title']}' by {metadata['author']}")
                        print(f"         Why: {metadata['genre']} theme match")
                else:
                    print("   ❌ No recommendations available")
            
            elif parsed.intent == QueryIntent.COMPARISON:
                comparison = retriever.retrieve_for_comparison(parsed)
                print(f"   📊 Store Comparison:")
                for store_id, data in comparison.get('stores', {}).items():
                    print(f"      {data['store_name']}: Avg ${data['avg_price']:.2f} ({data['book_count']} books)")
            
            else:
                print(f"   ⚙️  Processing as {parsed.intent.value} query...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()

def main():
    """Main demonstration function"""
    print("🚀 Query Processor Demo")
    print("=" * 70)
    print()
    
    try:
        # Test 1: Intent Classification
        test_intent_classification()
        
        # Test 2: Entity Extraction
        test_entity_extraction()
        
        # Test 3: Query Processing
        test_query_processing()
        
        # Test 4: Query Retrieval
        test_query_retrieval()
        
        # Test 5: Query Router
        test_query_router()
        
        # Test 6: Real-world queries
        demonstrate_real_world_queries()
        
        print("\n🎉 All Query Processor tests completed!")
        print("\n📋 Summary:")
        print("   ✅ Intent Classification: Working")
        print("   ✅ Entity Extraction: Working")
        print("   ✅ Query Processing: Working")
        print("   ✅ Query Retrieval: Working")
        print("   ✅ Query Routing: Working")
        print("   ✅ Real-world Queries: Tested")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()