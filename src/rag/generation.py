from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import json

class BaseGenerator(ABC):
    """Abstract base class for response generators"""
    
    @abstractmethod
    def generate(self, context: Dict[str, Any]) -> str:
        """Generate response from context"""
        pass


class TemplateGenerator(BaseGenerator):
    """Template-based response generator (no LLM required)"""
    
    def generate(self, context: Dict[str, Any]) -> str:
        """Generate response using templates"""
        intent = context['parsed_query'].intent
        
        if intent.value == 'search':
            return self._generate_search_response(context)
        elif intent.value == 'recommendation':
            return self._generate_recommendation_response(context)
        elif intent.value == 'comparison':
            return self._generate_comparison_response(context)
        elif intent.value == 'analytics':
            return self._generate_analytics_response(context)
        elif intent.value == 'filter':
            return self._generate_filter_response(context)
        elif intent.value == 'information':
            return self._generate_information_response(context)
        else:
            return self._generate_default_response(context)
    
    def _generate_search_response(self, context: Dict[str, Any]) -> str:
        """Generate search result response"""
        books = context['retrieved_books']
        query = context['query']
        
        if not books:
            return f"I couldn't find any books matching '{query}'. Try adjusting your search criteria."
        
        response = f"I found {len(books)} books for you:\n\n"
        
        for i, book in enumerate(books[:5], 1):
            metadata = book['metadata']
            response += f"{i}. **{metadata['title']}** by {metadata['author']}\n"
            response += f"   - Genre: {metadata['genre']}\n"
            response += f"   - Price: ${metadata['price']}\n"
            response += f"   - Store: {metadata['store_name']}\n"
            if metadata.get('rating'):
                response += f"   - Rating: {metadata['rating']}/5 ⭐\n"
            response += "\n"
        
        if len(books) > 5:
            response += f"... and {len(books) - 5} more results.\n"
        
        return response
    
    def _generate_recommendation_response(self, context: Dict[str, Any]) -> str:
        """Generate recommendation response"""
        books = context['retrieved_books']
        query = context['query']
        
        if not books:
            return "I don't have enough information to make recommendations. Please try a different query."
        
        response = f"Based on your interests, I recommend these books:\n\n"
        
        for i, book in enumerate(books[:5], 1):
            metadata = book['metadata']
            response += f"{i}. **{metadata['title']}** by {metadata['author']}\n"
            response += f"   - {metadata['genre']} • ${metadata['price']}"
            if metadata.get('rating'):
                response += f" • {metadata['rating']}/5 ⭐"
            response += f"\n   - Available at: {metadata['store_name']}\n"
            response += "\n"
        
        return response
    
    def _generate_comparison_response(self, context: Dict[str, Any]) -> str:
        """Generate comparison response"""
        comparison = context['comparison']
        
        if not comparison.get('stores'):
            return "I couldn't find enough data to compare stores."
        
        response = "📊 **Store Comparison:**\n\n"
        
        stores = comparison['stores']
        store_prices = []
        
        for store_id, data in stores.items():
            response += f"**{data['store_name']}**\n"
            response += f"  • Books available: {data['book_count']}\n"
            response += f"  • Average price: ${data['avg_price']:.2f}\n"
            response += f"  • Price range: ${data['min_price']:.2f} - ${data['max_price']:.2f}\n"
            if data.get('avg_rating'):
                response += f"  • Average rating: {data['avg_rating']:.1f}/5 ⭐\n"
            response += "\n"
            
            store_prices.append((data['store_name'], data['avg_price']))
        
        # Determine best value
        if store_prices:
            cheapest = min(store_prices, key=lambda x: x[1])
            response += f"💰 **Best Value:** {cheapest[0]} with an average price of ${cheapest[1]:.2f}\n"
        
        return response
    
    def _generate_analytics_response(self, context: Dict[str, Any]) -> str:
        """Generate analytics response"""
        analytics = context['analytics']
        
        if not analytics:
            return "I couldn't gather analytics for your query."
        
        response = "📈 **Analytics Report:**\n\n"
        
        # Price statistics
        if 'price_stats' in analytics:
            stats = analytics['price_stats']
            response += "**Price Statistics:**\n"
            response += f"  • Average: ${stats['average']:.2f}\n"
            response += f"  • Range: ${stats['min']:.2f} - ${stats['max']:.2f}\n"
            response += f"  • Median: ${stats.get('median', stats['average']):.2f}\n\n"
        
        # Genre distribution
        if 'genre_distribution' in analytics:
            response += "**Most Popular Genres:**\n"
            for i, (genre, count) in enumerate(list(analytics['genre_distribution'].items())[:5], 1):
                response += f"  {i}. {genre}: {count} books\n"
            response += "\n"
        
        # Store distribution
        if 'store_distribution' in analytics:
            response += "**Store Distribution:**\n"
            for store, count in analytics['store_distribution'].items():
                response += f"  • {store}: {count} books\n"
            response += "\n"
        
        # Rating statistics
        if 'rating_stats' in analytics and analytics['rating_stats'].get('average'):
            stats = analytics['rating_stats']
            response += "**Rating Statistics:**\n"
            response += f"  • Average rating: {stats['average']:.2f}/5 ⭐\n"
            response += f"  • Range: {stats['min']:.1f} - {stats['max']:.1f}\n\n"
        
        return response
    
    def _generate_filter_response(self, context: Dict[str, Any]) -> str:
        """Generate filtered results response"""
        books = context['retrieved_books']
        filters = context['parsed_query'].filters
        
        if not books:
            return "No books match your filter criteria. Try adjusting your filters."
        
        response = f"Found {len(books)} books matching your criteria:\n\n"
        
        # Show active filters
        if filters:
            response += "**Active Filters:**\n"
            for key, value in filters.items():
                if isinstance(value, dict):
                    for op, val in value.items():
                        if op == '$lte':
                            response += f"  • {key} ≤ {val}\n"
                        elif op == '$gte':
                            response += f"  • {key} ≥ {val}\n"
                else:
                    response += f"  • {key} = {value}\n"
            response += "\n"
        
        # Show results
        for i, book in enumerate(books[:5], 1):
            metadata = book['metadata']
            response += f"{i}. **{metadata['title']}** - ${metadata['price']}\n"
            response += f"   by {metadata['author']} • {metadata['genre']}\n"
            if metadata.get('rating'):
                response += f"   Rating: {metadata['rating']}/5 ⭐\n"
            response += "\n"
        
        if len(books) > 5:
            response += f"... and {len(books) - 5} more.\n"
        
        return response
    
    def _generate_information_response(self, context: Dict[str, Any]) -> str:
        """Generate book information response"""
        books = context['retrieved_books']
        
        if not books:
            return "I couldn't find information about that book."
        
        metadata = books[0]['metadata']
        
        response = f"📖 **{metadata['title']}**\n\n"
        response += f"**Author:** {metadata['author']}\n"
        response += f"**Genre:** {metadata['genre']}\n"
        response += f"**Price:** ${metadata['price']}\n"
        
        if metadata.get('publisher'):
            response += f"**Publisher:** {metadata['publisher']}\n"
        
        if metadata.get('publication_year'):
            response += f"**Published:** {metadata['publication_year']}\n"
        
        if metadata.get('rating'):
            response += f"**Rating:** {metadata['rating']}/5 ⭐\n"
        
        response += f"**Available at:** {metadata['store_name']}\n"
        
        if metadata.get('availability'):
            response += f"**Status:** In Stock ✅\n"
        else:
            response += f"**Status:** Out of Stock ❌\n"
        
        return response
    
    def _generate_default_response(self, context: Dict[str, Any]) -> str:
        """Generate default response"""
        return "I understood your query but I'm not sure how to help. Could you rephrase it?"


class LLMGenerator(BaseGenerator):
    """LLM-based response generator using OpenAI or other LLMs"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        try:
            import openai
            self.openai = openai
        except ImportError:
            raise ImportError("OpenAI package required. Install with: pip install openai")
        
        self.model = model
        self.api_key = api_key
        
        if self.api_key:
            self.openai.api_key = self.api_key
    
    def generate(self, context: Dict[str, Any]) -> str:
        """Generate response using LLM"""
        
        # Build prompt
        prompt = self._build_prompt(context)
        
        try:
            # Call OpenAI API
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful bookstore assistant. Provide clear, concise recommendations and information about books. Format your responses nicely with markdown."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            if response and response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            return "Sorry, I couldn't generate a response."
            
        except Exception as e:
            # Fallback to template generator
            print(f"LLM generation failed: {e}. Falling back to template.")
            template_gen = TemplateGenerator()
            return template_gen.generate(context)
    
    def _build_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt for LLM"""
        query = context['query']
        intent = context['parsed_query'].intent.value
        books = context['retrieved_books']
        
        prompt = f"User Query: {query}\n"
        prompt += f"Query Intent: {intent}\n\n"
        
        if books:
            prompt += "Retrieved Books:\n"
            for i, book in enumerate(books[:10], 1):
                metadata = book['metadata']
                prompt += f"{i}. {metadata['title']} by {metadata['author']}\n"
                prompt += f"   Genre: {metadata['genre']}, Price: ${metadata['price']}"
                if metadata.get('rating'):
                    prompt += f", Rating: {metadata['rating']}/5"
                prompt += f", Store: {metadata['store_name']}\n"
            prompt += "\n"
        
        if context.get('comparison'):
            prompt += "Store Comparison Data:\n"
            prompt += json.dumps(context['comparison'], indent=2)
            prompt += "\n\n"
        
        if context.get('analytics'):
            prompt += "Analytics Data:\n"
            prompt += json.dumps(context['analytics'], indent=2)
            prompt += "\n\n"
        
        prompt += "Please provide a helpful response to the user's query based on this information. "
        prompt += "Be concise, friendly, and format your response with markdown for readability."
        
        return prompt

