import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def quick_test():
    """Quick test of vector store functionality"""
    print("⚡ Quick Vector Store Test")
    print("=" * 30)
    
    try:
        # Test imports
        from src.vectorstore import SentenceTransformerEmbeddings, BookEmbeddingGenerator
        from src.core.models import UnifiedBookModel, GenreEnum
        print("✅ Imports successful")
        
        # Test embedding generation
        embedder = SentenceTransformerEmbeddings()
        embedding = embedder.generate_embedding("test text")
        print(f"✅ Generated embedding (dim: {len(embedding)})")
        
        # Test book embedding
        book = UnifiedBookModel(
            title="Test Book",
            author="Test Author", 
            genre=GenreEnum.FICTION,
            price=9.99,
            description="A test book for demonstration",
            store_id="test",
            store_name="Test Store",
            source_schema="test",
            rating=4,
        )
        
        book_embedder = BookEmbeddingGenerator(embedder)
        book_embedding = book_embedder.generate_book_embedding(book)
        print("✅ Generated book embedding")
        
        print(f"\n📊 Book embedding info:")
        print(f"   • Text: {book_embedding['text'][:100]}...")
        print(f"   • Embedding length: {len(book_embedding['embedding'])}")
        print(f"   • Metadata keys: {list(book_embedding['metadata'].keys())}")
        
        print("\n🎉 Quick test passed! Vector store is ready.")
        print("Run 'python demo_vector_store.py' for full demo.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Run: python setup_vector_store.py")
        print("2. Check that all requirements are installed")

if __name__ == "__main__":
    quick_test()