# 🎙️ Uzbek Audio AI Platform v2.0

**Professional AI-powered audio processing platform** for Uzbek language with FastAPI backend and React frontend.

## 🆕 Version 2.0 Yangiliklar

### ✨ Yangi Funksiyalar

1. **📥 Model Pre-download** - Whisper modellarni oldindan yuklash skripti
2. **🔄 Batch Processing** - Bir nechta faylni parallel qayta ishlash
3. **🌐 FastAPI Backend** - RESTful API server
4. **⚛️ React Frontend** - Modern, responsive web interfeys
5. **🚀 Production Ready** - Docker, systemd, nginx support

---

## 📦 Arxitektura

```
uzbek-audio-ai-platform/
├── api/                     # FastAPI Backend
│   ├── main.py             # API server
│   └── __init__.py
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── styles/         # CSS files
│   ├── public/
│   └── package.json
├── scripts/
│   └── download_models.py  # Model download script
├── batch_processor.py       # Batch processing
├── app.py                   # Streamlit app (legacy)
└── [audio_utils, stt, diarization, emotion, subtitles]
```

---

## 🚀 Quick Start

### 1️⃣ Model Download (Bir marta)

```bash
# Whisper modellarni oldindan yuklash
python scripts/download_models.py --models base medium

# Yoki barcha modellar
python scripts/download_models.py --all
```

**Nima uchun kerak?**
- ✅ Birinchi marta tezroq ishlash
- ✅ Internet kerak emas (offline mode)
- ✅ Bir joyda saqlash (cache)

---

### 2️⃣ Backend (FastAPI)

```bash
# Dependencies
pip install -r requirements.txt

# Backend serverni ishga tushirish
cd api
python main.py

# Yoki uvicorn bilan
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Backend:** `http://localhost:8000`  
**API Docs:** `http://localhost:8000/docs` (Swagger UI)

---

### 3️⃣ Frontend (React)

```bash
cd frontend

# Dependencies o'rnatish
npm install

# Development server
npm start
```

**Frontend:** `http://localhost:3000`

---

## 🔄 Batch Processing

Bir nechta faylni avtomatik qayta ishlash:

```bash
# Oddiy ishlatish
python batch_processor.py --input-dir ./audio_files

# To'liq sozlamalar
python batch_processor.py \
    --input-dir ./audio_files \
    --output-dir ./results \
    --model medium \
    --language uz \
    --workers 2

# Faqat transkripsiya (tezroq)
python batch_processor.py \
    --input-dir ./audio_files \
    --no-diarization \
    --no-emotion \
    --workers 4
```

**Parametrlar:**
- `--input-dir` - Audio fayllar papkasi
- `--output-dir` - Natijalar papkasi
- `--model` - Whisper model (tiny, base, small, medium, large)
- `--language` - Til (uz, ru, en)
- `--workers` - Parallel worker'lar soni (2-4 optimal)
- `--no-preprocessing` - Preprocessing o'chirish
- `--no-diarization` - Speaker diarization o'chirish
- `--no-emotion` - Emotion detection o'chirish
- `--no-subtitles` - Subtitrlar o'chirish

**Misol natija:**
```
batch_outputs/
├── file1/
│   ├── file1_transcript.txt
│   ├── file1_speakers.txt
│   ├── file1_emotions.txt
│   ├── file1.srt
│   ├── file1.vtt
│   └── file1_report.txt
├── file2/
│   └── ...
└── batch_summary.json
```

---

## 🌐 FastAPI Endpoints

### POST /upload
Audio/video faylni yuklash

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@audio.mp3"
```

Response:
```json
{
  "file_id": "uuid",
  "filename": "audio.mp3",
  "size": 5242880
}
```

### POST /process/{file_id}
Qayta ishlashni boshlash

```bash
curl -X POST "http://localhost:8000/process/{file_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "whisper_model": "medium",
    "language": "uz",
    "enable_preprocessing": true,
    "enable_diarization": true,
    "enable_emotion": true,
    "enable_subtitles": true
  }'
```

Response:
```json
{
  "task_id": "task-uuid",
  "message": "Qayta ishlash boshlandi",
  "status_url": "/status/task-uuid"
}
```

### GET /status/{task_id}
Task statusini tekshirish

```bash
curl "http://localhost:8000/status/{task_id}"
```

Response:
```json
{
  "task_id": "task-uuid",
  "status": "processing",
  "progress": 45.0,
  "message": "Transkripsiya...",
  "result": null
}
```

### GET /download/{task_id}/{file_type}
Natijalarni yuklab olish

```bash
# Transkripsiya
curl -O "http://localhost:8000/download/{task_id}/transcript"

# Subtitrlar
curl -O "http://localhost:8000/download/{task_id}/srt"
curl -O "http://localhost:8000/download/{task_id}/vtt"
```

File types: `transcript`, `srt`, `vtt`, `speakers`, `emotions`, `audio`

### GET /tasks
Barcha tasklarni ko'rish

```bash
curl "http://localhost:8000/tasks"
```

### DELETE /task/{task_id}
Taskni o'chirish

```bash
curl -X DELETE "http://localhost:8000/task/{task_id}"
```

---

## ⚛️ React Frontend

### Features
- 🎨 Modern, responsive UI (Tailwind CSS)
- 📤 Drag & drop file upload
- ⚙️ Real-time configuration
- 📊 Progress tracking
- 💾 One-click downloads
- 📱 Mobile-friendly

### Components
- `FileUpload` - Fayl yuklash
- `ProcessingConfig` - Sozlamalar
- `TaskProgress` - Progress bar
- `Results` - Natijalar va yuklab olish

### API Integration
- Axios HTTP client
- Real-time polling (2s interval)
- Error handling
- Loading states

---

## 🐳 Docker Deployment

### Docker Compose

```bash
# Build va run
docker-compose up --build

# Background mode
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker

```bash
# Backend
docker build -t audio-ai-backend .
docker run -p 8000:8000 -v $(pwd)/models:/app/models audio-ai-backend

# Frontend
cd frontend
docker build -t audio-ai-frontend .
docker run -p 3000:80 audio-ai-frontend
```

---

## 📊 Performance

### Model Size & Speed

| Model | Size | RAM | 1 min audio | 5 min audio |
|-------|------|-----|-------------|-------------|
| tiny | 39 MB | ~1GB | 5s | 20s |
| base | 74 MB | ~1GB | 10s | 40s |
| small | 244 MB | ~2GB | 20s | 1.5min |
| medium | 769 MB | ~5GB | 40s | 3min |
| large | 1550 MB | ~10GB | 80s | 6min |

### Batch Processing

**Test environment:** CPU (Intel i7), 8GB RAM

| Files | Model | Workers | Total Time |
|-------|-------|---------|------------|
| 10 x 1min | medium | 2 | ~5 min |
| 10 x 5min | medium | 2 | ~25 min |
| 20 x 1min | small | 4 | ~5 min |

**GPU** bilan 5-10x tezroq!

---

## 🔧 Konfiguratsiya

### Environment Variables

```bash
# .env
WHISPER_CACHE_DIR=./models/whisper
UPLOAD_DIR=./api_uploads
OUTPUT_DIR=./api_outputs
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend Config

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
```

---

## 📚 Documentation

- **README.md** - Asosiy qo'llanma
- **QUICK_START.md** - 5 daqiqada ishga tushirish
- **DEPLOYMENT_GUIDE.md** - Production deployment
- **API Docs** - http://localhost:8000/docs

---

## 🆚 Streamlit vs FastAPI+React

| Feature | Streamlit | FastAPI+React |
|---------|-----------|---------------|
| Tezlik | O'rtacha | Tez ⚡ |
| Scalability | Cheklangan | Yuqori 📈 |
| Customization | Cheklangan | To'liq 🎨 |
| API | Yo'q | Ha ✅ |
| Production | Basic | Professional 🚀 |
| Mobile | Yaxshi emas | Responsive 📱 |

**Tavsiya:**
- **Development/Test:** Streamlit (tezkor)
- **Production:** FastAPI+React (professional)

---

## 🐛 Troubleshooting

### Port already in use

```bash
# Port bandligini tekshirish
lsof -i :8000
lsof -i :3000

# Process'ni to'xtatish
kill -9 <PID>
```

### Model yuklanmayapti

```bash
# Qo'lda yuklash
python scripts/download_models.py --models medium

# Cache papkani tekshirish
ls -la ./models/whisper/
```

### CORS xatosi

Frontend'da API URL'ni to'g'ri sozlang:

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:8000
```

### Memory xatosi

```bash
# Kichikroq model ishlatish
--model base

# Workers kamaytirish
--workers 1

# Swap qo'shish
sudo fallocate -l 4G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License

---

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Streamlit](https://streamlit.io/)

---

## 📧 Contact

- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Made with ❤️ in Uzbekistan 🇺🇿**
