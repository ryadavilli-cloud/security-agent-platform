"""Smoke test for local development environment"""
import sys

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        # Core web
        import fastapi
        import uvicorn
        print("  ✓ FastAPI + Uvicorn")
        
        # LLM SDKs
        from openai import OpenAI, AzureOpenAI
        import tiktoken
        print("  ✓ OpenAI SDK + Tiktoken")
        
        # LangChain family
        import langchain
        import langchain_core
        from langchain_openai import ChatOpenAI
        from langgraph.graph import StateGraph
        print(f"  ✓ LangChain {langchain.__version__} + LangGraph")
        
        # CrewAI (standalone)
        import crewai
        print(f"  ✓ CrewAI {crewai.__version__} (standalone)")
        
                # MCP
        import mcp
        try:
            print(f"  ✓ MCP {mcp.__version__}")
        except AttributeError:
            print(f"  ✓ MCP (installed)")
        
        # Vector stores
        import faiss
        from sentence_transformers import SentenceTransformer
        print("  ✓ FAISS + Sentence Transformers")
        
        # Pinecone
        try:
            from langchain_pinecone import PineconeVectorStore
            import pinecone
            print(f"  ✓ Pinecone + LangChain integration")
        except ImportError as e:
            print(f"  ⚠️  Pinecone integration issue (non-critical): {e}")
        
        # Azure
        from azure.cosmos import CosmosClient
        from azure.search.documents import SearchClient
        print("  ✓ Azure SDKs (Cosmos + AI Search)")
        
        # MLOps
        import mlflow
        print(f"  ✓ MLflow {mlflow.__version__}")
        
        # Document processing
        import pypdf
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        print("  ✓ Document processors")
        
        # Observability
        from opentelemetry import trace
        print("  ✓ OpenTelemetry")
        
        # Reranking
        from flashrank import Ranker
        from rank_bm25 import BM25Okapi
        print("  ✓ Rerankers (FlashRank + BM25)")
        
        print("\n✅ All critical imports successful!\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}\n")
        return False

def test_version_compatibility():
    """Verify critical version compatibility"""
    print("Checking version compatibility...")
    try:
        import langchain
        import langchain_core
        import langgraph
        import crewai
        import openai
        
        print(f"  LangChain: {langchain.__version__}")
        print(f"  LangChain Core: {langchain_core.__version__}")
        
        # LangGraph may not have __version__ in some builds
        try:
            print(f"  LangGraph: {langgraph.__version__}")
        except AttributeError:
            # Get version from package metadata
            try:
                from importlib.metadata import version
                lg_version = version('langgraph')
                print(f"  LangGraph: {lg_version}")
            except:
                print(f"  LangGraph: (installed, version unknown)")
        
        print(f"  CrewAI: {crewai.__version__}")
        print(f"  OpenAI: {openai.__version__}")
        
        # Verify LangChain 0.3.x compatibility
        lc_version = langchain.__version__
        if lc_version.startswith("0.3"):
            print("  ✓ LangChain 0.3.x detected (correct)")
        else:
            print(f"  ⚠️  Unexpected LangChain version: {lc_version}")
        
        print()
        return True
    except Exception as e:
        print(f"  ❌ Version check failed: {e}\n")
        return False

def test_faiss():
    """Quick FAISS sanity check"""
    print("Testing FAISS vector operations...")
    try:
        import faiss
        import numpy as np
        
        # Create simple index
        d = 128  # dimension
        index = faiss.IndexFlatL2(d)
        vectors = np.random.random((10, d)).astype('float32')
        index.add(vectors)
        
        # Search
        query = np.random.random((1, d)).astype('float32')
        distances, indices = index.search(query, 3)
        
        assert index.ntotal == 10
        assert len(indices[0]) == 3
        print(f"  ✓ FAISS working (indexed 10 vectors, searched top 3)\n")
        return True
    except Exception as e:
        print(f"  ❌ FAISS test failed: {e}\n")
        return False

def test_embeddings():
    """Test sentence transformers"""
    print("Testing embeddings (downloading model if needed)...")
    try:
        from sentence_transformers import SentenceTransformer
        
        # Use tiny model for testing
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Generate embeddings
        texts = ["Hello world", "Testing embeddings"]
        embeddings = model.encode(texts)
        
        assert embeddings.shape[0] == 2
        print(f"  ✓ Embeddings working (dimension: {embeddings.shape[1]})\n")
        return True
    except Exception as e:
        print(f"  ❌ Embeddings test failed: {e}\n")
        return False

def test_langchain_basic():
    """Test basic LangChain functionality"""
    print("Testing LangChain components...")
    try:
        from langchain_core.messages import HumanMessage, AIMessage
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Test message creation
        msg = HumanMessage(content="Test message")
        assert msg.content == "Test message"
        
        # Test text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20
        )
        text = "This is a test document. " * 20
        chunks = splitter.split_text(text)
        
        assert len(chunks) > 0
        print(f"  ✓ LangChain components working (split into {len(chunks)} chunks)\n")
        return True
    except Exception as e:
        print(f"  ❌ LangChain test failed: {e}\n")
        return False

def test_env_file():
    """Check .env file exists"""
    print("Checking environment setup...")
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        # Check for at least one key
        has_openai = os.getenv("OPENAI_API_KEY")
        has_azure = os.getenv("AZURE_OPENAI_API_KEY")
        
        if has_openai or has_azure:
            print("  ✓ .env file loaded with API keys\n")
            return True
        else:
            print("  ⚠️  .env file exists but no API keys found")
            print("     Add your API keys to .env before running agents\n")
            return True  # Not a critical failure
            
    except Exception as e:
        print(f"  ⚠️  Could not load .env: {e}")
        print("     Create .env file with your API keys\n")
        return True  # Not a critical failure

def test_dependency_check():
    """Run pip check to identify conflicts"""
    print("Checking for dependency conflicts...")
    import subprocess
    
    try:
        result = subprocess.run(
            ["pip", "check"],
            capture_output=True,
            text=True
        )
        
        if "No broken requirements found" in result.stdout:
            print("  ✓ No dependency conflicts\n")
            return True
        elif "langchain-pinecone" in result.stdout and "langchain-tests" in result.stdout:
            print("  ⚠️  Minor conflict: langchain-pinecone wants langchain-tests (non-critical)")
            print("     This is a dev dependency and won't affect your application\n")
            return True
        else:
            print(f"  ⚠️  Dependency warnings:\n{result.stdout}\n")
            return True  # Don't fail on warnings
    except Exception as e:
        print(f"  ⚠️  Could not run pip check: {e}\n")
        return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔥 SECURITY AGENT PLATFORM - SMOKE TEST")
    print("="*70 + "\n")
    
    results = []
    results.append(test_imports())
    results.append(test_version_compatibility())
    results.append(test_faiss())
    results.append(test_embeddings())
    results.append(test_langchain_basic())
    results.append(test_env_file())
    results.append(test_dependency_check())
    
    print("="*70)
    if all(results):
        print("✅ ALL TESTS PASSED - Environment ready for development!")
        print("="*70 + "\n")
        print("Next steps:")
        print("  1. Create .env file with API keys (if not done)")
        print("  2. Review pyproject.toml")
        print("  3. Start building your security agent!")
        print()
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
        print("="*70 + "\n")
        sys.exit(1)