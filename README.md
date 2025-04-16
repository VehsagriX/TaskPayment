# Wallet Payment Service

Простой REST API для оплаты услуги с кошелька.

## Возможности

- Создание платежа (POST /payment)
- Проверка статуса платежа (GET /payment/{payment_id})
- Асинхронная работа с 2 базами данных
- Асинхронные запросы к 2 внешним API
- Обработка успешных и неуспешных транзакций

## Технологии

- FastAPI
- SQLAlchemy (async)
- aiohttp
- Pydantic
- Uvicorn
- python-dotenv

## Установка

1. Клонируйте репозиторий

```bash
    git clone https://github.com/VehsagriX/TaskPayment.git
    cd TaskPayment
```
2. Установка зависимостей

```bash
  pip install -r requirements.txt
```
3. Создайте файл .env в корне проекта:


```bash
# .env

WALLET_DB_URL=postgresql+asyncpg://user:password@localhost:5432/wallet_db
PAYMENT_DB_URL=postgresql+asyncpg://user:password@localhost:5432/payment_db

```
4. Запустите приложение
```bash
  uvicorn main:app --reload

```