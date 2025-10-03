from typing import Dict, Any, List, Optional, Callable
from src.query.processor import QueryProcessor, ParsedQuery
from src.query.intent_classifier import QueryIntent

class QueryRouter:
    """Routes queries to appropriate handlers based on intent"""
    
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.handlers = {}
    
    def register_handler(self, intent: QueryIntent, handler: Callable):
        """Register a handler for a specific intent"""
        self.handlers[intent] = handler
    
    def route(self, query: str) -> Dict[str, Any]:
        """Process and route a query to the appropriate handler"""
        # Parse the query
        parsed_query = self.query_processor.process(query)
        
        # Get the appropriate handler
        handler = self.handlers.get(parsed_query.intent)
        
        if handler is None:
            return {
                'success': False,
                'error': f'No handler registered for intent: {parsed_query.intent}',
                'parsed_query': parsed_query
            }
        
        # Execute handler
        try:
            result = handler(parsed_query)
            return {
                'success': True,
                'parsed_query': parsed_query,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'parsed_query': parsed_query
            }