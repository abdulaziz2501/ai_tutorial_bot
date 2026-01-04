"""
FastAPI Backend Server
======================
RESTful API for Uzbek Audio AI Platform

Endpoints:
    POST /upload           - Audio fayl yuklash
    POST /process          - Audio qayta ishlash
    GET  /status/{task_id} - Task statusini tekshirish
    GET  /download/{task_id}/{file_type} - Natijalarni yuklab olish
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
import json

from audio_utils import AudioLoader, AudioPreprocessor, SilenceRemover
from stt import WhisperTranscriber
from diarization import SpeakerDiarizer
from emotion import EmotionDetector
from subtitles import SubtitleGenerator


# FastAPI app
app = FastAPI(
    title="Uzbek Audio AI Platform API",
    description="O'zbek tilidagi audio va video fayllarni AI bilan qayta ishlash API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da faqat kerakli originlarni qo'shing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global o'zgaruvchilar
UPLOAD_DIR = "api_uploads"
OUTPUT_DIR = "api_outputs"
TASKS = {}  # Task statuslarini saqlash

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Pydantic models
class ProcessingRequest(BaseModel):
    whisper_model: str = "medium"
    language: str = "uz"
    enable_preprocessing: bool = True
    enable_diarization: bool = True
    enable_emotion: bool = True
    enable_subtitles: bool = True


class TaskStatus(BaseModel):
    task_id: str
    status: str  # pending, processing, completed, failed
    progress: float  # 0-100
    message: str
    result: Optional[dict] = None
    created_at: str
    updated_at: str


# Helper functions
def generate_task_id() -> str:
    """Unique task ID yaratish"""
    return str(uuid.uuid4())


def update_task_status(task_id: str, status: str, progress: float, message: str, result: dict = None):
    """Task statusini yangilash"""
    if task_id not in TASKS:
        TASKS[task_id] = {
            'created_at': datetime.now().isoformat()
        }
    
    TASKS[task_id].update({
        'task_id': task_id,
        'status': status,
        'progress': progress,
        'message': message,
        'result': result,
        'updated_at': datetime.now().isoformat()
    })


def process_audio_task(
    task_id: str,
    file_path: str,
    config: ProcessingRequest
):
    """
    Background task - audio qayta ishlash
    """
    output_dir = os.path.join(OUTPUT_DIR, task_id)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        update_task_status(task_id, "processing", 10, "Audio yuklanmoqda...")
        
        # 1. Audio yuklash
        loader = AudioLoader()
        audio_data, sr = loader.load_audio(file_path)
        
        update_task_status(task_id, "processing", 20, "Preprocessing...")
        
        # 2. Preprocessing
        if config.enable_preprocessing:
            preprocessor = AudioPreprocessor()
            audio_data = preprocessor.preprocess_audio(audio_data)
            
            remover = SilenceRemover()
            audio_data, _ = remover.remove_silence(audio_data)
            
            # Tozalangan audiodni saqlash
            clean_path = os.path.join(output_dir, "clean_audio.wav")
            loader.save_audio(audio_data, clean_path, sr)
        
        update_task_status(task_id, "processing", 40, "Transkripsiya...")
        
        # 3. Transkripsiya
        transcriber = WhisperTranscriber(
            model_name=config.whisper_model,
            language=config.language
        )
        segments = transcriber.transcribe_with_timestamps(audio_data, sr)
        
        # Transkripsiyani saqlash
        transcript_path = os.path.join(output_dir, "transcript.txt")
        transcriber.save_transcript(segments, transcript_path)
        
        update_task_status(task_id, "processing", 60, "Speaker diarization...")
        
        # 4. Speaker Diarization
        aligned = segments
        if config.enable_diarization:
            diarizer = SpeakerDiarizer()
            speaker_segments = diarizer.diarize(audio_data)
            aligned = diarizer.align_with_transcription(speaker_segments, segments)
            
            # Spikerlar bo'yicha matn
            diarization_path = os.path.join(output_dir, "speakers.txt")
            formatted = diarizer.format_diarization(aligned)
            with open(diarization_path, 'w', encoding='utf-8') as f:
                f.write(formatted)
        
        update_task_status(task_id, "processing", 75, "Emotion detection...")
        
        # 5. Emotion Detection
        if config.enable_emotion:
            detector = EmotionDetector()
            emotions = detector.detect_emotions_segments(audio_data, segments)
            
            emotion_path = os.path.join(output_dir, "emotions.txt")
            formatted_emotions = detector.format_emotions(emotions)
            with open(emotion_path, 'w', encoding='utf-8') as f:
                f.write(formatted_emotions)
        
        update_task_status(task_id, "processing", 90, "Subtitrlar yaratilmoqda...")
        
        # 6. Subtitrlar
        if config.enable_subtitles:
            generator = SubtitleGenerator()
            srt_path, vtt_path = generator.generate_both(
                aligned,
                output_dir,
                filename="subtitles",
                include_speaker=config.enable_diarization
            )
        
        # Natijalar
        result = {
            'duration': len(audio_data) / sr,
            'segments_count': len(segments),
            'files': {
                'transcript': 'transcript.txt',
                'srt': 'subtitles.srt' if config.enable_subtitles else None,
                'vtt': 'subtitles.vtt' if config.enable_subtitles else None,
                'speakers': 'speakers.txt' if config.enable_diarization else None,
                'emotions': 'emotions.txt' if config.enable_emotion else None,
                'clean_audio': 'clean_audio.wav' if config.enable_preprocessing else None
            }
        }
        
        update_task_status(task_id, "completed", 100, "Qayta ishlash tugallandi!", result)
        
    except Exception as e:
        update_task_status(task_id, "failed", 0, f"Xatolik: {str(e)}")


# API Endpoints
@app.get("/")
async def root():
    """API ma'lumotlari"""
    return {
        "name": "Uzbek Audio AI Platform API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "upload": "POST /upload",
            "process": "POST /process",
            "status": "GET /status/{task_id}",
            "download": "GET /download/{task_id}/{file_type}"
        }
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Audio/video fayl yuklash
    
    Returns:
        file_id: Yuklangan fayl ID
    """
    try:
        # File ID yaratish
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_extension}")
        
        # Faylni saqlash
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": os.path.getsize(file_path),
            "message": "Fayl yuklandi"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process/{file_id}")
async def process_audio(
    file_id: str,
    background_tasks: BackgroundTasks,
    config: ProcessingRequest = ProcessingRequest()
):
    """
    Audio qayta ishlashni boshlash
    
    Args:
        file_id: Yuklangan fayl ID
        config: Qayta ishlash sozlamalari
    
    Returns:
        task_id: Task ID (statusini tekshirish uchun)
    """
    try:
        # Faylni topish
        file_path = None
        for ext in ['.mp3', '.wav', '.mp4', '.avi', '.mov', '.mkv', '.m4a', '.flac']:
            potential_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(potential_path):
                file_path = potential_path
                break
        
        if not file_path:
            raise HTTPException(status_code=404, detail="Fayl topilmadi")
        
        # Task yaratish
        task_id = generate_task_id()
        update_task_status(task_id, "pending", 0, "Navbatda...")
        
        # Background task qo'shish
        background_tasks.add_task(process_audio_task, task_id, file_path, config)
        
        return {
            "task_id": task_id,
            "message": "Qayta ishlash boshlandi",
            "status_url": f"/status/{task_id}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Task statusini tekshirish
    
    Args:
        task_id: Task ID
    
    Returns:
        TaskStatus: Task ma'lumotlari
    """
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task topilmadi")
    
    return TASKS[task_id]


@app.get("/download/{task_id}/{file_type}")
async def download_file(task_id: str, file_type: str):
    """
    Natija faylni yuklab olish
    
    Args:
        task_id: Task ID
        file_type: Fayl turi (transcript, srt, vtt, speakers, emotions)
    
    Returns:
        FileResponse: Fayl
    """
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task topilmadi")
    
    task = TASKS[task_id]
    
    if task['status'] != 'completed':
        raise HTTPException(status_code=400, detail="Task hali tugallanmagan")
    
    # Fayl nomini olish
    file_mapping = {
        'transcript': 'transcript.txt',
        'srt': 'subtitles.srt',
        'vtt': 'subtitles.vtt',
        'speakers': 'speakers.txt',
        'emotions': 'emotions.txt',
        'audio': 'clean_audio.wav'
    }
    
    if file_type not in file_mapping:
        raise HTTPException(status_code=400, detail="Noto'g'ri fayl turi")
    
    filename = file_mapping[file_type]
    file_path = os.path.join(OUTPUT_DIR, task_id, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fayl topilmadi")
    
    return FileResponse(
        file_path,
        media_type='application/octet-stream',
        filename=filename
    )


@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """
    Taskni va uning fayllarini o'chirish
    
    Args:
        task_id: Task ID
    """
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task topilmadi")
    
    # Fayllarni o'chirish
    output_dir = os.path.join(OUTPUT_DIR, task_id)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # Taskni o'chirish
    del TASKS[task_id]
    
    return {"message": "Task o'chirildi"}


@app.get("/tasks")
async def list_tasks():
    """
    Barcha tasklarni ko'rish
    
    Returns:
        List[TaskStatus]: Tasklar ro'yxati
    """
    return list(TASKS.values())


# Health check
@app.get("/health")
async def health_check():
    """Server holatini tekshirish"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
