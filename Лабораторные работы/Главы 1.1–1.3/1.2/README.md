# 1.2 C и Python вместе

Собрать ядро на C в динамическую библиотеку и вызвать его из Python через ctypes.

[Открыть отчёт в PDF](Отчёт.pdf) · [Скриншот проверки](Проверка.jpg)

Собрала ядро из 1.1 в динамическую библиотеку. Подключила её через `ctypes`, проверила раскладку структуры и ошибку пустого указателя. Python формирует событие `agent_started` в JSON.

Запуск из папки «Главы 1.1–1.3» на macOS:

```sh
clang -Wall -Wextra -Werror -dynamiclib 1.1/core_info.c -o 1.2/libcore.dylib
python3 1.2/brain.py --layout
python3 1.2/brain.py --check-null
python3 1.2/brain.py
```

[Результат проверки](Проверка.txt) · [Глава курса](https://maximbytecamp.github.io/sysprog_makarov/temy/07-c-i-python-vmeste/index.html)
