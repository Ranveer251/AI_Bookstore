# tests/unit/test_harmonizer.py
import pytest
from datetime import datetime
from src.data.harmonizer import HarmonizerFactory, DataTransformers
from src.core.models import GenreEnum, UnifiedBookModel

class TestDataTransformers:
    """Test data transformation utilities"""
    
    def test_clean_text(self):
        assert DataTransformers.clean_text("  Hello   World  ") == "Hello World"
        assert DataTransformers.clean_text("Book@#$%Title!") == "BookTitle!"
        assert DataTransformers.clean_text("") is None
        assert DataTransformers.clean_text(None) is None
    
    def test_parse_price(self):
        assert DataTransformers.parse_price("$19.99") == 19.99
        assert DataTransformers.parse_price("€24.50") == 24.50
        assert DataTransformers.parse_price(29.99) == 29.99
        assert DataTransformers.parse_price("invalid") == 0.0
        assert DataTransformers.parse_price("£15.99") == 15.99
    
    def test_parse_date(self):
        date_str = "2020-03-15"
        result = DataTransformers.parse_date(date_str)
        assert result is not None
        assert result.year == 2020
        assert result.month == 3
        assert result.day == 15
        
        assert DataTransformers.parse_date("2019") == datetime(2019, 1, 1)
        assert DataTransformers.parse_date("invalid") is None
        assert DataTransformers.parse_date(None) is None
    
    def test_normalize_genre(self):
        assert DataTransformers.normalize_genre("Science Fiction") == GenreEnum.SCIENCE_FICTION
        assert DataTransformers.normalize_genre("sci-fi") == GenreEnum.SCIENCE_FICTION
        assert DataTransformers.normalize_genre("Mystery") == GenreEnum.MYSTERY
        assert DataTransformers.normalize_genre("unknown") == GenreEnum.OTHER
        assert DataTransformers.normalize_genre(None) == GenreEnum.OTHER
    
    def test_parse_authors(self):
        assert DataTransformers.parse_authors("John Doe") == ["John Doe"]
        assert DataTransformers.parse_authors("John Doe, Jane Smith") == ["John Doe", "Jane Smith"]
        assert DataTransformers.parse_authors("John Doe & Jane Smith") == ["John Doe", "Jane Smith"]
        assert DataTransformers.parse_authors("") == []
        assert DataTransformers.parse_authors(None) == []
    
    def test_normalize_rating(self):
        assert DataTransformers.normalize_rating(4.5) == 4.5
        assert DataTransformers.normalize_rating(9, max_scale=10) == 4.5
        assert DataTransformers.normalize_rating(80, max_scale=100) == 4.0
        assert DataTransformers.normalize_rating("4.3") == 4.3
        assert DataTransformers.normalize_rating(None) is None
    
    def test_parse_isbn(self):
        assert DataTransformers.parse_isbn("978-1234567890") == "9781234567890"
        assert DataTransformers.parse_isbn("1234567890") == "1234567890"
        assert DataTransformers.parse_isbn("978-1-234-56789-0") == "9781234567890"
        assert DataTransformers.parse_isbn("123") is None
        assert DataTransformers.parse_isbn(None) is None


class TestHarmonizers:
    """Test schema harmonization"""
    
    @pytest.fixture
    def bookstore_a_data(self):
        return {
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
    
    @pytest.fixture
    def bookstore_b_data(self):
        return {
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
    
    def test_bookstore_a_harmonization(self, bookstore_a_data):
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
        result = harmonizer.harmonize(bookstore_a_data)
        
        assert isinstance(result, UnifiedBookModel)
        assert result.title == "The Great Adventure"
        assert result.author == "John Smith"
        assert result.authors == ["John Smith"]
        assert result.genre == GenreEnum.SCIENCE_FICTION
        assert result.price == 19.99
        assert result.rating == 4.3
        assert result.rating_count == 127
        assert result.availability == True
        assert result.publication_year == 2020
        assert result.publisher == "Future Books"
        assert result.isbn == "9781234567890"
        assert result.store_id == "store_a"
        assert result.store_name == "Bookstore A"
        assert result.source_schema == "bookstore_a"
    
    def test_bookstore_b_harmonization(self, bookstore_b_data):
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_b")
        result = harmonizer.harmonize(bookstore_b_data)
        
        assert isinstance(result, UnifiedBookModel)
        assert result.title == "Mystery of the Ancient Castle"
        assert result.author == "Jane Doe"
        assert result.authors == ["Jane Doe", "Robert Brown"]
        assert result.genre == GenreEnum.MYSTERY
        assert result.genres is not None
        assert GenreEnum.MYSTERY in result.genres
        assert GenreEnum.THRILLER in result.genres
        assert result.price == 24.99
        assert result.rating == 4.7
        assert result.rating_count == 203
        assert result.availability == True
        assert result.publication_date is not None
        assert result.publication_date.year == 2019
        assert result.publication_date.month == 3
        assert result.publication_date.day == 15
        assert result.publisher == "Mystery House Publishers"
        assert result.isbn == "9789876543210"
        assert result.format_type == "Hardcover"
        assert result.pages == 384
        assert result.store_id == "store_b"
        assert result.store_name == "Bookstore B"
        assert result.source_schema == "bookstore_b"
    
    def test_batch_harmonization(self, bookstore_a_data, bookstore_b_data):
        harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
        harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
        
        # Test batch processing
        batch_a = harmonizer_a.batch_harmonize([bookstore_a_data, bookstore_a_data])
        batch_b = harmonizer_b.batch_harmonize([bookstore_b_data, bookstore_b_data])
        
        assert len(batch_a) == 2
        assert len(batch_b) == 2
        assert all(isinstance(book, UnifiedBookModel) for book in batch_a)
        assert all(isinstance(book, UnifiedBookModel) for book in batch_b)
    
    def test_factory_methods(self):
        # Test factory creation
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
        assert harmonizer.store_id == "store_a"
        
        # Test available schemas
        schemas = HarmonizerFactory.get_available_schemas()
        assert "bookstore_a" in schemas
        assert "bookstore_b" in schemas
        
        # Test invalid schema
        with pytest.raises(ValueError):
            HarmonizerFactory.create_harmonizer("invalid_schema")


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_required_fields(self):
        # Test with minimal required data
        minimal_data = {
            "book_title": "Test Book",
            "author_name": "Test Author",
            "retail_price": "10.99"
        }
        
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
        result = harmonizer.harmonize(minimal_data)
        
        assert result.title == "Test Book"
        assert result.author == "Test Author"
        assert result.price == 10.99
        assert result.genre == GenreEnum.OTHER  # Default value
        assert result.availability == True  # Default value
    
    def test_malformed_data(self):
        malformed_data = {
            "book_title": "",  # Empty title
            "author_name": None,  # None author
            "retail_price": "invalid_price",
            "customer_rating": "not_a_number",
            "pub_year": "invalid_year"
        }
        
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
        result = harmonizer.harmonize(malformed_data)
        
        assert result.title == ""
        assert result.author == ""
        assert result.price == 0.0
        assert result.rating is None
        assert result.publication_year is None
    
    def test_extreme_values(self):
        extreme_data = {
            "book_title": "A" * 1000,  # Very long title
            "retail_price": "999999.99",  # High price
            "customer_rating": "10.0",  # Rating out of normal range
            "num_reviews": "-5"  # Negative reviews
        }
        
        harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
        result = harmonizer.harmonize(extreme_data)
        
        assert len(result.title) == 1000
        assert result.price == 999999.99
        assert result.rating == 5.0  # Should be clamped to max
        assert result.rating_count == -5  # Preserved as-is (validation could be added)


# Example demonstration script
def demonstrate_harmonization():
    """Demonstrate the harmonization process with sample data"""
    
    print("=== Schema Harmonization Demonstration ===\n")
    
    # Sample data from different bookstores
    bookstore_a_samples = [
        {
            "book_id": "A001",
            "book_title": "Dune",
            "author_name": "Frank Herbert",
            "category": "Science Fiction",
            "retail_price": "$16.99",
            "customer_rating": "4.6",
            "num_reviews": "2847",
            "in_stock": True,
            "pub_year": "1965",
            "publisher_name": "Chilton Books",
            "book_description": "A science fiction masterpiece about politics, religion, and ecology on the desert planet Arrakis.",
            "isbn_number": "978-0441172719"
        },
        {
            "book_id": "A002",
            "book_title": "The Hobbit",
            "author_name": "J.R.R. Tolkien",
            "category": "Fantasy",
            "retail_price": "$14.99",
            "customer_rating": "4.8",
            "num_reviews": "5203",
            "in_stock": True,
            "pub_year": "1937",
            "publisher_name": "George Allen & Unwin",
            "book_description": "A classic fantasy adventure following Bilbo Baggins on his unexpected journey.",
            "isbn_number": "978-0547928227"
        }
    ]
    
    bookstore_b_samples = [
        {
            "id": "B001",
            "name": "1984",
            "writers": "George Orwell",
            "genre_tags": ["Fiction", "Dystopian"],
            "cost": 13.99,
            "stars": 4.4,
            "total_ratings": 8921,
            "available": "yes",
            "published": "1949-06-08",
            "publishing_house": "Secker & Warburg",
            "summary": "A dystopian social science fiction novel about totalitarian control.",
            "isbn13": "9780451524935",
            "format": "Paperback",
            "page_count": 328
        },
        {
            "id": "B002",
            "name": "To Kill a Mockingbird",
            "writers": "Harper Lee",
            "genre_tags": ["Fiction", "Classic"],
            "cost": 12.99,
            "stars": 4.3,
            "total_ratings": 6754,
            "available": "yes",
            "published": "1960-07-11",
            "publishing_house": "J.B. Lippincott & Co.",
            "summary": "A gripping tale of racial injustice and childhood innocence in the American South.",
            "isbn13": "9780061120084",
            "format": "Paperback",
            "page_count": 376
        }
    ]
    
    # Initialize harmonizers
    harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
    harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
    
    print("📚 Processing Bookstore A Data:")
    print("-" * 40)
    harmonized_a = harmonizer_a.batch_harmonize(bookstore_a_samples)
    for i, book in enumerate(harmonized_a):
        print(f"Book {i+1}: {book.title} by {book.author}")
        print(f"  Genre: {book.genre.value}")
        print(f"  Price: ${book.price}")
        print(f"  Rating: {book.rating}/5.0 ({book.rating_count} reviews)")
        print(f"  Store: {book.store_name}")
        print()
    
    print("📚 Processing Bookstore B Data:")
    print("-" * 40)
    harmonized_b = harmonizer_b.batch_harmonize(bookstore_b_samples)
    for i, book in enumerate(harmonized_b):
        print(f"Book {i+1}: {book.title} by {', '.join(book.authors or [])}")
        print(f"  Genres: {[g.value for g in (book.genres or [])]}")
        print(f"  Price: ${book.price}")
        print(f"  Rating: {book.rating}/5.0 ({book.rating_count} reviews)")
        print(f"  Format: {book.format_type}, Pages: {book.pages}")
        print(f"  Store: {book.store_name}")
        print()
    
    # Combine all harmonized data
    all_books = harmonized_a + harmonized_b
    
    print("📊 Summary Statistics:")
    print("-" * 40)
    print(f"Total books processed: {len(all_books)}")
    print(f"Average price: ${sum(book.price for book in all_books) / len(all_books):.2f}")
    print(f"Average rating: {sum(book.rating for book in all_books if book.rating) / len([b for b in all_books if b.rating]):.2f}")
    
    # Genre distribution
    from collections import Counter
    genres = [book.genre.value for book in all_books]
    genre_counts = Counter(genres)
    print(f"Genre distribution: {dict(genre_counts)}")
    
    print("\n✅ Harmonization complete! All books now follow the unified schema.")
    
    return all_books


if __name__ == "__main__":
    # Run demonstration
    demonstrate_harmonization()
    
    # Run basic tests
    print("\n🧪 Running basic validation tests...")
    
    # Test data transformers
    transformer_tests = TestDataTransformers()
    transformer_tests.test_parse_price()
    transformer_tests.test_normalize_genre()
    transformer_tests.test_parse_authors()
    print("✅ Data transformer tests passed!")
    
    # Test harmonizers with sample data
    bookstore_a_sample = {
        "book_title": "Test Book",
        "author_name": "Test Author",
        "retail_price": "$9.99",
        "category": "Fiction"
    }
    
    harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
    result = harmonizer.harmonize(bookstore_a_sample)
    assert isinstance(result, UnifiedBookModel)
    print("✅ Basic harmonization test passed!")
    
    print("\n🎉 All tests completed successfully!")