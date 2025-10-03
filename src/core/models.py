from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, validator
from enum import Enum
import uuid

class GenreEnum(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE_FICTION = "Science Fiction"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    HORROR = "Horror"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    SCIENCE = "Science"
    TECHNOLOGY = "Technology"
    BUSINESS = "Business"
    SELF_HELP = "Self-Help"
    CHILDREN = "Children"
    YOUNG_ADULT = "Young Adult"
    OTHER = "Other"

class UnifiedBookModel(BaseModel):
    """Unified book model for harmonized data"""
    
    # Core identifiers
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    isbn: Optional[str] = None
    
    # Basic book information
    title: str
    author: str
    authors: Optional[List[str]] = None  # For multiple authors
    genre: GenreEnum = GenreEnum.OTHER
    genres: Optional[List[GenreEnum]] = None  # For multiple genres
    
    # Publication details
    publisher: Optional[str] = None
    publication_date: Optional[datetime] = None
    publication_year: Optional[int] = None
    edition: Optional[str] = None
    language: str = "English"
    pages: Optional[int] = None
    
    # Content
    description: Optional[str] = None
    summary: Optional[str] = None
    
    # Commercial information
    price: float
    currency: str = "USD"
    original_price: Optional[float] = None  # For discount tracking
    
    # Quality metrics
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    rating_count: Optional[int] = None
    rating_source: Optional[str] = None  # goodreads, amazon, etc.
    
    # Availability
    availability: bool = True
    stock_quantity: Optional[int] = None
    format_type: str = "Physical"  # Physical, Ebook, Audiobook
    
    # Store information
    store_id: str
    store_name: str
    store_url: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    source_schema: str  # Track original schema type
    
    @field_validator("authors", mode="before")
    def set_authors(cls, v, values):
        if v is None and 'author' in values:
            return [values['author']]
        return v
    
    @field_validator("genres", mode="before")
    def set_genres(cls, v, values):
        if v is None and 'genre' in values:
            return [values['genre']]
        return v
    
    @field_validator("publication_year", mode="before")
    def extract_year(cls, v, values):
        if v is None and 'publication_date' in values and values['publication_date']:
            return values['publication_date'].year
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }