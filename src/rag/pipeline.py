from typing import Dict, Any, Optional
from src.rag.retrieval import RAGRetriever
from src.rag.generation import BaseGenerator, TemplateGenerator, LLMGenerator
from src.vectorstore import BookIndexer
import time

class RAGPipeline:
    """Complete RAG pipeline orchestrator"""
    
    def __init__(self, 
                 indexer: BookIndexer,
                 generator: Optional[BaseGenerator] = None,
                 use_llm: bool = False,
                 llm_model: str = "gpt-3.5-turbo",
                 api_key: Optional[str] = None):
        
        self.retriever = RAGRetriever(indexer)
        
        # Initialize generator
        if generator:
            self.generator = generator
        elif use_llm:
            try:
                self.generator = LLMGenerator(model=llm_model, api_key=api_key)
                print("✅ Using LLM-based generation")
            except Exception as e:
                print(f"⚠️  LLM initialization failed: {e}. Using template generator.")
                self.generator = TemplateGenerator()
        else:
            self.generator = TemplateGenerator()
            print("✅ Using template-based generation")
    
    def query(self, user_query: str, max_results: int = 10, include_metadata: bool = False) -> Dict[str, Any]:
        """Process a query through the complete RAG pipeline"""
        
        start_time = time.time()
        
        try:
            # Step 1: Retrieve context
            retrieval_start = time.time()
            context = self.retriever.retrieve_context(user_query, max_results)
            retrieval_time = time.time() - retrieval_start
            
            # Step 2: Generate response
            generation_start = time.time()
            response = self.generator.generate(context)
            generation_time = time.time() - generation_start
            
            # Build result
            result = {
                'success': True,
                'query': user_query,
                'response': response,
                'intent': context['parsed_query'].intent.value,
                'confidence': context['parsed_query'].confidence,
                'total_results': context['metadata']['total_results']
            }
            
            # Add metadata if requested
            if include_metadata:
                result['metadata'] = {
                    'retrieval_time_ms': retrieval_time * 1000,
                    'generation_time_ms': generation_time * 1000,
                    'total_time_ms': (time.time() - start_time) * 1000,
                    'retrieved_books_count': len(context['retrieved_books']),
                    'filters_applied': context['parsed_query'].filters,
                    'has_comparison': context['metadata']['has_comparison'],
                    'has_analytics': context['metadata']['has_analytics']
                }
                result['context'] = context
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'query': user_query,
                'error': str(e),
                'response': f"I encountered an error processing your query: {str(e)}"
            }
    
    def batch_query(self, queries: list, max_results: int = 10) -> list:
        """Process multiple queries"""
        results = []
        
        for query in queries:
            result = self.query(query, max_results, include_metadata=False)
            results.append(result)
        
        return results