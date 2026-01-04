# 🎙️ Uzbek Speech-to-Text & Audio Intelligence Platform

O'zbek tilidagi audio va video fayllarni AI texnologiyalari bilan qayta ishlash platformasi.

## 📋 Funksiyalar

### ✨ Asosiy Imkoniyatlar

1. **Audio/Video Yuklash**
   - Qo'llab-quvvatlanadigan formatlar: MP3, WAV, FLAC, OGG, M4A, MP4, AVI, MOV, MKV, WEBM
   - Video fayllardan audio ajratish

2. **Audio Preprocessing**
   - 🧹 Shovqinlarni olib tashlash (Noise Reduction)
   - ✂️ Sukut qismlarini kesish (Silence Removal)
   - 📊 Audio normalizatsiya
   - 🎛️ High-pass va Low-pass filter
   - 🎤 Nutq sifatini yaxshilash

3. **Speech-to-Text (STT)**
   - 🤖 OpenAI Whisper modeli
   - 🇺🇿 O'zbek tilini qo'llab-quvvatlash
   - ⏰ Vaqt belgilari bilan transkripsiya
   - 📝 Uzun audio fayllarni segmentlab qayta ishlash

4. **Speaker Diarization**
   - 👥 Nechta kishi gapirayotganini aniqlash
   - 🎯 Har bir gapni alohida spikerga bog'lash
   - ⏱️ Vaqt oralig'i bilan natija

5. **Emotion Detection**
   - 😊 Hissiy holatni aniqlash
   - 📊 5 ta emotsiya: neutral, happy, sad, angry, stressed
   - 📈 Segment bo'yicha tahlil

6. **Subtitle Generation**
   - 📝 SRT format
   - 🎬 VTT format
   - 💾 Yuklab olish imkoniyati

## 🚀 O'rnatish va Ishga Tushirish

### 1. Talablar

- Python 3.10 yoki yuqori
- 4GB+ RAM (Whisper medium model uchun)
- ffmpeg (audio/video processing uchun)

### 2. Loyihani Klonlash

```bash
# GitHub'dan klonlash (agar repozitoriy mavjud bo'lsa)
git clone https://github.com/username/uzbek-audio-ai-platform.git
cd uzbek-audio-ai-platform

# Yoki fayllarni zip'dan extract qiling
```

### 3. Virtual Environment Yaratish

```bash
# Virtual environment yaratish
python -m venv venv

# Aktivlashtirish (Windows)
venv\Scripts\activate

# Aktivlashtirish (Linux/Mac)
source venv/bin/activate
```

### 4. Dependencies O'rnatish

```bash
# Barcha kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt

# ffmpeg o'rnatish
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows:
# https://ffmpeg.org/download.html dan yuklab oling
# va PATH ga qo'shing

# Mac:
brew install ffmpeg
```

### 5. Ilovani Ishga Tushirish

```bash
# Streamlit ilovani ishga tushirish
streamlit run app.py
```

Brauzer avtomatik ochiladi: `http://localhost:8501`

## 📖 Foydalanish Qo'llanmasi

### Qadam 1: Audio/Video Yuklash
1. "📤 Yuklash" tabini oching
2. Audio yoki video faylni tanlang
3. "🚀 Audio Yuklash" tugmasini bosing

### Qadam 2: Audio Preprocessing
1. "🔧 Preprocessing" tabiga o'ting
2. Sidebar'dan kerakli sozlamalarni tanlang:
   - Shovqin tozalash
   - Sukut kesish
   - Normalizatsiya
3. "🔄 Preprocessing Boshlash" tugmasini bosing

### Qadam 3: Transkripsiya
1. "📝 Transkripsiya" tabiga o'ting
2. Whisper modelni tanlang (sidebar)
3. "🎤 Transkripsiya Boshlash" tugmasini bosing
4. Natijani ko'ring

### Qadam 4: Speaker & Emotsiya
1. "👥 Speaker & Emotsiya" tabiga o'ting
2. Speaker Diarization:
   - "🎯 Spikerlarni Aniqlash" tugmasini bosing
3. Emotion Detection:
   - "🎭 Emotsiyalarni Aniqlash" tugmasini bosing

### Qadam 5: Natijalarni Yuklab Olish
1. "💾 Natijalar" tabiga o'ting
2. Kerakli fayllarni yuklab oling:
   - 📄 Transkripsiya (TXT)
   - 📝 Subtitrlar (SRT/VTT)
   - 📊 To'liq Hisobot

## 📁 Loyiha Strukturasi

```
uzbek-audio-ai-platform/
├── audio_utils/              # Audio qayta ishlash modullari
│   ├── __init__.py
│   ├── loader.py            # Audio/video yuklash
│   ├── preprocessing.py     # Shovqin tozalash, normalizatsiya
│   └── silence_removal.py   # Sukut kesish
├── stt/                     # Speech-to-Text moduli
│   ├── __init__.py
│   └── whisper_model.py     # Whisper transkripsiya
├── diarization/             # Speaker diarization
│   ├── __init__.py
│   └── speaker.py           # Spikerlarni aniqlash
├── emotion/                 # Emotion detection
│   ├── __init__.py
│   └── emotion_model.py     # Emotsiya aniqlash
├── subtitles/               # Subtitle generation
│   ├── __init__.py
│   └── srt_generator.py     # SRT/VTT yaratish
├── models/                  # ML modellar (auto yuklanadi)
├── uploads/                 # Yuklangan fayllar
├── outputs/                 # Chiqish fayllari
├── app.py                   # Streamlit interfeys
├── requirements.txt         # Dependencies
├── .env.example            # Environment variables namunasi
└── README.md               # Bu fayl
```

## ⚙️ Sozlamalar

### Whisper Model Tanlash

Model hajmi va aniqlik o'rtasida tanlov:

| Model  | Hajm   | VRAM  | Tezlik | Aniqlik |
|--------|--------|-------|--------|---------|
| tiny   | 39 MB  | ~1 GB | Juda tez | Past |
| base   | 74 MB  | ~1 GB | Tez | O'rtacha |
| small  | 244 MB | ~2 GB | O'rtacha | Yaxshi |
| medium | 769 MB | ~5 GB | Sekin | Juda yaxshi |
| large  | 1550 MB| ~10 GB| Juda sekin | Eng yaxshi |

**Tavsiya:** 
- Test uchun: `small` yoki `base`
- Production uchun: `medium` yoki `large`

### Preprocessing Parametrlari

```python
# Shovqin tozalash
enable_noise_reduction = True

# Sukut kesish
enable_silence_removal = True
threshold_db = -40.0  # Sukut chegarasi
min_silence_duration = 0.5  # Minimal sukut (soniya)

# Normalizatsiya
enable_normalization = True
target_level = -20.0  # Target dB darajasi
```

## 🔧 Muammolarni Hal Qilish

### Audio yuklash xatoligi

```bash
# ffmpeg o'rnatilganligini tekshiring
ffmpeg -version

# Agar o'rnatilmagan bo'lsa, o'rnating
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg           # Mac
```

### Whisper model yuklanmayapti

```bash
# Internet ulanishini tekshiring
# Model birinchi marta yuklanadi (~500MB - 1.5GB)
```

### CUDA xatosi (GPU)

```bash
# CPU'da ishlatish uchun
device = 'cpu'

# Agar GPU bo'lsa
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Memory xatosi

Agar RAM yetmasa:
1. Kichikroq Whisper model tanlang (tiny, base)
2. Audio faylni qisqaroq bo'laklarga bo'ling
3. Preprocessing qadamlarini alohida bajaring

## 📊 Performance

**Test natijalar (medium model, CPU):**

| Audio davomiyligi | Preprocessing | Transkripsiya | Diarization | Umumiy |
|-------------------|---------------|---------------|-------------|---------|
| 1 min             | 5-10 sek      | 30-60 sek     | 10-15 sek   | ~1 min  |
| 5 min             | 20-30 sek     | 3-5 min       | 30-45 sek   | ~5 min  |
| 10 min            | 40-60 sek     | 6-10 min      | 1-2 min     | ~10 min |

**Tavsiyalar:**
- GPU bo'lsa, 5-10x tezroq ishlaydi
- Katta fayllar uchun `small` yoki `base` model ishlatish

## 🤝 Hissa Qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch'ga push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## 📝 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi.

## 🙏 Minnatdorchilik

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech-to-Text model
- [Streamlit](https://streamlit.io/) - Web interfeys
- [Librosa](https://librosa.org/) - Audio qayta ishlash
- [PyDub](https://github.com/jiaaro/pydub) - Audio manipulation

## 📧 Aloqa

Savol va takliflar uchun:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🔮 Kelajak Rejalari

- [ ] Real-time audio processing
- [ ] GPU support optimization
- [ ] Ko'proq tillarni qo'llab-quvvatlash
- [ ] Advanced emotion detection models
- [ ] API endpoint yaratish
- [ ] Docker container
- [ ] Cloud deployment qo'llanmasi

---

**Made with ❤️ in Uzbekistan** 🇺🇿
