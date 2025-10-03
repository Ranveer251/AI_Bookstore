# demo_complete_pipeline.py
# Complete end-to-end demonstration of the bookstore AI system

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.data.harmonizer import HarmonizerFactory
from src.vectorstore import BookIndexer
from src.query import QueryRouter, QueryRetriever, QueryIntent
import json

class BookstoreAISystem:
    """Complete bookstore AI system integration"""
    
    def __init__(self):
        self.indexer = None
        self.retriever = None
        self.router = None
        self.books_indexed = 0
    
    def setup(self):
        """Initialize the system"""
        print("🚀 Initializing Bookstore AI System")
        print("=" * 70)
        
        # Initialize vector store and indexer
        print("1️⃣ Setting up Vector Store...")
        self.indexer = BookIndexer()
        print("   ✅ Vector store ready")
        
        # Initialize retriever
        print("2️⃣ Setting up Query Retriever...")
        self.retriever = QueryRetriever(self.indexer)
        print("   ✅ Retriever ready")
        
        # Initialize router with handlers
        print("3️⃣ Setting up Query Router...")
        self.router = QueryRouter()
        self.router.register_handler(QueryIntent.SEARCH, self.retriever.retrieve_for_search)
        self.router.register_handler(QueryIntent.RECOMMENDATION, self.retriever.retrieve_for_recommendation)
        self.router.register_handler(QueryIntent.COMPARISON, self.retriever.retrieve_for_comparison)
        self.router.register_handler(QueryIntent.ANALYTICS, self.retriever.retrieve_for_analytics)
        self.router.register_handler(QueryIntent.FILTER, self.retriever.retrieve_for_filter)
        self.router.register_handler(QueryIntent.INFORMATION, self.retriever.retrieve_for_information)
        print("   ✅ Router ready with 6 intent handlers")
        
        print("\n✅ System initialization complete!\n")
    
    def load_and_harmonize_data(self, data_sources):
        """Load raw data and harmonize it"""
        print("📥 Loading and Harmonizing Data")
        print("=" * 70)
        
        all_unified_books = []
        
        for source in data_sources:
            schema_type = source['schema_type']
            raw_data = source['data']
            
            print(f"Processing {len(raw_data)} records from {schema_type}...")
            
            # Get harmonizer
            harmonizer = HarmonizerFactory.create_harmonizer(schema_type)
            
            # Harmonize data
            unified_books = harmonizer.batch_harmonize(raw_data)
            all_unified_books.extend(unified_books)
            
            print(f"   ✅ Harmonized {len(unified_books)} books")
        
        print(f"\n📊 Total unified books: {len(all_unified_books)}\n")
        return all_unified_books
    
    def index_books(self, books):
        """Index books into vector store"""
        if not self.indexer:
            raise RuntimeError("Indexer not initialized. Call setup() first.")
        print("🔧 Indexing Books into Vector Store")
        print("=" * 70)
        
        results = self.indexer.index_books(books, show_progress=True)
        self.books_indexed = results['indexed_count']
        
        print(f"\n✅ Indexing complete: {self.books_indexed} books ready for search\n")
        return results
    
    def query(self, user_query):
        """Process a user query"""
        if not self.router:
            raise RuntimeError("Router not initialized. Call setup() first.")
        result = self.router.route(user_query)
        return result
    
    def display_results(self, query, result):
        """Display query results in a user-friendly format"""
        print(f"💬 Query: '{query}'")
        
        if not result['success']:
            print(f"   ❌ Error: {result['error']}")
            return
        
        parsed = result['parsed_query']
        print(f"   🎯 Intent: {parsed.intent.value} (confidence: {parsed.confidence:.2f})")
        
        data = result['result']
        
        # Handle different result types
        if parsed.intent in [QueryIntent.SEARCH, QueryIntent.RECOMMENDATION, QueryIntent.FILTER]:
            if isinstance(data, list) and data:
                print(f"   📚 Found {len(data)} results:")
                for i, book in enumerate(data[:5], 1):
                    metadata = book['metadata']
                    score = book.get('score', 0)
                    print(f"      {i}. {metadata['title']}")
                    print(f"         Author: {metadata['author']}")
                    print(f"         Genre: {metadata['genre']} | Price: ${metadata['price']}")
                    print(f"         Store: {metadata['store_name']} | Rating: {metadata.get('rating', 'N/A')}/5")
                    if score > 0:
                        print(f"         Relevance: {score:.3f}")
            else:
                print("   ❌ No results found")
        
        elif parsed.intent == QueryIntent.COMPARISON:
            if isinstance(data, dict) and 'stores' in data:
                print(f"   📊 Comparison Results:")
                for store_id, store_data in data['stores'].items():
                    print(f"\n      {store_data['store_name']}:")
                    print(f"         Total Books: {store_data['book_count']}")
                    print(f"         Avg Price: ${store_data['avg_price']:.2f}")
                    print(f"         Price Range: ${store_data['min_price']:.2f} - ${store_data['max_price']:.2f}")
                    if store_data['avg_rating']:
                        print(f"         Avg Rating: {store_data['avg_rating']:.1f}/5")
                
                # Determine winner
                prices = {sid: sd['avg_price'] for sid, sd in data['stores'].items()}
                cheapest = min(prices.items(), key=lambda x: x[1])
                print(f"\n      💰 Best Value: {data['stores'][cheapest[0]]['store_name']} (${cheapest[1]:.2f} avg)")
        
        elif parsed.intent == QueryIntent.ANALYTICS:
            if isinstance(data, dict):
                print(f"   📈 Analytics Results:")
                
                if 'price_stats' in data:
                    stats = data['price_stats']
                    print(f"      Price Statistics:")
                    print(f"         Average: ${stats['average']:.2f}")
                    print(f"         Range: ${stats['min']:.2f} - ${stats['max']:.2f}")
                
                if 'genre_distribution' in data:
                    print(f"      Genre Distribution:")
                    for genre, count in list(data['genre_distribution'].items())[:5]:
                        print(f"         {genre}: {count} books")
                
                if 'store_distribution' in data:
                    print(f"      Store Distribution:")
                    for store, count in data['store_distribution'].items():
                        print(f"         {store}: {count} books")
        
        elif parsed.intent == QueryIntent.INFORMATION:
            if isinstance(data, dict):
                metadata = data['metadata']
                print(f"   📖 Book Information:")
                print(f"      Title: {metadata['title']}")
                print(f"      Author: {metadata['author']}")
                print(f"      Genre: {metadata['genre']}")
                print(f"      Price: ${metadata['price']}")
                print(f"      Publisher: {metadata.get('publisher', 'Unknown')}")
                print(f"      Year: {metadata.get('publication_year', 'Unknown')}")
                print(f"      Rating: {metadata.get('rating', 'N/A')}/5")
                print(f"      Store: {metadata['store_name']}")
        
        print()


def generate_sample_data():
    """Generate sample data for demonstration"""
    from scripts.generate_sample_data import generate_bookstore_a_data, generate_bookstore_b_data
    
    return [
        {
            'schema_type': 'bookstore_a',
            'data': generate_bookstore_a_data(25)
        },
        {
            'schema_type': 'bookstore_b',
            'data': generate_bookstore_b_data(25)
        }
    ]


def run_demo_queries(system):
    """Run demonstration queries"""
    print("🎯 Running Demo Queries")
    print("=" * 70)
    print()
    
    demo_queries = [
        # Search queries
        "Find science fiction books about space exploration",
        "Looking for fantasy novels with magic and adventure",
        
        # Filtered search
        "Show me books under $20",
        "Find highly rated books in store A",
        
        # Recommendations
        "Recommend books similar to fantasy adventure",
        
        # Comparison
        "Which store has cheaper sci-fi books?",
        "Compare fantasy book prices between stores",
        
        # Analytics
        "What are the most popular genres?",
        "Show me average prices by store",
        
        # Complex queries
        "Find affordable science fiction books rated above 4 stars",
        "Top 5 cheapest fantasy books available"
    ]
    
    for query in demo_queries:
        result = system.query(query)
        system.display_results(query, result)
        print("-" * 70)
        print()


def interactive_mode(system):
    """Interactive query mode"""
    print("🎮 Interactive Mode")
    print("=" * 70)
    print("Type your queries below. Type 'exit' or 'quit' to stop.")
    print("Examples:")
    print("  - Find science fiction books about space")
    print("  - Which store is cheaper?")
    print("  - Show me books under $15")
    print("  - Recommend fantasy books")
    print()
    
    while True:
        try:
            query = input("💬 Your query: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print()
            result = system.query(query)
            system.display_results(query, result)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def main():
    """Main demonstration"""
    print("\n" + "=" * 70)
    print("📚 BOOKSTORE AI SYSTEM - COMPLETE PIPELINE DEMO")
    print("=" * 70)
    print()
    
    try:
        # Initialize system
        system = BookstoreAISystem()
        system.setup()
        
        # Generate and load sample data
        print("📊 Generating Sample Data...")
        data_sources = generate_sample_data()
        print(f"   Generated data from {len(data_sources)} sources\n")
        
        # Harmonize data
        unified_books = system.load_and_harmonize_data(data_sources)
        
        # Index books
        system.index_books(unified_books)
        
        # Run demo queries
        run_demo_queries(system)
        
        # Show system stats
        print("\n📈 System Statistics")
        print("=" * 70)
        print(f"   Books indexed: {system.books_indexed}")
        print(f"   Data sources: {len(data_sources)}")
        print(f"   Query intents supported: 6")
        print(f"   Status: ✅ Fully operational")
        print()
        
        # Offer interactive mode
        response = input("Would you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print()
            interactive_mode(system)
        
        print("\n🎉 Demo completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()