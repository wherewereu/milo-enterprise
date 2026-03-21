# Qdrant Query Skill

Query and index your vector knowledge base on Titan.

## Trigger Phrases
- "search my knowledge"
- "query qdrant"
- "search rag"
- "index to knowledge"
- "add to knowledge base"

## Usage

### Search Knowledge Base
```bash
python3 ~/.openclaw/skills/qdrant-query/query.py search "your question"
```

### Index (Add) Text
```bash
python3 ~/.openclaw/skills/qdrant-query/query.py index "important info to store"
```

### List Collections
```bash
python3 ~/.openclaw/skills/qdrant-query/query.py list
```

### Collection Info
```bash
python3 ~/.openclaw/skills/qdrant-query/query.py info hydra-rag
```

## Configuration

Set these environment variables:
- `QDRANT_HOST` (default: 192.168.0.247)
- `QDRANT_PORT` (default: 6333)
- `QDRANT_COLLECTION` (default: hydra-rag)
- `OLLAMA_HOST` (default: 192.168.0.247)
- `OLLAMA_PORT` (default: 11434)

## Example Queries

- "search my knowledge base for flume project updates"
- "index Tyler asked about Qdrant setup today"
- "list qdrant collections"
