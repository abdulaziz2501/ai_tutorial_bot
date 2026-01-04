"""
Audio Preprocessing Module
===========================
Audio shovqinlarini tozalash, normalizatsiya va sifatni yaxshilash
"""

import numpy as np
import librosa
import noisereduce as nr
from scipy import signal
from typing import Tuple, Optional


class AudioPreprocessor:
    """
    Audio preprocessing va sifatni yaxshilash klassi
    
    Funksiyalar:
        - Shovqinni olib tashlash (noise reduction)
        - Audio normalizatsiya
        - High-pass va low-pass filter
        - Audio sifatini yaxshilash
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Args:
            sample_rate (int): Audio sample rate (Hz). Default: 16000
        """
        self.sample_rate = sample_rate
    
    def remove_noise(
        self, 
        audio_data: np.ndarray, 
        noise_profile: Optional[np.ndarray] = None,
        stationary: bool = True
    ) -> np.ndarray:
        """
        Shovqinni olib tashlash (Noise Reduction)
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            noise_profile (np.ndarray, optional): Shovqin profili (birinchi 1 soniya)
            stationary (bool): Stationar shovqin uchun True
            
        Returns:
            np.ndarray: Tozalangan audio
        """
        try:
            print("🧹 Shovqin olib tashlanmoqda...")
            
            # Agar noise profile berilmagan bo'lsa, birinchi 1 soniyani ishlatish
            if noise_profile is None:
                # Birinchi 1 soniyani noise profile sifatida olish
                noise_duration = min(1.0, len(audio_data) / self.sample_rate)
                noise_len = int(noise_duration * self.sample_rate)
                noise_profile = audio_data[:noise_len]
            
            # Noise reduction algoritmi
            reduced_noise = nr.reduce_noise(
                y=audio_data,
                sr=self.sample_rate,
                y_noise=noise_profile,
                stationary=stationary,
                prop_decrease=0.8  # Shovqinni 80% kamaytirish
            )
            
            print("✅ Shovqin tozalandi")
            return reduced_noise
            
        except Exception as e:
            print(f"⚠️ Shovqin tozalashda muammo: {str(e)}")
            return audio_data  # Xato bo'lsa, asl audio qaytarish
    
    def normalize_audio(self, audio_data: np.ndarray, target_level: float = -20.0) -> np.ndarray:
        """
        Audio normalizatsiya (ovoz balandligini bir xil qilish)
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            target_level (float): Maqsadli ovoz darajasi (dB). Default: -20.0
            
        Returns:
            np.ndarray: Normalizatsiya qilingan audio
        """
        try:
            print("📊 Audio normalizatsiya qilinmoqda...")
            
            # RMS (Root Mean Square) hisoblash
            rms = np.sqrt(np.mean(audio_data ** 2))
            
            if rms == 0:
                print("⚠️ Audio bo'sh yoki juda past ovoz darajasi")
                return audio_data
            
            # Target RMS hisoblash
            target_rms = 10 ** (target_level / 20)
            
            # Normalizatsiya koeffitsienti
            gain = target_rms / rms
            
            # Audio normalizatsiya qilish
            normalized = audio_data * gain
            
            # Clipping oldini olish (-1 dan 1 gacha)
            normalized = np.clip(normalized, -1.0, 1.0)
            
            print("✅ Audio normalizatsiya qilindi")
            return normalized
            
        except Exception as e:
            print(f"⚠️ Normalizatsiya qilishda muammo: {str(e)}")
            return audio_data
    
    def apply_highpass_filter(self, audio_data: np.ndarray, cutoff_freq: float = 80.0) -> np.ndarray:
        """
        High-pass filter (past chastotalarni olib tashlash)
        Odatda 80 Hz dan pastni olib tashlash yaxshi (bas shovqinlari)
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            cutoff_freq (float): Kesish chastotasi (Hz). Default: 80.0
            
        Returns:
            np.ndarray: Filtrlangan audio
        """
        try:
            print(f"🔊 High-pass filter qo'llanmoqda (cutoff: {cutoff_freq} Hz)...")
            
            # Butterworth filter yaratish
            nyquist = self.sample_rate / 2
            normal_cutoff = cutoff_freq / nyquist
            
            # Filter koeffitsiyentlari
            b, a = signal.butter(5, normal_cutoff, btype='high', analog=False)
            
            # Filtrni qo'llash
            filtered = signal.filtfilt(b, a, audio_data)
            
            print("✅ High-pass filter qo'llandi")
            return filtered
            
        except Exception as e:
            print(f"⚠️ High-pass filter qo'llashda muammo: {str(e)}")
            return audio_data
    
    def apply_lowpass_filter(self, audio_data: np.ndarray, cutoff_freq: float = 8000.0) -> np.ndarray:
        """
        Low-pass filter (yuqori chastotalarni olib tashlash)
        Odatda 8000 Hz dan yuqorini olib tashlash yaxshi
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            cutoff_freq (float): Kesish chastotasi (Hz). Default: 8000.0
            
        Returns:
            np.ndarray: Filtrlangan audio
        """
        try:
            print(f"🔉 Low-pass filter qo'llanmoqda (cutoff: {cutoff_freq} Hz)...")
            
            # Butterworth filter yaratish
            nyquist = self.sample_rate / 2
            normal_cutoff = cutoff_freq / nyquist
            
            # Filter koeffitsiyentlari
            b, a = signal.butter(5, normal_cutoff, btype='low', analog=False)
            
            # Filtrni qo'llash
            filtered = signal.filtfilt(b, a, audio_data)
            
            print("✅ Low-pass filter qo'llandi")
            return filtered
            
        except Exception as e:
            print(f"⚠️ Low-pass filter qo'llashda muammo: {str(e)}")
            return audio_data
    
    def enhance_speech(self, audio_data: np.ndarray) -> np.ndarray:
        """
        Nutq sifatini yaxshilash (speech enhancement)
        Speech frequency range: 300-3400 Hz
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            
        Returns:
            np.ndarray: Yaxshilangan audio
        """
        try:
            print("🎤 Nutq sifati yaxshilanmoqda...")
            
            # Band-pass filter (300-3400 Hz)
            nyquist = self.sample_rate / 2
            low_cutoff = 300.0 / nyquist
            high_cutoff = 3400.0 / nyquist
            
            # Filter yaratish
            b, a = signal.butter(4, [low_cutoff, high_cutoff], btype='band')
            
            # Filtrni qo'llash
            enhanced = signal.filtfilt(b, a, audio_data)
            
            print("✅ Nutq sifati yaxshilandi")
            return enhanced
            
        except Exception as e:
            print(f"⚠️ Nutq yaxshilashda muammo: {str(e)}")
            return audio_data
    
    def preprocess_audio(
        self, 
        audio_data: np.ndarray,
        remove_noise: bool = True,
        normalize: bool = True,
        enhance_speech: bool = True,
        highpass_filter: bool = True
    ) -> np.ndarray:
        """
        To'liq audio preprocessing pipeline
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            remove_noise (bool): Shovqin tozalash
            normalize (bool): Normalizatsiya qilish
            enhance_speech (bool): Nutq sifatini yaxshilash
            highpass_filter (bool): High-pass filter qo'llash
            
        Returns:
            np.ndarray: Qayta ishlangan audio
        """
        processed_audio = audio_data.copy()
        
        print("\n" + "="*50)
        print("🔧 AUDIO PREPROCESSING BOSHLANDI")
        print("="*50)
        
        # 1. High-pass filter (bas shovqinlarini olib tashlash)
        if highpass_filter:
            processed_audio = self.apply_highpass_filter(processed_audio)
        
        # 2. Shovqinni olib tashlash
        if remove_noise:
            processed_audio = self.remove_noise(processed_audio)
        
        # 3. Nutq sifatini yaxshilash
        if enhance_speech:
            processed_audio = self.enhance_speech(processed_audio)
        
        # 4. Normalizatsiya (oxirida qilish kerak)
        if normalize:
            processed_audio = self.normalize_audio(processed_audio)
        
        print("="*50)
        print("✅ PREPROCESSING TUGALLANDI")
        print("="*50 + "\n")
        
        return processed_audio
    
    def compare_audio_quality(self, original: np.ndarray, processed: np.ndarray) -> dict:
        """
        Asl va qayta ishlangan audio sifatini solishtirish
        
        Args:
            original (np.ndarray): Asl audio
            processed (np.ndarray): Qayta ishlangan audio
            
        Returns:
            dict: Sifat ko'rsatkichlari
        """
        try:
            # RMS hisoblash
            original_rms = np.sqrt(np.mean(original ** 2))
            processed_rms = np.sqrt(np.mean(processed ** 2))
            
            # Signal-to-Noise Ratio (SNR) hisoblash
            noise = original - processed
            signal_power = np.mean(processed ** 2)
            noise_power = np.mean(noise ** 2)
            
            if noise_power > 0:
                snr = 10 * np.log10(signal_power / noise_power)
            else:
                snr = float('inf')
            
            comparison = {
                'original_rms': float(original_rms),
                'processed_rms': float(processed_rms),
                'rms_change': float(processed_rms / original_rms if original_rms > 0 else 0),
                'snr_db': float(snr),
                'noise_reduction_percent': float((1 - noise_power / np.mean(original ** 2)) * 100)
            }
            
            return comparison
            
        except Exception as e:
            print(f"⚠️ Sifat solishtirish xatolik: {str(e)}")
            return {}


# Test funksiyasi
if __name__ == "__main__":
    # Preprocessor yaratish
    preprocessor = AudioPreprocessor(sample_rate=16000)
    
    print("AudioPreprocessor moduli ishga tushdi!")
    print("Mavjud funksiyalar:")
    print("  - remove_noise(): Shovqinni olib tashlash")
    print("  - normalize_audio(): Audio normalizatsiya")
    print("  - apply_highpass_filter(): Past chastotalarni tozalash")
    print("  - apply_lowpass_filter(): Yuqori chastotalarni tozalash")
    print("  - enhance_speech(): Nutq sifatini yaxshilash")
    print("  - preprocess_audio(): To'liq preprocessing pipeline")
