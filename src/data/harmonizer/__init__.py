from typing import List
from .base import BaseHarmonizer
from .schema_mapper import BookstoreAHarmonizer, BookstoreBHarmonizer
from .transformers import DataTransformers

class HarmonizerFactory:
    """Factory class for creating appropriate harmonizers"""
    
    _harmonizers = {
        "bookstore_a": BookstoreAHarmonizer,
        "bookstore_b": BookstoreBHarmonizer,
    }
    
    @classmethod
    def create_harmonizer(cls, schema_type: str) -> BaseHarmonizer:
        """Create harmonizer instance based on schema type"""
        if schema_type not in cls._harmonizers:
            raise ValueError(f"Unknown schema type: {schema_type}")
        
        return cls._harmonizers[schema_type]()
    
    @classmethod
    def get_available_schemas(cls) -> List[str]:
        """Get list of available schema types"""
        return list(cls._harmonizers.keys())
    
    @classmethod
    def register_harmonizer(cls, schema_type: str, harmonizer_class: type):
        """Register new harmonizer class"""
        cls._harmonizers[schema_type] = harmonizer_class

if __name__ == "__main__":
    # Sample data for testing
    bookstore_a_sample = {
        "book_id": "123",
        "book_title": "The Great Adventure",
        "author_name": "John Smith",
        "category": "Science Fiction",
        "retail_price": "$19.99",
        "customer_rating": "4.3",
        "num_reviews": "127",
        "in_stock": True,
        "pub_year": "2020",
        "publisher_name": "Future Books",
        "book_description": "An epic journey through space and time.",
        "isbn_number": "978-1234567890"
    }
    
    bookstore_b_sample = {
        "id": "456",
        "name": "Mystery of the Ancient Castle",
        "writers": "Jane Doe, Robert Brown",
        "genre_tags": ["Mystery", "Thriller"],
        "cost": 24.99,
        "stars": 4.7,
        "total_ratings": 203,
        "available": "yes",
        "published": "2019-03-15",
        "publishing_house": "Mystery House Publishers",
        "summary": "A thrilling mystery set in medieval times.",
        "isbn13": "9789876543210",
        "format": "Hardcover",
        "page_count": 384
    }
    
    # Test harmonizers
    harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
    harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
    
    unified_book_a = harmonizer_a.harmonize(bookstore_a_sample)
    unified_book_b = harmonizer_b.harmonize(bookstore_b_sample)
    
    print("Harmonized Book A:")
    print(unified_book_a.json(indent=2))
    print("\nHarmonized Book B:")
    print(unified_book_b.json(indent=2))