"""
Audio Loader Module
===================
Audio va video fayllarni yuklash, format tekshirish va konvertatsiya qilish
"""

import os
import tempfile
from pathlib import Path
from typing import Tuple, Optional
import librosa
import soundfile as sf
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
import numpy as np


class AudioLoader:
    """
    Audio va video fayllarni yuklash va qayta ishlash klassi
    
    Qo'llab-quvvatlanadigan formatlar:
        Audio: mp3, wav, flac, ogg, m4a
        Video: mp4, avi, mov, mkv, webm
    """
    
    # Qo'llab-quvvatlanadigan formatlar
    SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac']
    SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
    
    def __init__(self, sample_rate: int = 16000):
        """
        Args:
            sample_rate (int): Audio sample rate (Hz). Default: 16000
        """
        self.sample_rate = sample_rate
        self.temp_dir = tempfile.gettempdir()
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Fayl formatini tekshirish
        
        Args:
            file_path (str): Fayl yo'li
            
        Returns:
            bool: Qo'llab-quvvatlanadigan format bo'lsa True
        """
        ext = Path(file_path).suffix.lower()
        return ext in (self.SUPPORTED_AUDIO_FORMATS + self.SUPPORTED_VIDEO_FORMATS)
    
    def is_video(self, file_path: str) -> bool:
        """
        Fayl video ekanligini tekshirish
        
        Args:
            file_path (str): Fayl yo'li
            
        Returns:
            bool: Video fayl bo'lsa True
        """
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_VIDEO_FORMATS
    
    def extract_audio_from_video(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Video fayldan audio qismini ajratib olish
        
        Args:
            video_path (str): Video fayl yo'li
            output_path (str, optional): Chiqish audio fayl yo'li
            
        Returns:
            str: Yaratilgan audio fayl yo'li
        """
        try:
            if output_path is None:
                output_path = os.path.join(
                    self.temp_dir, 
                    f"{Path(video_path).stem}_audio.wav"
                )
            
            print(f"🎥 Video fayldan audio ajratib olinmoqda: {Path(video_path).name}")
            
            # Video faylni ochish
            video = VideoFileClip(video_path)
            
            # Audio qismini ajratish
            audio = video.audio
            
            if audio is None:
                raise ValueError("Video faylda audio trek topilmadi!")
            
            # WAV formatda saqlash
            audio.write_audiofile(
                output_path,
                fps=self.sample_rate,
                codec='pcm_s16le',
                verbose=False,
                logger=None
            )
            
            # Resurslarni tozalash
            audio.close()
            video.close()
            
            print(f"✅ Audio ajratildi: {Path(output_path).name}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Video fayldan audio ajratishda xatolik: {str(e)}")
    
    def convert_to_wav(self, input_path: str, output_path: Optional[str] = None) -> str:
        """
        Audio faylni WAV formatiga o'tkazish
        
        Args:
            input_path (str): Kirish audio fayl yo'li
            output_path (str, optional): Chiqish WAV fayl yo'li
            
        Returns:
            str: WAV fayl yo'li
        """
        try:
            if output_path is None:
                output_path = os.path.join(
                    self.temp_dir,
                    f"{Path(input_path).stem}_converted.wav"
                )
            
            print(f"🔄 Audio WAV formatiga o'tkazilmoqda...")
            
            # PyDub yordamida konvertatsiya
            audio = AudioSegment.from_file(input_path)
            
            # Mono formatga o'tkazish (agar stereo bo'lsa)
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Sample rate sozlash
            audio = audio.set_frame_rate(self.sample_rate)
            
            # WAV formatda saqlash
            audio.export(output_path, format='wav')
            
            print(f"✅ Konvertatsiya tugallandi: {Path(output_path).name}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Audio konvertatsiya qilishda xatolik: {str(e)}")
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Audio faylni yuklash va numpy array qaytarish
        
        Args:
            file_path (str): Audio fayl yo'li
            
        Returns:
            Tuple[np.ndarray, int]: (audio_data, sample_rate)
        """
        try:
            # Format tekshirish
            if not self.is_supported_format(file_path):
                raise ValueError(
                    f"Qo'llab-quvvatlanmaydigan format: {Path(file_path).suffix}\n"
                    f"Qo'llab-quvvatlanadigan formatlar: "
                    f"{', '.join(self.SUPPORTED_AUDIO_FORMATS + self.SUPPORTED_VIDEO_FORMATS)}"
                )
            
            # Agar video bo'lsa, avval audio ajratish
            if self.is_video(file_path):
                file_path = self.extract_audio_from_video(file_path)
            
            # WAV formatiga o'tkazish (agar kerak bo'lsa)
            if Path(file_path).suffix.lower() != '.wav':
                file_path = self.convert_to_wav(file_path)
            
            print(f"📂 Audio yuklanmoqda: {Path(file_path).name}")
            
            # Librosa yordamida yuklash
            audio_data, sr = librosa.load(
                file_path,
                sr=self.sample_rate,
                mono=True
            )
            
            print(f"✅ Audio yuklandi: {len(audio_data)/sr:.2f} soniya")
            return audio_data, sr
            
        except Exception as e:
            raise Exception(f"Audio yuklashda xatolik: {str(e)}")
    
    def save_audio(self, audio_data: np.ndarray, output_path: str, sample_rate: Optional[int] = None) -> str:
        """
        Audio ma'lumotlarni faylga saqlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            output_path (str): Saqlash yo'li
            sample_rate (int, optional): Sample rate
            
        Returns:
            str: Saqlangan fayl yo'li
        """
        try:
            if sample_rate is None:
                sample_rate = self.sample_rate
            
            # Papkani yaratish (agar mavjud bo'lmasa)
            os.makedirs(Path(output_path).parent, exist_ok=True)
            
            # Audio saqlash
            sf.write(output_path, audio_data, sample_rate)
            
            print(f"💾 Audio saqlandi: {Path(output_path).name}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Audio saqlashda xatolik: {str(e)}")
    
    def get_audio_duration(self, file_path: str) -> float:
        """
        Audio davomiyligini olish (soniyalarda)
        
        Args:
            file_path (str): Audio fayl yo'li
            
        Returns:
            float: Davomiylik (soniya)
        """
        try:
            audio_data, sr = self.load_audio(file_path)
            duration = len(audio_data) / sr
            return duration
            
        except Exception as e:
            raise Exception(f"Audio davomiyligini olishda xatolik: {str(e)}")
    
    def get_audio_info(self, file_path: str) -> dict:
        """
        Audio fayl haqida to'liq ma'lumot
        
        Args:
            file_path (str): Audio fayl yo'li
            
        Returns:
            dict: Audio ma'lumotlari
        """
        try:
            audio_data, sr = self.load_audio(file_path)
            
            info = {
                'filename': Path(file_path).name,
                'duration_seconds': len(audio_data) / sr,
                'sample_rate': sr,
                'samples': len(audio_data),
                'channels': 1,  # Biz doim mono formatda ishlaymiz
                'format': Path(file_path).suffix,
                'file_size_mb': Path(file_path).stat().st_size / (1024 * 1024)
            }
            
            return info
            
        except Exception as e:
            raise Exception(f"Audio ma'lumotlarini olishda xatolik: {str(e)}")


# Test funksiyasi
if __name__ == "__main__":
    # Loader yaratish
    loader = AudioLoader(sample_rate=16000)
    
    # Test
    print("AudioLoader moduli ishga tushdi!")
    print(f"Qo'llab-quvvatlanadigan audio formatlar: {', '.join(loader.SUPPORTED_AUDIO_FORMATS)}")
    print(f"Qo'llab-quvvatlanadigan video formatlar: {', '.join(loader.SUPPORTED_VIDEO_FORMATS)}")
