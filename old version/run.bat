@echo off
REM AI Tutoring Bot - Ishga Tushirish Scripti (Windows)

echo ╔═══════════════════════════════════════════════════╗
echo ║   🤖 AI Tutoring Bot - ML Teacher                ║
echo ║   Starting the application...                    ║
echo ╚═══════════════════════════════════════════════════╝
echo.

REM Virtual environment borligini tekshirish
if not exist "venv\" (
    echo 📦 Virtual environment topilmadi. Yaratilmoqda...
    python -m venv venv
    echo ✅ Virtual environment yaratildi!
    echo.
)

REM Virtual environment faollashtirish
echo 🔄 Virtual environment faollashtirilmoqda...
call venv\Scripts\activate.bat

REM Dependency'larni tekshirish
echo 📋 Dependency'lar tekshirilmoqda...
pip install -q -r requirements.txt

echo.
echo ✅ Barcha tayyor!
echo 🚀 Server ishga tushirilmoqda...
echo.

REM Serverni ishga tushirish
python app.py

pause
