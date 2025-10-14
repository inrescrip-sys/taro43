# 🔮 Oracle Luck Bot - Мистический Telegram Бот

![Version](https://img.shields.io/badge/version-1.0.0-gold)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![TON](https://img.shields.io/badge/blockchain-TON-0098ea)
![License](https://img.shields.io/badge/license-MIT-green)

**Oracle Luck Bot** (@OracleLuck_Bot) - полнофункциональный Telegram-бот для эзотерики и таро раскладов с интеграцией TON blockchain и Mini App.

---

## ✨ Основные Возможности

### 🎴 10 Типов Раскладов Таро

**Бесплатные (7):**
- 🎴 **Карта дня** - Одна карта на сегодня
- 🔮 **Три карты** - Прошлое-Настоящее-Будущее
- 💼 **Карьера** - Работа и финансы (5 карт)
- 🎭 **Ситуация** - Анализ конкретной ситуации (5 карт)
- 🌟 **Совет дня** - Что нужно знать сегодня (3 карты)

**Премиум (5):**
- 💕 **Отношения** - Глубокий анализ (7 карт) - **0.03 TON**
- 🎯 **Выбор** - Помощь в принятии решений (7 карт) - **0.03 TON**
- ✨ **Кельтский крест** - Полный расклад (10 карт) - **0.05 TON**
- 🧘 **Чакры** - Энергетический анализ (7 карт) - **0.05 TON**
- 📅 **Годовой** - Прогноз на год (13 карт) - **0.1 TON**

### 🌐 TON Web3 Интеграция

- ✅ **TON Connect** - Подключение кошелька в Mini App
- ✅ **Крипто платежи** - Оплата раскладов в TON
- ✅ **Автоматическая проверка** - Мгновенное зачисление средств
- ✅ **История транзакций** - Полная прозрачность

### 📱 Telegram Mini App

- 🎨 **Красивый UI** - Мистический дизайн с анимациями
- 🃏 **3D Карты** - Переворот карт при наведении
- 📊 **Визуализация** - Графическое отображение раскладов
- 📚 **История** - Все расклады в одном месте

### 🤖 AI Интерпретация

- 🧠 **Gemini 2.0 Flash** - Умные предсказания
- 🔮 **Мистические толкования** - Глубокий анализ
- 💫 **Персонализация** - Учет контекста вопроса

### 🔔 Уведомления

- ⏰ **Ежедневные напоминания** - Карта дня в 9:00
- 🎁 **Специальные события** - Полнолуние, ретроград и т.д.
- 📬 **Новые расклады** - Уведомления о новых функциях

---

## 🏗️ Архитектура Проекта

```
oracle_luck_bot/
├── bot.py                    # Основной файл бота
├── ton_integration.py        # TON Web3 модуль
├── miniapp.html             # Telegram Mini App
├── requirements.txt         # Зависимости
├── .env                     # Конфигурация
└── README.md               # Эта документация
```

### Технологический Стек

**Backend:**
- `python-telegram-bot` 22.5 - Telegram Bot API
- `pytoniq` - TON blockchain интеграция
- `motor` / `pymongo` - MongoDB для хранения данных
- `google-generativeai` - AI интерпретация через Gemini

**Frontend (Mini App):**
- Vanilla JavaScript - Без зависимостей
- Telegram Web App SDK - Интеграция с Telegram
- TON Connect UI - Web3 кошельки

---

## 🚀 Быстрый Старт

### 1. Предварительные Требования

- Python 3.10+
- MongoDB (локально или Atlas)
- TON кошелек для приема платежей
- Gemini API ключ (бесплатно на ai.google.dev)

### 2. Установка

```bash
# Клонировать репозиторий (или скачать архив)
cd oracle_luck_bot

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp .env.example .env
```

### 3. Настройка .env

Отредактируйте файл `.env`:

```env
# Telegram Bot
BOT_TOKEN=8294883971:AAG2hefSYbh-idoL_xhAeMhfZCvzARWFAls
BOT_USERNAME=OracleLuck_Bot

# Mini App URL (замените после деплоя)
WEBAPP_URL=https://your-mini-app.vercel.app

# TON Wallet
TON_WALLET_ADDRESS=UQD...ваш_TON_адрес

# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=oracle_luck_bot

# AI Integration
GEMINI_API_KEY=ваш_ключ_от_gemini

# Settings
DAILY_REMINDER_TIME=09:00
TIMEZONE=Europe/Moscow
LOG_LEVEL=INFO
```

### 4. Запуск Бота

```bash
# Запуск в обычном режиме
python bot.py

# Запуск в фоновом режиме (Linux/Mac)
nohup python bot.py > bot.log 2>&1 &

# Запуск через systemd (production)
sudo systemctl start oracle-luck-bot
```

### 5. Деплой Mini App

**Вариант A: Vercel (рекомендуется)**

```bash
# Установить Vercel CLI
npm install -g vercel

# Деплой
cd oracle_luck_bot
vercel --prod miniapp.html
```

**Вариант B: GitHub Pages**

1. Создать репозиторий на GitHub
2. Загрузить `miniapp.html`
3. Включить GitHub Pages
4. Использовать URL: `https://username.github.io/repo/miniapp.html`

**Вариант C: Netlify**

1. Перетащить `miniapp.html` на netlify.com/drop
2. Получить URL
3. Обновить `WEBAPP_URL` в `.env`

### 6. Настройка TON Connect

Создайте файл `tonconnect-manifest.json`:

```json
{
  "url": "https://your-domain.com",
  "name": "Oracle Luck Bot",
  "iconUrl": "https://your-domain.com/icon.png",
  "termsOfUseUrl": "https://your-domain.com/terms",
  "privacyPolicyUrl": "https://your-domain.com/privacy"
}
```

Разместите его по адресу из `manifestUrl` в коде.

---

## 📱 Использование Бота

### Команды

| Команда | Описание |
|---------|----------|
| `/start` | Запустить бота и увидеть главное меню |
| `/daily` | Получить бесплатную карту дня |
| `/balance` | Проверить баланс TON |
| `/history` | Посмотреть историю раскладов |
| `/help` | Справка по командам |

### Inline Меню

**Главное меню:**
- 🎴 Получить расклад
- 🔮 Карта дня
- 💰 Баланс TON
- 📚 История
- 🌐 Открыть Mini App
- ⚙️ Настройки
- ℹ️ Помощь

**Меню раскладов:**
- Список всех 10 типов раскладов
- Цена указана рядом с названием
- Бесплатные помечены зеленым

### Рабочий Процесс

1. **Пользователь запускает бота** → Получает приветствие
2. **Выбирает "Получить расклад"** → Видит список раскладов
3. **Выбирает расклад** → Система проверяет баланс
4. **Для платных:** Оплачивает через TON → Мгновенное зачисление
5. **Получает результат** → Карты + AI интерпретация
6. **Сохраняется в истории** → Доступ в Mini App

---

## 🔮 Карты Таро

### Старшие Арканы (22 карты)

| # | Карта | Ключевые слова |
|---|-------|----------------|
| 0 | 🃏 Дурак | Новые начинания, спонтанность |
| 1 | 🎩 Маг | Мастерство, сила воли |
| 2 | 👸 Верховная Жрица | Интуиция, тайны |
| 3 | 👑 Императрица | Плодородие, изобилие |
| 4 | 🤴 Император | Авторитет, структура |
| 5 | ⛪ Иерофант | Традиции, духовность |
| 6 | 💑 Влюбленные | Любовь, выбор, гармония |
| 7 | 🏇 Колесница | Победа, контроль |
| 8 | 💪 Сила | Храбрость, терпение |
| 9 | 🧙 Отшельник | Мудрость, поиск |
| 10 | 🎡 Колесо Фортуны | Судьба, изменения |
| 11 | ⚖️ Справедливость | Честность, правда |
| 12 | 🙃 Повешенный | Жертва, новый взгляд |
| 13 | 💀 Смерть | Трансформация, конец |
| 14 | 🧘 Умеренность | Баланс, терпение |
| 15 | 😈 Дьявол | Зависимость, искушение |
| 16 | 🏰 Башня | Разрушение, откровение |
| 17 | ⭐ Звезда | Надежда, вдохновение |
| 18 | 🌙 Луна | Иллюзия, страхи |
| 19 | ☀️ Солнце | Радость, успех |
| 20 | 📯 Суд | Возрождение, прощение |
| 21 | 🌍 Мир | Завершение, целостность |

### Младшие Арканы (56 карт)

**4 масти:**
- 🔥 **Жезлы** (Огонь) - Действие, энергия
- 💧 **Кубки** (Вода) - Эмоции, отношения
- ⚔️ **Мечи** (Воздух) - Разум, конфликты
- 💎 **Пентакли** (Земля) - Материальность, работа

**Каждая масть содержит:**
- Туз (1) - Новые начинания
- 2-10 - Различные ситуации
- Паж - Молодость, новости
- Рыцарь - Действие, движение
- Королева - Женская энергия
- Король - Мужская энергия

---

## 💰 Монетизация и Экономика

### Ценообразование

```
Бесплатные расклады: 7 типов
├── Привлечение пользователей
└── Знакомство с функционалом

Премиум расклады: 5 типов
├── 0.03 TON - Базовые (Отношения, Выбор)
├── 0.05 TON - Расширенные (Кельтский крест, Чакры)
└── 0.1 TON - Полные (Годовой расклад)
```

### Целевая Экономика

**Цель:** $10/день (~0.5 TON на октябрь 2025)

**Сценарий 1: Микротранзакции**
- 10 пользователей × 0.03 TON = 0.3 TON
- 4 пользователя × 0.1 TON = 0.4 TON
- **Итого: 0.7 TON/день ✅**

**Сценарий 2: Подписка** (будущая функция)
- Premium подписка: 1 TON/месяц
- 20 подписчиков = 20 TON/месяц = 0.67 TON/день ✅

### Стратегия Роста

1. **Неделя 1-2:** Органический рост
   - Публикация в тематических каналах
   - Реферальная программа (10% кэшбек)

2. **Неделя 3-4:** Масштабирование
   - Платная реклама в TON-сообществах
   - Партнерства с эзотерическими каналами

3. **Месяц 2+:** Автоматизация
   - Подписки и абонементы
   - Персонализированные предложения

---

## 🔧 Настройка и Кастомизация

### Добавление Новых Раскладов

В файле `bot.py` найдите `SPREAD_TYPES` и добавьте:

```python
{
    "id": "new_spread",
    "name": "🌙 Лунный расклад",
    "cards": 8,
    "price": 0.04,
    "description": "Расклад по фазам луны"
}
```

### Изменение Цен

```python
# В SPREAD_TYPES измените значение "price"
{
    "id": "love",
    "name": "💕 Расклад на отношения",
    "cards": 7,
    "price": 0.05,  # Было 0.03
    "description": "Глубокий анализ отношений"
}
```

### Настройка Уведомлений

```python
# В функции main()
job_queue.run_daily(
    send_daily_reminder,
    time=time(hour=10, minute=30),  # Измените время
    days=(0, 1, 2, 3, 4, 5, 6)
)
```

### Добавление Новых Карт

```python
# В TAROT_CARDS добавьте:
"new_suit": [
    {
        "name": "Туз Звезд",
        "emoji": "⭐",
        "keywords": "космическая энергия"
    }
]
```

---

## 📊 Мониторинг и Аналитика

### Логирование

Бот записывает все действия в лог:

```bash
# Просмотр логов
tail -f bot.log

# Поиск ошибок
grep "ERROR" bot.log

# Статистика по раскладам
grep "расклад" bot.log | wc -l
```

### Метрики для Отслеживания

```python
# В users_db хранятся:
- Количество раскладов на пользователя
- Баланс пользователя
- История платежей
- Последняя активность
```

### Интеграция с Analytics

```python
# Добавьте в bot.py:
from mixpanel import Mixpanel

mp = Mixpanel("YOUR_TOKEN")

def track_event(user_id, event_name, properties={}):
    mp.track(user_id, event_name, properties)

# Использование:
track_event(user_id, "Reading Created", {
    "spread_type": spread_id,
    "price": spread["price"]
})
```

---

## 🔒 Безопасность

### Защита API Ключей

```bash
# НИКОГДА не коммитьте .env файл
echo ".env" >> .gitignore

# Используйте переменные окружения
export BOT_TOKEN="..."
export GEMINI_API_KEY="..."
```

### Валидация Платежей

```python
# В ton_integration.py реализована:
- Проверка подписи транзакции
- Верификация отправителя
- Защита от двойной траты
```

### Rate Limiting

```python
# Добавьте ограничения:
from telegram.ext import CommandHandler

# Максимум 10 раскладов в час
user_limits = {}

async def check_rate_limit(user_id):
    if user_id in user_limits:
        count, timestamp = user_limits[user_id]
        if timestamp > datetime.now() - timedelta(hours=1):
            if count >= 10:
                return False
            user_limits[user_id] = (count + 1, timestamp)
        else:
            user_limits[user_id] = (1, datetime.now())
    else:
        user_limits[user_id] = (1, datetime.now())
    return True
```

---

## 🐛 Troubleshooting

### Бот не отвечает

```bash
# Проверьте логи
tail -f bot.log

# Проверьте токен
python -c "print(open('.env').read())"

# Проверьте подключение
curl https://api.telegram.org/bot<TOKEN>/getMe
```

### TON платежи не работают

```bash
# Проверьте pytoniq
pip install --upgrade pytoniq pytoniq-core

# Проверьте подключение к сети
python -c "from pytoniq import LiteClient; import asyncio; asyncio.run(LiteClient.from_mainnet_config(ls_i=0).connect())"

# Проверьте адрес кошелька
# Должен начинаться с UQ или EQ
```

### Mini App не открывается

1. Проверьте `WEBAPP_URL` в `.env`
2. Убедитесь что `miniapp.html` доступен по URL
3. Проверьте CORS настройки хостинга
4. Откройте DevTools в Telegram Desktop

### MongoDB ошибки

```bash
# Проверьте подключение
mongo mongodb://localhost:27017

# Создайте базу данных
use oracle_luck_bot
db.createCollection("users")

# Проверьте права
db.users.insertOne({test: "data"})
```

---

## 📈 Roadmap

### v1.0 (Текущая) ✅
- ✅ Основной функционал бота
- ✅ 10 типов раскладов
- ✅ TON Web3 интеграция
- ✅ Mini App
- ✅ Ежедневные уведомления

### v1.1 (Ближайшие 2 недели)
- [ ] Реальная AI интерпретация (Gemini)
- [ ] MongoDB интеграция
- [ ] Полная история раскладов
- [ ] Система достижений

### v1.2 (Месяц)
- [ ] Подписки и абонементы
- [ ] Реферальная программа
- [ ] Персонализированные рекомендации
- [ ] Экспорт раскладов в PDF

### v2.0 (3-6 месяцев)
- [ ] NFT карты Таро
- [ ] Marketplace предсказаний
- [ ] Социальные функции
- [ ] Мобильное приложение

---

## 🤝 Вклад и Поддержка

### Как помочь проекту

1. **⭐ Star на GitHub**
2. **🐛 Сообщить об ошибке** - создайте Issue
3. **💡 Предложить идею** - обсудим в Discussions
4. **🔧 Контрибьют** - создайте Pull Request

### Контакты

- **Telegram:** @OracleLuck_Bot
- **Support:** @your_support_contact
- **Email:** support@oracleluck.com

### Лицензия

MIT License - свободное использование с указанием автора

---

## 🙏 Благодарности

- **Telegram** - За отличный Bot API и Mini Apps
- **TON Foundation** - За TON blockchain
- **Google** - За Gemini AI
- **Open Source Community** - За библиотеки и инструменты

---

## 📄 Дополнительные Ресурсы

### Документация

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- [TON Documentation](https://docs.ton.org)
- [Gemini AI](https://ai.google.dev/docs)

### Полезные Ссылки

- [TON Connect](https://docs.ton.org/develop/dapps/ton-connect/overview)
- [Python Telegram Bot](https://docs.python-telegram-bot.org)
- [Pytoniq](https://github.com/yungwine/pytoniq)

### Примеры

- [TON Payment Bot](https://github.com/ton-blockchain/payment-bot)
- [Mini App Example](https://github.com/telegram/webapp-bot-example)

---

**Создано с ✨ и 🔮 мистической энергией**

_"Карты никогда не лгут. Они показывают правду, которую ты готов увидеть."_

© 2025 Oracle Luck Bot. All rights reserved.
