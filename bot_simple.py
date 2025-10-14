#!/usr/bin/env python3
"""
🔮 Oracle Luck Bot - Упрощенная Рабочая Версия
@OracleLuck_Bot

Быстрый старт без сложных зависимостей
"""

import asyncio
import logging
import random
from datetime import datetime
from typing import List, Dict

# Простая проверка установки библиотек
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
    from telegram.constants import ParseMode
except ImportError:
    print("❌ Библиотека python-telegram-bot не установлена!")
    print("Установите: pip install python-telegram-bot")
    exit(1)

# Конфигурация
BOT_TOKEN = "8294883971:AAG2hefSYbh-idoL_xhAeMhfZCvzARWFAls"
WEBAPP_URL = "https://your-mini-app-url.com"  # Обновите после деплоя

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# База данных (в памяти)
users_db = {}

# ==================== ДАННЫЕ ====================

# Упрощенные карты Таро (22 Старших Аркана)
TAROT_CARDS = [
    {"name": "Дурак", "emoji": "🃏", "keywords": "новые начинания, свобода"},
    {"name": "Маг", "emoji": "🎩", "keywords": "мастерство, сила воли"},
    {"name": "Верховная Жрица", "emoji": "👸", "keywords": "интуиция, тайны"},
    {"name": "Императрица", "emoji": "👑", "keywords": "плодородие, изобилие"},
    {"name": "Император", "emoji": "🤴", "keywords": "авторитет, структура"},
    {"name": "Иерофант", "emoji": "⛪", "keywords": "традиции, духовность"},
    {"name": "Влюбленные", "emoji": "💑", "keywords": "любовь, выбор"},
    {"name": "Колесница", "emoji": "🏇", "keywords": "победа, контроль"},
    {"name": "Сила", "emoji": "💪", "keywords": "храбрость, терпение"},
    {"name": "Отшельник", "emoji": "🧙", "keywords": "мудрость, поиск"},
    {"name": "Колесо Фортуны", "emoji": "🎡", "keywords": "судьба, изменения"},
    {"name": "Справедливость", "emoji": "⚖️", "keywords": "честность, правда"},
    {"name": "Повешенный", "emoji": "🙃", "keywords": "жертва, новый взгляд"},
    {"name": "Смерть", "emoji": "💀", "keywords": "трансформация, конец"},
    {"name": "Умеренность", "emoji": "🧘", "keywords": "баланс, терпение"},
    {"name": "Дьявол", "emoji": "😈", "keywords": "зависимость, искушение"},
    {"name": "Башня", "emoji": "🏰", "keywords": "разрушение, откровение"},
    {"name": "Звезда", "emoji": "⭐", "keywords": "надежда, вдохновение"},
    {"name": "Луна", "emoji": "🌙", "keywords": "иллюзия, страхи"},
    {"name": "Солнце", "emoji": "☀️", "keywords": "радость, успех"},
    {"name": "Суд", "emoji": "📯", "keywords": "возрождение, прощение"},
    {"name": "Мир", "emoji": "🌍", "keywords": "завершение, целостность"},
]

# Предсказания
PREDICTIONS = [
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
]

# Типы раскладов (упрощенные)
SPREADS = [
    {"id": "daily", "name": "🎴 Карта дня", "cards": 1, "free": True},
    {"id": "three", "name": "🔮 Три карты", "cards": 3, "free": True},
    {"id": "love", "name": "💕 Отношения", "cards": 5, "free": True},
    {"id": "career", "name": "💼 Карьера", "cards": 5, "free": True},
    {"id": "advice", "name": "🌟 Совет дня", "cards": 3, "free": True},
]

# ==================== ФУНКЦИИ ====================

def get_random_cards(count: int) -> List[Dict]:
    """Получить случайные карты"""
    return random.sample(TAROT_CARDS, min(count, len(TAROT_CARDS)))

def format_card(card: Dict) -> str:
    """Форматировать карту"""
    return f"{card['emoji']} **{card['name']}**\n_{card['keywords']}_"

def get_interpretation() -> str:
    """Получить интерпретацию"""
    return random.choice([
        "🔮 Карты указывают на период важных перемен в твоей жизни.",
        "✨ Энергия этих карт говорит о необходимости довериться интуиции.",
        "💫 Расклад показывает, что ты на правильном пути.",
        "🌟 Вселенная поддерживает твои начинания сейчас.",
        "🎯 Время действовать - благоприятный момент для решительных шагов.",
    ])

# ==================== КЛАВИАТУРЫ ====================

def get_main_keyboard():
    """Главное меню"""
    keyboard = [
        [
            InlineKeyboardButton("🎴 Получить расклад", callback_data="spreads"),
            InlineKeyboardButton("🔮 Карта дня", callback_data="daily")
        ],
        [
            InlineKeyboardButton("📚 История", callback_data="history"),
            InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_spreads_keyboard():
    """Меню раскладов"""
    keyboard = []
    for spread in SPREADS:
        keyboard.append([
            InlineKeyboardButton(f"{spread['name']} ({spread['cards']} карт)", 
                               callback_data=f"spread_{spread['id']}")
        ])
    keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

# ==================== КОМАНДЫ ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    user_id = user.id
    
    # Инициализация пользователя
    if user_id not in users_db:
        users_db[user_id] = {
            "readings": [],
            "username": user.first_name
        }
    
    welcome_text = f"""
🔮 **Добро пожаловать в Храм Судьбы, {user.first_name}!**

Я — **Оракул Удачи**, хранитель древних тайн Таро.

✨ **Что я могу:**

🎴 **5 типов раскладов** (все бесплатно!)
   • Карта дня (1 карта)
   • Три карты (3 карты)
   • Отношения (5 карт)
   • Карьера (5 карт)
   • Совет дня (3 карты)

🔮 **22 карты Таро**
   • Старшие Арканы
   • Мистические предсказания

📚 **История раскладов**
   • Сохранение всех раскладов

Начни свое путешествие в мир мистики! ✨
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )
    logger.info(f"Пользователь {user_id} ({user.first_name}) запустил бота")

async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /daily"""
    user_id = update.effective_user.id
    
    # Проверка на сегодня
    today = datetime.now().date()
    if user_id in users_db:
        last_daily = users_db[user_id].get("last_daily")
        if last_daily == today:
            await update.message.reply_text(
                "🎴 Ты уже получил карту дня сегодня!\n\n"
                "Попробуй другие расклады. ✨",
                reply_markup=get_main_keyboard()
            )
            return
    
    # Получаем карту
    card = random.choice(TAROT_CARDS)
    prediction = random.choice(PREDICTIONS)
    
    # Сохраняем
    if user_id not in users_db:
        users_db[user_id] = {"readings": []}
    users_db[user_id]["last_daily"] = today
    
    card_text = f"""
🎴 **КАРТА ДНЯ**
━━━━━━━━━━━━━━━

{format_card(card)}

**🔮 Предсказание:**
{prediction}

**✨ Толкование:**
{get_interpretation()}

━━━━━━━━━━━━━━━
_Пусть эта карта освещает твой путь!_ 💫
    """
    
    # Сохраняем в историю
    users_db[user_id]["readings"].append({
        "type": "daily",
        "date": datetime.now().isoformat(),
        "card": card["name"]
    })
    
    await update.message.reply_text(
        card_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )
    logger.info(f"Пользователь {user_id} получил карту дня: {card['name']}")

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /history"""
    user_id = update.effective_user.id
    
    if user_id not in users_db or not users_db[user_id]["readings"]:
        await update.message.reply_text(
            "📚 У тебя пока нет раскладов.\n\n"
            "Получи свою первую карту дня! 🔮",
            reply_markup=get_main_keyboard()
        )
        return
    
    readings = users_db[user_id]["readings"][-10:]
    
    history_text = "📚 **ИСТОРИЯ РАСКЛАДОВ**\n━━━━━━━━━━━━━━━\n\n"
    
    for i, reading in enumerate(reversed(readings), 1):
        date = datetime.fromisoformat(reading["date"]).strftime("%d.%m.%Y %H:%M")
        history_text += f"{i}. {reading['type'].upper()}\n   📅 {date}\n\n"
    
    await update.message.reply_text(
        history_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    help_text = """
ℹ️ **СПРАВКА**
━━━━━━━━━━━━━━━

**Команды:**
/start - Начать работу
/daily - Карта дня
/history - История раскладов
/help - Эта справка

**Как получить расклад:**
1. Нажми "🎴 Получить расклад"
2. Выбери тип расклада
3. Получи карты и толкование

**Типы раскладов:**
🎴 Карта дня - 1 карта
🔮 Три карты - 3 карты
💕 Отношения - 5 карт
💼 Карьера - 5 карт
🌟 Совет дня - 3 карты

Все расклады бесплатны! ✨
    """
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard()
    )

# ==================== ОБРАБОТЧИК КНОПОК ====================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    # Главное меню
    if data == "main":
        await query.edit_message_text(
            "🔮 **Храм Судьбы**\n\nВыбери действие:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
    
    # Меню раскладов
    elif data == "spreads":
        await query.edit_message_text(
            "🎴 **ВЫБЕРИ ТИП РАСКЛАДА**\n━━━━━━━━━━━━━━━\n\n"
            "Все расклады бесплатны! 🎁",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_spreads_keyboard()
        )
    
    # Карта дня
    elif data == "daily":
        today = datetime.now().date()
        if user_id in users_db:
            last_daily = users_db[user_id].get("last_daily")
            if last_daily == today:
                await query.edit_message_text(
                    "🎴 Ты уже получил карту дня сегодня!\n\n"
                    "Возвращайся завтра. ✨",
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=get_main_keyboard()
                )
                return
        
        card = random.choice(TAROT_CARDS)
        prediction = random.choice(PREDICTIONS)
        
        if user_id not in users_db:
            users_db[user_id] = {"readings": []}
        users_db[user_id]["last_daily"] = today
        
        card_text = f"""
🎴 **КАРТА ДНЯ**
━━━━━━━━━━━━━━━

{format_card(card)}

**🔮 Предсказание:**
{prediction}

**✨ Толкование:**
{get_interpretation()}

━━━━━━━━━━━━━━━
_Пусть эта карта освещает твой путь!_ 💫
        """
        
        users_db[user_id]["readings"].append({
            "type": "daily",
            "date": datetime.now().isoformat(),
            "card": card["name"]
        })
        
        await query.edit_message_text(
            card_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard()
        )
        logger.info(f"Пользователь {user_id} получил карту дня через кнопку")
    
    # Конкретный расклад
    elif data.startswith("spread_"):
        spread_id = data.replace("spread_", "")
        spread = next((s for s in SPREADS if s["id"] == spread_id), None)
        
        if not spread:
            await query.answer("Расклад не найден", show_alert=True)
            return
        
        # Получаем карты
        cards = get_random_cards(spread["cards"])
        
        # Формируем текст
        reading_text = f"""
✨ **{spread['name'].upper()}**
━━━━━━━━━━━━━━━

**Карт:** {spread['cards']}

**🎴 КАРТЫ:**

"""
        
        for i, card in enumerate(cards, 1):
            reading_text += f"{i}. {format_card(card)}\n\n"
        
        reading_text += f"""
**🔮 ТОЛКОВАНИЕ:**
{get_interpretation()}

━━━━━━━━━━━━━━━
_Пусть карты укажут тебе путь!_ 💫
        """
        
        # Сохраняем
        if user_id not in users_db:
            users_db[user_id] = {"readings": []}
        
        users_db[user_id]["readings"].append({
            "type": spread_id,
            "date": datetime.now().isoformat(),
            "cards": [c["name"] for c in cards]
        })
        
        await query.edit_message_text(
            reading_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Новый расклад", callback_data="spreads")],
                [InlineKeyboardButton("◀️ Главное меню", callback_data="main")]
            ])
        )
        logger.info(f"Пользователь {user_id} получил расклад: {spread_id}")
    
    # История
    elif data == "history":
        if user_id not in users_db or not users_db[user_id]["readings"]:
            await query.edit_message_text(
                "📚 У тебя пока нет раскладов.\n\n"
                "Получи свою первую карту дня! 🔮",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard()
            )
            return
        
        readings = users_db[user_id]["readings"][-10:]
        
        history_text = "📚 **ИСТОРИЯ РАСКЛАДОВ**\n━━━━━━━━━━━━━━━\n\n"
        
        for i, reading in enumerate(reversed(readings), 1):
            date = datetime.fromisoformat(reading["date"]).strftime("%d.%m.%Y %H:%M")
            history_text += f"{i}. {reading['type'].upper()}\n   📅 {date}\n\n"
        
        await query.edit_message_text(
            history_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ Назад", callback_data="main")]
            ])
        )
    
    # Помощь
    elif data == "help":
        help_text = """
ℹ️ **СПРАВКА**
━━━━━━━━━━━━━━━

**Команды:**
/start - Начать
/daily - Карта дня
/history - История
/help - Справка

**Расклады:**
🎴 Карта дня (1 карта)
🔮 Три карты (3 карты)
💕 Отношения (5 карт)
💼 Карьера (5 карт)
🌟 Совет дня (3 карты)

Все бесплатно! ✨
        """
        
        await query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("◀️ Назад", callback_data="main")]
            ])
        )

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

async def main():
    """Запуск бота"""
    logger.info("🔮 Oracle Luck Bot запускается...")
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Регистрируем команды
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("daily", daily_command))
        application.add_handler(CommandHandler("history", history_command))
        application.add_handler(CommandHandler("help", help_command))
        
        # Регистрируем обработчик кнопок
        application.add_handler(CallbackQueryHandler(button_callback))
        
        logger.info("✅ Бот успешно запущен!")
        logger.info(f"🤖 Username: @OracleLuck_Bot")
        logger.info("Ожидание сообщений...")
        
        # Запускаем бота
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
