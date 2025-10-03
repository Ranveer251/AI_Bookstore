from typing import Dict, Any, List
from src.data.harmonizer.base import BaseHarmonizer
from src.data.harmonizer.transformers import DataTransformers
from src.core.models import UnifiedBookModel

class BookstoreAHarmonizer(BaseHarmonizer):
    """
    Harmonizer for Bookstore A schema
    Example schema: {
        "book_id": "123",
        "book_title": "Example Book",
        "author_name": "John Doe",
        "category": "Fiction",
        "retail_price": "$19.99",
        "customer_rating": "4.5",
        "num_reviews": "150",
        "in_stock": true,
        "pub_year": "2020",
        "publisher_name": "Example Publishers",
        "book_description": "A great book...",
        "isbn_number": "978-1234567890"
    }
    """
    
    def __init__(self):
        super().__init__("store_a", "Bookstore A")
    
    def get_schema_mapping(self) -> Dict[str, str]:
        return {
            "book_id": "source_id",
            "book_title": "title",
            "author_name": "author",
            "category": "genre",
            "retail_price": "price",
            "customer_rating": "rating",
            "num_reviews": "rating_count",
            "in_stock": "availability",
            "pub_year": "publication_year",
            "publisher_name": "publisher",
            "book_description": "description",
            "isbn_number": "isbn"
        }
    
    def harmonize(self, raw_data: Dict[str, Any]) -> UnifiedBookModel:

        return UnifiedBookModel(
            title=DataTransformers.clean_text(raw_data.get("book_title", "")) or "",
            author=DataTransformers.clean_text(raw_data.get("author_name", "")) or "",
            authors=DataTransformers.parse_authors(raw_data.get("author_name")),
            genre=DataTransformers.normalize_genre(raw_data.get("category")),
            price=DataTransformers.parse_price(raw_data.get("retail_price", 0)),
            rating=DataTransformers.normalize_rating(raw_data.get("customer_rating")),
            rating_count=int(raw_data.get("num_reviews", 0)) if raw_data.get("num_reviews") else None,
            availability=bool(raw_data.get("in_stock", True)),
            publication_year = next((int(raw_data["pub_year"]) for v in [raw_data.get("pub_year")] if v and str(v).strip().lstrip('-').isdigit()), None),
            publisher=DataTransformers.clean_text(raw_data.get("publisher_name")),
            description=DataTransformers.clean_text(raw_data.get("book_description")),
            isbn=DataTransformers.parse_isbn(raw_data.get("isbn_number")),
            store_id=self.store_id,
            store_name=self.store_name,
            source_schema="bookstore_a"
        )


class BookstoreBHarmonizer(BaseHarmonizer):
    """
    Harmonizer for Bookstore B schema
    Example schema: {
        "id": "456",
        "name": "Another Book",
        "writers": "Jane Smith, Bob Wilson",
        "genre_tags": ["Fantasy", "Adventure"],
        "cost": 24.99,
        "stars": 3.8,
        "total_ratings": 89,
        "available": "yes",
        "published": "2019-03-15",
        "publishing_house": "Great Books Inc",
        "summary": "An amazing story...",
        "isbn13": "9781234567890",
        "format": "Hardcover",
        "page_count": 320
    }
    """
    
    def __init__(self):
        super().__init__("store_b", "Bookstore B")
    
    def get_schema_mapping(self) -> Dict[str, str]:
        return {
            "id": "source_id",
            "name": "title",
            "writers": "authors",
            "genre_tags": "genres",
            "cost": "price",
            "stars": "rating",
            "total_ratings": "rating_count",
            "available": "availability",
            "published": "publication_date",
            "publishing_house": "publisher",
            "summary": "description",
            "isbn13": "isbn",
            "format": "format_type",
            "page_count": "pages"
        }
    
    def harmonize(self, raw_data: Dict[str, Any]) -> UnifiedBookModel:
        # Handle multiple genres
        genre_tags = raw_data.get("genre_tags", [])
        primary_genre = DataTransformers.normalize_genre(
            genre_tags[0] if isinstance(genre_tags, list) and genre_tags else None
        )
        
        # Handle availability string
        availability = raw_data.get("available", "yes")
        is_available = availability.lower() in ["yes", "true", "1", "available"]
        
        return UnifiedBookModel(
            title=DataTransformers.clean_text(raw_data.get("name", "")) or "",
            author=DataTransformers.parse_authors(raw_data.get("writers", ""))[0] if raw_data.get("writers") else "",
            authors=DataTransformers.parse_authors(raw_data.get("writers")),
            genre=primary_genre,
            genres=[DataTransformers.normalize_genre(g) for g in genre_tags] if isinstance(genre_tags, list) else [primary_genre],
            price=DataTransformers.parse_price(raw_data.get("cost", 0)),
            rating=DataTransformers.normalize_rating(raw_data.get("stars")),
            rating_count=int(raw_data.get("total_ratings", 0)) if raw_data.get("total_ratings") else None,
            availability=is_available,
            publication_date=DataTransformers.parse_date(raw_data.get("published")),
            publisher=DataTransformers.clean_text(raw_data.get("publishing_house")),
            description=DataTransformers.clean_text(raw_data.get("summary")),
            isbn=DataTransformers.parse_isbn(raw_data.get("isbn13")),
            format_type=DataTransformers.clean_text(raw_data.get("format", "Physical")) or "Physical",
            pages=int(raw_data.get("page_count", "0")) if raw_data.get("page_count") else None,
            store_id=self.store_id,
            store_name=self.store_name,
            source_schema="bookstore_b"
        )