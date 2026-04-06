# EchoVault Specifications Guide

All project specifications are now stored in EchoVault for efficient semantic search.

## New EchoVault Features (2026-04-06)

### 1. Cached Embeddings
LRU cache for embedding providers to reduce latency from ~200ms to ~5ms on repeated queries.

```python
from memory.embeddings import OllamaEmbedding, CachedEmbeddingProvider

provider = CachedEmbeddingProvider(
    OllamaEmbedding(model="nomic-embed-text"),
    maxsize=1000,  # LRU cache size
    ttl_seconds=None  # Optional TTL
)
```

### 2. Temporal Queries
Search by time range and calendar dates.

```python
# Search by timestamp range
results = memory.search_by_time_range(
    start_timestamp=1609459200,
    end_timestamp=1640995200
)

# Search by calendar date (e.g., "what we did in March 2025")
results = memory.search_by_date(2025, month=3)  # March 2025
results = memory.search_by_date(2025, month=3, day=15)  # March 15, 2025
```

### 3. LLM-Based Compression
Semantic compression for Slow tier using LLM summarization.

```python
from memory.compression import OllamaCompressor, OpenAICompressor

# Ollama-based compression
compressor = OllamaCompressor(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)

# Or OpenAI-based
compressor = OpenAICompressor(
    model="gpt-4o-mini",
    api_key="your-key"
)

memory = create_unified_memory(compression_provider=compressor)
```

### 4. Graph Relations
Model relationships between memory entries: depends_on, related_to, part_of, supersedes.

```python
from memory.graph_relations import MemoryRelation, RelationType

# Add relation
memory.graph.add_relation(MemoryRelation(
    source_id="entry-1",
    target_id="entry-2",
    relation_type=RelationType.DEPENDS_ON,
    strength=0.9,
    notes="Depends on config"
))

# Find path between entries
path = memory.graph.get_path("A", "B", max_depth=3)

# Get transitive dependencies
deps = memory.graph.get_dependencies("entry-id")

# Find cycles
cycles = memory.graph.find_cycles("entry-id")
```

---

## How to Use Specifications

### Searching Specifications

```javascript
// Find all specifications
mcp_echovault_memory_search({
  query: "specs requirements design",
  limit: 10
})

// Find specific specification
mcp_echovault_memory_search({
  query: "docker optimization requirements",
  limit: 5
})

// Find by topic
mcp_echovault_memory_search({
  query: "github actions workflow",
  limit: 5
})
```

## Available Specifications

### CI/CD and Automation
- **cancel-old-workflows** - automatic cancellation of old workflows
- **fix-github-actions** - fixing GitHub Actions
- **manual-release-process** - manual release process
- **restore-missing-releases** - restoring missing releases

### Docker and Build
- **docker-windows-optimization** - Docker optimization for Windows
- **fix-docker-sdk-download** - fixing SDK download
- **openwrt-build-optimization** - OpenWrt build optimization

### Functionality
- **captive-portal-automation** - captive portal automation
- **daemon-cookie-management** - cookie management in daemon
- **remove-ipv6-support** - removing IPv6 support

## Query Examples

```javascript
// Find requirements for Docker optimization
mcp_echovault_memory_search({
  query: "docker windows optimization requirements",
  limit: 3
})

// Find design for GitHub Actions
mcp_echovault_memory_search({
  query: "github actions fix design",
  limit: 3
})

// Find tasks for captive portal
mcp_echovault_memory_search({
  query: "captive portal automation tasks",
  limit: 3
})

// Find all requirements
mcp_echovault_memory_search({
  query: "requirements EARS SHALL",
  limit: 10
})

// Find correctness properties
mcp_echovault_memory_search({
  query: "correctness properties for any",
  limit: 10
})
```

## Specification Structure

Each specification contains:

1. **requirements.md** - requirements in EARS format
   - Ubiquitous: THE {system} SHALL {response}
   - Event-driven: WHEN {trigger}, THE {system} SHALL {response}
   - State-driven: WHILE {condition}, THE {system} SHALL {response}
   - Unwanted event: IF {condition}, THEN THE {system} SHALL {response}
   - Optional feature: WHERE {option}, THE {system} SHALL {response}

2. **design.md** - detailed design with correctness properties
   - Property N: {description}
   - For any {condition}, {property should hold}
   - Validates: Requirements X.Y

3. **tasks.md** - implementation task list
   - Tasks with checkboxes
   - Links to requirements
   - Priorities and dependencies

## Working with Specifications

### Creating New Specification

1. Create directory in `.kiro/specs-old/{feature-name}/`
2. Create files: requirements.md, design.md, tasks.md
3. Load into EchoVault via PowerShell script

### Updating Specification

1. Update files in `.kiro/specs-old/{feature-name}/`
2. Reload into EchoVault
3. Reindex: `memory reindex`

### Searching Specifications

```javascript
// Semantic search across all specifications
mcp_echovault_memory_search({
  query: "your query",
  limit: 5
})

// Filter by category
mcp_echovault_memory_search({
  query: "category:context tags:specs",
  limit: 10
})
```

## Legacy Files

Original specifications preserved in `.kiro/specs-old/` for reference and editing.

## Benefits

1. **Semantic search** - finds relevant specifications by query meaning
2. **Fast access** - no need to manually search files
3. **Contextual search** - finds related requirements, design and tasks
4. **Token efficiency** - only needed information loaded
5. **Change history** - all versions saved in EchoVault

## Workflow Patterns

### Starting Work on Feature

```javascript
// 1. Find specification
mcp_echovault_memory_search({
  query: "feature-name requirements",
  limit: 3
})

// 2. Find design
mcp_echovault_memory_search({
  query: "feature-name design properties",
  limit: 3
})

// 3. Find tasks
mcp_echovault_memory_search({
  query: "feature-name tasks",
  limit: 3
})
```

### Coverage Check

```javascript
// Find all requirements
mcp_echovault_memory_search({
  query: "feature-name requirements SHALL",
  limit: 10
})

// Find all properties
mcp_echovault_memory_search({
  query: "feature-name property validates",
  limit: 10
})
```

### Troubleshooting

```javascript
// Find similar problems
mcp_echovault_memory_search({
  query: "problem description",
  limit: 5
})

// Find solutions
mcp_echovault_memory_search({
  query: "solution approach",
  limit: 5
})
```

---

*Last updated: 2026-04-06*
*EchoVault Version: Unified Memory Model with Caching, Temporal Queries, Compression, and Graph Relations*
