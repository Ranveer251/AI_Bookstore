import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def demonstrate_full_pipeline():
    """Demonstrate harmonizer + vector store pipeline"""
    print("🔄 Full Pipeline Demo: Harmonizer → Vector Store")
    print("=" * 60)
    
    try:
        # Step 1: Generate sample data
        from scripts.generate_sample_data import generate_bookstore_a_data, generate_bookstore_b_data
        print("1️⃣ Generating sample data...")
        
        raw_data_a = generate_bookstore_a_data(10)
        raw_data_b = generate_bookstore_b_data(10) 
        print(f"   ✅ Generated {len(raw_data_a + raw_data_b)} raw records")
        
        # Step 2: Harmonize data
        from src.data.harmonizer import HarmonizerFactory
        print("2️⃣ Harmonizing data...")
        
        harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
        harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
        
        unified_books_a = harmonizer_a.batch_harmonize(raw_data_a)
        unified_books_b = harmonizer_b.batch_harmonize(raw_data_b)
        all_books = unified_books_a + unified_books_b
        print(f"   ✅ Harmonized {len(all_books)} books")
        
        # Step 3: Index in vector store
        from src.vectorstore import BookIndexer
        print("3️⃣ Indexing in vector store...")
        
        indexer = BookIndexer()
        results = indexer.index_books(all_books, show_progress=True)
        
        if results['indexed_count'] > 0:
            print(f"   ✅ Successfully indexed {results['indexed_count']} books")
            
            # Step 4: Test search
            print("4️⃣ Testing search functionality...")
            
            test_queries = [
                "science fiction space adventure",
                "romantic story love",
                "mystery crime detective"
            ]
            
            for query in test_queries:
                print(f"\n   🔍 Query: '{query}'")
                search_results = indexer.search_books(query, n_results=3)
                
                for i, result in enumerate(search_results, 1):
                    metadata = result['metadata']
                    print(f"      {i}. {metadata['title']} by {metadata['author']}")
                    print(f"         Store: {metadata['store_name']}, Price: ${metadata['price']}")
            
            print("\n🎉 Full pipeline working successfully!")
            print(f"\nPipeline Summary:")
            print(f"   • Raw data → Harmonized → Indexed → Searchable")
            print(f"   • Total processing time: {results['total_time_seconds']:.2f}s")
            print(f"   • Search capability: ✅ Semantic similarity")
            print(f"   • Multi-store support: ✅ Cross-store queries")
            
        else:
            print("   ❌ Indexing failed")
            
    except Exception as e:
        print(f"❌ Pipeline demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demonstrate_full_pipeline()