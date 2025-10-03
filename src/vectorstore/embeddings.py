# src/vectorstore/embeddings.py
import numpy as np
from typing import List, Dict, Any, Optional, Union, cast
from sentence_transformers import SentenceTransformer
from abc import ABC, abstractmethod
import hashlib
import json

import torch
from src.core.models import UnifiedBookModel
from config.setting import settings

class BaseEmbeddingGenerator(ABC):
    """Abstract base class for embedding generators"""
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        pass
    
    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        pass
    
    @abstractmethod
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        pass


class SentenceTransformerEmbeddings(BaseEmbeddingGenerator):
    """Sentence Transformer based embedding generator"""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension: int = cast(int, self.model.get_sentence_embedding_dimension())
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not text or not text.strip():
            return [0.0] * self.dimension
        
        embedding: np.ndarray = cast(np.ndarray, self.model.encode(text, convert_to_numpy=True))
        return embedding.tolist()
    
    def to_list(self, x: Any):
        if isinstance(x, list) and all(isinstance(t, torch.Tensor) for t in x):
            # Case: List[Tensor]
            return [t.tolist() for t in x]
        elif isinstance(x, torch.Tensor):
            # Case: single Tensor
            return x.tolist()
        elif isinstance(x, np.ndarray):
            # Case: numpy array
            return x.tolist()
        else:
            raise TypeError(f"Unsupported type: {type(x)}")
    
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not texts:
            return []

        # Track valid texts
        valid_indices = [i for i, t in enumerate(texts) if t and t.strip()]
        valid_texts = [texts[i] for i in valid_indices]

        # Default zero vectors
        embeddings: List[List[float]] = [[0.0] * self.dimension for _ in range(len(texts))]

        if valid_texts:
            valid_embeddings = self.model.encode(valid_texts, convert_to_numpy=True)

            # Convert to list of lists explicitly
            valid_embeddings_list: List[List[float]] = (
                valid_embeddings.tolist()
                if isinstance(valid_embeddings, np.ndarray)
                else [e.tolist() if isinstance(e, torch.Tensor) else e for e in valid_embeddings]
            )

            for idx, emb in zip(valid_indices, valid_embeddings_list):
                embeddings[idx] = emb

        return embeddings

    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        return self.dimension


class OpenAIEmbeddings(BaseEmbeddingGenerator):
    """OpenAI API based embedding generator"""
    
    def __init__(self, model_name: str = "text-embedding-ada-002", api_key: Optional[str] = None):
        try:
            import openai
            self.openai = openai
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        self.model_name = model_name
        self.api_key = api_key or settings.OPENAI_API_KEY
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.openai.api_key = self.api_key
        self.dimension = 1536  # ada-002 dimension
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        if not text or not text.strip():
            return [0.0] * self.dimension
        
        response = self.openai.embeddings.create(
            model=self.model_name,
            input=text
        )
        
        return response.data[0].embedding
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        # Filter out empty texts
        valid_texts = [text if text and text.strip() else " " for text in texts]
        
        response = self.openai.embeddings.create(
            model=self.model_name,
            input=valid_texts
        )
        
        embeddings = []
        for item in response.data:
            embeddings.append(item.embedding)
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        return self.dimension


class BookEmbeddingGenerator:
    """Generate composite embeddings for book data"""
    
    def __init__(self, embedding_generator: BaseEmbeddingGenerator):
        self.embedding_generator = embedding_generator
        self.dimension = embedding_generator.get_embedding_dimension()
    
    def create_book_text(self, book: UnifiedBookModel) -> str:
        """Create composite text representation of a book"""
        components = []
        
        # Title (highest weight)
        if book.title:
            components.append(f"Title: {book.title}")
        
        # Author information
        if book.authors:
            authors_str = ", ".join(book.authors)
            components.append(f"Author: {authors_str}")
        elif book.author:
            components.append(f"Author: {book.author}")
        
        # Genre information
        if book.genres:
            genres_str = ", ".join([g for g in book.genres])
            components.append(f"Genre: {genres_str}")
        elif book.genre:
            components.append(f"Genre: {book.genre}")
        
        # Description/Summary
        if book.description:
            components.append(f"Description: {book.description}")
        elif book.summary:
            components.append(f"Summary: {book.summary}")
        
        # Publisher and publication info
        if book.publisher:
            components.append(f"Publisher: {book.publisher}")
        
        if book.publication_year:
            components.append(f"Year: {book.publication_year}")
        
        # Format information
        if book.format_type and book.format_type != "Physical":
            components.append(f"Format: {book.format_type}")
        
        return " | ".join(components)
    
    def generate_book_embedding(self, book: UnifiedBookModel) -> Dict[str, Any]:
        """Generate embedding for a single book"""
        book_text = self.create_book_text(book)
        embedding = self.embedding_generator.generate_embedding(book_text)
        
        # Create embedding hash for deduplication
        embedding_hash = hashlib.md5(
            json.dumps(embedding, sort_keys=True).encode()
        ).hexdigest()
        
        return {
            "book_id": book.id,
            "embedding": embedding,
            "text": book_text,
            "embedding_hash": embedding_hash,
            "metadata": {
                "title": book.title,
                "author": book.author,
                "authors": book.authors,
                "genre": book.genre,
                "genres": [g for g in book.genres] if book.genres else [book.genre],
                "price": book.price,
                "rating": book.rating,
                "store_id": book.store_id,
                "store_name": book.store_name,
                "isbn": book.isbn,
                "publisher": book.publisher,
                "publication_year": book.publication_year,
                "format_type": book.format_type,
                "availability": book.availability
            }
        }
    
    def generate_book_embeddings(self, books: List[UnifiedBookModel]) -> List[Dict[str, Any]]:
        """Generate embeddings for multiple books"""
        # Create text representations
        book_texts = [self.create_book_text(book) for book in books]
        
        # Generate embeddings in batch
        embeddings = self.embedding_generator.generate_embeddings(book_texts)
        
        # Create embedding objects
        results = []
        for book, embedding, text in zip(books, embeddings, book_texts):
            embedding_hash = hashlib.md5(
                json.dumps(embedding, sort_keys=True).encode()
            ).hexdigest()
            
            result = {
                "book_id": book.id,
                "embedding": embedding,
                "text": text,
                "embedding_hash": embedding_hash,
                "metadata": {
                    "title": book.title,
                    "author": book.author,
                    "authors": book.authors,
                    "genre": book.genre,
                    "genres": [g for g in book.genres] if book.genres else [book.genre],
                    "price": book.price,
                    "rating": book.rating,
                    "store_id": book.store_id,
                    "store_name": book.store_name,
                    "isbn": book.isbn,
                    "publisher": book.publisher,
                    "publication_year": book.publication_year,
                    "format_type": book.format_type,
                    "availability": book.availability
                }
            }
            results.append(result)
        
        return results