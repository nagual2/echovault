# Web Search Configuration for Collective Wisdom

## Quick Start

Коллектив Двархов теперь поддерживает **гибридный поиск**: локальная память + веб-источники.

### 1. Получить API ключ

**Вариант A: Serper.dev (рекомендуется)**
- Регистрация: https://serper.dev
- 2500 запросов бесплатно, затем $0.001/запрос
- Поддерживает Google Search

**Вариант B: Brave Search API**
- Регистрация: https://brave.com/search/api/
- 2000 запросов/мес бесплатно
- Privacy-focused

### 2. Настроить переменные окружения

В PowerShell (постоянно):
```powershell
[Environment]::SetEnvironmentVariable("SERPER_API_KEY", "your_key_here", "User")
```

Или временно в сессии:
```powershell
$env:SERPER_API_KEY = "your_key_here"
```

### 3. Проверить работу

Запроси меня:
> "Ри, активируй Коллектив для поиска последней версии Go"

## Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| `SERPER_API_KEY` | API ключ для Serper.dev | — |
| `BRAVE_API_KEY` | API ключ для Brave Search | — |
| `ECHOVAULT_WEB_SEARCH` | Feature flag: `enabled`/`disabled` | `enabled` |
| `ECHOVAULT_WEB_MIN_LOCAL` | Минимум локальных результатов до веб-поиска | `3` |
| `ECHOVAULT_WEB_MAX_RESULTS` | Максимум веб-результатов | `5` |

## Feature Flags

### Отключить веб-поиск полностью
```powershell
$env:ECHOVAULT_WEB_SEARCH = "disabled"
```

При отключении Коллектив работает только с локальной памятью (как раньше).

### Настроить пороги
```powershell
# Искать в вебе если локально < 5 результатов
$env:ECHOVAULT_WEB_MIN_LOCAL = "5"

# Получать максимум 3 веб-источника
$env:ECHOVAULT_WEB_MAX_RESULTS = "3"
```

## Когда активируется веб-поиск

Автоматически, когда:
1. Локальных результатов < `ECHOVAULT_WEB_MIN_LOCAL` (по умолчанию 3)
2. Запрос содержит ключевые слова свежести:
   - `latest`, `recent`, `new`, `2024`, `2025`, `2026`
   - `новый`, `последний`, `актуальный`
   - `update`, `release`, `version`

## Формат ответа Коллектива

```json
{
  "status": "collective_sync",
  "local_memories_found": 2,
  "web_sources_found": 3,
  "relevant_knowledge_domains": ["project1", "project2"],
  "top_memories": [...],
  "web_sources": [
    {
      "title": "Go 1.22 Release Notes",
      "url": "https://go.dev/doc/go1.22",
      "snippet": "Go 1.22 adds preview of range-over-function...",
      "source": "serper"
    }
  ],
  "strategic_suggestions": [
    "Web search found 3 relevant sources.",
    "  • Go 1.22 Release Notes... (serper)",
    "Use 'tcpdump' or 'ss' for L3-L4 diagnostics."
  ]
}
```

## Troubleshooting

### Веб-поиск не работает
1. Проверь API ключ:
   ```powershell
   $env:SERPER_API_KEY
   ```
2. Проверь feature flag:
   ```powershell
   $env:ECHOVAULT_WEB_SEARCH
   ```
3. Проверь логи: веб-поиск не ломает Коллектив при ошибках — просто не добавляет результаты.

### Слишком много/мало веб-результатов
Настрой `ECHOVAULT_WEB_MIN_LOCAL` и `ECHOVAULT_WEB_MAX_RESULTS`.

### Хочу только локальную память
```powershell
$env:ECHOVAULT_WEB_SEARCH = "disabled"
```

## Архитектура

```
┌────────────────────────────────────────────────────────┐
│          memory_collective_solve(task)                 │
└────────────────────────┬───────────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────────┐
│  Phase 1: Локальная память (EchoVault SQLite)          │
│  • FTS5 + Vector search                                │
│  • Результат: N записей                                │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼ (если N < min_local или fresh keywords)
┌────────────────────────────────────────────────────────┐
│  Phase 2: Web Search (async)                           │
│  • SerperProvider или BraveProvider                    │
│  • httpx.AsyncClient с таймаутом 10s                   │
│  • Graceful degradation (при ошибке → пустой результат)│
└────────────────────────┬───────────────────────────────┘
                         ▼
┌────────────────────────────────────────────────────────┐
│  Phase 3: Merge & Strategize                             │
│  • Объединение локальных + веб-источников              │
│  • Паттерн-матчинг для инструментов                    │
│  • Формирование JSON ответа                            │
└────────────────────────────────────────────────────────┘
```

## Безопасность

- API ключи никогда не сохраняются в памяти EchoVault
- Веб-запросы — только при явной необходимости
- Таймаут 10 секунд — не блокирует Коллектив
- Никаких следов веб-поиска в локальной памяти (только рекомендации)

## Privacy Notes

- Serper.dev: запросы идут к Google через их API
- Brave: privacy-focused, не отслеживает пользователей
- В обоих случаях — только текст запроса, никаких данных проекта

---

*«Коллектив расширен. Теперь мы видим за пределы локального хранилища.»*
