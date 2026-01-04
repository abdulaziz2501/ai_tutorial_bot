# ⚡ Tezkor Boshlash Qo'llanmasi

Bu qo'llanma loyihani 5 daqiqada ishga tushirishga yordam beradi!

## 🚀 3 Qadam - Ishga Tushirish

### 1️⃣ QADAM: Virtual Environment va Dependencies

```bash
# Terminal ochish va loyiha papkasiga kirish
cd uzbek-audio-ai-platform

# Virtual environment yaratish
python -m venv venv

# Aktivlashtirish
# Windows uchun:
venv\Scripts\activate

# Linux/Mac uchun:
source venv/bin/activate

# Dependencies o'rnatish (3-5 daqiqa)
pip install -r requirements.txt
```

### 2️⃣ QADAM: ffmpeg O'rnatish

**Windows:**
```bash
# Chocolatey orqali (agar o'rnatilgan bo'lsa)
choco install ffmpeg

# Yoki manual: https://ffmpeg.org/download.html dan yuklab oling
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**Tekshirish:**
```bash
ffmpeg -version
```

### 3️⃣ QADAM: Ilovani Ishga Tushirish

```bash
# Streamlit ilovani ishga tushirish
streamlit run app.py
```

Brauzer avtomatik ochiladi: `http://localhost:8501` 🎉

---

## 📖 Birinchi Test

### Test Audio Fayl

1. **Oddiy test audio yozish:**
   - Telefoningizdan 10-20 soniyalik audio yozing
   - O'zbek tilida gaplashing
   - WAV yoki MP3 formatda saqlang

2. **Yoki test fayl yuklab oling:**
   ```bash
   # Telegram, YouTube yoki boshqa manbadan kichik audio
   ```

### Platforma Ishlatish

1. **"📤 Yuklash" tab:**
   - Audio faylni yuklang
   - "🚀 Audio Yuklash" tugmasini bosing

2. **"🔧 Preprocessing" tab:**
   - "🔄 Preprocessing Boshlash" tugmasini bosing
   - 5-10 soniya kutish

3. **"📝 Transkripsiya" tab:**
   - Sidebar'dan model tanlang: **small** (tez test uchun)
   - "🎤 Transkripsiya Boshlash" tugmasini bosing
   - Birinchi marta 1-2 daqiqa (model yuklanadi)
   - Keyingi safar tezroq ishlaydi

4. **"👥 Speaker & Emotsiya" tab:**
   - "🎯 Spikerlarni Aniqlash" - kim gapirayotganini aniqlash
   - "🎭 Emotsiyalarni Aniqlash" - hissiy holatni aniqlash

5. **"💾 Natijalar" tab:**
   - Barcha natijalarni yuklab olish

---

## ⚙️ Sozlamalar (Sidebar)

### Whisper Model Tanlash

**Test uchun:**
- `tiny` - Juda tez, kam aniq (39 MB)
- `base` - Tez, o'rtacha aniq (74 MB) ✅ **Tavsiya!**
- `small` - O'rtacha tezlik va aniqlik (244 MB)

**Production uchun:**
- `medium` - Sekin, yuqori aniqlik (769 MB) ✅ **Eng yaxshi tanlov!**
- `large` - Juda sekin, maksimal aniqlik (1550 MB)

### Preprocessing Sozlamalari

✅ **Tavsiya: Hammasini yoqish**

- ✅ Shovqin tozalash - Orqa fon shovqinini olib tashlash
- ✅ Sukut kesish - Jimlik qismlarini kesish
- ✅ Audio normalizatsiya - Ovoz balandligini bir xil qilish

### Til Tanlash

- `uz` - O'zbek tili ✅ **Default**
- `ru` - Rus tili
- `en` - Ingliz tili

---

## 💡 Maslahatlar

### 1. Birinchi Marta
- **Kichik model** bilan boshlang (`base` yoki `small`)
- **Qisqa audio** bilan test qiling (30 soniya - 2 daqiqa)
- **Internet** ulanishi bo'lsin (model yuklanadi)

### 2. Tez Ishlash Uchun
- **CPU:** `tiny` yoki `base` model
- **RAM 8GB+:** `small` yoki `medium` model
- **GPU bor bo'lsa:** `medium` yoki `large` model

### 3. Eng Yaxshi Natija Uchun
- **Sifatli audio:** Kam shovqin, aniq ovoz
- **Medium model:** Tezlik va aniqlik balansi
- **Preprocessing:** Hammasini yoqing

### 4. Audio Tayyorlash
- Shovqinsiz muhitda yozish
- Mikrofonni yaqin tutish
- Aniq va sekin gapirish
- 1-10 daqiqa optimal davomiylik

---

## 🐛 Tez-tez Uchraydigan Muammolar

### ❌ "ffmpeg not found"
```bash
# ffmpeg o'rnatilganligini tekshiring
ffmpeg -version

# O'rnatish (yuqoriga qarang)
```

### ❌ "Module not found"
```bash
# Virtual environment aktivlashtiring
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Dependencies qayta o'rnating
pip install -r requirements.txt
```

### ❌ "Out of memory"
- Kichikroq model tanlang (`tiny` yoki `base`)
- Qisqaroq audio yuklang
- Boshqa ilovalarni yoping

### ❌ "Model downloading too slow"
- Internet tezligini tekshiring
- VPN yoqing (agar kerak bo'lsa)
- Sabr qiling - birinchi marta 1-2 daqiqa

---

## 📊 Kutilayotgan Vaqtlar

**Test Environment (CPU, 8GB RAM):**

| Vazifa | tiny | base | small | medium |
|--------|------|------|-------|--------|
| Model yuklash (birinchi marta) | 10s | 15s | 30s | 1min |
| 1 min audio transkripsiya | 5s | 10s | 20s | 40s |
| 5 min audio transkripsiya | 20s | 40s | 1.5min | 3min |

---

## 🎯 Keyingi Qadamlar

Platformani o'rgandingizmi? Endi:

1. **README.md** faylini o'qing - to'liq qo'llanma
2. **Sozlamalarni** o'zgartiring - o'zingizga moslang
3. **Katta audio** yuklang - real test
4. **Natijalarni** tahlil qiling - qanday ishlayotganini ko'ring

---

## 🆘 Yordam Kerakmi?

1. **README.md** - To'liq documentation
2. **GitHub Issues** - Savol va muammolar
3. **Email:** your.email@example.com

---

**Omad! Platformadan foydalaning! 🚀**
