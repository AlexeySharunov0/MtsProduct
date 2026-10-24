# Prodboard Autotests

Проект автоматизации тестирования: UI-тесты (Playwright + pytest) и API-тесты (requests + pytest).

## Подготовка окружения

1. Установите зависимости:

```bash
pip install -r requirements.txt
pip install -r requirements_all.txt
```

2. Создайте файл `.env` на основе `.env.example` и заполните переменные:

```bash
cp .env.example .env
```

| Переменная | Назначение |
| --- | --- |
| `ENV` | Окружение: `dev`, `stage`, `prod`, `local` |
| `BASE_URL` | Базовый URL приложения (переопределяет URL выбранного окружения) |
| `API_BASE_URL` | Базовый URL API |
| `IS_HEADLESS` | `FALSE` — запускать браузер с интерфейсом, иначе headless |
| `AUTH_TOKEN_URL` | Endpoint выдачи OAuth-токена |
| `AUTH_LOGIN` | Логин для заголовков API-запросов |
| `VAULT_URL`, `VAULT_MOUNT_POINT`, `ROLE_VAULT`, `SECRET_VAULT` | Параметры Vault для получения учётных данных (опционально) |

> Учётные данные тестовых пользователей не хранятся в репозитории: они читаются из Vault во время выполнения.

## Запуск тестов

```bash
pytest
pytest -v # визуальный режим
pytest -q # тихий режим
```

## Кастомизация запусков

### Запуск API/UI тестов

```bash
pytest API
pytest UI
```

### Запуск тестов по фиче

```bash
pytest -m search
```

### Запуск тестов для мониторинга

```bash
pytest -m monitoring
```

### Запуск тестов по сложному условию

```bash
pytest -m "(monitoring and search) or not ui"
```

Полный список меток доступен в `pytest.ini`.

## Создание отчётов в Allure

```bash
pytest --alluredir=allure-results
```

Команда создаст директорию `allure-results` с отчётом о прогоне. Далее эту директорию можно загрузить в Allure TestOps.

## Запуск в многопоточном режиме

```bash
pytest -n8 # запустит тесты в 8 потоков
```

## Автоперезапуск упавших тестов

```bash
pytest --reruns 2 # запустит тесты и перезапустит упавший ещё 2 раза
```

## Структура проекта

```
/Prodboard
│
├── /UI                        # Тесты и ресурсы, связанные с пользовательским интерфейсом
│   ├── /data                  # Данные для тестов
│   ├── /pages                 # Page Object описание страниц
│   ├── /tests                 # UI-тесты
│   ├── /utils                 # Вспомогательные модули
│   └── ui_fixtures.py         # Фикстуры для UI
│
├── /API                       # Тесты и ресурсы, связанные с API
│   ├── /data                  # Pydantic-модели данных
│   ├── /models                # Методы, разбитые по микросервисам
│   ├── /tests                 # API-тесты
│   ├── /utils                 # Вспомогательные модули
│   └── api_fixtures.py        # Фикстуры для API
│
├── /notifications             # Шаблоны уведомлений о результатах прогона
├── .env.example               # Пример переменных окружения
├── conftest.py                # Общие фикстуры pytest
├── pytest.ini                 # Конфигурация pytest и метки
└── requirements.txt           # Зависимости проекта
```

## Уведомления о результатах

`notifications/json_creator.sh` формирует конфигурацию для allure-notifications.
Секреты и адреса передаются через переменные окружения:

| Переменная | Назначение |
| --- | --- |
| `ALLURE_REPORT_URL` | Ссылка на отчёт |
| `TELEGRAM_TOKEN`, `TELEGRAM_CHAT` | Доступ к Telegram-боту |
| `PROXY_HOST`, `PROXY_PORT`, `PROXY_USERNAME`, `PROXY_PASSWORD` | Прокси (при необходимости) |
