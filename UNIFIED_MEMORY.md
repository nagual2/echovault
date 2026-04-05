# Unified 3-Tier Memory System

## Overview

Unified memory model для EchoVault, интегрирующая иерархическую память с 3 tiers:

| Tier | Скорость | Хранение | Жизненный цикл | Поиск |
|------|----------|----------|----------------|-------|
| **Fast** | <1ms | RAM (in-memory SQLite) | 24h TTL | Синхронный |
| **Medium** | <100ms | SSD | 7 дней + LRU eviction | Синхронный FTS |
| **Slow** | 100ms-10s | HDD | Бессрочно | **Асинхронный** semantic |

## Соответствие модели пользователя

```
Твоя модель          →  Unified EchoVault
─────────────────────────────────────────────
Быстрая память       →  Fast tier (Core)
Средняя память       →  Medium tier (Short-term)
Медленная память     →  Slow tier (Long-term)
```

## Особенности Slow tier

**Ключевое отличие**: Поиск в Slow tier — **неблокирующий**:

```python
# Синхронный поиск (Fast + Medium) — результат сразу
results = unified.search_sync("query", limit=5)

# Асинхронный поиск (Slow) — callback когда найдено
def on_found(results):
    print(f"Найдено в архиве: {len(results)}")

unified.search_async("query", callback=on_found)

# Полный поиск: сразу Fast+Medium, в фоне Slow
results = unified.search_full("query", async_callback=on_found)
```

## Pipeline миграции

```
Входящие данные
      ↓
   [Fast] ← 24h TTL, cleanup каждые 60s
      ↓ (через 1-2 часа, структурирование)
  [Medium] ← 7 дней, LRU eviction при переполнении
      ↓ (низкий access, старость)
   [Slow] ← семантическая компрессия, embeddings
```

## Использование

### Базовое

```python
from memory.unified import create_unified_memory

# Создать сервис
memory = create_unified_memory()
await memory.start()  # Запустить background workers

# Сохранить (в Fast tier)
entry = MemoryEntry(
    id="mem-1",
    title="Важное уточнение",
    what="Суть для будущих сессий",
    tier=MemoryTier.FAST,
    timestamp=int(time.time()),
    tags=["rule", "workflow"]
)
memory.save(entry)

# Поиск
results = memory.search_sync("уточнение", limit=5)
```

### С async поиском

```python
# Callback для результатов из Slow tier
def handle_slow_results(results):
    for r in results:
        print(f"[Архив] {r.title}: {r.what}")

# Полный поиск: sync + async
sync_results = memory.search_full(
    "конфигурация",
    limit=5,
    async_callback=handle_slow_results
)
# sync_results — сразу из Fast/Medium
# handle_slow_results вызовется позже с результатами из Slow
```

### Получение контекста

```python
# Контекст для инъекции в промпт
context = memory.get_context(limit=10, project="MyProject")
for entry in context:
    print(f"- {entry.title}: {entry.what}")
```

## Интеграция с существующим EchoVault

```python
from memory.unified_adapter import create_unified_adapter

# Адаптер для постепенной миграции
adapter = create_unified_adapter(memory_home="~/.memory")
await adapter.start()

# Писать в обе системы
adapter.save_unified(
    memory_id="...",
    title="...",
    what="...",
    project="..."
)

# Поиск в unified (fallback к существующей)
results = adapter.search_unified("query")
```

## Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                   UnifiedMemoryService                   │
├──────────────┬──────────────┬───────────────────────────┤
│   FastTier   │  MediumTier  │        SlowTier           │
│  (in-memory) │    (SSD)     │        (HDD)              │
├──────────────┼──────────────┼───────────────────────────┤
│ SQLite :mem  │ SQLite file  │ SQLite file + embeddings  │
│ 24h TTL      │ 7d retention │ Бессрочно                 │
│ Sync search  │ FTS search   │ Async semantic search     │
│ Cleanup 60s  │ LRU eviction │ Background worker         │
└──────────────┴──────────────┴───────────────────────────┘
       ↑              ↑                    ↑
   Migration Pipeline (каждые 5 минут)
```

## Файлы

- `src/memory/unified.py` — Core implementation (887 строк)
- `src/memory/unified_adapter.py` — Интеграция с существующим
- `tests/test_unified_memory.py` — Тесты
- `src/memory/unified.pyi` — Type stubs

## TODO для production

1. **Интеграция MCP**: Добавить tools для unified search
2. **Мониторинг**: Метрики по тирам (hit rate, latency)
3. **Настройки**: Configurable TTL, размеры, пути
4. **Восстановление**: Startup scan для consistency
5. **Компрессия**: NLP summarization для Slow tier
