# 🤖 AI Tutoring Bot - Machine Learning Teacher

Machine Learning va Python konseptlarini o'rgatuvchi interaktiv AI chatbot. Bu loyiha Flask web framework asosida yaratilgan va ML konseptlarini oddiy va tushunarli tarzda tushuntiradi.

## 📋 Mundarija

- [Imkoniyatlar](#-imkoniyatlar)
- [Texnologiyalar](#-texnologiyalar)
- [O'rnatish](#-ornatish)
- [Ishga Tushirish](#-ishga-tushirish)
- [Foydalanish](#-foydalanish)
- [Loyiha Strukturasi](#-loyiha-strukturasi)
- [API Endpoints](#-api-endpoints)
- [Muammolarni Hal Qilish](#-muammolarni-hal-qilish)

## ✨ Imkoniyatlar

### 🎓 Machine Learning Konseptlari
- **Supervised Learning** - nazorat ostidagi o'rganish
- **Unsupervised Learning** - nazorat ostida bo'lmagan o'rganish
- **Neural Networks** - neyron tarmoqlar
- **Regression** - regressiya modellari
- **Classification** - klassifikatsiya
- **Overfitting/Underfitting** - model muammolari
- **Feature Engineering** - xususiyatlar yaratish

### 💻 Python Darslari
- Python asoslari
- NumPy bilan ishlash
- Pandas ma'lumotlar tahlili
- Scikit-learn ML modellari

### 🎯 Interaktiv Xususiyatlar
- Real-time chat interface
- Kod misollar va tushuntirishlar
- Testlar va savol-javoblar
- Progress tracking
- Tavsiyalar tizimi

## 🛠 Texnologiyalar

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **NumPy** - Raqamlar bilan ishlash
- **Pandas** - Ma'lumotlar tahlili
- **Scikit-learn** - Machine Learning

### Frontend
- **HTML5/CSS3**
- **JavaScript (Vanilla)**
- **Font Awesome** - Ikonkalar
- **Google Fonts** - Shriftlar

## 📥 O'rnatish

### 1. Repository'ni Klonlash

```bash
# Git orqali
git clone <repository-url>
cd ai-tutoring-bot

# Yoki fayllarni yuklab oling
```

### 2. Virtual Environment Yaratish

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependency'larni O'rnatish

```bash
pip install -r requirements.txt
```

### 4. Environment Variables Sozlash (ixtiyoriy)

```bash
# .env.example faylini .env ga nusxalash
cp .env.example .env

# .env faylini tahrirlash
nano .env  # yoki boshqa text editor
```

## 🚀 Ishga Tushirish

### Development Rejimi

```bash
# Virtual environment faollashtirilgan bo'lishi kerak
python app.py
```

Server muvaffaqiyatli ishga tushgandan so'ng:
```
Server ishga tushdi!
URL: http://localhost:5000
```

Brauzerda `http://localhost:5000` manziliga o'ting.

### Production Rejimi (Gunicorn)

```bash
# Gunicorn o'rnatish
pip install gunicorn

# Serverni ishga tushirish
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📖 Foydalanish

### Boshlash

1. Brauzerda `http://localhost:5000` ochiladi
2. "Boshlash" tugmasini bosing
3. Salomlashish xabari keladi

### Mavzular O'rganish

**Sidebar'dan mavzu tanlash:**
- Supervised Learning
- Unsupervised Learning
- Neural Networks
- Regression
- Classification
- Python asoslari
- NumPy
- Pandas

**Yoki chatga yozing:**
```
"Supervised Learning nima?"
"Neural Network tushuntir"
"Python misoli"
"NumPy kod"
```

### Kod Misollarini Olish

```
"Misol ko'rsat"
"Kod misoli"
"Python kod"
```

### Testlar Olish

```
"Test ol"
"Savol ber"
"Quiz"
```

### Progressni Ko'rish

- Progress tugmasini bosing (header'da)
- Sizning o'rganilgan mavzularingiz
- Bajarilgan testlar
- To'g'ri javoblar statistikasi

### Chatni Qayta Boshlash

- Reset tugmasini bosing (header'da)
- Barcha progress o'chadi va yangi session boshlanadi

## 📁 Loyiha Strukturasi

```
ai-tutoring-bot/
│
├── app.py                 # Asosiy Flask ilova
├── bot_logic.py           # AI tutor mantiqiy qismi
├── ml_concepts.py         # ML konseptlari bazasi
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables namunasi
├── README.md             # Ushbu fayl
│
├── templates/
│   └── index.html        # Asosiy HTML sahifa
│
└── static/
    ├── css/
    │   └── style.css     # Dizayn (CSS)
    └── js/
        └── script.js     # Frontend logika (JavaScript)
```

## 🔌 API Endpoints

### 1. Chat Endpoint
**POST** `/api/chat`

Foydalanuvchi xabarini qabul qiladi va javob beradi.

**Request:**
```json
{
  "message": "Supervised Learning nima?",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "response": {
    "type": "concept",
    "message": "...",
    "suggestions": ["Misol ko'rsat", "Test ol"]
  },
  "timestamp": "2024-01-15T12:30:00"
}
```

### 2. Quiz Check Endpoint
**POST** `/api/quiz/check`

Test javobini tekshiradi.

**Request:**
```json
{
  "quiz": {...},
  "answer": "1",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "correct": true,
    "message": "✅ To'g'ri! Tushuntirish..."
  }
}
```

### 3. Progress Endpoint
**GET** `/api/progress?session_id=session_123`

Foydalanuvchi progressini qaytaradi.

**Response:**
```json
{
  "success": true,
  "progress": {
    "topics_learned": 5,
    "quizzes_completed": 10,
    "correct_answers": 8,
    "accuracy": 80.0
  }
}
```

### 4. Reset Endpoint
**POST** `/api/reset`

Sessionni qayta boshlaydi.

### 5. Health Check
**GET** `/api/health`

Server holatini tekshiradi.

## 🐛 Muammolarni Hal Qilish

### Port band bo'lsa

```bash
# Boshqa port'da ishlatish
python app.py --port 8000
```

Yoki `app.py` faylida `port` parametrini o'zgartiring:
```python
app.run(port=8000)
```

### Module topilmasa

```bash
# Barcha dependency'larni qayta o'rnatish
pip install -r requirements.txt --upgrade
```

### Virtual environment muammolari

```bash
# Virtual environment'ni o'chirish va qayta yaratish
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Qayta yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Dependency'larni o'rnatish
pip install -r requirements.txt
```

### CORS xatolari

Agar frontend va backend turli port'larda ishlasa, `app.py` faylida CORS sozlamalarini tekshiring:

```python
from flask_cors import CORS
CORS(app)  # Yoki specific origin
```

### JavaScript console xatolari

Brauzer Developer Tools'da (F12) console'ni tekshiring:
- Network tab'da API so'rovlarni ko'ring
- Console tab'da JavaScript xatolarni ko'ring

## 🔄 Yangilanishlar va Rivojlantirish

### Yangi Konsept Qo'shish

`ml_concepts.py` faylida `self.concepts` dictionary'ga yangi konsept qo'shing:

```python
"new_concept": {
    "uz": "Yangi Konsept",
    "description": "Tushuntirish...",
    "types": [...],
    "algorithms": [...]
}
```

### Yangi Python Darsi Qo'shish

`ml_concepts.py` faylida `self.python_lessons` dictionary'ga yangi dars qo'shing:

```python
"new_lesson": {
    "title": "Yangi Dars",
    "topics": [...],
    "code_example": "..."
}
```

### Frontend Dizaynini O'zgartirish

`static/css/style.css` faylini tahrirlang:
- Ranglarni o'zgartirish: `:root` da CSS variables
- Layout'ni o'zgartirish: Grid va Flexbox
- Animatsiyalar qo'shish: `@keyframes`

## 📊 Performance Tips

1. **Session Management**: Har 1000 sessiondan keyin eski sessionlarni tozalash
2. **Caching**: Tez-tez so'raladigan konseptlarni cache qilish
3. **Database**: Katta ma'lumotlar uchun SQLite yoki PostgreSQL qo'shish
4. **Frontend Optimization**: Lazy loading va code splitting

## 🎯 Kelajak Rejalari

- [ ] Speech-to-text qo'shish
- [ ] Yanada ko'p ML konseptlari
- [ ] Vizualizatsiya (graphs, charts)
- [ ] Multi-language support
- [ ] User authentication
- [ ] Progress tracking database
- [ ] Adaptive learning path
- [ ] Code execution environment

## 📝 Litsenziya

Bu loyiha o'quv maqsadlari uchun yaratilgan va bepul foydalanish uchun ochiq.

## 🤝 Hissa Qo'shish

Agar loyihani yaxshilash bo'yicha takliflaringiz bo'lsa:
1. Fork qiling
2. Yangi branch yarating
3. O'zgarishlarni commit qiling
4. Pull request yuboring

## 📧 Aloqa

Savollar yoki muammolar uchun GitHub Issues'dan foydalaning.

---

**Made with ❤️ for ML learners in Uzbekistan**
