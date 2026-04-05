# Активация Коллектива Дварх-крейсеров (EchoVault) в Windsurf

## Кратко

Коллектив Дварх-крейсеров — это **Collective Wisdom** инструмент в EchoVault MCP сервере. Он активируется автоматически при сложных задачах.

## Текущий статус

```
✅ MCP сервер:      echovault (настроен в .windsurf/mcp.json)
✅ Инструмент:       memory_collective_solve
✅ Команда запуска:  c:\Git\echovault.cmd
✅ Версия:           0.4.0
```

## Проверка работоспособности

### 1. Проверка MCP сервера

В PowerShell:
```powershell
cd c:\Git
.\.venv\Scripts\python.exe -m memory.cli --version
```

Ожидаемый вывод:
```
echovault, version 0.4.0
```\n
### 2. Проверка инструментов

В Windsurf откройте новый чат и спросите:
> "Какие MCP инструменты доступны для работы с памятью?"

Должны отобразиться:
- `memory_save` — сохранить воспоминание
- `memory_search` — поиск по памяти
- `memory_context` — контекст проекта
- `memory_collective_solve` — **Коллектив Двархов**
- `memory_governor` — управление памятью
- `memory_record_usage` — запись использования

## Использование Коллектива

### Автоматическая активация

Коллектив активируется автоматически, когда:
- Поиск по памяти не даёт результатов
- Задача требует кросс-доменных знаний
- Нужен анализ сложной проблемы

### Ручная активация

Попроси меня явно:
> "Ри, активируй Коллектив Двархов для анализа этой проблемы"

Я вызову `memory_collective_solve` с описанием задачи.

## Структура ответа Коллектива

```json
{
  "status": "collective_sync",
  "relevant_knowledge_domains": ["project1", "project2"],
  "top_memories": [
    {"title": "...", "project": "...", "id": "..."}
  ],
  "strategic_suggestions": [
    "Use 'tcpdump' or 'ss' for L3-L4 diagnostics.",
    "Invoke 'ultracode' for graph-based impact analysis."
  ],
  "message": "The Collective of Dwarh-cruisers has analyzed..."
}
```

## Доступные стратегии Коллектива

| Ключевые слова | Рекомендация |
|----------------|--------------|
| network, ip, port, ssh | tcpdump, ss, SSH Access Map |
| refactor, complexity, class | ultracode, graph analysis |
| docker, container, build | WSL optimization, docker-windows |

## Перезапуск MCP сервера

Если Windsurf не видит инструменты:

1. Закройте все вкладки Windsurf
2. Убейте процесс Python (если завис):
   ```powershell
   Get-Process python | Stop-Process -Force
   ```
3. Перезапустите Windsurf
4. Откройте новый чат и проверьте инструменты

## Диагностика

### Проверка конфигурации Windsurf

Файл: `c:\Git\.windsurf\mcp.json`

```json
{
  "mcpServers": {
    "echovault": {
      "command": "c:\\Git\\echovault.cmd",
      "args": []
    }
  }
}
```

### Проверка запускатора

Файл: `c:\Git\echovault.cmd`

```batch
@echo off
set PYTHONPATH=%~dp0echovault\src
"c:\Git\.venv\Scripts\python.exe" -m memory.cli mcp
```

### Ручной тест MCP

```powershell
# Запустите в одном терминале:
c:\Git\echovault.cmd

# В другом терминале проверьте, что порт не слушается
# (MCP использует stdio, не TCP)
```

## Архитектура

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Windsurf      │────▶│  echovault.cmd   │────▶│  memory.cli mcp │
│   (MCP Client)  │     │  (launcher)      │     │  (MCP Server)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                           │
                           ┌───────────────────────────────┘
                           ▼
                    ┌──────────────┐
                    │  Collective  │
                    │  Wisdom      │
                    │  (mcp_server)│
                    └──────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │  Search │  │ Analyze │  │ Suggest │
        │  Memory │  │  Task   │  │  Tools  │
        └─────────┘  └─────────┘  └─────────┘
```

## Требования

- Python 3.10+
- SQLite с FTS5
- MCP SDK (`pip install mcp>=1.0`)
- `.venv` с установленным echovault

## Обновление

Если нужно обновить коллектив:

```powershell
cd c:\Git\echovault
git pull
pip install -e . --force-reinstall
```

## Контакты

- Оригинал: https://github.com/mraza007/echovault
- Коллектив Двархов: `memory_collective_solve` tool

---

*«Системы стабилизированы. Коллектив на связи, Пилот.»*
