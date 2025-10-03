# Quick test script
from src.data.harmonizer import HarmonizerFactory
import json

# Load sample data
with open('data/raw/bookstore_b_sample.json', 'r') as f:
    raw_data = json.load(f)

# Harmonize data
harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
unified_books = harmonizer.batch_harmonize(raw_data[:10])

# Print results
for book in unified_books:
    print(f"{book.title} by {book.author} - ${book.price}")