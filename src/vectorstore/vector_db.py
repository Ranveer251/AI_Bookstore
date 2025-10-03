import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional, Tuple, Union
import uuid
from datetime import datetime
from src.core.models import UnifiedBookModel

class ChromaVectorStore:
    """ChromaDB vector store implementation"""
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 8001,
                 collection_name: str = "books"):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        try:
            self.client = chromadb.HttpClient(
                host=host,
                port=port,
                settings=ChromaSettings(
                    chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
                    chroma_client_auth_credentials=""
                )
            )
        except Exception:
            # Fallback to persistent client for local development
            self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Book embeddings for semantic search"}
        )
    
    def add_books(self, book_embeddings: List[Dict[str, Any]]) -> bool:
        """Add book embeddings to the vector store"""
        try:
            ids = [item["book_id"] for item in book_embeddings]
            embeddings = [item["embedding"] for item in book_embeddings]
            metadatas = [item["metadata"] for item in book_embeddings]
            documents = [item["text"] for item in book_embeddings]
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents
            )
            
            return True
            
        except Exception as e:
            print(f"Error adding books to vector store: {e}")
            return False
    
    def search_similar_books(self, 
                           query_embedding: List[float], 
                           n_results: int = 10,
                           where_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar books using vector similarity"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i in range(len(results['ids'][0])):
                    result = {
                        "id": results['ids'][0][i],
                        "score": 1 - results['distances'][0][i],  # Convert distance to similarity
                        "metadata": results['metadatas'][0][i],
                        "document": results['documents'][0][i]
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching similar books: {e}")
            return []
    
    def search_by_text(self,
                      query_text: str,
                      embedding_generator,
                      n_results: int = 10,
                      where_filter: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search books using text query"""
        query_embedding = embedding_generator.generate_embedding(query_text)
        return self.search_similar_books(query_embedding, n_results, where_filter)
    
    def get_book_by_id(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific book by ID"""
        try:
            results = self.collection.get(ids=[book_id])
            
            if results['ids']:
                return {
                    "id": results['ids'][0],
                    "metadata": results['metadatas'][0],
                    "document": results['documents'][0]
                }
            return None
            
        except Exception as e:
            print(f"Error getting book by ID: {e}")
            return None
    
    def delete_books(self, book_ids: List[str]) -> bool:
        """Delete books from the vector store"""
        try:
            self.collection.delete(ids=book_ids)
            return True
        except Exception as e:
            print(f"Error deleting books: {e}")
            return False
    
    def update_book(self, book_id: str, book_embedding: Dict[str, Any]) -> bool:
        """Update a book's embedding and metadata"""
        try:
            # Delete existing entry
            self.collection.delete(ids=[book_id])
            
            # Add updated entry
            self.collection.add(
                ids=[book_embedding["book_id"]],
                embeddings=[book_embedding["embedding"]],
                metadatas=[book_embedding["metadata"]],
                documents=[book_embedding["text"]]
            )
            
            return True
            
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            
            return {
                "collection_name": self.collection_name,
                "total_books": count,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {}