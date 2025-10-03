import re
from typing import Dict, Any, List, Optional
from src.core.models import GenreEnum

class EntityExtractor:
    """Extract entities and parameters from queries"""
    
    def __init__(self):
        # Genre mappings
        self.genre_keywords = {
            'science fiction': ['sci-fi', 'scifi', 'science fiction', 'sf', 'space', 'futuristic'],
            'fantasy': ['fantasy', 'magic', 'wizard', 'dragon', 'medieval', 'quest'],
            'mystery': ['mystery', 'detective', 'crime', 'thriller', 'investigation', 'murder'],
            'romance': ['romance', 'love', 'romantic', 'relationship'],
            'horror': ['horror', 'scary', 'terror', 'haunted', 'ghost'],
            'biography': ['biography', 'autobiography', 'memoir', 'life story'],
            'history': ['history', 'historical', 'war', 'ancient'],
            'self-help': ['self-help', 'self help', 'personal development', 'motivation'],
            'children': ['children', 'kids', 'young readers', 'picture book'],
            'young adult': ['ya', 'young adult', 'teen', 'teenage']
        }
        
        # Store name patterns
        self.store_patterns = [
            r'(store|bookstore)\s+([AB]|a|b)',
            r'(bookstore|shop)\s+([AB]|a|b)',
        ]
    
    def extract(self, query: str) -> Dict[str, Any]:
        """Extract entities from query"""
        query_lower = query.lower().strip()
        entities = {
            'genres': [],
            'price_range': None,
            'rating_range': None,
            'authors': [],
            'stores': [],
            'format': None,
            'availability': None,
            'sort_by': None,
            'limit': None
        }
        
        # Extract genres
        entities['genres'] = self._extract_genres(query_lower)
        
        # Extract price range
        entities['price_range'] = self._extract_price_range(query_lower)
        
        # Extract rating range
        entities['rating_range'] = self._extract_rating_range(query_lower)
        
        # Extract stores
        entities['stores'] = self._extract_stores(query_lower)
        
        # Extract format
        entities['format'] = self._extract_format(query_lower)
        
        # Extract availability
        entities['availability'] = self._extract_availability(query_lower)
        
        # Extract sorting preference
        entities['sort_by'] = self._extract_sort_preference(query_lower)
        
        # Extract result limit
        entities['limit'] = self._extract_limit(query_lower)
        
        return entities
    
    def _extract_genres(self, query: str) -> List[str]:
        """Extract genre mentions"""
        found_genres = []
        
        for genre, keywords in self.genre_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    found_genres.append(genre)
                    break
        
        return list(set(found_genres))
    
    def _extract_price_range(self, query: str) -> Optional[Dict[str, float]]:
        """Extract price constraints"""
        price_range = {}
        
        # Under/below/less than
        under_match = re.search(r'(under|below|less than)\s+\$?(\d+(?:\.\d{2})?)', query)
        if under_match:
            price_range['max'] = float(under_match.group(2))
        
        # Over/above/more than
        over_match = re.search(r'(over|above|more than)\s+\$?(\d+(?:\.\d{2})?)', query)
        if over_match:
            price_range['min'] = float(over_match.group(2))
        
        # Between X and Y
        between_match = re.search(r'between\s+\$?(\d+(?:\.\d{2})?)\s+and\s+\$?(\d+(?:\.\d{2})?)', query)
        if between_match:
            price_range['min'] = float(between_match.group(1))
            price_range['max'] = float(between_match.group(2))
        
        return price_range if price_range else None
    
    def _extract_rating_range(self, query: str) -> Optional[Dict[str, float]]:
        """Extract rating constraints"""
        rating_range = {}
        
        # Rated above/over
        above_match = re.search(r'rated?\s+(above|over)\s+(\d(?:\.\d)?)', query)
        if above_match:
            rating_range['min'] = float(above_match.group(2))
        
        # Rated below/under
        below_match = re.search(r'rated?\s+(below|under)\s+(\d(?:\.\d)?)', query)
        if below_match:
            rating_range['max'] = float(below_match.group(2))
        
        # Highly rated
        if 'highly rated' in query or 'high rating' in query:
            rating_range['min'] = 4.0
        
        return rating_range if rating_range else None
    
    def _extract_stores(self, query: str) -> List[str]:
        """Extract store mentions"""
        stores = []
        
        for pattern in self.store_patterns:
            match = re.search(pattern, query)
            if match:
                store_letter = match.group(2).upper()
                stores.append(f"store_{store_letter.lower()}")
        
        # Check for "both stores"
        if 'both stores' in query or 'all stores' in query:
            stores = ['store_a', 'store_b']
        
        return stores
    
    def _extract_format(self, query: str) -> Optional[str]:
        """Extract book format preference"""
        format_keywords = {
            'ebook': ['ebook', 'e-book', 'digital', 'kindle'],
            'audiobook': ['audiobook', 'audio book', 'audible'],
            'hardcover': ['hardcover', 'hardback'],
            'paperback': ['paperback', 'softcover']
        }
        
        for format_type, keywords in format_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return format_type.capitalize()
        
        return None
    
    def _extract_availability(self, query: str) -> Optional[bool]:
        """Extract availability requirement"""
        if any(phrase in query for phrase in ['in stock', 'available', 'available now']):
            return True
        
        if any(phrase in query for phrase in ['out of stock', 'unavailable']):
            return False
        
        return None
    
    def _extract_sort_preference(self, query: str) -> Optional[str]:
        """Extract sorting preference"""
        if 'cheapest' in query or 'lowest price' in query:
            return 'price_asc'
        
        if 'most expensive' in query or 'highest price' in query:
            return 'price_desc'
        
        if 'highest rated' in query or 'best rated' in query:
            return 'rating_desc'
        
        if 'newest' in query or 'most recent' in query:
            return 'year_desc'
        
        if 'oldest' in query:
            return 'year_asc'
        
        return None
    
    def _extract_limit(self, query: str) -> Optional[int]:
        """Extract result limit"""
        # Top N pattern
        top_match = re.search(r'top\s+(\d+)', query)
        if top_match:
            return int(top_match.group(1))
        
        # N books pattern
        books_match = re.search(r'(\d+)\s+books?', query)
        if books_match:
            return int(books_match.group(1))
        
        # First N pattern
        first_match = re.search(r'first\s+(\d+)', query)
        if first_match:
            return int(first_match.group(1))
        
        return None
