# 🚀 Deployment Guide

Bu qo'llanma Uzbek Audio AI Platform'ni to'liq deployment qilish jarayonini tushuntiradi.

## 📋 Umumiy Ko'rinish

Platforma 3 ta qismdan iborat:
1. **Backend API** - FastAPI (Python)
2. **Frontend** - React (Node.js)
3. **ML Models** - Whisper (local yoki cached)

---

## 🔧 1. Local Development

### Backend Ishga Tushirish

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Dependencies o'rnatish
pip install -r requirements.txt

# ffmpeg o'rnatish (agar yo'q bo'lsa)
# Ubuntu: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
# Windows: choco install ffmpeg

# Whisper modellarni oldindan yuklash (tavsiya)
python scripts/download_models.py --models base medium

# FastAPI serverni ishga tushirish
cd api
python main.py
# Yoki
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### Frontend Ishga Tushirish

```bash
cd frontend

# Dependencies o'rnatish
npm install

# Development server
npm start
```

Frontend: `http://localhost:3000`

---

## 🌐 2. Production Deployment

### Option 1: Docker (Tavsiya)

#### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./api_uploads:/app/api_uploads
      - ./api_outputs:/app/api_outputs
    environment:
      - WHISPER_CACHE_DIR=/app/models/whisper
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000
```

#### Dockerfile (Backend)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# ffmpeg o'rnatish
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodni ko'chirish
COPY . .

# Whisper modellarni oldindan yuklash
RUN python scripts/download_models.py --models medium --cache-dir /app/models/whisper

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile (Frontend)

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Ishga tushirish

```bash
# Build va run
docker-compose up --build

# Background'da ishlatish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f

# To'xtatish
docker-compose down
```

---

### Option 2: VPS/Server (Manual)

#### Backend (Systemd Service)

```bash
# /etc/systemd/system/audio-ai-backend.service

[Unit]
Description=Uzbek Audio AI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/audio-ai-platform
Environment="PATH=/var/www/audio-ai-platform/venv/bin"
Environment="WHISPER_CACHE_DIR=/var/www/audio-ai-platform/models/whisper"
ExecStart=/var/www/audio-ai-platform/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Serviceni yoqish
sudo systemctl enable audio-ai-backend
sudo systemctl start audio-ai-backend
sudo systemctl status audio-ai-backend
```

#### Frontend (Nginx)

```nginx
# /etc/nginx/sites-available/audio-ai-frontend

server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    root /var/www/audio-ai-platform/frontend/build;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 600s;
    }
}
```

```bash
# Nginx'ni qayta yuklash
sudo ln -s /etc/nginx/sites-available/audio-ai-frontend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

### Option 3: Cloud Platforms

#### Railway.app

```bash
# Railway CLI o'rnatish
npm install -g @railway/cli

# Login
railway login

# Project yaratish
railway init

# Backend deploy
railway up

# Environment variables
railway variables set WHISPER_CACHE_DIR=/app/models/whisper
```

#### Heroku

```bash
# Procfile
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

```bash
# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Vercel (Frontend only)

```bash
cd frontend
vercel --prod
```

---

## ⚙️ 3. Konfiguratsiya

### Environment Variables

```bash
# .env
WHISPER_CACHE_DIR=./models/whisper
UPLOAD_DIR=./api_uploads
OUTPUT_DIR=./api_outputs
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment

```bash
# frontend/.env
REACT_APP_API_URL=http://your-api-domain.com
```

---

## 🔐 4. Xavfsizlik

### CORS Sozlamalari

```python
# api/main.py

# Development
allow_origins=["*"]

# Production
allow_origins=[
    "https://your-domain.com",
    "https://www.your-domain.com"
]
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/upload")
@limiter.limit("10/minute")
async def upload_file(...):
    ...
```

### File Size Limits

```python
# api/main.py
app.add_middleware(
    LimitUploadSize,
    max_upload_size=500_000_000  # 500 MB
)
```

---

## 📊 5. Monitoring & Logging

### Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

---

## 🚀 6. Performance Optimization

### Model Caching

```python
# Bir marta yuklash
transcriber = WhisperTranscriber(model_name='medium')
transcriber.load_model()  # Startup'da

# Global instance
app.state.transcriber = transcriber
```

### Batch Processing

```bash
# Ko'p fayllarni parallel qayta ishlash
python batch_processor.py --input-dir ./audio_files --workers 4
```

### GPU Support

```bash
# PyTorch CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Konfiguratsiya
DEVICE=cuda python api/main.py
```

---

## 📝 7. Backup & Maintenance

### Database (agar kerak bo'lsa)

```bash
# PostgreSQL
pg_dump audio_ai_db > backup.sql

# Restore
psql audio_ai_db < backup.sql
```

### Disk Space Management

```bash
# Eski fayllarni tozalash (7 kundan eski)
find api_uploads -type f -mtime +7 -delete
find api_outputs -type f -mtime +7 -delete
```

### Model Updates

```bash
# Yangi Whisper modellarni yuklash
python scripts/download_models.py --models large
```

---

## 🐛 8. Troubleshooting

### Backend ishlamayapti

```bash
# Loglarni tekshirish
journalctl -u audio-ai-backend -f

# Port band bo'lsa
lsof -i :8000
kill -9 <PID>
```

### Frontend build xatosi

```bash
# Node modules tozalash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Memory xatosi

```bash
# Swap qo'shish
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📚 Qo'shimcha Resurslar

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Whisper GitHub](https://github.com/openai/whisper)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

**Omad! Platform'ni production'da ishlatishingiz bilan! 🚀**
