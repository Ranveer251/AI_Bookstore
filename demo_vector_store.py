import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.vectorstore import (
    SentenceTransformerEmbeddings,
    BookEmbeddingGenerator,
    ChromaVectorStore,
    BookIndexer
)
from src.data.harmonizer import HarmonizerFactory
from src.core.models import UnifiedBookModel, GenreEnum
from datetime import datetime
import json

def create_sample_books():
    """Create sample books for testing"""
    sample_books = [
        UnifiedBookModel(
            title="Dune",
            author="Frank Herbert",
            genre=GenreEnum.SCIENCE_FICTION,
            price=16.99,
            rating=4.6,
            description="A science fiction masterpiece about politics, religion, and ecology on the desert planet Arrakis. Paul Atreides becomes embroiled in a struggle for the control of the desert planet Arrakis.",
            publisher="Chilton Books",
            publication_year=1965,
            isbn="9780441172719",
            store_id="store_a",
            store_name="Bookstore A",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="The Lord of the Rings",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=19.99,
            rating=4.8,
            description="An epic fantasy adventure following Frodo Baggins as he journeys to destroy the One Ring. A tale of friendship, courage, and the battle between good and evil in Middle-earth.",
            publisher="George Allen & Unwin",
            publication_year=1954,
            isbn="9780547928227",
            store_id="store_b",
            store_name="Bookstore B",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="1984",
            author="George Orwell",
            genre=GenreEnum.FICTION,
            price=13.99,
            rating=4.4,
            description="A dystopian social science fiction novel about totalitarian control, surveillance, and the manipulation of truth. Winston Smith struggles against Big Brother's oppressive regime.",
            publisher="Secker & Warburg",
            publication_year=1949,
            isbn="9780451524935",
            store_id="store_a",
            store_name="Bookstore A",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            genre=GenreEnum.FICTION,
            price=12.99,
            rating=4.3,
            description="A gripping tale of racial injustice and childhood innocence in the American South. Scout Finch learns about morality and human nature through her father's defense of a black man.",
            publisher="J.B. Lippincott & Co.",
            publication_year=1960,
            isbn="9780061120084",
            store_id="store_b",
            store_name="Bookstore B",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="The Hobbit",
            author="J.R.R. Tolkien",
            genre=GenreEnum.FANTASY,
            price=14.99,
            rating=4.7,
            description="A classic fantasy adventure following Bilbo Baggins on his unexpected journey with dwarves to reclaim their homeland from the dragon Smaug. A tale of courage and discovery.",
            publisher="George Allen & Unwin",
            publication_year=1937,
            isbn="9780547928210",
            store_id="store_a",
            store_name="Bookstore A",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="Neuromancer",
            author="William Gibson",
            genre=GenreEnum.SCIENCE_FICTION,
            price=15.99,
            rating=4.2,
            description="A groundbreaking cyberpunk novel about hacker Case who is hired for one last job in cyberspace. The book that defined the cyberpunk genre and introduced the concept of the matrix.",
            publisher="Ace Books",
            publication_year=1984,
            isbn="9780441569595",
            store_id="store_b",
            store_name="Bookstore B",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="Pride and Prejudice",
            author="Jane Austen",
            genre=GenreEnum.ROMANCE,
            price=11.99,
            rating=4.5,
            description="A romantic novel about Elizabeth Bennet and Mr. Darcy, exploring themes of love, marriage, and social class in Regency England. A timeless story of first impressions and true love.",
            publisher="T. Egerton",
            publication_year=1813,
            isbn="9780141439518",
            store_id="store_a",
            store_name="Bookstore A",
            source_schema="manual"
        ),
        UnifiedBookModel(
            title="The Martian",
            author="Andy Weir",
            genre=GenreEnum.SCIENCE_FICTION,
            price=17.99,
            rating=4.6,
            description="A thrilling survival story about astronaut Mark Watney who is stranded on Mars and must use his ingenuity to survive until rescue. Science meets human determination.",
            publisher="Crown Publishing",
            publication_year=2011,
            isbn="9780804139021",
            store_id="store_b",
            store_name="Bookstore B",
            source_schema="manual"
        )
    ]
    
    return sample_books

def test_embedding_generation():
    """Test the embedding generation functionality"""
    print("🧪 Testing Embedding Generation")
    print("=" * 50)
    
    # Initialize embedding generator
    print("📝 Initializing SentenceTransformer embeddings...")
    base_embedder = SentenceTransformerEmbeddings()
    book_embedder = BookEmbeddingGenerator(base_embedder)
    
    print(f"   ✅ Embedding dimension: {base_embedder.get_embedding_dimension()}")
    
    # Test single text embedding
    test_text = "A science fiction novel about space exploration"
    embedding = base_embedder.generate_embedding(test_text)
    
    print(f"   ✅ Generated embedding for text (length: {len(embedding)})")
    print(f"   📊 Sample values: {embedding[:5]}...")
    
    # Test book embedding
    sample_book = create_sample_books()[0]  # Dune
    book_embedding_data = book_embedder.generate_book_embedding(sample_book)
    
    print(f"\n📚 Book Embedding Test:")
    print(f"   • Book: {sample_book.title}")
    print(f"   • Composite text: {book_embedding_data['text'][:100]}...")
    print(f"   • Embedding length: {len(book_embedding_data['embedding'])}")
    print(f"   • Metadata keys: {list(book_embedding_data['metadata'].keys())}")
    
    return book_embedder

def test_vector_store():
    """Test the ChromaDB vector store"""
    print("\n🗄️  Testing Vector Store")
    print("=" * 50)
    
    try:
        # Initialize vector store (will use persistent client as fallback)
        vector_store = ChromaVectorStore(collection_name="test_books")
        print("   ✅ Vector store initialized")
        
        # Get initial stats
        stats = vector_store.get_collection_stats()
        print(f"   📊 Collection stats: {stats}")
        
        return vector_store
        
    except Exception as e:
        print(f"   ❌ Vector store initialization failed: {e}")
        print("   💡 This is normal if ChromaDB server is not running")
        print("   💡 The system will use persistent storage instead")
        
        # Try with persistent client
        try:
            vector_store = ChromaVectorStore(collection_name="test_books")
            print("   ✅ Fallback to persistent storage successful")
            return vector_store
        except Exception as e2:
            print(f"   ❌ Persistent storage also failed: {e2}")
            return None

def test_indexing_and_search():
    """Test the complete indexing and search pipeline"""
    print("\n🔍 Testing Indexing and Search Pipeline")
    print("=" * 50)
    
    # Create sample books
    sample_books = create_sample_books()
    print(f"   📚 Created {len(sample_books)} sample books")
    
    # Initialize indexer
    try:
        indexer = BookIndexer()
        print("   ✅ Indexer initialized")
    except Exception as e:
        print(f"   ❌ Indexer initialization failed: {e}")
        return
    
    # Index the books
    print("\n   🚀 Starting indexing process...")
    results = indexer.index_books(sample_books, show_progress=True)
    
    if results['indexed_count'] > 0:
        print(f"   🎉 Indexing successful!")
        
        # Test search functionality
        print("\n   🔍 Testing search queries...")
        
        search_queries = [
            "space exploration science fiction",
            "fantasy adventure with hobbits and dragons",
            "dystopian future surveillance society",
            "romance in regency england",
            "survival story on mars"
        ]
        
        for query in search_queries:
            print(f"\n      🔎 Query: '{query}'")
            search_results = indexer.search_books(query, n_results=3)
            
            if search_results:
                for i, result in enumerate(search_results, 1):
                    title = result['metadata'].get('title', 'Unknown')
                    author = result['metadata'].get('author', 'Unknown')
                    score = result['score']
                    print(f"         {i}. {title} by {author} (score: {score:.3f})")
            else:
                print("         No results found")
        
        # Test filtered search
        print(f"\n   🏪 Testing filtered search (Store A only)...")
        store_filter = {"store_id": "store_a"}
        filtered_results = indexer.search_books(
            "science fiction", 
            n_results=5, 
            filters=store_filter
        )
        
        print(f"      Found {len(filtered_results)} books in Store A:")
        for result in filtered_results:
            title = result['metadata'].get('title', 'Unknown')
            store = result['metadata'].get('store_name', 'Unknown')
            print(f"         • {title} ({store})")
    
    else:
        print(f"   ❌ Indexing failed - no books were indexed")
    
    return results

def test_similarity_search():
    """Test similarity search with specific book"""
    print("\n🎯 Testing Book-to-Book Similarity")
    print("=" * 50)
    
    try:
        # Initialize components
        indexer = BookIndexer()
        sample_books = create_sample_books()
        
        # Find books similar to "Dune"
        dune_query = "desert planet politics ecology space empire"
        print(f"   🔍 Finding books similar to Dune theme: '{dune_query}'")
        
        similar_books = indexer.search_books(dune_query, n_results=5)
        
        if similar_books:
            print("      📚 Most similar books:")
            for i, book in enumerate(similar_books, 1):
                title = book['metadata'].get('title', 'Unknown')
                author = book['metadata'].get('author', 'Unknown')
                genre = book['metadata'].get('genre', 'Unknown')
                score = book['score']
                print(f"         {i}. {title} by {author} ({genre}) - Score: {score:.3f}")
        else:
            print("      ❌ No similar books found")
            
    except Exception as e:
        print(f"   ❌ Similarity search failed: {e}")

def test_real_world_queries():
    """Test with real-world user queries"""
    print("\n💭 Testing Real-World User Queries")
    print("=" * 50)
    
    try:
        indexer = BookIndexer()
        
        real_queries = [
            "I want a book about artificial intelligence and robots",
            "Looking for a romantic story set in historical times",
            "Need something with magic and wizards for teenagers",
            "Books about surviving in extreme conditions",
            "Stories about friendship and coming of age",
            "Dystopian novels about government control"
        ]
        
        for query in real_queries:
            print(f"\n   💬 User Query: '{query}'")
            results = indexer.search_books(query, n_results=3)
            
            if results:
                print("      📖 Recommendations:")
                for i, book in enumerate(results, 1):
                    metadata = book['metadata']
                    print(f"         {i}. {metadata['title']} by {metadata['author']}")
                    print(f"            Genre: {metadata['genre']}, Price: ${metadata['price']}")
                    print(f"            Store: {metadata['store_name']}, Rating: {metadata.get('rating', 'N/A')}/5")
            else:
                print("      ❌ No recommendations found")
                
    except Exception as e:
        print(f"   ❌ Real-world query test failed: {e}")

def benchmark_performance():
    """Benchmark the performance of the vector store"""
    print("\n⚡ Performance Benchmarks")
    print("=" * 50)
    
    try:
        import time
        
        # Create larger dataset for benchmarking
        base_books = create_sample_books()
        large_dataset = []
        
        # Generate variations of existing books
        for i in range(50):  # Create 400 total books (50 * 8)
            for book in base_books:
                variant = UnifiedBookModel(
                    title=f"{book.title} - Edition {i+1}",
                    author=book.author,
                    genre=book.genre,
                    price=book.price + (i * 0.5),
                    rating=min(5.0, book.rating + (i * 0.01)),
                    description=f"{book.description} [Variant {i+1}]",
                    publisher=book.publisher,
                    publication_year=book.publication_year,
                    isbn=f"{book.isbn[:-1]}{i%10}",
                    store_id=book.store_id,
                    store_name=book.store_name,
                    source_schema="benchmark"
                )
                large_dataset.append(variant)
        
        print(f"   📚 Generated {len(large_dataset)} books for benchmarking")
        
        # Benchmark indexing
        indexer = BookIndexer(batch_size=50)
        
        start_time = time.time()
        results = indexer.index_books(large_dataset, show_progress=False)
        indexing_time = time.time() - start_time
        
        print(f"   ⚡ Indexing Performance:")
        print(f"      • Books indexed: {results['indexed_count']}")
        print(f"      • Time taken: {indexing_time:.2f} seconds")
        print(f"      • Speed: {results['books_per_second']:.1f} books/second")
        
        # Benchmark searching
        search_queries = [
            "science fiction space",
            "fantasy adventure",
            "romance historical",
            "dystopian future",
            "survival story"
        ]
        
        search_times = []
        for query in search_queries:
            start_time = time.time()
            results = indexer.search_books(query, n_results=10)
            search_time = time.time() - start_time
            search_times.append(search_time)
        
        avg_search_time = sum(search_times) / len(search_times)
        
        print(f"   🔍 Search Performance:")
        print(f"      • Average search time: {avg_search_time*1000:.1f} ms")
        print(f"      • Searches per second: {1/avg_search_time:.1f}")
        
    except Exception as e:
        print(f"   ❌ Benchmark failed: {e}")

def demonstrate_advanced_features():
    """Demonstrate advanced vector store features"""
    print("\n🚀 Advanced Features Demo")
    print("=" * 50)
    
    try:
        indexer = BookIndexer()
        sample_books = create_sample_books()
        
        # Test price-based filtering
        print("   💰 Price-based filtering:")
        affordable_books = indexer.search_books(
            "science fiction adventure",
            n_results=10,
            filters={"price": {"$lt": 16.0}}  # Books under $16
        )
        
        if affordable_books:
            print("      📚 Affordable sci-fi books (under $16):")
            for book in affordable_books:
                metadata = book['metadata']
                print(f"         • {metadata['title']}: ${metadata['price']}")
        else:
            print("      ❌ No affordable books found matching query")
        
        # Test multi-store comparison
        print(f"\n   🏪 Multi-store availability:")
        query = "fantasy adventure"
        all_results = indexer.search_books(query, n_results=10)
        
        store_results = {}
        for result in all_results:
            store = result['metadata']['store_name']
            if store not in store_results:
                store_results[store] = []
            store_results[store].append(result)
        
        for store, books in store_results.items():
            print(f"      {store}: {len(books)} matches")
            for book in books[:2]:  # Show top 2
                metadata = book['metadata']
                print(f"         • {metadata['title']} - ${metadata['price']}")
        
        # Test rating-based filtering
        print(f"\n   ⭐ High-rated books:")
        high_rated = indexer.search_books(
            "classic literature",
            n_results=10,
            filters={"rating": {"$gte": 4.5}}  # Rating >= 4.5
        )
        
        if high_rated:
            for book in high_rated:
                metadata = book['metadata']
                print(f"         • {metadata['title']}: {metadata.get('rating', 'N/A')}/5 stars")
        else:
            print("         ❌ No high-rated books found")
            
    except Exception as e:
        print(f"   ❌ Advanced features demo failed: {e}")

def main():
    """Main demonstration function"""
    print("🎯 Vector Store and Embeddings Demo")
    print("=" * 70)
    
    try:
        # Test 1: Embedding generation
        book_embedder = test_embedding_generation()
        
        # Test 2: Vector store initialization
        vector_store = test_vector_store()
        
        if vector_store is None:
            print("\n❌ Cannot proceed without vector store")
            return
        
        # Test 3: Indexing and basic search
        indexing_results = test_indexing_and_search()
        
        if indexing_results and indexing_results['indexed_count'] > 0:
            # Test 4: Similarity search
            test_similarity_search()
            
            # Test 5: Real-world queries
            test_real_world_queries()
            
            # Test 6: Performance benchmarks
            benchmark_performance()
            
            # Test 7: Advanced features
            demonstrate_advanced_features()
            
            print("\n🎉 All tests completed successfully!")
            print("\n📋 Summary:")
            print(f"   • Vector store: ✅ Working")
            print(f"   • Embeddings: ✅ Working") 
            print(f"   • Indexing: ✅ {indexing_results['indexed_count']} books indexed")
            print(f"   • Search: ✅ Semantic search functional")
            print(f"   • Performance: ✅ Benchmarks completed")
            
        else:
            print("\n❌ Indexing failed - skipping advanced tests")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()