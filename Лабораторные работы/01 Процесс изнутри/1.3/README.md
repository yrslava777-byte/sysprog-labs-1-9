# 1.3 n8n и Ollama

Подготовила отправку события `agent_started` и сценарий для импорта в n8n. В сценарии вебхук передаёт данные в цепочку с Ollama, а её ответ используется в тестовом письме.

Для запуска в n8n импортируйте [agent-started.json](agent-started.json), подключите локальную Ollama и тестовый SMTP (например, Mailpit). Запустите прослушивание тестового вебхука и выполните из папки первой лабораторной:

```sh
python3 -B 1.3/send_event.py http://localhost:5678/webhook-test/agent --library 1.2/libcore.dylib
```

Проверила отправку JSON на локальный HTTP-приёмник. Сквозная проверка в n8n с ответом модели и тестовым письмом ещё не выполнена.

[Результат проверки](Проверка.txt) · [Глава курса](https://maximbytecamp.github.io/sysprog_makarov/temy/08-n8n-i-ollama/index.html)
