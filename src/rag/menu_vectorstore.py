"""Menu Vector Store - Provides access to ChromaDB for menu searches"""

import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config.settings import PERSIST_DIR

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL,
)

# Initialize vector store (connects to existing database)
menu_vectorstore = Chroma(
    collection_name="restaurant_menus",
    embedding_function=embeddings,
    persist_directory=str(PERSIST_DIR)
)

def search_menus(query: str, k: int = 5, dietary_filter: str = None):
    """Semantic search for restaurant menus.
    Args: 
        query: Searh  query (e.g., vegan pasta)
        k: Number of results to return
        dietary_filter: Optional dietary requirement to filter by
    
    Returns:
        List of documents with metadata
    """

    # Perform similarity search
    results = menu_vectorstore.similarity_search(query, k=k)

    # Apply dietary filter if specified
    if dietary_filter:
        results = [
            r for r in results
            if dietary_filter.lower() in [d.strip().lower() for d in r.metadata.get("dietary", "").split(",")]
        ]

    return results

def get_restaurant_dishes(restaurant_name: str, dietary_filter: str = None):
    """Get all dishes from the specific restaurant.
    Args: 
        restaurant_name: Name of the restaurant
        dietary_filter: Optional dietary requirement
    Returns: 
        List of dishes
    """

    # Use metadata filtering
    results = menu_vectorstore.similarity_search(
        query="all dishes",
        k=100,
        filter={"restaurant_name": restaurant_name}
    )

    # Apply dietary filter if specified
    if dietary_filter:
        results = [
            r for r in results
            if dietary_filter.lower() in [d.strip().lower() for d in r.metadata.get("dietary", "").split(",")]
        ]
    return results