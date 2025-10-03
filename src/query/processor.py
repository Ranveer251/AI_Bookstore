from typing import Dict, Any, List, Optional
from src.query.intent_classifier import IntentClassifier, QueryIntent, ParsedQuery
from src.query.entity_extractor import EntityExtractor
import re

class QueryProcessor:
    """Main query processing orchestrator"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
    
    def process(self, query: str) -> ParsedQuery:
        """Process a natural language query"""
        # Classify intent
        intent, confidence = self.intent_classifier.classify(query)
        
        # Extract entities
        entities = self.entity_extractor.extract(query)
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        # Build filters based on entities
        filters = self._build_filters(entities)
        
        # Extract metadata
        metadata = self._extract_metadata(query, intent, entities)
        
        return ParsedQuery(
            original_query=query,
            intent=intent,
            confidence=confidence,
            entities=entities,
            keywords=keywords,
            filters=filters,
            metadata=metadata
        )
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract relevant keywords from query"""
        # Remove common stop words
        stop_words = {
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'about', 'as', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'should', 'could', 'may', 'might', 'can', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'find', 'search', 'looking', 'show', 'get', 'want', 'need'
        }
        
        # Tokenize and clean
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def _build_filters(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Build filter dictionary from extracted entities"""
        filters = {}
        
        # Price filters
        if entities.get('price_range'):
            price_range = entities['price_range']
            if 'min' in price_range:
                filters.setdefault('price', {})['$gte'] = price_range['min']
            if 'max' in price_range:
                filters.setdefault('price', {})['$lte'] = price_range['max']
        
        # Rating filters
        if entities.get('rating_range'):
            rating_range = entities['rating_range']
            if 'min' in rating_range:
                filters.setdefault('rating', {})['$gte'] = rating_range['min']
            if 'max' in rating_range:
                filters.setdefault('rating', {})['$lte'] = rating_range['max']
        
        # Store filters
        if entities.get('stores'):
            if len(entities['stores']) == 1:
                filters['store_id'] = entities['stores'][0]
            else:
                filters['store_id'] = {'$in': entities['stores']}
        
        # Format filters
        if entities.get('format'):
            filters['format_type'] = entities['format']
        
        # Availability filters
        if entities.get('availability') is not None:
            filters['availability'] = entities['availability']
        
        # Genre filters
        if entities.get('genres'):
            if len(entities['genres']) == 1:
                filters['genre'] = entities['genres'][0]
            else:
                filters['genre'] = {'$in': entities['genres']}
        
        return filters
    
    def _extract_metadata(self, query: str, intent: QueryIntent, 
                         entities: Dict[str, Any]) -> Dict[str, Any]:
        """Extract additional metadata about the query"""
        metadata = {
            'query_length': len(query),
            'word_count': len(query.split()),
            'has_price_constraint': entities.get('price_range') is not None,
            'has_rating_constraint': entities.get('rating_range') is not None,
            'has_store_preference': len(entities.get('stores', [])) > 0,
            'genre_count': len(entities.get('genres', [])),
            'sort_preference': entities.get('sort_by'),
            'result_limit': entities.get('limit'),
            'requires_comparison': intent == QueryIntent.COMPARISON,
            'requires_aggregation': intent == QueryIntent.ANALYTICS
        }
        
        return metadata
