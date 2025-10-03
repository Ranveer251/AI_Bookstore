from typing import Dict, Any, List, Optional
from src.query.processor import ParsedQuery
from src.query.intent_classifier import QueryIntent
from src.vectorstore import BookIndexer

class QueryRetriever:
    """Retrieves relevant information based on parsed queries"""
    
    def __init__(self, indexer: BookIndexer):
        self.indexer = indexer
    
    def retrieve_for_search(self, parsed_query: ParsedQuery) -> List[Dict[str, Any]]:
        """Retrieve books for search queries"""
        # Build search query from keywords and entities
        search_text = self._build_search_text(parsed_query)
        
        # Determine result limit
        limit = parsed_query.entities.get('limit') or parsed_query.metadata.get('result_limit') or 10
        
        # Execute search
        results = self.indexer.search_books(
            query=search_text,
            n_results=limit,
            filters=parsed_query.filters
        )
        
        # Apply sorting if specified
        if parsed_query.entities.get('sort_by'):
            results = self._apply_sorting(results, parsed_query.entities['sort_by'])
        
        return results
    
    def retrieve_for_recommendation(self, parsed_query: ParsedQuery) -> List[Dict[str, Any]]:
        """Retrieve book recommendations"""
        # Build recommendation query focusing on genres and themes
        search_text = self._build_recommendation_text(parsed_query)
        
        limit = parsed_query.entities.get('limit') or 10
        
        # Get more results for recommendations, then filter
        results = self.indexer.search_books(
            query=search_text,
            n_results=limit * 2,
            filters=parsed_query.filters
        )
        
        # Diversify recommendations by author/genre
        diversified = self._diversify_results(results, limit)
        
        return diversified
    
    def retrieve_for_comparison(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Retrieve data for comparison queries"""
        # Get books matching the query
        search_text = self._build_search_text(parsed_query)
        
        all_books = self.indexer.search_books(
            query=search_text,
            n_results=50,  # Get more for comparison
            filters={}  # Don't filter by store for comparisons
        )
        
        # Group by stores
        store_data = {}
        for book in all_books:
            store_id = book['metadata']['store_id']
            if store_id not in store_data:
                store_data[store_id] = []
            store_data[store_id].append(book)
        
        # Calculate comparison metrics
        comparison = {
            'stores': {},
            'overall': {
                'total_books': len(all_books),
                'stores_compared': len(store_data)
            }
        }
        
        for store_id, books in store_data.items():
            if books:
                prices = [b['metadata']['price'] for b in books]
                ratings = [b['metadata'].get('rating', 0) for b in books if b['metadata'].get('rating')]
                
                comparison['stores'][store_id] = {
                    'store_name': books[0]['metadata']['store_name'],
                    'book_count': len(books),
                    'avg_price': sum(prices) / len(prices),
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'avg_rating': sum(ratings) / len(ratings) if ratings else None,
                    'sample_books': books[:3]
                }
        
        return comparison
    
    def retrieve_for_analytics(self, parsed_query: ParsedQuery) -> Dict[str, Any]:
        """Retrieve data for analytics queries"""
        # Get a larger sample for analytics
        search_text = self._build_search_text(parsed_query)
        
        books = self.indexer.search_books(
            query=search_text,
            n_results=100,
            filters=parsed_query.filters
        )
        
        if not books:
            return {'error': 'No books found for analytics'}
        
        # Calculate various statistics
        analytics = {
            'total_books': len(books),
            'price_stats': self._calculate_price_stats(books),
            'rating_stats': self._calculate_rating_stats(books),
            'genre_distribution': self._calculate_genre_distribution(books),
            'store_distribution': self._calculate_store_distribution(books),
            'format_distribution': self._calculate_format_distribution(books)
        }
        
        return analytics
    
    def retrieve_for_filter(self, parsed_query: ParsedQuery) -> List[Dict[str, Any]]:
        """Retrieve books with specific filters"""
        # For filter queries, use minimal search text
        search_text = ' '.join(parsed_query.keywords) if parsed_query.keywords else 'books'
        
        limit = parsed_query.entities.get('limit') or 20
        
        results = self.indexer.search_books(
            query=search_text,
            n_results=limit,
            filters=parsed_query.filters
        )
        
        return results
    
    def retrieve_for_information(self, parsed_query: ParsedQuery) -> Optional[Dict[str, Any]]:
        """Retrieve information about a specific book"""
        search_text = self._build_search_text(parsed_query)
        
        results = self.indexer.search_books(
            query=search_text,
            n_results=1,
            filters=parsed_query.filters
        )
        
        return results[0] if results else None
    
    # Helper methods
    
    def _build_search_text(self, parsed_query: ParsedQuery) -> str:
        """Build search text from parsed query"""
        components = []
        
        # Add keywords
        if parsed_query.keywords:
            components.extend(parsed_query.keywords)
        
        # Add genres
        if parsed_query.entities.get('genres'):
            components.extend(parsed_query.entities['genres'])
        
        # If no components, use original query
        if not components:
            # Remove query intent keywords
            text = parsed_query.original_query.lower()
            for word in ['find', 'search', 'looking for', 'show me', 'get', 'want', 'need']:
                text = text.replace(word, '')
            return text.strip()
        
        return ' '.join(components)
    
    def _build_recommendation_text(self, parsed_query: ParsedQuery) -> str:
        """Build text optimized for recommendations"""
        components = []
        
        # Prioritize genres for recommendations
        if parsed_query.entities.get('genres'):
            components.extend(parsed_query.entities['genres'])
        
        # Add thematic keywords
        thematic_keywords = [kw for kw in parsed_query.keywords 
                           if kw not in ['book', 'books', 'recommend', 'suggest', 'similar']]
        components.extend(thematic_keywords)
        
        return ' '.join(components) if components else 'popular books'
    
    def _apply_sorting(self, results: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
        """Apply sorting to results"""
        if sort_by == 'price_asc':
            return sorted(results, key=lambda x: x['metadata']['price'])
        elif sort_by == 'price_desc':
            return sorted(results, key=lambda x: x['metadata']['price'], reverse=True)
        elif sort_by == 'rating_desc':
            return sorted(results, key=lambda x: x['metadata'].get('rating', 0), reverse=True)
        elif sort_by == 'year_desc':
            return sorted(results, key=lambda x: x['metadata'].get('publication_year', 0), reverse=True)
        elif sort_by == 'year_asc':
            return sorted(results, key=lambda x: x['metadata'].get('publication_year', 9999))
        
        return results
    
    def _diversify_results(self, results: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Diversify results by author and genre"""
        diversified = []
        seen_authors = set()
        seen_genres = set()
        
        # First pass: unique authors and genres
        for result in results:
            author = result['metadata']['author']
            genre = result['metadata']['genre']
            
            if author not in seen_authors or genre not in seen_genres:
                diversified.append(result)
                seen_authors.add(author)
                seen_genres.add(genre)
                
                if len(diversified) >= limit:
                    break
        
        # Second pass: fill remaining slots
        if len(diversified) < limit:
            for result in results:
                if result not in diversified:
                    diversified.append(result)
                    if len(diversified) >= limit:
                        break
        
        return diversified[:limit]
    
    def _calculate_price_stats(self, books: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate price statistics"""
        prices = [b['metadata']['price'] for b in books]
        
        return {
            'average': sum(prices) / len(prices),
            'min': min(prices),
            'max': max(prices),
            'median': sorted(prices)[len(prices) // 2]
        }
    
    def _calculate_rating_stats(self, books: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate rating statistics"""
        ratings = [b['metadata'].get('rating') for b in books if b['metadata'].get('rating')]
        
        if not ratings:
            return {'average': None, 'min': None, 'max': None}
        
        return {
            'average': sum(ratings) / len(ratings),
            'min': min(ratings),
            'max': max(ratings),
            'count': len(ratings)
        }
    
    def _calculate_genre_distribution(self, books: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate genre distribution"""
        from collections import Counter
        
        genres = [b['metadata']['genre'] for b in books]
        return dict(Counter(genres).most_common())
    
    def _calculate_store_distribution(self, books: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate store distribution"""
        from collections import Counter
        
        stores = [b['metadata']['store_name'] for b in books]
        return dict(Counter(stores))
    
    def _calculate_format_distribution(self, books: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate format distribution"""
        from collections import Counter
        
        formats = [b['metadata'].get('format_type', 'Physical') for b in books]
        return dict(Counter(formats))