#!/usr/bin/env python3
"""
Qdrant MCP Server
Enables AI agents to query Qdrant vector database via MCP protocol.
"""

import os
import json
from typing import Any, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import qdrant_client
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
DEFAULT_COLLECTION = os.getenv("QDRANT_COLLECTION", "hydra-rag")

app = Server("qdrant-mcp")

# Initialize Qdrant client
def get_client() -> QdrantClient:
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="search",
            description="Semantic search against Qdrant vector database",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query text"},
                    "collection": {"type": "string", "description": "Collection name", "default": DEFAULT_COLLECTION},
                    "limit": {"type": "integer", "description": "Max results", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="list_collections",
            description="List all available Qdrant collections",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="collection_info",
            description="Get information about a collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name", "default": DEFAULT_COLLECTION},
                },
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    client = get_client()
    
    if name == "search":
        query = arguments["query"]
        collection = arguments.get("collection", DEFAULT_COLLECTION)
        limit = arguments.get("limit", 5)
        
        try:
            results = client.search(
                collection_name=collection,
                query_text=query,
                limit=limit,
                with_payload=True,
            )
            
            formatted = []
            for i, result in enumerate(results, 1):
                payload = result.payload or {}
                formatted.append({
                    "score": result.score,
                    "id": result.id,
                    "text": payload.get("text", payload.get("content", str(payload))),
                })
            
            return [TextContent(type="text", text=json.dumps(formatted, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "list_collections":
        try:
            collections = client.get_collections()
            names = [c.name for c in collections.collections]
            return [TextContent(type="text", text=json.dumps(names, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    elif name == "collection_info":
        collection = arguments.get("collection", DEFAULT_COLLECTION)
        try:
            info = client.get_collection(collection_name=collection)
            return [TextContent(type="text", text=json.dumps({
                "name": info.name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.name,
            }, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    return [TextContent(type="text", text="Unknown tool")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
