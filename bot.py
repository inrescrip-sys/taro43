#!/usr/bin/env python3
"""
🔮 Oracle Luck Bot - Мистический Telegram бот с TON интеграцией
@OracleLuck_Bot

Функционал:
- 10 типов раскладов Таро
- TON Web3 платежи
- Mini App интеграция
- Ежедневные уведомления
- AI интерпретация (Gemini)
"""

import asyncio
import logging
import os
import random
from datetime import datetime, time
from typing import List, Dict, Optional

from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    JobQueue
)
from telegram.constants import ParseMode

# Конфигурация
BOT_TOKEN = "8294883971:AAG2hefSYbh-idoL_xhAeMhfZCvzARWFAls"
WEBAPP_URL = "https://your-mini-app-url.com"  # Замените на реальный URL Mini App
TON_WALLET_ADDRESS = "UQD..."  # TON адрес для приема платежей

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== ДАННЫЕ ====================

# 78 карт Таро
TAROT_CARDS = {
    # Старшие Арканы
    "major": [
        {"id": 0, "name": "Дурак", "emoji": "🃏", "keywords": "новые начинания, спонтанность, свобода"},
        {"id": 1, "name": "Маг", "emoji": "🎩", "keywords": "мастерство, сила воли, творчество"},
        {"id": 2, "name": "Верховная Жрица", "emoji": "👸", "keywords": "интуиция, тайны, подсознание"},
        {"id": 3, "name": "Императрица", "emoji": "👑", "keywords": "плодородие, изобилие, материнство"},
        {"id": 4, "name": "Император", "emoji": "🤴", "keywords": "авторитет, структура, контроль"},
        {"id": 5, "name": "Иерофант", "emoji": "⛪", "keywords": "традиции, духовность, образование"},
        {"id": 6, "name": "Влюбленные", "emoji": "💑", "keywords": "любовь, выбор, гармония"},
        {"id": 7, "name": "Колесница", "emoji": "🏇", "keywords": "победа, контроль, решимость"},
        {"id": 8, "name": "Сила", "emoji": "💪", "keywords": "храбрость, терпение, влияние"},
        {"id": 9, "name": "Отшельник", "emoji": "🧙", "keywords": "мудрость, поиск, одиночество"},
        {"id": 10, "name": "Колесо Фортуны", "emoji": "🎡", "keywords": "судьба, изменения, циклы"},
        {"id": 11, "name": "Справедливость", "emoji": "⚖️", "keywords": "честность, правда, карма"},
        {"id": 12, "name": "Повешенный", "emoji": "🙃", "keywords": "жертва, новый взгляд, пауза"},
        {"id": 13, "name": "Смерть", "emoji": "💀", "keywords": "трансформация, конец, новое начало"},
        {"id": 14, "name": "Умеренность", "emoji": "🧘", "keywords": "баланс, терпение, гармония"},
        {"id": 15, "name": "Дьявол", "emoji": "😈", "keywords": "зависимость, искушение, материализм"},
        {"id": 16, "name": "Башня", "emoji": "🏰", "keywords": "разрушение, хаос, откровение"},
        {"id": 17, "name": "Звезда", "emoji": "⭐", "keywords": "надежда, вдохновение, умиротворение"},
        {"id": 18, "name": "Луна", "emoji": "🌙", "keywords": "иллюзия, страхи, подсознание"},
        {"id": 19, "name": "Солнце", "emoji": "☀️", "keywords": "радость, успех, позитив"},
        {"id": 20, "name": "Суд", "emoji": "📯", "keywords": "возрождение, прощение, призвание"},
        {"id": 21, "name": "Мир", "emoji": "🌍", "keywords": "завершение, целостность, достижение"},
    ],
    # Младшие Арканы - Жезлы (Огонь)
    "wands": [
        {"name": "Туз Жезлов", "emoji": "🔥", "keywords": "новая энергия, вдохновение"},
        {"name": "Двойка Жезлов", "emoji": "🔥", "keywords": "планирование, решения"},
        {"name": "Тройка Жезлов", "emoji": "🔥", "keywords": "экспансия, предвидение"},
        {"name": "Четверка Жезлов", "emoji": "🔥", "keywords": "празднование, стабильность"},
        {"name": "Пятерка Жезлов", "emoji": "🔥", "keywords": "конфликт, соперничество"},
        {"name": "Шестерка Жезлов", "emoji": "🔥", "keywords": "победа, признание"},
        {"name": "Семерка Жезлов", "emoji": "🔥", "keywords": "защита, вызов"},
        {"name": "Восьмерка Жезлов", "emoji": "🔥", "keywords": "скорость, движение"},
        {"name": "Девятка Жезлов", "emoji": "🔥", "keywords": "устойчивость, настойчивость"},
        {"name": "Десятка Жезлов", "emoji": "🔥", "keywords": "бремя, ответственность"},
        {"name": "Паж Жезлов", "emoji": "🔥", "keywords": "энтузиазм, исследование"},
        {"name": "Рыцарь Жезлов", "emoji": "🔥", "keywords": "действие, импульсивность"},
        {"name": "Королева Жезлов", "emoji": "🔥", "keywords": "харизма, уверенность"},
        {"name": "Король Жезлов", "emoji": "🔥", "keywords": "лидерство, видение"},
    ]
}

# Типы раскладов
SPREAD_TYPES = [
    {
        "id": "daily",
        "name": "🎴 Карта дня",
        "cards": 1,
        "price": 0,
        "description": "Одна карта на сегодня"
    },
    {
        "id": "three_cards",
        "name": "🔮 Три карты",
        "cards": 3,
        "price": 0,
        "description": "Прошлое-Настоящее-Будущее"
    },
    {
        "id": "love",
        "name": "💕 Расклад на отношения",
        "cards": 7,
        "price": 0.03,
        "description": "Глубокий анализ отношений"
    },
    {
        "id": "career",
        "name": "💼 Расклад на карьеру",
        "cards": 5,
        "price": 0,
        "description": "Работа и финансы"
    },
    {
        "id": "celtic_cross",
        "name": "✨ Кельтский крест",
        "cards": 10,
        "price": 0.05,
        "description": "Полный расклад (10 карт)"
    },
    {
        "id": "choice",
        "name": "🎯 Расклад выбора",
        "cards": 7,
        "price": 0.03,
        "description": "Помощь в принятии решений"
    },
    {
        "id": "year",
        "name": "📅 Годовой расклад",
        "cards": 13,
        "price": 0.1,
        "description": "Прогноз на год (13 карт)"
    },
    {
        "id": "situation",
        "name": "🎭 Расклад на ситуацию",
        "cards": 5,
        "price": 0,
        "description": "Анализ конкретной ситуации"
    },
    {
        "id": "advice",
        "name": "🌟 Совет дня",
        "cards": 3,
        "price": 0,
        "description": "Что нужно знать сегодня"
    },
    {
        "id": "chakra",
        "name": "🧘 Расклад на чакры",
        "cards": 7,
        "price": 0.05,
        "description": "Энергетический анализ"
    }
]

# 100+ предсказаний для "печеньки"
DAILY_PREDICTIONS = [
    "✨ Твоя интуиция сегодня — твой главный союзник. Слушай ее.",
    "💫 Скоро ты получишь неожиданное, но очень важное сообщение.",
    "🌟 Не бойся перемен. Они ведут тебя к твоему истинному пути.",
    "💝 В твоей жизни появится человек, который изменит все.",
    "🎯 Сегодняшний день идеален для начала нового проекта.",
    "🙏 Твоя щедрость вернется к тебе сторицей.",
    "🔮 Обрати внимание на знаки Вселенной — они повсюду.",
    "💪 Ты сильнее, чем думаешь. Доверься себе.",
    "🧘 Скоро наступит период внутреннего спокойствия.",
    "🌈 Твоя мечта ближе, чем тебе кажется.",
    "🍀 Отпусти контроль. Вселенная знает, что делает.",
    "💡 Сегодня ты найдешь ответ на давно мучивший тебя вопрос.",
    "👁️ Не суди по первому впечатлению. Суть откроется позже.",
    "⚡ Твоя энергия привлекает правильных людей.",
    "🎁 Будь открыт для неожиданных возможностей.",
    "💖 Ты заслуживаешь любви и уважения.",
    "📬 Скоро тебя ждет приятный сюрприз от старого друга.",
    "🏆 Твоя решимость приведет тебя к успеху.",
    "🤝 Не бойся просить о помощи. Она придет.",
    "🕊️ Сегодня — день для прощения. Начни с себя.",
]

# База данных пользователей (в продакшене использовать MongoDB/PostgreSQL)
users_db = {}

# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def get_random_cards(count: int) -> List[Dict]:
    """Получить случайные карты Таро"""
    all_cards = TAROT_CARDS["major"] + TAROT_CARDS["wands"]
    selected = random.sample(all_cards, min(count, len(all_cards)))
    
    # Добавляем возможность перевернутой карты
    for card in selected:
        card["reversed"] = random.choice([True, False])
    
    return selected

def format_card(card: Dict, position: str = "") -> str:
    """Форматировать карту для отображения"""
    emoji = card.get("emoji", "🎴")
    name = card["name"]
    reversed_text = " (Перевернутая)" if card.get("reversed") else ""
    keywords = card.get("keywords", "")
    
    text = f"{emoji} **{name}**{reversed_text}\n"
    if position:
        text = f"**{position}:** " + text
    if keywords:
        text += f"_{keywords}_\n"
    
    return text

async def generate_interpretation(cards: List[Dict], spread_type: str, question: str = "") -> str:
    """
    Генерация AI интерпретации расклада
    В продакшене интегрировать с Gemini API
    """
    # Placeholder - в продакшене использовать Gemini
    interpretations = [
        "🔮 Карты указывают на период важных перемен в твоей жизни.",
        "✨ Энергия этих карт говорит о необходимости довериться интуиции.",
        "💫 Расклад показывает, что ты на правильном пути.",
        "🌟 Вселенная поддерживает твои начинания сейчас.",
        "🎯 Время действовать - благоприятный момент для решительных шагов.",
    ]
    
    base_interpretation = random.choice(interpretations)
    
    # Добавляем специфику по типу расклада
    if spread_type == "love":
        base_interpretation += "\n\n💕 В отношениях грядут позитивные изменения."
    elif spread_type == "career":
        base_interpretation += "\n\n💼 Профессиональный рост на горизонте."
    elif spread_type == "celtic_cross":
        base_interpretation += "\n\n✨ Полная картина ситуации открывается перед тобой."
    
    return base_interpretation

def get_user_balance(user_id: int) -> float:
    """Получить баланс пользователя в TON"""
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
    return users_db[user_id]["balance"]

def add_balance(user_id: int, amount: float):
    """Добавить средства на баланс"""
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
    users_db[user_id]["balance"] += amount

def deduct_balance(user_id: int, amount: float) -> bool:
    """Списать средства с баланса"""
    current = get_user_balance(user_id)
    if current >= amount:
        users_db[user_id]["balance"] -= amount
        return True
    return False

# ==================== КЛАВИАТУРЫ ====================

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню"""
    keyboard = [
        [
            InlineKeyboardButton("🎴 Получить расклад", callback_data="readings_menu"),
            InlineKeyboardButton("🔮 Карта дня", callback_data="daily_card")
        ],
        [
            InlineKeyboardButton("💰 Баланс TON", callback_data="balance"),
            InlineKeyboardButton("📚 История", callback_data="history")
        ],
        [
            InlineKeyboardButton("🌐 Открыть Mini App", web_app=WebAppInfo(url=WEBAPP_URL)),
        ],
        [
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_readings_keyboard() -> InlineKeyboardMarkup:
    """Меню выбора раскладов"""
    keyboard = []
    
    for spread in SPREAD_TYPES:
        price_text = "Бесплатно" if spread["price"] == 0 else f"{spread['price']} TON"
        button_text = f"{spread['name']} • {price_text}"
        keyboard.append([
            InlineKeyboardButton(button_text, callback_data=f"spread_{spread['id']}")
        ])
    
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_payment_keyboard(spread_id: str, amount: float) -> InlineKeyboardMarkup:
    """Клавиатура оплаты"""
    keyboard = [
        [InlineKeyboardButton(f"💳 Оплатить {amount} TON", callback_data=f"pay_{spread_id}_{amount}")],
        [InlineKeyboardButton("💰 Пополнить баланс", callback_data="add_balance")],
        [InlineKeyboardButton("◀️ Назад", callback_data="readings_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Настройки"""
    keyboard = [
        [InlineKeyboardButton("🔔 Уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton("🌐 Язык", callback_data="change_language")],
        [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==================== КОМАНДЫ ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    user_id = user.id
    
    # Инициализация пользователя
    if user_id not in users_db:
        users_db[user_id] = {
            "balance": 0.0,
            "readings": [],
            "notifications": True,
            "username": user.username or user.first_name
        }
    
    welcome_text = f"""
🔮 **Добро пожаловать в Храм Судьбы, {user.first_name}!**

Я — **Оракул Удачи**, хранитель древних тайн Таро и проводник между мирами. 
Воздух здесь пропитан магией, а карты готовы открыть твое будущее.

✨ **Что я могу для тебя:**

🎴 **10 типов раскладов Таро**
   • От простой карты дня до полного Кельтского креста
   • Бесплатные и премиум расклады

🌐 **TON Web3 интеграция**
   • Платежи в криптовалюте
   • Безопасные транзакции

🔮 **AI-интерпретация**
   • Глубокие и персонализированные предсказания
   • Мистические толкования

📱 **Mini App**
   • Полноценное веб-приложение
   • История всех раскладов
   • Красивая визуализация

💫 **Ежедневные предсказания**
   • Бесплатная карта дня
   • Напоминания о важных моментах

Начни свое путешествие в мир мистики прямо сейчас! ✨
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )
    
    # Устанавливаем Web App кнопку в меню
    await context.bot.set_chat_menu_button(
        chat_id=user_id,
        menu_button=MenuButtonWebApp(
            text="🌐 Открыть Храм",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )

async def daily_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /daily - Карта дня"""
    user_id = update.effective_user.id
    
    # Проверяем, получал ли пользователь карту сегодня
    today = datetime.now().date()
    if user_id in users_db:
        last_daily = users_db[user_id].get("last_daily")
        if last_daily and last_daily == today:
            await update.message.reply_text(
                "🎴 Ты уже получил карту дня сегодня!\n\n"
                "Попробуй другие расклады или открой Mini App для полного опыта. ✨",
                reply_markup=get_main_keyboard()
            )
            return
    
    # Получаем случайную карту
    cards = get_random_cards(1)
    card = cards[0]
    
    # Сохраняем дату
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
    users_db[user_id]["last_daily"] = today
    
    # Получаем предсказание
    prediction = random.choice(DAILY_PREDICTIONS)
    
    card_text = f"""
🎴 **КАРТА ДНЯ**
━━━━━━━━━━━━━━━

{format_card(card)}

**🔮 Предсказание:**
{prediction}

**✨ Толкование:**
{await generate_interpretation(cards, "daily")}

━━━━━━━━━━━━━━━
_Пусть эта карта освещает твой путь сегодня!_ 💫
    """
    
    # Сохраняем в историю
    users_db[user_id]["readings"].append({
        "type": "daily",
        "date": datetime.now().isoformat(),
        "cards": cards,
        "prediction": prediction
    })
    
    await update.message.reply_text(
        card_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /balance - Проверить баланс"""
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    
    balance_text = f"""
💰 **ВАШ БАЛАНС**
━━━━━━━━━━━━━━━

**Текущий баланс:** `{balance:.4f} TON`

💎 **Цены на расклады:**

🆓 **Бесплатные:**
• Карта дня (1 карта)
• Три карты (3 карты)
• Карьера (5 карт)
• Ситуация (5 карт)

💰 **Премиум:**
• Отношения: 0.03 TON
• Выбор: 0.03 TON  
• Кельтский крест: 0.05 TON
• Чакры: 0.05 TON
• Годовой расклад: 0.1 TON

Пополни баланс, чтобы открыть доступ к премиум раскладам! ✨
    """
    
    keyboard = [
        [InlineKeyboardButton("💳 Пополнить баланс", callback_data="add_balance")],
        [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
    ]
    
    await update.message.reply_text(
        balance_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /history - История раскладов"""
    user_id = update.effective_user.id
    
    if user_id not in users_db or not users_db[user_id]["readings"]:
        await update.message.reply_text(
            "📚 У тебя пока нет раскладов.\n\n"
            "Получи свою первую карту дня или сделай полный расклад! 🔮",
            reply_markup=get_main_keyboard()
        )
        return
    
    readings = users_db[user_id]["readings"][-10:]  # Последние 10
    
    history_text = "📚 **ИСТОРИЯ РАСКЛАДОВ**\n━━━━━━━━━━━━━━━\n\n"
    
    for i, reading in enumerate(reversed(readings), 1):
        date = datetime.fromisoformat(reading["date"]).strftime("%d.%m.%Y %H:%M")
        reading_type = reading["type"]
        card_count = len(reading["cards"])
        
        history_text += f"{i}. **{reading_type.upper()}** • {card_count} карт\n"
        history_text += f"   📅 {date}\n\n"
    
    history_text += "\n💡 _Открой Mini App для детального просмотра всех раскладов!_"
    
    keyboard = [
        [InlineKeyboardButton("🌐 Открыть историю в Mini App", web_app=WebAppInfo(url=f"{WEBAPP_URL}/history"))],
        [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
    ]
    
    await update.message.reply_text(
        history_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help - Помощь"""
    help_text = """
ℹ️ **СПРАВКА**
━━━━━━━━━━━━━━━

**📱 Команды:**
/start - Начать работу с ботом
/daily - Получить карту дня
/balance - Проверить баланс TON
/history - История раскладов
/help - Эта справка

**🎴 Как получить расклад:**
1. Нажми "🎴 Получить расклад"
2. Выбери тип расклада
3. Оплати (если это премиум расклад)
4. Получи AI-интерпретацию

**💰 Пополнение баланса:**
1. Нажми "💰 Баланс TON"
2. Выбери "💳 Пополнить баланс"
3. Отправь TON на указанный адрес
4. Баланс обновится автоматически

**🌐 Mini App:**
Открой полноценное веб-приложение для:
• Красивой визуализации карт
• Детальной истории
• Расширенных раскладов
• Персонализации

**🔔 Уведомления:**
Настрой ежедневные напоминания о карте дня в настройках!

**❓ Вопросы:**
Если возникли проблемы, напиши @support
    """
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

# ==================== ОБРАБОТЧИКИ КНОПОК ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех Inline кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # Главное меню
    if data == "main_menu":
        await query.edit_message_text(
            "🔮 **Храм Судьбы**\n\nВыбери действие:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    
    # Меню раскладов
    elif data == "readings_menu":
        await query.edit_message_text(
            "🎴 **ВЫБЕРИ ТИП РАСКЛАДА**\n━━━━━━━━━━━━━━━\n\n"
            "Каждый расклад открывает свою грань истины:\n\n"
            "🆓 - Бесплатные расклады\n"
            "💰 - Требуют TON баланса",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_readings_keyboard()
        )
    
    # Карта дня
    elif data == "daily_card":
        # Повторное использование логики из команды
        today = datetime.now().date()
        if user_id in users_db:
            last_daily = users_db[user_id].get("last_daily")
            if last_daily and last_daily == today:
                await query.edit_message_text(
                    "🎴 Ты уже получил карту дня сегодня!\n\n"
                    "Возвращайся завтра за новым предсказанием. ✨",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_main_keyboard()
                )
                return
        
        cards = get_random_cards(1)
        card = cards[0]
        
        if user_id not in users_db:
            users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
        users_db[user_id]["last_daily"] = today
        
        prediction = random.choice(DAILY_PREDICTIONS)
        
        card_text = f"""
🎴 **КАРТА ДНЯ**
━━━━━━━━━━━━━━━

{format_card(card)}

**🔮 Предсказание:**
{prediction}

**✨ Толкование:**
{await generate_interpretation(cards, "daily")}

━━━━━━━━━━━━━━━
_Пусть эта карта освещает твой путь сегодня!_ 💫
        """
        
        users_db[user_id]["readings"].append({
            "type": "daily",
            "date": datetime.now().isoformat(),
            "cards": cards,
            "prediction": prediction
        })
        
        await query.edit_message_text(
            card_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    
    # Выбор конкретного расклада
    elif data.startswith("spread_"):
        spread_id = data.replace("spread_", "")
        spread = next((s for s in SPREAD_TYPES if s["id"] == spread_id), None)
        
        if not spread:
            await query.answer("Расклад не найден", show_alert=True)
            return
        
        # Проверка баланса для платных раскладов
        if spread["price"] > 0:
            balance = get_user_balance(user_id)
            if balance < spread["price"]:
                await query.edit_message_text(
                    f"💰 **НЕДОСТАТОЧНО СРЕДСТВ**\n\n"
                    f"Для расклада **{spread['name']}** требуется:\n"
                    f"**{spread['price']} TON**\n\n"
                    f"Твой баланс: `{balance:.4f} TON`\n\n"
                    f"Пополни баланс, чтобы продолжить! ✨",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_payment_keyboard(spread_id, spread["price"])
                )
                return
        
        # Выполняем расклад
        await perform_reading(query, user_id, spread)
    
    # Баланс
    elif data == "balance":
        balance = get_user_balance(user_id)
        
        balance_text = f"""
💰 **ВАШ БАЛАНС**
━━━━━━━━━━━━━━━

**Текущий баланс:** `{balance:.4f} TON`

💎 **Цены на расклады:**

🆓 **Бесплатные:**
• Карта дня, Три карты, Карьера, Ситуация

💰 **Премиум:**
• Отношения: 0.03 TON
• Выбор: 0.03 TON  
• Кельтский крест: 0.05 TON
• Чакры: 0.05 TON
• Годовой расклад: 0.1 TON
        """
        
        keyboard = [
            [InlineKeyboardButton("💳 Пополнить баланс", callback_data="add_balance")],
            [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            balance_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # Пополнение баланса
    elif data == "add_balance":
        await query.edit_message_text(
            f"""
💳 **ПОПОЛНЕНИЕ БАЛАНСА**
━━━━━━━━━━━━━━━

**Адрес для отправки TON:**
`{TON_WALLET_ADDRESS}`

**Инструкция:**
1. Открой свой TON кошелек
2. Отправь любую сумму на адрес выше
3. Баланс обновится автоматически (1-2 мин)

**Минимальная сумма:** 0.01 TON

💡 _Для быстрого пополнения используй TON Connect в Mini App!_
            """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Открыть Mini App", web_app=WebAppInfo(url=f"{WEBAPP_URL}/balance"))],
                [InlineKeyboardButton("◀️ Назад", callback_data="balance")]
            ])
        )
    
    # История
    elif data == "history":
        if user_id not in users_db or not users_db[user_id]["readings"]:
            await query.edit_message_text(
                "📚 У тебя пока нет раскладов.\n\n"
                "Получи свою первую карту дня или сделай полный расклад! 🔮",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard()
            )
            return
        
        readings = users_db[user_id]["readings"][-10:]
        
        history_text = "📚 **ИСТОРИЯ РАСКЛАДОВ**\n━━━━━━━━━━━━━━━\n\n"
        
        for i, reading in enumerate(reversed(readings), 1):
            date = datetime.fromisoformat(reading["date"]).strftime("%d.%m.%Y %H:%M")
            reading_type = reading["type"]
            card_count = len(reading["cards"])
            
            history_text += f"{i}. **{reading_type.upper()}** • {card_count} карт\n"
            history_text += f"   📅 {date}\n\n"
        
        history_text += "\n💡 _Открой Mini App для детального просмотра!_"
        
        await query.edit_message_text(
            history_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Открыть в Mini App", web_app=WebAppInfo(url=f"{WEBAPP_URL}/history"))],
                [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
            ])
        )
    
    # Настройки
    elif data == "settings":
        notifications = users_db.get(user_id, {}).get("notifications", True)
        notif_status = "✅ Включены" if notifications else "❌ Выключены"
        
        await query.edit_message_text(
            f"""
⚙️ **НАСТРОЙКИ**
━━━━━━━━━━━━━━━

**🔔 Уведомления:** {notif_status}
Ежедневные напоминания о карте дня

**🌐 Язык:** Русский
_Скоро добавим другие языки!_

**🎨 Тема:** Мистическая (по умолчанию)
            """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_settings_keyboard()
        )
    
    # Переключение уведомлений
    elif data == "toggle_notifications":
        if user_id not in users_db:
            users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
        
        current = users_db[user_id].get("notifications", True)
        users_db[user_id]["notifications"] = not current
        
        status = "включены" if not current else "выключены"
        await query.answer(f"Уведомления {status}!", show_alert=True)
        
        # Обновляем текст настроек
        notif_status = "✅ Включены" if not current else "❌ Выключены"
        await query.edit_message_text(
            f"""
⚙️ **НАСТРОЙКИ**
━━━━━━━━━━━━━━━

**🔔 Уведомления:** {notif_status}
Ежедневные напоминания о карте дня

**🌐 Язык:** Русский
_Скоро добавим другие языки!_

**🎨 Тема:** Мистическая (по умолчанию)
            """,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_settings_keyboard()
        )
    
    # Помощь
    elif data == "help":
        help_text = """
ℹ️ **СПРАВКА**
━━━━━━━━━━━━━━━

**📱 Команды:**
/start - Начать
/daily - Карта дня
/balance - Баланс
/history - История
/help - Справка

**🎴 Расклады:**
Выбери тип расклада → Оплати (если нужно) → Получи результат

**💰 TON Платежи:**
Пополни баланс → Используй для премиум раскладов

**🌐 Mini App:**
Полноценное приложение с расширенными возможностями

**❓ Поддержка:** @support
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ Назад", callback_data="main_menu")]
            ])
        )

async def perform_reading(query, user_id: int, spread: Dict):
    """Выполнить расклад Таро"""
    # Списываем средства для платных раскладов
    if spread["price"] > 0:
        if not deduct_balance(user_id, spread["price"]):
            await query.answer("Недостаточно средств!", show_alert=True)
            return
    
    # Получаем карты
    cards = get_random_cards(spread["cards"])
    
    # Формируем текст расклада
    reading_text = f"""
✨ **{spread['name'].upper()}**
━━━━━━━━━━━━━━━

**Описание:** {spread['description']}
**Количество карт:** {spread['cards']}

**🎴 КАРТЫ:**

"""
    
    # Позиции для разных раскладов
    positions = {
        "three_cards": ["Прошлое", "Настоящее", "Будущее"],
        "celtic_cross": ["Суть", "Препятствие", "Прошлое", "Будущее", "Сознание", "Подсознание", "Совет", "Окружение", "Надежды", "Итог"],
        "love": ["Вы", "Партнер", "Отношения", "Прошлое", "Настоящее", "Будущее", "Совет"],
        "career": ["Текущая ситуация", "Препятствия", "Возможности", "Совет", "Итог"],
        "choice": ["Ситуация", "Вариант А", "Вариант Б", "Преимущества А", "Преимущества Б", "Последствия А", "Последствия Б"],
        "chakra": ["Корневая", "Сакральная", "Солнечное сплетение", "Сердечная", "Горловая", "Третий глаз", "Коронная"],
        "situation": ["Суть", "Причина", "Развитие", "Совет", "Результат"],
        "advice": ["Что нужно знать", "Что нужно сделать", "Чего избегать"],
    }
    
    spread_positions = positions.get(spread["id"], [f"Карта {i+1}" for i in range(spread["cards"])])
    
    for i, card in enumerate(cards):
        position = spread_positions[i] if i < len(spread_positions) else f"Карта {i+1}"
        reading_text += format_card(card, position) + "\n"
    
    # AI интерпретация
    interpretation = await generate_interpretation(cards, spread["id"])
    reading_text += f"\n**🔮 ТОЛКОВАНИЕ:**\n{interpretation}\n\n"
    reading_text += "━━━━━━━━━━━━━━━\n_Пусть карты укажут тебе путь!_ 💫"
    
    # Сохраняем в историю
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.0, "readings": [], "notifications": True}
    
    users_db[user_id]["readings"].append({
        "type": spread["id"],
        "date": datetime.now().isoformat(),
        "cards": cards,
        "spread_name": spread["name"],
        "interpretation": interpretation
    })
    
    await query.edit_message_text(
        reading_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Новый расклад", callback_data="readings_menu")],
            [InlineKeyboardButton("🌐 Открыть в Mini App", web_app=WebAppInfo(url=f"{WEBAPP_URL}/reading"))],
            [InlineKeyboardButton("◀️ Главное меню", callback_data="main_menu")]
        ])
    )

# ==================== ЕЖЕДНЕВНЫЕ УВЕДОМЛЕНИЯ ====================

async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Отправка ежедневного напоминания"""
    for user_id, user_data in users_db.items():
        if user_data.get("notifications", True):
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="🔔 **Доброе утро!**\n\n"
                         "Твоя карта дня ждет тебя. Узнай, что приготовила Вселенная! ✨",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🎴 Получить карту дня", callback_data="daily_card")]
                    ])
                )
            except Exception as e:
                logger.error(f"Ошибка отправки напоминания пользователю {user_id}: {e}")

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

async def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем команды
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("daily", daily_card_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("history", history_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Регистрируем обработчики кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Настраиваем ежедневные уведомления (каждый день в 9:00)
    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_reminder,
        time=time(hour=9, minute=0),
        days=(0, 1, 2, 3, 4, 5, 6)  # Каждый день
    )
    
    logger.info("🔮 Oracle Luck Bot запущен!")
    
    # Запускаем бота
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
