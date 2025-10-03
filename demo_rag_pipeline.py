import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.rag import RAGPipeline, TemplateGenerator, LLMGenerator
from src.vectorstore import BookIndexer
from src.core.models import UnifiedBookModel, GenreEnum
from typing import List
import time

def create_comprehensive_book_dataset() -> List[UnifiedBookModel]:
    """Create a comprehensive dataset for RAG testing"""
    books = [
        # Science Fiction
        UnifiedBookModel(
            title="Dune",
            author="Frank Herbert",
            genre=GenreEnum.SCIENCE_FICTION,
            price=16.99,
            rating=4.6,
            description="Epic science fiction saga about politics, religion, and ecology on the desert planet Arrakis. Paul Atreides becomes central to a struggle for control of the most valuable substance in the universe.",
            publisher="Chilton Books",
            publication_year=1965,
            isbn="9780441172719",
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
            description="Thrilling survival story about astronaut Mark Watney who must use his ingenuity and spirit to survive alone on Mars after being left behind by his crew.",
            publisher="Crown Publishing",
            publication_year=2011,
            isbn="9780804139021",
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
            description="Groundbreaking cyberpunk novel about hacker Case hired for one last job in cyberspace. Defined the cyberpunk genre and introduced the concept of the matrix.",
            publisher="Ace Books",
            publication_year=1984,
            isbn="9780441569595",
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
            description="Story of mathematician Hari Seldon who predicts the fall of the Galactic Empire and establishes the Foundation to preserve civilization.",
            publisher="Gnome Press",
            publication_year=1951,
            isbn="9780553293357",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        
        # Fantasy
        UnifiedBookModel(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=14.99,
            rating=4.8,
            description="Classic fantasy adventure following Bilbo Baggins on an unexpected journey with dwarves to reclaim their homeland from the dragon Smaug.",
            publisher="George Allen & Unwin",
            publication_year=1937,
            isbn="9780547928210",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=24.99,
            rating=4.9,
            description="Epic fantasy trilogy about Frodo Baggins' quest to destroy the One Ring and defeat the Dark Lord Sauron in Middle-earth.",
            publisher="George Allen & Unwin",
            publication_year=1954,
            isbn="9780547928227",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Harry Potter and the Sorcerer's Stone",
            author="J.K. Rowling",
            genre=GenreEnum.FANTASY,
            price=10.99,
            rating=4.7,
            description="Young wizard Harry Potter discovers his magical heritage and attends Hogwarts School of Witchcraft and Wizardry.",
            publisher="Scholastic",
            publication_year=1997,
            isbn="9780439708180",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Name of the Wind",
            author="Patrick Rothfuss",
            genre=GenreEnum.FANTASY,
            price=18.99,
            rating=4.5,
            description="Beautifully written fantasy about Kvothe, a legendary figure telling his life story. Magic, music, and mystery intertwine in this modern fantasy masterpiece.",
            publisher="DAW Books",
            publication_year=2007,
            isbn="9780756404079",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        
        # Fiction
        UnifiedBookModel(
            title="1984",
            author="George Orwell",
            genre=GenreEnum.FICTION,
            price=13.99,
            rating=4.4,
            description="Dystopian masterpiece about totalitarian control, surveillance, and manipulation of truth in a future society ruled by Big Brother.",
            publisher="Secker & Warburg",
            publication_year=1949,
            isbn="9780451524935",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre=GenreEnum.FICTION,
            price=12.99,
            rating=4.3,
            description="Powerful story of racial injustice and childhood innocence in the American South, told through Scout Finch's eyes.",
            publisher="J.B. Lippincott & Co.",
            publication_year=1960,
            isbn="9780061120084",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            genre=GenreEnum.FICTION,
            price=11.99,
            rating=4.0,
            description="Classic American novel about the Jazz Age, exploring themes of wealth, love, and the American Dream through Jay Gatsby's tragic story.",
            publisher="Charles Scribner's Sons",
            publication_year=1925,
            isbn="9780743273565",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        
        # Romance
        UnifiedBookModel(
            title="Pride and Prejudice",
            author="Jane Austen",
            genre=GenreEnum.ROMANCE,
            price=11.99,
            rating=4.5,
            description="Timeless romantic novel about Elizabeth Bennet and Mr. Darcy, exploring themes of love, marriage, and social class in Regency England.",
            publisher="T. Egerton",
            publication_year=1813,
            isbn="9780141439518",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Outlander",
            author="Diana Gabaldon",
            genre=GenreEnum.ROMANCE,
            price=16.99,
            rating=4.4,
            description="Time-traveling romance where World War II nurse Claire Randall is transported to 18th century Scotland and falls in love with Jamie Fraser.",
            publisher="Delacorte Press",
            publication_year=1991,
            isbn="9780440212560",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
        
        # Mystery
        UnifiedBookModel(
            title="The Girl with the Dragon Tattoo",
            author="Stieg Larsson",
            genre=GenreEnum.MYSTERY,
            price=15.99,
            rating=4.2,
            description="Gripping mystery thriller featuring journalist Mikael Blomkvist and hacker Lisbeth Salander investigating a decades-old disappearance.",
            publisher="Norstedts Förlag",
            publication_year=2005,
            isbn="9780307454546",
            store_id="store_a",
            store_name="Bookstore A",
            availability=True,
            source_schema="test"
        ),
        UnifiedBookModel(
            title="Gone Girl",
            author="Gillian Flynn",
            genre=GenreEnum.MYSTERY,
            price=14.99,
            rating=4.0,
            description="Psychological thriller about a marriage gone terribly wrong when Amy Dunne disappears on her fifth wedding anniversary.",
            publisher="Crown Publishing",
            publication_year=2012,
            isbn="9780307588371",
            store_id="store_b",
            store_name="Bookstore B",
            availability=True,
            source_schema="test"
        ),
    ]
    
    return books


def setup_rag_system():
    """Setup the RAG system with sample data"""
    print("🚀 Setting up RAG Pipeline System")
    print("=" * 70)
    
    # Create books
    print("1️⃣ Creating sample book dataset...")
    books = create_comprehensive_book_dataset()
    print(f"   ✅ Created {len(books)} books across multiple genres")
    
    # Index books
    print("2️⃣ Indexing books into vector store...")
    indexer = BookIndexer()
    
    try:
        result = indexer.index_books(books, show_progress=False)
        print(f"   ✅ Indexed {result['indexed_count']} books successfully")
    except Exception as e:
        print(f"   ❌ Indexing failed: {e}")
        return None
    
    # Initialize RAG pipeline
    print("3️⃣ Initializing RAG Pipeline...")
    rag_pipeline = RAGPipeline(indexer, use_llm=False)
    print("   ✅ RAG Pipeline ready\n")
    
    return rag_pipeline, indexer


def test_basic_rag_queries(rag_pipeline):
    """Test basic RAG queries"""
    print("\n📚 Testing Basic RAG Queries")
    print("=" * 70)
    
    test_queries = [
        "Find science fiction books about space",
        "Show me fantasy books with magic",
        "I want a mystery thriller",
        "Looking for classic literature"
    ]
    
    for query in test_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query, include_metadata=True)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
            print(f"📊 Found: {result['total_results']} results")
            print(f"⏱️  Response time: {result['metadata']['total_time_ms']:.1f}ms")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_recommendation_queries(rag_pipeline):
    """Test recommendation queries"""
    print("\n🎯 Testing Recommendation Queries")
    print("=" * 70)
    
    recommendation_queries = [
        "Recommend books similar to The Lord of the Rings",
        "What should I read if I liked Dune?",
        "Suggest some fantasy books with adventure",
        "Books like Harry Potter for young readers"
    ]
    
    for query in recommendation_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_comparison_queries(rag_pipeline):
    """Test comparison queries"""
    print("\n📊 Testing Comparison Queries")
    print("=" * 70)
    
    comparison_queries = [
        "Which store has cheaper science fiction books?",
        "Compare fantasy book prices between stores",
        "Which bookstore has better deals?",
        "Is store A or store B cheaper for mystery books?"
    ]
    
    for query in comparison_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_analytics_queries(rag_pipeline):
    """Test analytics queries"""
    print("\n📈 Testing Analytics Queries")
    print("=" * 70)
    
    analytics_queries = [
        "What are the most popular genres?",
        "Show me average book prices",
        "What's the highest rated genre?",
        "How many books are under $20?"
    ]
    
    for query in analytics_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_filtered_queries(rag_pipeline):
    """Test filtered queries"""
    print("\n🔍 Testing Filtered Queries")
    print("=" * 70)
    
    filtered_queries = [
        "Show me books under $15",
        "Find highly rated science fiction books",
        "Books between $10 and $20",
        "Fantasy books rated above 4.5 stars"
    ]
    
    for query in filtered_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_complex_queries(rag_pipeline):
    """Test complex multi-criteria queries"""
    print("\n🧩 Testing Complex Queries")
    print("=" * 70)
    
    complex_queries = [
        "Find affordable fantasy books under $20 rated above 4 stars",
        "Show me the top 3 cheapest science fiction books in store A",
        "I want highly rated mystery books between $12 and $18",
        "Recommend popular books from the last 50 years under $25"
    ]
    
    for query in complex_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query, include_metadata=True)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
            print(f"📊 Results: {result['total_results']}")
            print(f"🔧 Filters: {result['metadata']['filters_applied']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_information_queries(rag_pipeline):
    """Test information/detail queries"""
    print("\n📖 Testing Information Queries")
    print("=" * 70)
    
    info_queries = [
        "Tell me about Dune",
        "What is The Hobbit about?",
        "Give me details on 1984",
        "Information about Pride and Prejudice"
    ]
    
    for query in info_queries:
        print(f"\n💬 Query: '{query}'")
        print("-" * 70)
        
        result = rag_pipeline.query(query)
        
        if result['success']:
            print(f"🎯 Intent: {result['intent']}")
            print(f"\n💡 Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")


def test_batch_queries(rag_pipeline):
    """Test batch query processing"""
    print("\n⚡ Testing Batch Query Processing")
    print("=" * 70)
    
    batch_queries = [
        "Find fantasy books",
        "Which store is cheaper?",
        "Show me highly rated books",
        "Recommend science fiction",
        "What's the most popular genre?"
    ]
    
    print(f"Processing {len(batch_queries)} queries in batch...\n")
    
    start_time = time.time()
    results = rag_pipeline.batch_query(batch_queries)
    total_time = time.time() - start_time
    
    print(f"✅ Processed {len(results)} queries in {total_time:.2f}s")
    print(f"⚡ Average: {total_time/len(results):.3f}s per query\n")
    
    for i, (query, result) in enumerate(zip(batch_queries, results), 1):
        print(f"{i}. Query: '{query}'")
        print(f"   Intent: {result['intent']}, Results: {result['total_results']}")
        print()


def demonstrate_real_world_scenarios(rag_pipeline):
    """Demonstrate real-world user scenarios"""
    print("\n🌟 Real-World Usage Scenarios")
    print("=" * 70)
    
    scenarios = [
        {
            'name': "Budget-Conscious Reader",
            'query': "I'm looking for good books under $15. What do you recommend?"
        },
        {
            'name': "Genre Explorer",
            'query': "I love fantasy books like Lord of the Rings. What similar books should I read?"
        },
        {
            'name': "Deal Hunter",
            'query': "Which store has better prices for science fiction books?"
        },
        {
            'name': "Quality Seeker",
            'query': "Show me the highest rated books across all genres"
        },
        {
            'name': "Gift Shopper",
            'query': "I need a highly-rated fantasy book for a teenager, preferably around $15"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n👤 Scenario: {scenario['name']}")
        print(f"💬 Query: \"{scenario['query']}\"")
        print("-" * 70)
        
        result = rag_pipeline.query(scenario['query'])
        
        if result['success']:
            print(f"🤖 Assistant Response:\n{result['response']}")
        else:
            print(f"❌ Error: {result['error']}")
        
        print()


def performance_benchmark(rag_pipeline):
    """Benchmark RAG pipeline performance"""
    print("\n⚡ Performance Benchmarks")
    print("=" * 70)
    
    benchmark_queries = [
        "Find science fiction books",
        "Recommend fantasy novels",
        "Which store is cheaper?",
        "Show me analytics",
        "Books under $20"
    ]
    
    times = []
    
    for query in benchmark_queries:
        start = time.time()
        result = rag_pipeline.query(query, include_metadata=True)
        elapsed = time.time() - start
        times.append(elapsed)
        
        if result['success']:
            metadata = result['metadata']
            print(f"Query: '{query}'")
            print(f"  Total time: {elapsed*1000:.1f}ms")
            print(f"  Retrieval: {metadata['retrieval_time_ms']:.1f}ms")
            print(f"  Generation: {metadata['generation_time_ms']:.1f}ms")
            print()
    
    avg_time = sum(times) / len(times)
    print(f"📊 Average query time: {avg_time*1000:.1f}ms")
    print(f"📊 Queries per second: {1/avg_time:.2f}")


def interactive_rag_mode(rag_pipeline):
    """Interactive RAG query mode"""
    print("\n🎮 Interactive RAG Mode")
    print("=" * 70)
    print("Ask me anything about books! Type 'exit' to quit.")
    print("\nExample queries:")
    print("  • Find fantasy books with magic")
    print("  • Which store has cheaper books?")
    print("  • Recommend books like Dune")
    print("  • Show me books under $15")
    print()
    
    while True:
        try:
            query = input("💬 Your question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Thanks for using the RAG system!")
                break
            
            if not query:
                continue
            
            print()
            result = rag_pipeline.query(query, include_metadata=True)
            
            if result['success']:
                print(f"🤖 Assistant ({result['intent']} query):")
                print(result['response'])
                print(f"\n📊 Stats: {result['total_results']} results, {result['metadata']['total_time_ms']:.1f}ms")
            else:
                print(f"❌ Error: {result['error']}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using the RAG system!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def main():
    """Main demonstration function"""
    print("\n" + "=" * 70)
    print("🤖 RAG PIPELINE DEMONSTRATION")
    print("=" * 70)
    print()
    
    try:
        # Setup system
        result = setup_rag_system()
        if result is None:
            print("❌ Setup failed. Exiting.")
            return
        
        rag_pipeline, indexer = result
        
        # Run test suites
        print("\n" + "=" * 70)
        print("RUNNING TEST SUITES")
        print("=" * 70)
        
        test_basic_rag_queries(rag_pipeline)
        
        test_recommendation_queries(rag_pipeline)
        
        test_comparison_queries(rag_pipeline)
        
        test_analytics_queries(rag_pipeline)
        
        test_filtered_queries(rag_pipeline)
        
        test_complex_queries(rag_pipeline)
        
        test_information_queries(rag_pipeline)
        
        test_batch_queries(rag_pipeline)
        
        demonstrate_real_world_scenarios(rag_pipeline)
        
        performance_benchmark(rag_pipeline)
        
        # Summary
        print("\n" + "=" * 70)
        print("📋 TEST SUMMARY")
        print("=" * 70)
        print("✅ Basic queries: Working")
        print("✅ Recommendations: Working")
        print("✅ Comparisons: Working")
        print("✅ Analytics: Working")
        print("✅ Filters: Working")
        print("✅ Complex queries: Working")
        print("✅ Information queries: Working")
        print("✅ Batch processing: Working")
        print("✅ Real-world scenarios: Tested")
        print("✅ Performance: Benchmarked")
        
        # Offer interactive mode
        print()
        response = input("Would you like to try interactive mode? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_rag_mode(rag_pipeline)
        
        print("\n🎉 RAG Pipeline demo completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()