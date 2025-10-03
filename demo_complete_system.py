import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.data.harmonizer import HarmonizerFactory
from src.vectorstore import BookIndexer
from src.rag import RAGPipeline
from scripts.generate_sample_data import generate_bookstore_a_data, generate_bookstore_b_data
import time

class BookstoreAISystem:
    """Complete Bookstore AI System"""
    
    def __init__(self):
        self.harmonizers = {}
        self.indexer = None
        self.rag_pipeline = None
        self.stats = {
            'books_harmonized': 0,
            'books_indexed': 0,
            'queries_processed': 0,
            'total_processing_time': 0.0
        }
    
    def initialize(self):
        """Initialize the complete system"""
        print("🚀 Initializing Bookstore AI System")
        print("=" * 70)
        print()
        
        # Step 1: Initialize harmonizers
        print("1️⃣ Initializing Schema Harmonizers...")
        self.harmonizers['bookstore_a'] = HarmonizerFactory.create_harmonizer('bookstore_a')
        self.harmonizers['bookstore_b'] = HarmonizerFactory.create_harmonizer('bookstore_b')
        print(f"   ✅ {len(self.harmonizers)} schema harmonizers ready")
        
        # Step 2: Initialize vector store
        print("2️⃣ Initializing Vector Store...")
        self.indexer = BookIndexer()
        print("   ✅ Vector store ready")
        
        # Step 3: Initialize RAG pipeline
        print("3️⃣ Initializing RAG Pipeline...")
        self.rag_pipeline = RAGPipeline(self.indexer, use_llm=False)
        print("   ✅ RAG pipeline ready")
        
        print()
        print("✅ System initialization complete!")
        print()
    
    def load_data(self, num_books_per_store=50):
        """Load and harmonize data from multiple sources"""
        print("📥 Loading Data from Multiple Sources")
        print("=" * 70)
        print()
        
        # Generate sample data
        print(f"Generating {num_books_per_store} books per store...")
        raw_data_a = generate_bookstore_a_data(num_books_per_store)
        raw_data_b = generate_bookstore_b_data(num_books_per_store)
        print(f"   ✅ Generated {len(raw_data_a) + len(raw_data_b)} raw records")
        
        # Harmonize data
        print("\nHarmonizing data...")
        unified_books = []
        
        # Harmonize Store A data
        print("   Processing Bookstore A...")
        books_a = self.harmonizers['bookstore_a'].batch_harmonize(raw_data_a)
        unified_books.extend(books_a)
        print(f"   ✅ Harmonized {len(books_a)} books from Store A")
        
        # Harmonize Store B data
        print("   Processing Bookstore B...")
        books_b = self.harmonizers['bookstore_b'].batch_harmonize(raw_data_b)
        unified_books.extend(books_b)
        print(f"   ✅ Harmonized {len(books_b)} books from Store B")
        
        self.stats['books_harmonized'] = len(unified_books)
        print(f"\n📊 Total unified books: {len(unified_books)}")
        print()
        
        return unified_books
    
    def index_data(self, books):
        """Index books into vector store"""
        if not self.indexer:
            raise RuntimeError("Indexer not initialized. Call initialize() first.")
        print("🔧 Indexing Books into Vector Store")
        print("=" * 70)
        print()
        
        start_time = time.time()
        results = self.indexer.index_books(books, show_progress=True)
        indexing_time = time.time() - start_time
        
        self.stats['books_indexed'] = results['indexed_count']
        self.stats['total_processing_time'] += indexing_time
        
        print(f"\n✅ Indexing complete: {results['indexed_count']} books ready")
        print(f"⏱️  Time taken: {indexing_time:.2f}s")
        print()
        
        return results
    
    def query(self, user_query):
        """Process a user query through the RAG pipeline"""
        if not self.rag_pipeline:
            raise RuntimeError("RAG pipeline not initialized. Call initialize() first.")
        start_time = time.time()
        result = self.rag_pipeline.query(user_query, include_metadata=True)
        query_time = time.time() - start_time
        
        self.stats['queries_processed'] += 1
        self.stats['total_processing_time'] += query_time
        
        return result
    
    def display_result(self, query, result):
        """Display query result in a user-friendly format"""
        print(f"💬 Query: \"{query}\"")
        print("-" * 70)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
            print(f"📊 Results: {result['total_results']}")
            print(f"⏱️  Response time: {result['metadata']['total_time_ms']:.1f}ms")
            print()
            print("🤖 Response:")
            print(result['response'])
        else:
            print(f"❌ Error: {result['error']}")
        
        print()
    
    def show_stats(self):
        """Display system statistics"""
        print("📈 System Statistics")
        print("=" * 70)
        print(f"Books harmonized: {self.stats['books_harmonized']}")
        print(f"Books indexed: {self.stats['books_indexed']}")
        print(f"Queries processed: {self.stats['queries_processed']}")
        print(f"Total processing time: {self.stats['total_processing_time']:.2f}s")
        
        if self.stats['queries_processed'] > 0:
            avg_query_time = self.stats['total_processing_time'] / self.stats['queries_processed']
            print(f"Average query time: {avg_query_time*1000:.1f}ms")
        
        print()


def run_comprehensive_demo():
    """Run a comprehensive system demonstration"""
    
    print("\n" + "=" * 70)
    print("📚 BOOKSTORE AI SYSTEM - COMPLETE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Initialize system
    system = BookstoreAISystem()
    system.initialize()
    
    # Load and process data
    books = system.load_data(num_books_per_store=50)
    system.index_data(books)
    
    # Demo queries
    print("🎯 Running Demo Queries")
    print("=" * 70)
    print()
    
    demo_queries = [
        # Basic search
        {
            'category': 'Search',
            'queries': [
                "Find science fiction books about space",
                "Show me fantasy novels with magic"
            ]
        },
        # Recommendations
        {
            'category': 'Recommendations',
            'queries': [
                "Recommend books similar to fantasy adventures",
                "What should I read if I like science fiction?"
            ]
        },
        # Comparisons
        {
            'category': 'Store Comparisons',
            'queries': [
                "Which store has cheaper science fiction books?",
                "Compare fantasy book prices between stores"
            ]
        },
        # Analytics
        {
            'category': 'Analytics',
            'queries': [
                "What are the most popular genres?",
                "Show me the average book prices"
            ]
        },
        # Filtered searches
        {
            'category': 'Filtered Search',
            'queries': [
                "Find books under $20",
                "Show me highly rated books"
            ]
        },
        # Complex queries
        {
            'category': 'Complex Queries',
            'queries': [
                "Find affordable science fiction books under $20 rated above 4 stars",
                "Show me the top 5 cheapest fantasy books in store A"
            ]
        }
    ]
    
    for demo_group in demo_queries:
        print(f"\n{'='*70}")
        print(f"📁 {demo_group['category']}")
        print('='*70)
        print()
        
        for query in demo_group['queries']:
            result = system.query(query)
            system.display_result(query, result)
            print("-" * 70)
            print()
    
    # Show statistics
    system.show_stats()
    
    return system


def interactive_session(system):
    """Run an interactive query session"""
    print("🎮 Interactive Query Session")
    print("=" * 70)
    print("Ask me anything about books! Type 'exit' to quit.")
    print()
    print("Example queries:")
    print("  • Find fantasy books with dragons")
    print("  • Which store has better deals?")
    print("  • Recommend books like Harry Potter")
    print("  • Show me books under $15")
    print("  • What's the most popular genre?")
    print()
    
    while True:
        try:
            query = input("💬 Your question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Thanks for using the Bookstore AI System!")
                break
            
            if not query:
                continue
            
            print()
            result = system.query(query)
            system.display_result(query, result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using the Bookstore AI System!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def show_system_capabilities():
    """Display system capabilities"""
    print("\n🌟 System Capabilities")
    print("=" * 70)
    print()
    
    capabilities = [
        ("📊 Multi-Schema Support", "Harmonizes data from different bookstore formats"),
        ("🔍 Semantic Search", "Understands meaning, not just keywords"),
        ("💡 Smart Recommendations", "Suggests books based on preferences"),
        ("📈 Store Analytics", "Compare prices and selection across stores"),
        ("🎯 Intent Detection", "Understands 6 different query types"),
        ("⚡ Fast Performance", "Sub-second response times"),
        ("🤖 Natural Language", "Conversational query interface"),
        ("🔧 Flexible Filtering", "Price, rating, store, genre filters"),
        ("📚 Comprehensive", "Handles simple to complex queries"),
        ("🎨 Multiple Formats", "Template or LLM-based responses")
    ]
    
    for capability, description in capabilities:
        print(f"{capability}")
        print(f"   {description}")
        print()


def show_example_use_cases():
    """Show practical use cases"""
    print("\n💼 Real-World Use Cases")
    print("=" * 70)
    print()
    
    use_cases = [
        {
            'name': "Customer Service Bot",
            'description': "Answer customer questions about book availability and recommendations",
            'example': "Do you have any books about space exploration under $20?"
        },
        {
            'name': "Price Comparison Tool",
            'description': "Help customers find the best deals across stores",
            'example': "Which store has cheaper fantasy books?"
        },
        {
            'name': "Recommendation Engine",
            'description': "Provide personalized book suggestions",
            'example': "I loved Dune, what else would I like?"
        },
        {
            'name': "Inventory Analytics",
            'description': "Business intelligence for store owners",
            'example': "What are our most popular genres?"
        },
        {
            'name': "Gift Finder",
            'description': "Help customers find the perfect gift",
            'example': "I need a highly-rated fantasy book for a teenager around $15"
        }
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"{i}. {use_case['name']}")
        print(f"   Description: {use_case['description']}")
        print(f"   Example: \"{use_case['example']}\"")
        print()


def main():
    """Main entry point"""
    
    try:
        # Show capabilities
        show_system_capabilities()
        
        # Show use cases
        show_example_use_cases()
        
        # Run comprehensive demo
        system = run_comprehensive_demo()
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print()
        print("The system successfully demonstrated:")
        print("  ✅ Data harmonization from multiple sources")
        print("  ✅ Vector-based semantic search")
        print("  ✅ Natural language query processing")
        print("  ✅ RAG-powered response generation")
        print("  ✅ Multi-intent query handling")
        print("  ✅ Store comparison and analytics")
        print()
        
        # Offer interactive mode
        response = input("Would you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print()
            interactive_session(system)
        
        print("\n🎉 Thank you for exploring the Bookstore AI System!")
        print("\n📖 Next Steps:")
        print("  • Explore individual components in src/")
        print("  • Run specific demos: demo_query_processor.py, demo_rag_pipeline.py")
        print("  • Check documentation in the artifacts")
        print("  • Integrate into your own application")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()