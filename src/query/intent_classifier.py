from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
import re
from dataclasses import dataclass

class QueryIntent(str, Enum):
    """Types of query intents"""
    SEARCH = "search"  # Find specific books
    RECOMMENDATION = "recommendation"  # Get book recommendations
    COMPARISON = "comparison"  # Compare prices, stores, books
    ANALYTICS = "analytics"  # Statistical queries, aggregations
    FILTER = "filter"  # Filter by specific criteria
    INFORMATION = "information"  # Get info about a specific book
    UNKNOWN = "unknown"  # Unable to determine intent

@dataclass
class ParsedQuery:
    """Structured representation of a parsed query"""
    original_query: str
    intent: QueryIntent
    confidence: float
    entities: Dict[str, Any]
    keywords: List[str]
    filters: Dict[str, Any]
    metadata: Dict[str, Any]

class IntentClassifier:
    """Classify user query intent"""
    
    def __init__(self):
        # Intent patterns with keywords and phrases
        self.intent_patterns = {
            QueryIntent.SEARCH: {
                'keywords': ['find', 'search', 'looking for', 'show me', 'get', 'want', 'need'],
                'patterns': [
                    r'(find|search|looking for|show me|get me)\s+(books?|novels?)',
                    r'(want|need)\s+(a|an|some)\s+(book|novel)',
                    r'books?\s+(about|on|related to)',
                ]
            },
            QueryIntent.RECOMMENDATION: {
                'keywords': ['recommend', 'suggest', 'similar', 'like', 'based on'],
                'patterns': [
                    r'(recommend|suggest)\s+(books?|something)',
                    r'(similar|like)\s+',
                    r'based on',
                    r'what should I read',
                    r'good books?\s+(for|about)',
                ]
            },
            QueryIntent.COMPARISON: {
                'keywords': ['compare', 'cheaper', 'better', 'versus', 'vs', 'difference', 'which'],
                'patterns': [
                    r'(compare|comparison)\s+',
                    r'(cheaper|better|best)\s+(store|price)',
                    r'(which|what)\s+(store|bookstore)\s+(is|has)',
                    r'(versus|vs\.?)\s+',
                    r'difference between',
                ]
            },
            QueryIntent.ANALYTICS: {
                'keywords': ['most popular', 'average', 'statistics', 'how many', 'total', 'count'],
                'patterns': [
                    r'(most|least)\s+(popular|expensive|rated)',
                    r'(average|mean)\s+(price|rating)',
                    r'(how many|total|count)',
                    r'statistics\s+(about|on|for)',
                    r'(top|best)\s+\d+',
                ]
            },
            QueryIntent.FILTER: {
                'keywords': ['under', 'over', 'between', 'more than', 'less than', 'only'],
                'patterns': [
                    r'(under|below|less than)\s+\$?\d+',
                    r'(over|above|more than)\s+\$?\d+',
                    r'between\s+\$?\d+\s+and\s+\$?\d+',
                    r'(only|just)\s+(available|in stock)',
                    r'rated\s+(above|below|over)\s+\d',
                ]
            },
            QueryIntent.INFORMATION: {
                'keywords': ['tell me about', 'information', 'details', 'describe', 'what is'],
                'patterns': [
                    r'tell me about',
                    r'(information|details)\s+(about|on)',
                    r'(describe|explain)',
                    r'what is\s+',
                ]
            }
        }
    
    def classify(self, query: str) -> Tuple[QueryIntent, float]:
        """Classify query intent with confidence score"""
        query_lower = query.lower().strip()
        intent_scores = {intent: 0.0 for intent in QueryIntent}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            
            # Check keywords
            keyword_matches = sum(1 for kw in patterns['keywords'] if kw in query_lower)
            score += keyword_matches * 0.3
            
            # Check regex patterns
            pattern_matches = sum(1 for pattern in patterns['patterns'] 
                                if re.search(pattern, query_lower))
            score += pattern_matches * 0.5
            
            intent_scores[intent] = min(score, 1.0)
        
        # Get intent with highest score
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        if best_intent[1] < 0.3:
            return QueryIntent.UNKNOWN, best_intent[1]
        
        return best_intent[0], best_intent[1]