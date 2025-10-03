# debug_harmonizer.py
# Place this file in the project root directory

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from src.data.harmonizer import HarmonizerFactory, DataTransformers
from src.core.models import GenreEnum
import json

def debug_sample_data():
    """Debug what's in the sample data"""
    print("🔍 Debugging Sample Data...")
    
    # Check if files exist
    files_to_check = [
        'data/raw/bookstore_a_sample.json',
        'data/raw/bookstore_b_sample.json'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"\n✅ Found: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(f"   📊 Contains {len(data)} records")
                
                # Show first record structure
                if data:
                    print(f"   📋 First record structure:")
                    first_record = data[0]
                    for key, value in first_record.items():
                        print(f"      {key}: {repr(value)} ({type(value).__name__})")
                else:
                    print("   ⚠️  File is empty!")
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"\n❌ Missing: {file_path}")

def test_with_manual_data():
    """Test with manually created data to ensure harmonizer works"""
    print("\n🧪 Testing with Manual Data...")
    
    # Create test data manually
    manual_bookstore_a = {
        "book_id": "A001",
        "book_title": "The Great Manual Test",
        "author_name": "Test Author",
        "category": "Science Fiction",
        "retail_price": "$25.99",
        "customer_rating": "4.5",
        "num_reviews": "150",
        "in_stock": True,
        "pub_year": "2020",
        "publisher_name": "Test Publishers",
        "book_description": "A manually created test book for debugging.",
        "isbn_number": "978-1234567890"
    }
    
    manual_bookstore_b = {
        "id": "B001",
        "name": "Another Manual Test Book",
        "writers": "Jane Test, Bob Test",
        "genre_tags": ["Fantasy", "Adventure"],
        "cost": 19.99,
        "stars": 4.2,
        "total_ratings": 89,
        "available": "yes",
        "published": "2019-06-15",
        "publishing_house": "Manual Test Publishers",
        "summary": "Another manually created test book.",
        "isbn13": "9789876543210",
        "format": "Paperback",
        "page_count": 250
    }
    
    # Test harmonizers
    try:
        harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
        harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
        
        result_a = harmonizer_a.harmonize(manual_bookstore_a)
        result_b = harmonizer_b.harmonize(manual_bookstore_b)
        
        print("\n📚 Bookstore A Result: ")
        print(f"   Title: {result_a.title}")
        print(f"   Author: {result_a.author}")
        print(f"   Price: ${result_a.price}")
        print(f"   Genre: {result_a.genre}")
        print(f"   Store: {result_a.store_name}")
        
        print("\n📚 Bookstore B Result:")
        print(f"   Title: {result_b.title}")
        print(f"   Authors: {result_b.authors}")
        print(f"   Price: ${result_b.price}")
        print(f"   Genre: {result_b.genre}")
        print(f"   Store: {result_b.store_name}")
        
        print("\n✅ Manual test successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error in manual test: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_test_data_inline():
    """Generate test data inline and test"""
    print("\n🏭 Generating Test Data Inline...")
    
    # Generate small test dataset
    test_data_a = []
    test_data_b = []
    
    for i in range(5):
        # Bookstore A format
        book_a = {
            "book_id": f"TEST_A_{i+1}",
            "book_title": f"Test Book A {i+1}",
            "author_name": f"Author {chr(65+i)}",  # Author A, B, C, etc.
            "category": ["Fiction", "Science Fiction", "Fantasy", "Mystery", "Romance"][i],
            "retail_price": f"${15.99 + i*5:.2f}",
            "customer_rating": f"{3.5 + i*0.3:.1f}",
            "num_reviews": str(100 + i*50),
            "in_stock": i % 2 == 0,  # Alternate availability
            "pub_year": str(2020 + i),
            "publisher_name": f"Test Publisher {i+1}",
            "book_description": f"This is test book number {i+1} for bookstore A.",
            "isbn_number": f"978123456789{i}"
        }
        test_data_a.append(book_a)
        
        # Bookstore B format
        book_b = {
            "id": f"TEST_B_{i+1}",
            "name": f"Test Book B {i+1}",
            "writers": f"Writer {chr(65+i)}, Co-Writer {chr(90-i)}",
            "genre_tags": [["Fiction"], ["Science Fiction"], ["Fantasy"], ["Mystery"], ["Romance"]][i],
            "cost": 12.99 + i*3,
            "stars": 3.0 + i*0.4,
            "total_ratings": 80 + i*40,
            "available": ["yes", "no", "yes", "limited", "yes"][i],
            "published": f"201{9-i}-{6+i:02d}-15",
            "publishing_house": f"Test House {i+1}",
            "summary": f"This is test book number {i+1} for bookstore B.",
            "isbn13": f"979876543210{i}",
            "format": ["Paperback", "Hardcover", "Ebook", "Audiobook", "Paperback"][i],
            "page_count": 200 + i*50
        }
        test_data_b.append(book_b)
    
    # Test harmonization
    try:
        harmonizer_a = HarmonizerFactory.create_harmonizer("bookstore_a")
        harmonizer_b = HarmonizerFactory.create_harmonizer("bookstore_b")
        
        results_a = harmonizer_a.batch_harmonize(test_data_a)
        results_b = harmonizer_b.batch_harmonize(test_data_b)
        
        print(f"\n📊 Processed {len(results_a)} books from Bookstore A:")
        for book in results_a:
            print(f"   • {book.title} by {book.author} - ${book.price} ({book.genre})")
        
        print(f"\n📊 Processed {len(results_b)} books from Bookstore B:")
        for book in results_b:
            print(f"   • {book.title} by {', '.join(book.authors or [])} - ${book.price} ({book.genre})")
        
        # Calculate stats
        all_books = results_a + results_b
        avg_price = sum(book.price for book in all_books) / len(all_books)
        
        print(f"\n📈 Statistics:")
        print(f"   • Total harmonized books: {len(all_books)}")
        print(f"   • Average price: ${avg_price:.2f}")
        print(f"   • Price range: ${min(book.price for book in all_books):.2f} - ${max(book.price for book in all_books):.2f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in inline test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Harmonizer Debug Script")
    print("=" * 50)
    
    # Step 1: Check sample data files
    debug_sample_data()
    
    # Step 2: Test with manual data
    manual_success = test_with_manual_data()
    
    # Step 3: Generate and test inline data
    if manual_success:
        generate_test_data_inline()
        print("\n🎉 Debug complete! Harmonizer is working correctly.")
        print("\n💡 If your original sample data was empty, run:")
        print("   python scripts/generate_sample_data.py")
    else:
        print("\n❌ There's an issue with the harmonizer implementation.")

if __name__ == "__main__":
    main()