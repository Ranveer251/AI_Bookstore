import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing vector store requirements...")
    
    packages = [
        "chromadb==0.4.18",
        "sentence-transformers==2.2.2", 
        "numpy==1.25.2",
        "scipy==1.11.4"
    ]
    
    for package in packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}: {e}")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    dirs = [
        "data/embeddings",
        "data/vector_db", 
        "chroma_db",
        "logs"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✅ Created {dir_path}")

def test_installation():
    """Test if everything is working"""
    print("🧪 Testing installation...")
    
    try:
        # Test sentence transformers
        from sentence_transformers import SentenceTransformer
        print("   ✅ Sentence Transformers working")
        
        # Test chromadb
        import chromadb
        print("   ✅ ChromaDB working")
        
        # Test our components
        from src.vectorstore import SentenceTransformerEmbeddings, BookEmbeddingGenerator
        print("   ✅ Custom components working")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Vector Store Setup")
    print("=" * 50)
    
    # Install requirements
    install_requirements()
    
    # Create directories  
    create_directories()
    
    # Test installation
    success = test_installation()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run: python demo_vector_store.py")
        print("2. Or integrate into your existing code")
    else:
        print("\n❌ Setup failed. Please check error messages above.")

if __name__ == "__main__":
    main()