"""
Speaker Diarization Module
===========================
Audio ichida nechta kishi gapirayotganini aniqlash va
har bir gapni alohida spikerga bog'lash
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import cosine
import librosa


@dataclass
class SpeakerSegment:
    """
    Spiker segmenti ma'lumotlari
    
    Attributes:
        speaker_id (str): Spiker identifikatori (SPEAKER_01, SPEAKER_02, ...)
        start (float): Boshlanish vaqti (soniya)
        end (float): Tugash vaqti (soniya)
        confidence (float): Ishonch darajasi (0-1)
    """
    speaker_id: str
    start: float
    end: float
    confidence: float = 1.0


class SpeakerDiarizer:
    """
    Speaker Diarization - Kim gapirayotganini aniqlash
    
    Bu soddalashtirilgan versiya. Production uchun pyannote.audio
    yoki speechbrain ishlatish tavsiya etiladi.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Args:
            sample_rate (int): Audio sample rate (Hz). Default: 16000
        """
        self.sample_rate = sample_rate
        self.min_speakers = 1
        self.max_speakers = 10
    
    def extract_speaker_features(
        self,
        audio_data: np.ndarray,
        segment_duration: float = 1.0
    ) -> List[np.ndarray]:
        """
        Har bir segment uchun spiker xususiyatlarini ajratib olish
        (MFCC - Mel Frequency Cepstral Coefficients)
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            segment_duration (float): Segment davomiyligi (soniya). Default: 1.0
            
        Returns:
            List[np.ndarray]: Har bir segment uchun feature vector
        """
        try:
            segment_samples = int(segment_duration * self.sample_rate)
            features = []
            
            # Audiodni segmentlarga bo'lish
            num_segments = len(audio_data) // segment_samples
            
            for i in range(num_segments):
                start_idx = i * segment_samples
                end_idx = start_idx + segment_samples
                segment = audio_data[start_idx:end_idx]
                
                # MFCC xususiyatlarini ajratish
                mfcc = librosa.feature.mfcc(
                    y=segment,
                    sr=self.sample_rate,
                    n_mfcc=13
                )
                
                # O'rtacha qiymatni olish (har bir MFCC koeffitsiyenti uchun)
                mfcc_mean = np.mean(mfcc, axis=1)
                features.append(mfcc_mean)
            
            return features
            
        except Exception as e:
            print(f"⚠️ Feature extraction xatolik: {str(e)}")
            return []
    
    def cluster_speakers(
        self,
        features: List[np.ndarray],
        num_speakers: Optional[int] = None
    ) -> np.ndarray:
        """
        Feature'larni klasterlash orqali spikerlarni aniqlash
        
        Args:
            features (List[np.ndarray]): Feature vectorlar ro'yxati
            num_speakers (int, optional): Spikerlar soni (None = auto)
            
        Returns:
            np.ndarray: Har bir segment uchun spiker ID
        """
        try:
            if len(features) == 0:
                return np.array([])
            
            # Feature'larni array'ga aylantirish
            X = np.array(features)
            
            # Agar spiker soni berilmagan bo'lsa, auto aniqlash
            if num_speakers is None:
                # Sodda heuristik: segmentlar soniga qarab
                if len(X) < 10:
                    num_speakers = 1
                elif len(X) < 30:
                    num_speakers = 2
                else:
                    num_speakers = min(3, len(X) // 20)
            
            num_speakers = max(self.min_speakers, min(num_speakers, self.max_speakers, len(X)))
            
            # Agglomerative Clustering
            clustering = AgglomerativeClustering(
                n_clusters=num_speakers,
                metric='cosine',
                linkage='average'
            )
            
            labels = clustering.fit_predict(X)
            
            return labels
            
        except Exception as e:
            print(f"⚠️ Clustering xatolik: {str(e)}")
            return np.zeros(len(features), dtype=int)
    
    def diarize(
        self,
        audio_data: np.ndarray,
        num_speakers: Optional[int] = None,
        segment_duration: float = 1.0
    ) -> List[SpeakerSegment]:
        """
        Audio uchun speaker diarization amalga oshirish
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            num_speakers (int, optional): Spikerlar soni (None = auto)
            segment_duration (float): Segment davomiyligi (soniya). Default: 1.0
            
        Returns:
            List[SpeakerSegment]: Spiker segmentlari ro'yxati
        """
        try:
            print("\n" + "="*50)
            print("👥 SPEAKER DIARIZATION BOSHLANDI")
            print("="*50)
            
            total_duration = len(audio_data) / self.sample_rate
            print(f"  • Davomiylik: {total_duration:.2f} soniya")
            print(f"  • Segment davomiyligi: {segment_duration:.2f} soniya")
            
            # 1. Feature extraction
            print("\n🔍 Feature'lar ajratib olinmoqda...")
            features = self.extract_speaker_features(audio_data, segment_duration)
            
            if len(features) == 0:
                print("⚠️ Feature'lar ajratib olinmadi")
                return []
            
            print(f"✅ {len(features)} ta segment uchun feature'lar ajratildi")
            
            # 2. Clustering
            print("\n🎯 Spikerlar aniqlanmoqda...")
            labels = self.cluster_speakers(features, num_speakers)
            
            unique_speakers = len(np.unique(labels))
            print(f"✅ {unique_speakers} ta spiker aniqlandi")
            
            # 3. Segmentlarni yaratish
            segments = []
            segment_samples = int(segment_duration * self.sample_rate)
            
            current_speaker = labels[0]
            segment_start = 0.0
            
            for i in range(1, len(labels)):
                if labels[i] != current_speaker:
                    # Yangi spiker boshlandi
                    segment_end = i * segment_duration
                    
                    segment = SpeakerSegment(
                        speaker_id=f"SPEAKER_{current_speaker + 1:02d}",
                        start=segment_start,
                        end=segment_end,
                        confidence=0.85
                    )
                    segments.append(segment)
                    
                    current_speaker = labels[i]
                    segment_start = segment_end
            
            # Oxirgi segmentni qo'shish
            segment = SpeakerSegment(
                speaker_id=f"SPEAKER_{current_speaker + 1:02d}",
                start=segment_start,
                end=total_duration,
                confidence=0.85
            )
            segments.append(segment)
            
            # Statistika
            print(f"\n📊 Natijalar:")
            for i in range(unique_speakers):
                speaker_id = f"SPEAKER_{i + 1:02d}"
                speaker_segments = [s for s in segments if s.speaker_id == speaker_id]
                total_time = sum(s.end - s.start for s in speaker_segments)
                percentage = (total_time / total_duration) * 100
                
                print(f"  • {speaker_id}: {total_time:.2f}s ({percentage:.1f}%)")
            
            print("="*50)
            print("✅ SPEAKER DIARIZATION TUGALLANDI")
            print("="*50 + "\n")
            
            return segments
            
        except Exception as e:
            print(f"⚠️ Diarization xatolik: {str(e)}")
            return []
    
    def merge_short_segments(
        self,
        segments: List[SpeakerSegment],
        min_duration: float = 0.5
    ) -> List[SpeakerSegment]:
        """
        Qisqa segmentlarni qo'shni segmentlar bilan birlashtirish
        
        Args:
            segments (List[SpeakerSegment]): Segmentlar ro'yxati
            min_duration (float): Minimal segment davomiyligi (soniya)
            
        Returns:
            List[SpeakerSegment]: Birlashtirilgan segmentlar
        """
        if not segments:
            return []
        
        merged = []
        current = segments[0]
        
        for i in range(1, len(segments)):
            segment = segments[i]
            duration = current.end - current.start
            
            if duration < min_duration and segment.speaker_id == current.speaker_id:
                # Qo'shni segment bilan birlashtirish
                current.end = segment.end
            else:
                merged.append(current)
                current = segment
        
        merged.append(current)
        return merged
    
    def align_with_transcription(
        self,
        speaker_segments: List[SpeakerSegment],
        transcription_segments: List
    ) -> List[Dict]:
        """
        Spiker segmentlarini transkripsiya segmentlari bilan moslashtirish
        
        Args:
            speaker_segments (List[SpeakerSegment]): Spiker segmentlari
            transcription_segments (List): Transkripsiya segmentlari
            
        Returns:
            List[Dict]: Moshlashtirilgan segmentlar
        """
        aligned = []
        
        for trans_seg in transcription_segments:
            # Qaysi spiker bu vaqt oralig'ida gapirgan?
            trans_mid = (trans_seg.start + trans_seg.end) / 2
            
            for speaker_seg in speaker_segments:
                if speaker_seg.start <= trans_mid <= speaker_seg.end:
                    aligned.append({
                        'speaker': speaker_seg.speaker_id,
                        'text': trans_seg.text,
                        'start': trans_seg.start,
                        'end': trans_seg.end,
                        'confidence': (speaker_seg.confidence + trans_seg.confidence) / 2
                    })
                    break
            else:
                # Agar topilmasa, eng yaqin spikerni topish
                closest_speaker = min(
                    speaker_segments,
                    key=lambda s: min(abs(s.start - trans_mid), abs(s.end - trans_mid))
                )
                aligned.append({
                    'speaker': closest_speaker.speaker_id,
                    'text': trans_seg.text,
                    'start': trans_seg.start,
                    'end': trans_seg.end,
                    'confidence': trans_seg.confidence * 0.7  # Past confidence
                })
        
        return aligned
    
    def format_diarization(
        self,
        aligned_segments: List[Dict],
        include_timestamps: bool = True
    ) -> str:
        """
        Diarization natijasini formatlash
        
        Args:
            aligned_segments (List[Dict]): Moshlashtirilgan segmentlar
            include_timestamps (bool): Vaqt belgilarini qo'shish
            
        Returns:
            str: Formatlangan matn
        """
        lines = []
        current_speaker = None
        
        for seg in aligned_segments:
            speaker = seg['speaker']
            text = seg['text']
            
            if include_timestamps:
                start = self._format_time(seg['start'])
                end = self._format_time(seg['end'])
                
                if speaker != current_speaker:
                    lines.append(f"\n{speaker} [{start} --> {end}]:")
                    current_speaker = speaker
                
                lines.append(f"  {text}")
            else:
                if speaker != current_speaker:
                    lines.append(f"\n{speaker}:")
                    current_speaker = speaker
                
                lines.append(f"  {text}")
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Vaqtni formatlash (HH:MM:SS)
        
        Args:
            seconds (float): Soniyalar
            
        Returns:
            str: Formatlangan vaqt
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# Test funksiyasi
if __name__ == "__main__":
    print("SpeakerDiarizer moduli ishga tushdi!")
    print("Funksiyalar:")
    print("  - diarize(): Audioda spikerlarni aniqlash")
    print("  - align_with_transcription(): Spiker va transkripsiyani moslashtirish")
    print("  - format_diarization(): Natijani formatlash")
