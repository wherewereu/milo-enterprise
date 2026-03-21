#!/usr/bin/env python3
"""
Qdrant Query Skill
Query the vector knowledge base on Titan.
Requires text embeddings - use Ollama or an embedding API to generate vectors.
"""

import os
import sys
import json
import argparse
import requests

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "192.168.0.247")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "hydra-rag")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "192.168.0.247")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")

BASE_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

HEADERS = {"Content-Type": "application/json"}
if QDRANT_API_KEY:
    HEADERS["Authorization"] = f"Bearer {QDRANT_API_KEY}"


def get_embedding(text: str) -> list:
    """Get embedding vector from Ollama.
    
    Requires Ollama with an embedding model (nomic-embed-text or mxbai-embed-large).
    Make sure Ollama is running and accessible:
    
        systemctl start ollama  # on Titan
    
    If embeddings fail, you can also provide pre-computed vectors directly.
    """
    models = ["mxbai-embed-large:latest", "nomic-embed-text"]
    
    for model in models:
        try:
            resp = requests.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": model, "prompt": text},
                timeout=60
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("embedding"):
                    return data["embedding"]
        except Exception:
            continue
    
    return []


def search(query: str, collection: str = None, limit: int = 5) -> str:
    """Semantic search against a collection."""
    coll = collection or QDRANT_COLLECTION
    
    # Get embedding for query
    vector = get_embedding(query)
    if not vector:
        return "Error: Could not generate embedding. Make sure Ollama is running on Titan."
    
    url = f"{BASE_URL}/collections/{coll}/points/search"
    payload = {
        "vector": vector,
        "limit": limit,
        "with_payload": True,
    }
    
    try:
        resp = requests.post(url, json=payload, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if not data.get("result"):
            return f"No results found for '{query}'"
        
        results = []
        for i, point in enumerate(data["result"], 1):
            score = point.get("score", 0)
            payload = point.get("payload", {})
            text = payload.get("text", payload.get("content", str(payload)))
            # Truncate long text
            if len(text) > 500:
                text = text[:500] + "..."
            results.append(f"{i}. [score: {score:.3f}] {text}")
        
        return f"Results for '{query}':\n\n" + "\n\n".join(results)
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def list_collections() -> str:
    """List all collections."""
    url = f"{BASE_URL}/collections"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        collections = data.get("result", {}).get("collections", [])
        if not collections:
            return "No collections found."
        
        names = [c["name"] for c in collections]
        return "Available collections:\n- " + "\n- ".join(names)
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def collection_info(collection: str = None) -> str:
    """Get info about a collection."""
    coll = collection or QDRANT_COLLECTION
    url = f"{BASE_URL}/collections/{coll}"
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        info = data.get("result", {})
        return (
            f"Collection: {info.get('name')}\n"
            f"Status: {info.get('status')}\n"
            f"Points: {info.get('points_count')}\n"
            f"Vectors: {info.get('vectors_count')}"
        )
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def index_text(text: str, collection: str = None) -> str:
    """Add text to a collection."""
    coll = collection or QDRANT_COLLECTION
    
    # Get embedding for text
    vector = get_embedding(text)
    if not vector:
        return "Error: Could not generate embedding."
    
    import time
    import uuid
    
    point_id = str(uuid.uuid4())
    url = f"{BASE_URL}/collections/{coll}/points"
    payload = {
        "points": [{
            "id": point_id,
            "vector": vector,
            "payload": {
                "text": text,
                "source": "agent",
                "timestamp": time.time()
            }
        }]
    }
    
    try:
        resp = requests.put(url, json=payload, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return f"Indexed: {text[:50]}... (ID: {point_id})"
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Qdrant Query Skill")
    parser.add_argument("command", choices=["search", "list", "info", "index"], help="Command to run")
    parser.add_argument("query", nargs="?", help="Search query, text to index, or collection name")
    parser.add_argument("--collection", "-c", help="Collection name")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Max results")
    
    args = parser.parse_args()
    
    if args.command == "search":
        if not args.query:
            print("Error: search requires a query")
            sys.exit(1)
        print(search(args.query, args.collection, args.limit))
    
    elif args.command == "list":
        print(list_collections())
    
    elif args.command == "info":
        print(collection_info(args.collection))
    
    elif args.command == "index":
        if not args.query:
            print("Error: index requires text to add")
            sys.exit(1)
        print(index_text(args.query, args.collection))


if __name__ == "__main__":
    main()
