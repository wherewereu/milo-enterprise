# Qdrant MCP Server

An MCP (Model Context Protocol) server for Qdrant vector database. Enables AI agents to perform semantic search against your private knowledge base.

## Features

- Query Qdrant collections via natural language
- Add/Index text to collections
- List available collections
- Get collection info
- Semantic similarity search using Ollama embeddings (CPU mode)

## Installation

```bash
git clone https://codeberg.org/tylerdotai/qdrant-mcp.git
cd qdrant-mcp
pip install -r requirements.txt
```

## Quick Setup

```bash
mkdir -p ~/.openclaw/skills/qdrant-query
git clone https://codeberg.org/tylerdotai/qdrant-mcp.git ~/.openclaw/skills/qdrant-query
```

## Usage

```bash
# Search knowledge base
python3 ~/.openclaw/skills/qdrant-query/query.py search "your question"

# Add text to knowledge base
python3 ~/.openclaw/skills/qdrant-query/query.py index "important info to store"

# List collections
python3 ~/.openclaw/skills/qdrant-query/query.py list

# Get collection info
python3 ~/.openclaw/skills/qdrant-query/query.py info hydra-rag
```

## Configuration

Environment variables (optional):

```bash
export QDRANT_HOST="192.168.0.247"
export QDRANT_PORT="6333"
export QDRANT_COLLECTION="hydra-rag"
export OLLAMA_HOST="192.168.0.247"
export OLLAMA_PORT="11434"
```

## Titan Setup

### llama-server (GPU) - Running on ports 8402/8403

The Strix Halo runs llama-server in a Docker container:

```bash
# In llama-box container:
llama-server -m /models/Qwen3.5-35B-A3B-Q4_K_M.gguf -c 8192 -ngl 999 -fa 1 --no-mmap --host 0.0.0.0 --port 8402
llama-server -m /models/Qwen3-14B-Q4_K_M.gguf -c 8192 -ngl 999 -fa 1 --no-mmap --host 0.0.0.0 --port 8403
```

### Ollama (CPU) - For Embeddings

Ollama runs on the host in CPU mode due to ROCm issues:

```bash
# On Titan: /etc/systemd/system/ollama.service.d/override.conf
[Service]
Environment=OLLAMA_MODELS=/mnt/filestore/ollama_models
Environment=OLLAMA_HOST=0.0.0.0:11434
Environment=CUDA_VISIBLE_DEVICES=-1

systemctl daemon-reload && systemctl restart ollama
```

### Qdrant

Qdrant runs on the host on port 6333.

## Available Collections

- `hydra-rag` - General RAG/knowledge base (default)
- `workspace-memory` - Workspace memory
- `conversations` - Conversation history
- `personal` - Personal notes
- `ai-news` - AI news articles
- `mesh-docs` - Mesh network docs
- `agent-handoffs` - Agent handoff records
- `system_states` - System state snapshots
- `screenshots` - Screenshot metadata
- `openclaw-config` - OpenClaw configuration
- `documentation` - General docs
- `web-intel` - Web intelligence
- `strixhalo-wiki` - Strix Halo documentation

## Known Issues

- **Ollama embeddings on GPU**: llama.cpp embedding binary crashes on ROCm 7.x. Running in CPU mode (`CUDA_VISIBLE_DEVICES=-1`) works around this.
