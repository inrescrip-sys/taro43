#!/bin/bash
# Oracle Luck Bot - Скрипт быстрого запуска

echo "🔮 Oracle Luck Bot - Запуск..."
echo "================================"

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 не найден!${NC}"
    echo "Установите Python 3.10+: https://www.python.org/downloads/"
    exit 1
fi

echo -e "${GREEN}✅ Python найден: $(python3 --version)${NC}"

# Проверка .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Файл .env не найден!${NC}"
    echo "Создаю .env из примера..."
    cp .env.example .env 2>/dev/null || {
        echo "BOT_TOKEN=8294883971:AAG2hefSYbh-idoL_xhAeMhfZCvzARWFAls" > .env
        echo "WEBAPP_URL=https://your-mini-app.vercel.app" >> .env
        echo "TON_WALLET_ADDRESS=UQD..." >> .env
    }
    echo -e "${YELLOW}📝 Отредактируйте .env перед запуском!${NC}"
fi

# Проверка зависимостей
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Создание виртуального окружения...${NC}"
    python3 -m venv venv
fi

# Активация venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Установка зависимостей
echo -e "${YELLOW}📦 Установка зависимостей...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ошибка установки зависимостей!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Зависимости установлены${NC}"

# Проверка MongoDB
if command -v mongod &> /dev/null; then
    echo -e "${GREEN}✅ MongoDB установлен${NC}"
else
    echo -e "${YELLOW}⚠️  MongoDB не найден. Бот будет использовать локальное хранилище.${NC}"
fi

# Запуск бота
echo ""
echo -e "${GREEN}🚀 Запуск Oracle Luck Bot...${NC}"
echo "================================"
echo ""

python3 bot.py

# При завершении
echo ""
echo -e "${YELLOW}👋 Бот остановлен${NC}"
