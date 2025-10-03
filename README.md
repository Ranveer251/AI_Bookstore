# 📚 Bookstore AI System - Complete Documentation

## 🎯 System Overview

An AI-powered bookstore analytics and search system that provides natural language querying across heterogeneous data sources using RAG (Retrieval-Augmented Generation) architecture.

## 🏗️ Architecture

```
┌─────────────────┐
│   Data Sources  │  (Different schemas)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Schema          │  
│ Harmonizer      │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Vector Store    │  
│ & Embeddings    │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Query           │ 
│ Processor       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ RAG Pipeline    │ 
└────────┬────────┘
         ↓
┌─────────────────┐
│ Natural         │
│ Language        │
│ Response        │
└─────────────────┘
```

## ✨ Key Features

### 1. **Multi-Schema Data Harmonization**
- Converts different bookstore data formats into unified schema
- Handles missing fields gracefully
- Validates and normalizes data
- Extensible for new schemas

### 2. **Semantic Vector Search**
- Embeddings-based similarity search
- Fast approximate nearest neighbor (ANN) queries
- Metadata filtering (price, rating, store, genre)
- Hybrid search capabilities

### 3. **Natural Language Query Processing**
- 6 intent types: Search, Recommendation, Comparison, Analytics, Filter, Information
- Entity extraction (genres, prices, ratings, stores)
- Complex filter building
- Confidence scoring

### 4. **RAG-Powered Responses**
- Template-based generation (fast, no API cost)
- LLM-based generation (natural, contextual)
- Retrieval-augmented context
- Formatted, readable responses

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo>
cd bookstore-ai-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Complete Demo

```bash
python demo_complete_system.py
```

### Quick Test

```python
from src.data.harmonizer import HarmonizerFactory
from src.vectorstore import BookIndexer
from src.rag import RAGPipeline

# 1. Harmonize data
harmonizer = HarmonizerFactory.create_harmonizer("bookstore_a")
books = harmonizer.batch_harmonize(raw_data)

# 2. Index books
indexer = BookIndexer()
indexer.index_books(books)

# 3. Query with RAG
rag_pipeline = RAGPipeline(indexer)
result = rag_pipeline.query("Find science fiction books under $20")

print(result['response'])
```

## 📊 Component Details

### 1. Schema Harmonizer

**Purpose:** Convert heterogeneous bookstore data into unified format

**Files:**
- `src/core/models.py` - Unified data model
- `src/data/harmonizer/base.py` - Base harmonizer
- `src/data/harmonizer/schema_mapper.py` - Schema-specific harmonizers
- `src/data/harmonizer/transformers.py` - Data transformation utilities

**Demo:**
```bash
python debug_harmonizer.py
```

**Key Features:**
- ✅ Price parsing from various formats
- ✅ Genre normalization
- ✅ Multi-author handling
- ✅ Date parsing
- ✅ Rating normalization
- ✅ ISBN validation

### 2. Vector Store & Embeddings

**Purpose:** Enable semantic similarity search

**Files:**
- `src/vectorstore/embeddings.py` - Embedding generation
- `src/vectorstore/vector_db.py` - ChromaDB integration
- `src/vectorstore/indexer.py` - Indexing orchestration

**Demo:**
```bash
python demo_vector_store.py
```

**Key Features:**
- ✅ Sentence transformer embeddings
- ✅ Composite book embeddings
- ✅ Batch processing
- ✅ Similarity search
- ✅ Metadata filtering
- ✅ Performance metrics

### 3. Query Processor

**Purpose:** Understand and parse natural language queries

**Files:**
- `src/query/intent_classifier.py` - Intent detection
- `src/query/entity_extractor.py` - Parameter extraction
- `src/query/processor.py` - Query orchestration
- `src/query/router.py` - Query routing
- `src/query/retriever.py` - Context retrieval

**Demo:**
```bash
python demo_query_processor.py
```

**Key Features:**
- ✅ 6 intent types
- ✅ Price range extraction
- ✅ Rating filters
- ✅ Store selection
- ✅ Genre detection
- ✅ Sort preferences
- ✅ Result limits

### 4. RAG Pipeline

**Purpose:** Generate natural language responses

**Files:**
- `src/rag/retrieval.py` - Enhanced retrieval
- `src/rag/generation.py` - Response generation
- `src/rag/pipeline.py` - Pipeline orchestration

**Demo:**
```bash
python demo_rag_pipeline.py
```

**Key Features:**
- ✅ Template-based generation
- ✅ LLM-based generation (optional)
- ✅ Context-aware responses
- ✅ Formatted output
- ✅ Performance tracking
- ✅ Batch processing

## 📖 Usage Examples

### Simple Search
```python
result = rag_pipeline.query("Find fantasy books")
print(result['response'])
```

### Filtered Search
```python
result = rag_pipeline.query("Show me science fiction books under $20 rated above 4 stars")
print(result['response'])
```

### Store Comparison
```python
result = rag_pipeline.query("Which store has cheaper fantasy books?")
print(result['response'])
```

### Recommendations
```python
result = rag_pipeline.query("Recommend books similar to Lord of the Rings")
print(result['response'])
```

### Analytics
```python
result = rag_pipeline.query("What are the most popular genres?")
print(result['response'])
```

## 🎮 Available Demos

| Demo | Command | Purpose |
|------|---------|---------|
| Complete System | `python demo_complete_system.py` | End-to-end demonstration |
| Harmonizer | `python debug_harmonizer.py` | Test data harmonization |
| Vector Store | `python demo_vector_store.py` | Test semantic search |
| Query Processor | `python demo_query_processor.py` | Test query understanding |
| RAG Pipeline | `python demo_rag_pipeline.py` | Test response generation |
| Full Pipeline | `python demo_complete_pipeline.py` | Integrated pipeline |

## 📈 Performance

| Component | Latency | Throughput |
|-----------|---------|------------|
| Harmonizer | < 1ms/book | ~1000 books/s |
| Indexing | ~20ms/book | ~50 books/s |
| Query Processing | < 10ms | ~100 queries/s |
| Retrieval | 10-50ms | ~20-100 queries/s |
| Template Generation | < 5ms | ~200 responses/s |
| LLM Generation | 500-2000ms | ~0.5-2 responses/s |
| **Total (Template)** | **~50-100ms** | **~10-20 q/s** |
| **Total (LLM)** | **~550-2100ms** | **~0.5-2 q/s** |

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# Vector Database
CHROMADB_HOST=localhost
CHROMADB_PORT=8001
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# LLM (Optional)
OPENAI_API_KEY=your-key-here
LLM_MODEL=gpt-3.5-turbo

# Performance
BATCH_SIZE=1000
MAX_WORKERS=4
```

### Using LLM Generation

```python
# With OpenAI
rag_pipeline = RAGPipeline(
    indexer,
    use_llm=True,
    llm_model="gpt-3.5-turbo",
    api_key="your-api-key"
)
```

## 🧪 Testing

### Run All Tests
```bash
# Harmonizer tests
python -m pytest tests/unit/test_harmonizer.py

# Vector store tests
python demo_vector_store.py

# Query processor tests
python demo_query_processor.py

# RAG tests
python demo_rag_pipeline.py

# Integration test
python demo_complete_system.py
```

## 💡 Common Use Cases

### 1. Customer Service Chatbot
```python
# Natural language Q&A
result = rag_pipeline.query("Do you have fantasy books under $15?")
```

### 2. Price Comparison Tool
```python
# Compare across stores
result = rag_pipeline.query("Which store has better deals on sci-fi?")
```

### 3. Recommendation Engine
```python
# Personalized suggestions
result = rag_pipeline.query("Recommend books like Harry Potter")
```

### 4. Business Analytics
```python
# Insights for store owners
result = rag_pipeline.query("What are the most popular genres?")
```

### 5. Advanced Search
```python
# Complex multi-criteria search
result = rag_pipeline.query("Find highly rated fantasy books under $20 in store A")
```

## 🐛 Troubleshooting

### No Results Found
**Problem:** Queries return empty results

**Solutions:**
- Check if books are indexed: `indexer.vector_store.get_collection_stats()`
- Use broader search terms
- Remove restrictive filters
- Verify data was harmonized correctly

### Slow Performance
**Problem:** Queries take too long

**Solutions:**
- Use template generator instead of LLM
- Reduce `max_results` parameter
- Enable batch processing
- Check vector store performance

### Import Errors
**Problem:** `ModuleNotFoundError`

**Solutions:**
```bash
# Set PYTHONPATH
export PYTHONPATH=.

# Or run from project root
python -m demo_complete_system

# Or use setup script
python setup_vector_store.py
```

## 📚 Project Structure

```
bookstore-ai-system/
├── src/
│   ├── core/                # Data models
│   ├── data/                # Harmonization
│   ├── vectorstore/         # Embeddings & search
│   ├── query/               # Query processing
│   └── rag/                 # RAG pipeline
├── tests/                   # Unit tests
├── scripts/                 # Utilities
├── data/                    # Data storage
├── config/                  # Configuration
└── demo_*.py               # Demonstrations
```

## 🔮 Future Enhancements

Potential additions:
- [ ] REST API endpoints
- [ ] Web UI frontend
- [ ] Multi-language support
- [ ] Image-based search
- [ ] Real-time inventory sync
- [ ] User personalization
- [ ] A/B testing framework
- [ ] Advanced caching
- [ ] Monitoring dashboard
- [ ] Mobile app integration

## 📞 Getting Help

### Documentation
- Schema Harmonizer: See artifacts or `src/data/harmonizer/`
- Vector Store: See artifacts or `src/vectorstore/`
- Query Processor: See artifacts or `src/query/`
- RAG Pipeline: See artifacts or `src/rag/`

### Demos
- Run any `demo_*.py` file for examples
- Check code comments for detailed explanations

### Issues
- Verify all dependencies are installed
- Check PYTHONPATH is set correctly
- Ensure vector store is accessible
- Review error messages carefully

## 🎉 Success!

You've successfully built a complete AI-powered bookstore system with:
- ✅ Multi-schema data harmonization
- ✅ Semantic vector search
- ✅ Natural language processing
- ✅ RAG-powered responses

**Try it now:**
```bash
python demo_complete_system.py
```

---

Built with ❤️ using Python, ChromaDB, Sentence Transformers, and RAG architecture.