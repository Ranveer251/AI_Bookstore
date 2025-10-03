from typing import List, Dict, Any, Optional
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.core.models import UnifiedBookModel
from src.vectorstore.embeddings import BookEmbeddingGenerator, SentenceTransformerEmbeddings
from src.vectorstore.vector_db import ChromaVectorStore
from config.setting import settings

class BookIndexer:
    """Handles indexing of books into the vector store"""
    
    def __init__(self,
                 embedding_generator: Optional[BookEmbeddingGenerator] = None,
                 vector_store: Optional[ChromaVectorStore] = None,
                 batch_size: int = 0,
                 max_workers: int = 5):
        
        # Initialize embedding generator
        if embedding_generator is None:
            base_embedder = SentenceTransformerEmbeddings(settings.EMBEDDING_MODEL)
            embedding_generator = BookEmbeddingGenerator(base_embedder)
        
        self.embedding_generator = embedding_generator
        
        # Initialize vector store
        if vector_store is None:
            vector_store = ChromaVectorStore(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT
            )
        
        self.vector_store = vector_store
        self.batch_size = batch_size or settings.BATCH_SIZE
        self.max_workers = max_workers or settings.MAX_WORKERS
    
    def index_books(self, books: List[UnifiedBookModel], show_progress: bool = True) -> Dict[str, Any]:
        """Index a list of books into the vector store"""
        start_time = time.time()
        total_books = len(books)
        indexed_count = 0
        failed_count = 0
        
        if show_progress:
            print(f"🚀 Starting indexing of {total_books} books...")
        
        # Process books in batches
        for i in range(0, total_books, self.batch_size):
            batch = books[i:i + self.batch_size]
            batch_num = (i // self.batch_size) + 1
            total_batches = (total_books + self.batch_size - 1) // self.batch_size
            
            if show_progress:
                print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} books)...")
            
            try:
                # Generate embeddings for the batch
                batch_embeddings = self.embedding_generator.generate_book_embeddings(batch)
                
                # Add to vector store
                success = self.vector_store.add_books(batch_embeddings)
                
                if success:
                    indexed_count += len(batch)
                    if show_progress:
                        print(f"   ✅ Successfully indexed {len(batch)} books")
                else:
                    failed_count += len(batch)
                    if show_progress:
                        print(f"   ❌ Failed to index batch")
                
            except Exception as e:
                failed_count += len(batch)
                if show_progress:
                    print(f"   ❌ Error processing batch: {e}")
        
        # Calculate performance metrics
        end_time = time.time()
        total_time = end_time - start_time
        books_per_second = indexed_count / total_time if total_time > 0 else 0
        
        results = {
            "total_books": total_books,
            "indexed_count": indexed_count,
            "failed_count": failed_count,
            "success_rate": (indexed_count / total_books) * 100 if total_books > 0 else 0,
            "total_time_seconds": total_time,
            "books_per_second": books_per_second,
            "collection_stats": self.vector_store.get_collection_stats()
        }
        
        if show_progress:
            print(f"\n📊 Indexing Complete!")
            print(f"   • Total books: {total_books}")
            print(f"   • Successfully indexed: {indexed_count}")
            print(f"   • Failed: {failed_count}")
            print(f"   • Success rate: {results['success_rate']:.1f}%")
            print(f"   • Time taken: {total_time:.2f} seconds")
            print(f"   • Speed: {books_per_second:.2f} books/second")
        
        return results
    
    def index_single_book(self, book: UnifiedBookModel) -> bool:
        """Index a single book"""
        try:
            book_embedding = self.embedding_generator.generate_book_embedding(book)
            return self.vector_store.add_books([book_embedding])
        except Exception as e:
            print(f"Error indexing single book: {e}")
            return False
    
    def update_book_index(self, book: UnifiedBookModel) -> bool:
        """Update a book's index"""
        try:
            book_embedding = self.embedding_generator.generate_book_embedding(book)
            return self.vector_store.update_book(book.id, book_embedding)
        except Exception as e:
            print(f"Error updating book index: {e}")
            return False
    
    def remove_book_from_index(self, book_id: str) -> bool:
        """Remove a book from the index"""
        try:
            return self.vector_store.delete_books([book_id])
        except Exception as e:
            print(f"Error removing book from index: {e}")
            return False
    
    def search_books(self, 
                    query: str, 
                    n_results: int = 10,
                    filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for books using text query"""
        return self.vector_store.search_by_text(
            query_text=query,
            embedding_generator=self.embedding_generator.embedding_generator,
            n_results=n_results,
            where_filter=filters
        )
