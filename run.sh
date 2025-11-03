#!/bin/bash

# AI Tutoring Bot - Ishga Tushirish Scripti (Linux/Mac)

echo "╔═══════════════════════════════════════════════════╗"
echo "║   🤖 AI Tutoring Bot - ML Teacher                ║"
echo "║   Starting the application...                    ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Virtual environment borligini tekshirish
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment topilmadi. Yaratilmoqda..."
    python3 -m venv venv
    echo "✅ Virtual environment yaratildi!"
    echo ""
fi

# Virtual environment faollashtirish
echo "🔄 Virtual environment faollashtirilmoqda..."
source venv/bin/activate

# Dependency'larni tekshirish
echo "📋 Dependency'lar tekshirilmoqda..."
pip install -q -r requirements.txt

echo ""
echo "✅ Barcha tayyor!"
echo "🚀 Server ishga tushirilmoqda..."
echo ""

# Serverni ishga tushirish
python app.py
