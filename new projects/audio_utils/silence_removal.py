"""
Silence Removal Module
======================
Audio ichidagi sukut (jimlik) qismlarini aniqlash va kesish
"""

import numpy as np
import librosa
from typing import List, Tuple


class SilenceRemover:
    """
    Audio ichidagi sukut qismlarini aniqlash va olib tashlash klassi
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Args:
            sample_rate (int): Audio sample rate (Hz). Default: 16000
        """
        self.sample_rate = sample_rate
    
    def detect_silence(
        self, 
        audio_data: np.ndarray,
        threshold_db: float = -40.0,
        min_silence_duration: float = 0.5
    ) -> List[Tuple[float, float]]:
        """
        Sukut qismlarini aniqlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            threshold_db (float): Sukut chegarasi (dB). Default: -40.0
            min_silence_duration (float): Minimal sukut davomiyligi (soniya). Default: 0.5
            
        Returns:
            List[Tuple[float, float]]: Sukut intervallari (boshlanish, tugash) soniyalarda
        """
        try:
            print(f"🔍 Sukut qismlari aniqlanmoqda (threshold: {threshold_db} dB)...")
            
            # Frame davomiyligi (512 sample = ~32ms @ 16kHz)
            frame_length = 512
            hop_length = frame_length // 2
            
            # RMS energy hisoblash
            rms = librosa.feature.rms(
                y=audio_data,
                frame_length=frame_length,
                hop_length=hop_length
            )[0]
            
            # dB ga o'tkazish
            rms_db = librosa.amplitude_to_db(rms, ref=np.max)
            
            # Sukut framelarini aniqlash
            silence_frames = rms_db < threshold_db
            
            # Frame indekslarini vaqtga aylantirish
            times = librosa.frames_to_time(
                np.arange(len(silence_frames)),
                sr=self.sample_rate,
                hop_length=hop_length
            )
            
            # Sukut intervallarini aniqlash
            silence_intervals = []
            in_silence = False
            silence_start = 0.0
            
            for i, is_silent in enumerate(silence_frames):
                if is_silent and not in_silence:
                    # Sukut boshlandi
                    silence_start = times[i]
                    in_silence = True
                elif not is_silent and in_silence:
                    # Sukut tugadi
                    silence_end = times[i]
                    duration = silence_end - silence_start
                    
                    # Faqat minimal davomiylikdan katta sukutlarni qo'shish
                    if duration >= min_silence_duration:
                        silence_intervals.append((silence_start, silence_end))
                    
                    in_silence = False
            
            # Oxirgi sukut intervali
            if in_silence:
                silence_end = times[-1]
                duration = silence_end - silence_start
                if duration >= min_silence_duration:
                    silence_intervals.append((silence_start, silence_end))
            
            print(f"✅ {len(silence_intervals)} ta sukut qismi aniqlandi")
            
            return silence_intervals
            
        except Exception as e:
            print(f"⚠️ Sukut aniqlashda xatolik: {str(e)}")
            return []
    
    def remove_silence(
        self,
        audio_data: np.ndarray,
        threshold_db: float = -40.0,
        min_silence_duration: float = 0.5,
        keep_silence_duration: float = 0.1
    ) -> Tuple[np.ndarray, List[Tuple[float, float]]]:
        """
        Sukut qismlarini olib tashlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            threshold_db (float): Sukut chegarasi (dB). Default: -40.0
            min_silence_duration (float): Minimal sukut davomiyligi (soniya). Default: 0.5
            keep_silence_duration (float): Qoldiriladigan sukut (soniya). Default: 0.1
            
        Returns:
            Tuple[np.ndarray, List]: (Tozalangan audio, olib tashlangan intervallar)
        """
        try:
            print("\n" + "="*50)
            print("✂️ SUKUT QISMLARI OLIB TASHLANMOQDA")
            print("="*50)
            
            # Sukut intervallarini aniqlash
            silence_intervals = self.detect_silence(
                audio_data,
                threshold_db=threshold_db,
                min_silence_duration=min_silence_duration
            )
            
            if not silence_intervals:
                print("ℹ️ Sukut qismlari topilmadi")
                return audio_data, []
            
            # Audio segmentlarini ajratish (sukutdan tashqari qismlar)
            segments = []
            removed_intervals = []
            
            prev_end = 0.0
            total_duration = len(audio_data) / self.sample_rate
            
            for start, end in silence_intervals:
                # Sukutdan oldingi qismni qo'shish
                if start > prev_end:
                    start_sample = int(prev_end * self.sample_rate)
                    end_sample = int(start * self.sample_rate)
                    segments.append(audio_data[start_sample:end_sample])
                
                # Oz miqdorda sukutni qoldirish (tabiiy eshitish uchun)
                keep_samples = int(keep_silence_duration * self.sample_rate)
                start_sample = int(start * self.sample_rate)
                end_sample = min(int(end * self.sample_rate), len(audio_data))
                
                # Sukutning boshidan va oxiridan oz qoldirish
                if keep_samples > 0 and (end_sample - start_sample) > keep_samples * 2:
                    segments.append(audio_data[start_sample:start_sample + keep_samples])
                    segments.append(audio_data[end_sample - keep_samples:end_sample])
                    removed_intervals.append((start + keep_silence_duration, end - keep_silence_duration))
                else:
                    removed_intervals.append((start, end))
                
                prev_end = end
            
            # Oxirgi qismni qo'shish
            if prev_end < total_duration:
                start_sample = int(prev_end * self.sample_rate)
                segments.append(audio_data[start_sample:])
            
            # Segmentlarni birlashtirish
            if segments:
                cleaned_audio = np.concatenate(segments)
            else:
                cleaned_audio = audio_data
            
            # Statistika
            original_duration = len(audio_data) / self.sample_rate
            cleaned_duration = len(cleaned_audio) / self.sample_rate
            removed_duration = original_duration - cleaned_duration
            removed_percent = (removed_duration / original_duration) * 100
            
            print(f"\n📊 Statistika:")
            print(f"  • Asl davomiylik: {original_duration:.2f} soniya")
            print(f"  • Tozalangan davomiylik: {cleaned_duration:.2f} soniya")
            print(f"  • Olib tashlangan: {removed_duration:.2f} soniya ({removed_percent:.1f}%)")
            
            print("="*50)
            print("✅ SUKUT TOZALASH TUGALLANDI")
            print("="*50 + "\n")
            
            return cleaned_audio, removed_intervals
            
        except Exception as e:
            print(f"⚠️ Sukut olib tashlaganda xatolik: {str(e)}")
            return audio_data, []
    
    def split_on_silence(
        self,
        audio_data: np.ndarray,
        threshold_db: float = -40.0,
        min_silence_duration: float = 0.5,
        min_segment_duration: float = 1.0
    ) -> List[Tuple[np.ndarray, float, float]]:
        """
        Audiodni sukut qismlariga ko'ra bo'laklarga ajratish
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            threshold_db (float): Sukut chegarasi (dB). Default: -40.0
            min_silence_duration (float): Minimal sukut davomiyligi (soniya). Default: 0.5
            min_segment_duration (float): Minimal segment davomiyligi (soniya). Default: 1.0
            
        Returns:
            List[Tuple[np.ndarray, float, float]]: (segment_audio, start_time, end_time)
        """
        try:
            print("\n" + "="*50)
            print("✂️ AUDIO BO'LAKLARGA AJRATILMOQDA")
            print("="*50)
            
            # Sukut intervallarini aniqlash
            silence_intervals = self.detect_silence(
                audio_data,
                threshold_db=threshold_db,
                min_silence_duration=min_silence_duration
            )
            
            segments = []
            prev_end = 0.0
            total_duration = len(audio_data) / self.sample_rate
            
            for start, end in silence_intervals:
                # Sukutdan oldingi segmentni qo'shish
                if start > prev_end:
                    segment_start = prev_end
                    segment_end = start
                    segment_duration = segment_end - segment_start
                    
                    # Faqat minimal davomiylikdan katta segmentlarni qo'shish
                    if segment_duration >= min_segment_duration:
                        start_sample = int(segment_start * self.sample_rate)
                        end_sample = int(segment_end * self.sample_rate)
                        segment_audio = audio_data[start_sample:end_sample]
                        
                        segments.append((segment_audio, segment_start, segment_end))
                
                prev_end = end
            
            # Oxirgi segmentni qo'shish
            if prev_end < total_duration:
                segment_duration = total_duration - prev_end
                if segment_duration >= min_segment_duration:
                    start_sample = int(prev_end * self.sample_rate)
                    segment_audio = audio_data[start_sample:]
                    segments.append((segment_audio, prev_end, total_duration))
            
            print(f"✅ {len(segments)} ta segment yaratildi")
            
            for i, (seg_audio, seg_start, seg_end) in enumerate(segments, 1):
                duration = seg_end - seg_start
                print(f"  Segment {i}: {seg_start:.2f}s - {seg_end:.2f}s (davomiyligi: {duration:.2f}s)")
            
            print("="*50 + "\n")
            
            return segments
            
        except Exception as e:
            print(f"⚠️ Bo'laklarga ajratishda xatolik: {str(e)}")
            return [(audio_data, 0.0, len(audio_data) / self.sample_rate)]
    
    def get_speech_segments(
        self,
        audio_data: np.ndarray,
        threshold_db: float = -40.0
    ) -> List[Tuple[float, float]]:
        """
        Nutq segmentlarini (sukut bo'lmagan qismlar) aniqlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            threshold_db (float): Sukut chegarasi (dB). Default: -40.0
            
        Returns:
            List[Tuple[float, float]]: Nutq intervallari (boshlanish, tugash)
        """
        try:
            # Sukut intervallarini aniqlash
            silence_intervals = self.detect_silence(
                audio_data,
                threshold_db=threshold_db,
                min_silence_duration=0.3  # Qisqaroq sukutlarni ham aniqlash
            )
            
            # Nutq segmentlarini hisoblash (sukutdan tashqari qismlar)
            speech_segments = []
            prev_end = 0.0
            total_duration = len(audio_data) / self.sample_rate
            
            for start, end in silence_intervals:
                if start > prev_end:
                    speech_segments.append((prev_end, start))
                prev_end = end
            
            # Oxirgi qismni qo'shish
            if prev_end < total_duration:
                speech_segments.append((prev_end, total_duration))
            
            return speech_segments
            
        except Exception as e:
            print(f"⚠️ Nutq segmentlarini aniqlashda xatolik: {str(e)}")
            return [(0.0, len(audio_data) / self.sample_rate)]


# Test funksiyasi
if __name__ == "__main__":
    # Silence Remover yaratish
    remover = SilenceRemover(sample_rate=16000)
    
    print("SilenceRemover moduli ishga tushdi!")
    print("Mavjud funksiyalar:")
    print("  - detect_silence(): Sukut qismlarini aniqlash")
    print("  - remove_silence(): Sukut qismlarini olib tashlash")
    print("  - split_on_silence(): Audiodni bo'laklarga ajratish")
    print("  - get_speech_segments(): Nutq segmentlarini aniqlash")
