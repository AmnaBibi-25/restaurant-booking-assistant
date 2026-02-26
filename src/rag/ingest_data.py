"""Data Ingestion - Loads restaurant menu data into ChromaDB vector store.
Run this once to populate the database before using the system.
"""

from pathlib import Path
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
from src.config.settings import MENUS_DIR, PERSIST_DIR

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

def load_menu_data():
    """Loads all menu JSON files from data/menus directory.

    Returns:
        List of menu dictionaries
    """
    menus = []

    for menus_file in MENUS_DIR.glob("*.json"):
        with open(menus_file, 'r') as f:
            menu_data = json.load(f)
            menus.append(menu_data)

    return menus

def create_menu_documents(menus):
    """Converts menu data into text documents for embedding.
    Each dish becomes a separate document for granular search.

    Args: 
        menus: List of menu dictionaries

    Returns:
        Tuple of (texts, metadatas) for ChromaDB
    """

    texts = []
    metadatas = []

    for menu in menus:
        restaurant_name = menu["restaurant_name"]
        location = menu["location"]
        cuisine = menu["cuisine"]
        price_range = menu["price_range"]

        # Process each category (appetizers, mains, desserts)
        for category, items in menu["menu"].items():
            for item in items:
                # Create rich text description for embedding
                text = f"""
Restaurant: {restaurant_name}
Location: {location}
Cuisine: {cuisine}
Category: {category}
Dish: {item['name']}
Price: ${item['price']}
Description: {item['description']}
Dietary: {', '.join(item['dietary']) if item['dietary'] else 'None'}
Allergens: {', '.join(item['allergens']) if item['allergens'] else 'None'}
"""

                # Create metadata for filtering
                metadata = {
                    "restaurant_name": restaurant_name,
                    "location": location,
                    "cuisine": cuisine,
                    "category": category,
                    "price_range": price_range,
                    "dish_name": item['name'],
                    "price": item['price'],
                   "dietary": ",".join(item['dietary']) if item['dietary'] else "none",
                    "allergens": ",".join(item['allergens']) if item['allergens'] else "none"
                }

                texts.append(text.strip())
                metadatas.append(metadata)

    return texts, metadatas


def ingest_menus():
    """Main ingestion function. Loads menus and creates ChromaDB vector store.
    """
    
    # Load menu data
    print("Loading menu data...")
    menus = load_menu_data()
    print(f"Loaded {len(menus)} restaurant menus")

    # Convert to documents
    print("Creating documents for embedding...")
    texts, metadatas = create_menu_documents(menus)
    print(f"Created {len(texts)} dish documents")

    # Initialize embeddings (using free HuggingFace model)
    print("Initializing embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
    )
    print("Embeddings model loaded")

    # Create/update ChromaDB 
    print("Creating ChromaDB vector store...")
    vectorstore = Chroma.from_texts(
        texts=texts, 
        metadatas=metadatas,
        embedding=embeddings,
        collection_name="restaurant_menus",
        persist_directory=str(PERSIST_DIR)
    )
    print(f"ChromaDB vector store created at {PERSIST_DIR}")

    # Test search
    print("Testing semantic search...")
    test_query = "vegan pasta dishes"
    results = vectorstore.similarity_search(test_query, k=3)
    print(f"Test Query: '{test_query}'")
    print(f"Top {len(results)} results: ")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.metadata['restaurant_name']} - {doc.metadata['dish_name']}")
        print(f"  Price: ${doc.metadata['price']}")
        print(f"  Dietary: {doc.metadata['dietary']}")

    print("\nIngestion complete!")
    print("\nYou can now run the main application with RAG enabled.\n")



if __name__ == "__main__":
    ingest_menus()


    




 


        


