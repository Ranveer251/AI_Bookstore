import re
from typing import Optional, List, Union
from datetime import datetime
from src.core.models import GenreEnum

class DataTransformers:
    """Utility functions for data transformation"""
    
    @staticmethod
    def clean_text(text: Optional[str]) -> Optional[str]:
        """Clean and normalize text fields"""
        if not text:
            return None
        
        # Remove extra whitespace and normalize
        text = ' '.join(text.strip().split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-\.\,\!\?\:\;]', '', text)
        
        return text if text else None
    
    @staticmethod
    def parse_price(price_str: Union[str, float, int]) -> float:
        """Parse price from various formats"""
        if isinstance(price_str, (int, float)):
            return float(price_str)
        
        if isinstance(price_str, str):
            # Remove currency symbols and extra characters
            price_str = re.sub(r'[^\d\.]', '', price_str)
            try:
                return float(price_str)
            except ValueError:
                return 0.0
        
        return 0.0
    
    @staticmethod
    def parse_date(date_str: Optional[str]) -> Optional[datetime]:
        """Parse date from various string formats"""
        if not date_str:
            return None
        
        # Common date formats
        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%Y-%m-%d %H:%M:%S"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def normalize_genre(genre_str: Optional[str]) -> GenreEnum:
        """Normalize genre to standard enum"""
        if not genre_str:
            return GenreEnum.OTHER
        
        genre_str = genre_str.lower().strip()
        
        # Genre mapping dictionary
        genre_mapping = {
            'fiction': GenreEnum.FICTION,
            'non-fiction': GenreEnum.NON_FICTION,
            'nonfiction': GenreEnum.NON_FICTION,
            'science fiction': GenreEnum.SCIENCE_FICTION,
            'sci-fi': GenreEnum.SCIENCE_FICTION,
            'scifi': GenreEnum.SCIENCE_FICTION,
            'fantasy': GenreEnum.FANTASY,
            'mystery': GenreEnum.MYSTERY,
            'thriller': GenreEnum.THRILLER,
            'romance': GenreEnum.ROMANCE,
            'horror': GenreEnum.HORROR,
            'biography': GenreEnum.BIOGRAPHY,
            'history': GenreEnum.HISTORY,
            'science': GenreEnum.SCIENCE,
            'technology': GenreEnum.TECHNOLOGY,
            'tech': GenreEnum.TECHNOLOGY,
            'business': GenreEnum.BUSINESS,
            'self-help': GenreEnum.SELF_HELP,
            'self help': GenreEnum.SELF_HELP,
            'selfhelp': GenreEnum.SELF_HELP,
            'children': GenreEnum.CHILDREN,
            'kids': GenreEnum.CHILDREN,
            'young adult': GenreEnum.YOUNG_ADULT,
            'ya': GenreEnum.YOUNG_ADULT,
            'teen': GenreEnum.YOUNG_ADULT,
        }
        
        # Try exact match first
        if genre_str in genre_mapping:
            return genre_mapping[genre_str]
        
        # Try partial matches
        for key, value in genre_mapping.items():
            if key in genre_str or genre_str in key:
                return value
        
        return GenreEnum.OTHER
    
    @staticmethod
    def parse_authors(author_str: Optional[str]) -> List[str]:
        """Parse multiple authors from a string"""
        if not author_str:
            return []
        
        # Split by common separators
        separators = [',', ';', ' and ', ' & ', '|']
        authors = [author_str]
        
        for sep in separators:
            temp_authors = []
            for author in authors:
                temp_authors.extend([a.strip() for a in author.split(sep)])
            authors = temp_authors
        
        # Clean and filter empty strings
        authors = [DataTransformers.clean_text(author) for author in authors]
        authors = [author for author in authors if author]
        
        return authors
    
    @staticmethod
    def normalize_rating(rating: Optional[Union[str, float, int]], 
                        max_scale: int = 5) -> Optional[float]:
        """Normalize rating to 5-point scale"""
        if rating is None:
            return None
        
        try:
            rating_val = float(rating)
            
            # Convert to 5-point scale if necessary
            if max_scale == 10:
                rating_val = rating_val / 2
            elif max_scale == 100:
                rating_val = rating_val / 20
            
            # Clamp to valid range
            rating_val = max(0.0, min(5.0, rating_val))
            
            return round(rating_val, 1)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def parse_isbn(isbn_str: Optional[str]) -> Optional[str]:
        """Clean and validate ISBN"""
        if not isbn_str:
            return None
        
        # Remove all non-digit characters except X
        isbn = re.sub(r'[^\dX]', '', str(isbn_str).upper())
        
        # Validate length (ISBN-10 or ISBN-13)
        if len(isbn) in [10, 13]:
            return isbn
        
        return None
    
    @staticmethod
    def extract_year_from_text(text: Optional[str]) -> Optional[int]:
        """Extract publication year from text"""
        if not text:
            return None
        
        # Look for 4-digit years
        year_match = re.search(r'\b(19|20)\d{2}\b', str(text))
        if year_match:
            year = int(year_match.group())
            current_year = datetime.now().year
            if 1800 <= year <= current_year + 5:  # Reasonable year range
                return year
        
        return None