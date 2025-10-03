"""
Generate sample data for testing the harmonization system
"""
import json
import random
from datetime import datetime, timedelta
from faker import Faker
from typing import List, Dict, Any

fake = Faker()

# Sample genres and their variations
GENRES = {
    "Fiction": ["Fiction", "Literary Fiction", "Contemporary Fiction"],
    "Science Fiction": ["Science Fiction", "Sci-Fi", "Sci Fi", "SF"],
    "Fantasy": ["Fantasy", "Epic Fantasy", "Urban Fantasy"],
    "Mystery": ["Mystery", "Crime", "Detective"],
    "Thriller": ["Thriller", "Suspense"],
    "Romance": ["Romance", "Contemporary Romance", "Historical Romance"],
    "Horror": ["Horror", "Supernatural", "Gothic"],
    "Biography": ["Biography", "Autobiography", "Memoir"],
    "History": ["History", "Historical", "World History"],
    "Science": ["Science", "Popular Science", "Physics", "Biology"],
    "Business": ["Business", "Economics", "Management"],
    "Self-Help": ["Self-Help", "Self Help", "Personal Development"],
    "Children": ["Children", "Kids", "Picture Books"],
    "Young Adult": ["Young Adult", "YA", "Teen"]
}

def generate_isbn13():
    """Generate a realistic ISBN-13"""
    prefix = "978"
    group = str(random.randint(0, 9))
    publisher = str(random.randint(1000, 9999))
    title = str(random.randint(1000, 9999))
    check = str(random.randint(0, 9))
    return f"{prefix}{group}{publisher}{title}{check}"

def generate_isbn10():
    """Generate a realistic ISBN-10"""
    digits = [str(random.randint(0, 9)) for _ in range(9)]
    check = random.choice("0123456789X")
    return "".join(digits) + check

def generate_bookstore_a_data(num_books: int = 1000) -> List[Dict[str, Any]]:
    """Generate sample data for Bookstore A schema"""
    books = []
    
    for i in range(num_books):
        genre = random.choice(list(GENRES.keys()))
        genre_variant = random.choice(GENRES[genre])
        
        book = {
            "book_id": f"A{i+1:04d}",
            "book_title": fake.catch_phrase().replace(",", "").title(),
            "author_name": fake.name(),
            "category": genre_variant,
            "retail_price": f"${random.uniform(5.99, 49.99):.2f}",
            "customer_rating": str(round(random.uniform(1.0, 5.0), 1)),
            "num_reviews": str(random.randint(0, 10000)),
            "in_stock": random.choice([True, False]),
            "pub_year": str(random.randint(1950, 2024)),
            "publisher_name": fake.company(),
            "book_description": fake.text(max_nb_chars=500),
            "isbn_number": generate_isbn13() if random.random() > 0.3 else generate_isbn10()
        }
        books.append(book)
    
    return books

def generate_bookstore_b_data(num_books: int = 1000) -> List[Dict[str, Any]]:
    """Generate sample data for Bookstore B schema"""
    books = []
    
    for i in range(num_books):
        # Select multiple genres
        main_genre = random.choice(list(GENRES.keys()))
        genre_tags = [main_genre]
        if random.random() > 0.7:  # 30% chance of multiple genres
            secondary_genre = random.choice(list(GENRES.keys()))
            if secondary_genre != main_genre:
                genre_tags.append(secondary_genre)
        
        # Generate multiple authors sometimes
        authors = [fake.name()]
        if random.random() > 0.8:  # 20% chance of multiple authors
            authors.append(fake.name())
        
        # Random publication date
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2024, 12, 31)
        pub_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        book = {
            "id": f"B{i+1:04d}",
            "name": fake.catch_phrase().replace(",", "").title(),
            "writers": ", ".join(authors),
            "genre_tags": genre_tags,
            "cost": round(random.uniform(5.99, 49.99), 2),
            "stars": round(random.uniform(1.0, 5.0), 1),
            "total_ratings": random.randint(0, 10000),
            "available": random.choice(["yes", "no", "limited"]),
            "published": pub_date.strftime("%Y-%m-%d"),
            "publishing_house": fake.company(),
            "summary": fake.text(max_nb_chars=500),
            "isbn13": generate_isbn13(),
            "format": random.choice(["Hardcover", "Paperback", "Ebook", "Audiobook"]),
            "page_count": random.randint(100, 800)
        }
        books.append(book)
    
    return books

def main():
    """Generate and save sample data"""
    print("Generating sample bookstore data...")
    
    # Generate data
    bookstore_a_data = generate_bookstore_a_data(500)
    bookstore_b_data = generate_bookstore_b_data(500)
    
    # Save to files
    with open("data/raw/bookstore_a_sample.json", "w") as f:
        json.dump(bookstore_a_data, f, indent=2)
    
    with open("data/raw/bookstore_b_sample.json", "w") as f:
        json.dump(bookstore_b_data, f, indent=2, default=str)
    
    print(f"Generated {len(bookstore_a_data)} books for Bookstore A")
    print(f"Generated {len(bookstore_b_data)} books for Bookstore B")
    print("Sample data saved to data/raw/")
    
    # Print sample records
    print("\nSample Bookstore A record:")
    print(json.dumps(bookstore_a_data[0], indent=2))
    
    print("\nSample Bookstore B record:")
    print(json.dumps(bookstore_b_data[0], indent=2, default=str))

if __name__ == "__main__":
    main()