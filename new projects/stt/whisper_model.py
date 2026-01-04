"""
Whisper Speech-to-Text Module
==============================
OpenAI Whisper modeli yordamida nutqni matnga aylantirish
O'zbek tilini qo'llab-quvvatlash
"""

import os
import whisper
import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import warnings

# Whisper warning'larini yashirish
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


@dataclass
class TranscriptionSegment:
    """
    Transkripsiya segmenti ma'lumotlari
    
    Attributes:
        text (str): Matn
        start (float): Boshlanish vaqti (soniya)
        end (float): Tugash vaqti (soniya)
        confidence (float): Ishonch darajasi (0-1)
    """
    text: str
    start: float
    end: float
    confidence: float = 1.0


class WhisperTranscriber:
    """
    Whisper model yordamida Speech-to-Text amalga oshirish
    
    Qo'llab-quvvatlanadigan modellar:
        - tiny: Eng tez, kam aniq
        - base: Tez, o'rtacha aniq
        - small: O'rtacha tezlik va aniqlik
        - medium: Sekin, yuqori aniqlik
        - large: Eng sekin, eng yuqori aniqlik
    """
    
    AVAILABLE_MODELS = ['tiny', 'base', 'small', 'medium', 'large']
    
    def __init__(
        self, 
        model_name: str = 'medium',
        device: str = 'cpu',
        language: str = 'uz'
    ):
        """
        Args:
            model_name (str): Whisper model nomi. Default: 'medium'
            device (str): 'cpu' yoki 'cuda'. Default: 'cpu'
            language (str): Til kodi (uz, ru, en). Default: 'uz'
        """
        if model_name not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"Noto'g'ri model: {model_name}. "
                f"Mavjud modellar: {', '.join(self.AVAILABLE_MODELS)}"
            )
        
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model = None
        
        print(f"🤖 WhisperTranscriber yaratildi:")
        print(f"  • Model: {model_name}")
        print(f"  • Device: {device}")
        print(f"  • Til: {language}")
    
    def load_model(self):
        """Whisper modelni yuklash"""
        if self.model is None:
            print(f"\n📥 Whisper '{self.model_name}' modeli yuklanmoqda...")
            print("⏳ Bu biroz vaqt olishi mumkin (birinchi marta)...")
            
            try:
                self.model = whisper.load_model(
                    self.model_name,
                    device=self.device
                )
                print(f"✅ Model yuklandi: {self.model_name}\n")
                
            except Exception as e:
                raise Exception(f"Model yuklashda xatolik: {str(e)}")
    
    def transcribe_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        language: Optional[str] = None,
        task: str = 'transcribe',
        verbose: bool = False
    ) -> Dict:
        """
        Audiodni matnga aylantirish
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            sample_rate (int): Sample rate. Default: 16000
            language (str, optional): Til kodi (None = auto-detect)
            task (str): 'transcribe' yoki 'translate'. Default: 'transcribe'
            verbose (bool): Batafsil chiqarish. Default: False
            
        Returns:
            Dict: Transkripsiya natijalari
        """
        # Modelni yuklash (agar yuklanmagan bo'lsa)
        self.load_model()
        
        # Til sozlash
        if language is None:
            language = self.language
        
        try:
            print(f"\n🎤 Audio matnga aylantirilmoqda...")
            print(f"  • Til: {language}")
            print(f"  • Davomiyligi: {len(audio_data)/sample_rate:.2f} soniya")
            
            # Whisper uchun audio tayyorlash
            # Whisper 16kHz kutadi
            if sample_rate != 16000:
                import librosa
                audio_data = librosa.resample(
                    audio_data,
                    orig_sr=sample_rate,
                    target_sr=16000
                )
            
            # Audio normalizatsiya
            audio_data = audio_data.astype(np.float32)
            
            # Transkripsiya
            result = self.model.transcribe(
                audio_data,
                language=language,
                task=task,
                verbose=verbose,
                fp16=False  # CPU uchun False
            )
            
            print(f"✅ Transkripsiya tugallandi")
            print(f"  • Aniqlangan til: {result.get('language', 'unknown')}")
            print(f"  • Segmentlar soni: {len(result.get('segments', []))}")
            
            return result
            
        except Exception as e:
            raise Exception(f"Transkripsiya xatoligi: {str(e)}")
    
    def transcribe_with_timestamps(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        language: Optional[str] = None
    ) -> List[TranscriptionSegment]:
        """
        Audiodni matnga aylantirish (vaqt belgilari bilan)
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            sample_rate (int): Sample rate. Default: 16000
            language (str, optional): Til kodi
            
        Returns:
            List[TranscriptionSegment]: Segmentlar ro'yxati
        """
        # Transkripsiya qilish
        result = self.transcribe_audio(
            audio_data,
            sample_rate=sample_rate,
            language=language
        )
        
        # Segmentlarni TranscriptionSegment formatiga o'tkazish
        segments = []
        
        for seg in result.get('segments', []):
            segment = TranscriptionSegment(
                text=seg['text'].strip(),
                start=seg['start'],
                end=seg['end'],
                confidence=seg.get('confidence', 1.0)
            )
            segments.append(segment)
        
        return segments
    
    def transcribe_long_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        chunk_duration: float = 30.0,
        language: Optional[str] = None
    ) -> List[TranscriptionSegment]:
        """
        Uzun audiodni bo'laklarga bo'lib transkripsiya qilish
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            sample_rate (int): Sample rate. Default: 16000
            chunk_duration (float): Bo'lak davomiyligi (soniya). Default: 30.0
            language (str, optional): Til kodi
            
        Returns:
            List[TranscriptionSegment]: Segmentlar ro'yxati
        """
        total_duration = len(audio_data) / sample_rate
        
        print(f"\n📊 Uzun audio transkripsiyasi:")
        print(f"  • Umumiy davomiylik: {total_duration:.2f} soniya")
        print(f"  • Bo'lak davomiyligi: {chunk_duration:.2f} soniya")
        
        # Bo'laklarga ajratish
        chunk_samples = int(chunk_duration * sample_rate)
        overlap_samples = int(1.0 * sample_rate)  # 1 soniyalik overlap
        
        all_segments = []
        offset = 0.0
        chunk_num = 0
        
        while offset * sample_rate < len(audio_data):
            chunk_num += 1
            start_sample = int(offset * sample_rate)
            end_sample = min(start_sample + chunk_samples, len(audio_data))
            
            chunk_audio = audio_data[start_sample:end_sample]
            
            print(f"\n🔄 Bo'lak {chunk_num} transkripsiya qilinmoqda...")
            
            # Transkripsiya
            segments = self.transcribe_with_timestamps(
                chunk_audio,
                sample_rate=sample_rate,
                language=language
            )
            
            # Vaqt offsetini qo'shish
            for seg in segments:
                seg.start += offset
                seg.end += offset
                all_segments.append(seg)
            
            # Keyingi bo'lakka o'tish (overlap bilan)
            offset += (chunk_duration - 1.0)
        
        print(f"\n✅ Umumiy {len(all_segments)} ta segment yaratildi")
        
        return all_segments
    
    def get_full_text(self, segments: List[TranscriptionSegment]) -> str:
        """
        Segmentlardan to'liq matnni olish
        
        Args:
            segments (List[TranscriptionSegment]): Segmentlar ro'yxati
            
        Returns:
            str: To'liq matn
        """
        return ' '.join(seg.text for seg in segments)
    
    def format_transcript(
        self,
        segments: List[TranscriptionSegment],
        include_timestamps: bool = True
    ) -> str:
        """
        Transkripsiyani formatlash
        
        Args:
            segments (List[TranscriptionSegment]): Segmentlar ro'yxati
            include_timestamps (bool): Vaqt belgilarini qo'shish. Default: True
            
        Returns:
            str: Formatlangan matn
        """
        lines = []
        
        for i, seg in enumerate(segments, 1):
            if include_timestamps:
                start_time = self._format_time(seg.start)
                end_time = self._format_time(seg.end)
                line = f"[{start_time} --> {end_time}] {seg.text}"
            else:
                line = seg.text
            
            lines.append(line)
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Vaqtni formatlash (HH:MM:SS.mmm)
        
        Args:
            seconds (float): Soniyalar
            
        Returns:
            str: Formatlangan vaqt
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    
    def save_transcript(
        self,
        segments: List[TranscriptionSegment],
        output_path: str,
        include_timestamps: bool = True
    ):
        """
        Transkripsiyani faylga saqlash
        
        Args:
            segments (List[TranscriptionSegment]): Segmentlar ro'yxati
            output_path (str): Chiqish fayl yo'li
            include_timestamps (bool): Vaqt belgilarini qo'shish
        """
        try:
            # Papkani yaratish
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Matnni formatlash
            formatted_text = self.format_transcript(
                segments,
                include_timestamps=include_timestamps
            )
            
            # Faylga yozish
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_text)
            
            print(f"💾 Transkripsiya saqlandi: {output_path}")
            
        except Exception as e:
            raise Exception(f"Transkripsiya saqlashda xatolik: {str(e)}")


# Test funksiyasi
if __name__ == "__main__":
    print("WhisperTranscriber moduli ishga tushdi!")
    print(f"Mavjud modellar: {', '.join(WhisperTranscriber.AVAILABLE_MODELS)}")
    print("\nFoydalanish:")
    print("  transcriber = WhisperTranscriber(model_name='medium', language='uz')")
    print("  segments = transcriber.transcribe_with_timestamps(audio_data)")
