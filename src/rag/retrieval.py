from typing import List, Dict, Any, Optional
from src.query import QueryProcessor, QueryRetriever, ParsedQuery, QueryIntent
from src.vectorstore import BookIndexer

class RAGRetriever:
    """Enhanced retrieval for RAG pipeline"""
    
    def __init__(self, indexer: BookIndexer):
        self.query_processor = QueryProcessor()
        self.query_retriever = QueryRetriever(indexer)
        self.indexer = indexer
    
    def retrieve_context(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Retrieve context for RAG generation"""
        
        # Parse the query
        parsed_query = self.query_processor.process(query)
        
        # Retrieve based on intent
        context = {
            'query': query,
            'parsed_query': parsed_query,
            'retrieved_books': [],
            'analytics': {},
            'comparison': {},
            'metadata': {}
        }
        
        # Route to appropriate retrieval method
        if parsed_query.intent == QueryIntent.SEARCH:
            context['retrieved_books'] = self.query_retriever.retrieve_for_search(parsed_query)
        
        elif parsed_query.intent == QueryIntent.RECOMMENDATION:
            context['retrieved_books'] = self.query_retriever.retrieve_for_recommendation(parsed_query)
        
        elif parsed_query.intent == QueryIntent.COMPARISON:
            context['comparison'] = self.query_retriever.retrieve_for_comparison(parsed_query)
            # Also get sample books for context
            context['retrieved_books'] = self._extract_books_from_comparison(context['comparison'])
        
        elif parsed_query.intent == QueryIntent.ANALYTICS:
            context['analytics'] = self.query_retriever.retrieve_for_analytics(parsed_query)
            # Get sample books
            context['retrieved_books'] = self.query_retriever.retrieve_for_search(parsed_query)
        
        elif parsed_query.intent == QueryIntent.FILTER:
            context['retrieved_books'] = self.query_retriever.retrieve_for_filter(parsed_query)
        
        elif parsed_query.intent == QueryIntent.INFORMATION:
            book_info = self.query_retriever.retrieve_for_information(parsed_query)
            if book_info:
                context['retrieved_books'] = [book_info]
        
        # Limit results
        context['retrieved_books'] = context['retrieved_books'][:max_results]
        
        # Add metadata
        context['metadata'] = {
            'total_results': len(context['retrieved_books']),
            'intent': parsed_query.intent.value,
            'confidence': parsed_query.confidence,
            'filters_applied': parsed_query.filters,
            'has_comparison': bool(context['comparison']),
            'has_analytics': bool(context['analytics'])
        }
        
        return context
    
    def _extract_books_from_comparison(self, comparison: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract sample books from comparison data"""
        books = []
        for store_id, store_data in comparison.get('stores', {}).items():
            books.extend(store_data.get('sample_books', [])[:2])
        return books