"""
Emotion Detection Module
=========================
Audio orqali spiker hissiy holatini aniqlash

Qo'llab-quvvatlanadigan emotsiyalar:
    - neutral: Neytral
    - happy: Quvonchli
    - sad: Xafa
    - angry: G'azablangan
    - stressed: Stressda
"""

import numpy as np
import librosa
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class EmotionPrediction:
    """
    Emotsiya bashorati ma'lumotlari
    
    Attributes:
        emotion (str): Emotsiya nomi
        confidence (float): Ishonch darajasi (0-1)
        start (float): Boshlanish vaqti (soniya)
        end (float): Tugash vaqti (soniya)
    """
    emotion: str
    confidence: float
    start: float
    end: float


class EmotionDetector:
    """
    Audio orqali emotsiyani aniqlash klassi
    
    Bu soddalashtirilgan versiya - audio xususiyatlariga asoslangan.
    Production uchun pre-trained ML model (HuggingFace) ishlatish tavsiya etiladi.
    """
    
    EMOTIONS = {
        'neutral': 'Neytral',
        'happy': 'Quvonchli',
        'sad': 'Xafa',
        'angry': 'G\'azablangan',
        'stressed': 'Stressda'
    }
    
    def __init__(self, sample_rate: int = 16000):
        """
        Args:
            sample_rate (int): Audio sample rate (Hz). Default: 16000
        """
        self.sample_rate = sample_rate
    
    def extract_audio_features(self, audio_data: np.ndarray) -> Dict[str, float]:
        """
        Audio xususiyatlarini ajratib olish
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            
        Returns:
            Dict[str, float]: Audio xususiyatlari
        """
        try:
            features = {}
            
            # 1. Pitch (balandlik) - ovoz balandligi
            pitches, magnitudes = librosa.piptrack(
                y=audio_data,
                sr=self.sample_rate,
                fmin=50,
                fmax=500
            )
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                features['pitch_mean'] = np.mean(pitch_values)
                features['pitch_std'] = np.std(pitch_values)
            else:
                features['pitch_mean'] = 0
                features['pitch_std'] = 0
            
            # 2. Energy (energiya) - ovoz kuchi
            energy = np.sum(audio_data ** 2) / len(audio_data)
            features['energy'] = energy
            
            # 3. Zero Crossing Rate - signal o'zgarishi tezligi
            zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
            features['zcr_mean'] = np.mean(zcr)
            features['zcr_std'] = np.std(zcr)
            
            # 4. Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(
                y=audio_data,
                sr=self.sample_rate
            )[0]
            features['spectral_centroid_mean'] = np.mean(spectral_centroids)
            
            # 5. MFCC features
            mfccs = librosa.feature.mfcc(
                y=audio_data,
                sr=self.sample_rate,
                n_mfcc=13
            )
            features['mfcc_mean'] = np.mean(mfccs)
            features['mfcc_std'] = np.std(mfccs)
            
            # 6. Tempo (tezlik)
            onset_env = librosa.onset.onset_strength(
                y=audio_data,
                sr=self.sample_rate
            )
            tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.sample_rate)[0]
            features['tempo'] = tempo
            
            return features
            
        except Exception as e:
            print(f"⚠️ Feature extraction xatolik: {str(e)}")
            return {}
    
    def predict_emotion_simple(self, features: Dict[str, float]) -> Tuple[str, float]:
        """
        Sodda qoidalarga asoslangan emotsiya bashorati
        
        Bu real ML model emas, balki heuristik yondashuv.
        Production uchun HuggingFace modelini ishlatish kerak.
        
        Args:
            features (Dict[str, float]): Audio xususiyatlari
            
        Returns:
            Tuple[str, float]: (emotion, confidence)
        """
        try:
            # Pitch va energy asosida sodda aniqlash
            pitch_mean = features.get('pitch_mean', 0)
            energy = features.get('energy', 0)
            zcr_mean = features.get('zcr_mean', 0)
            tempo = features.get('tempo', 0)
            
            # Normalizatsiya
            pitch_norm = min(pitch_mean / 200, 1.0)
            energy_norm = min(energy * 1000, 1.0)
            zcr_norm = min(zcr_mean * 10, 1.0)
            tempo_norm = min(tempo / 150, 1.0)
            
            # Sodda qoidalar
            scores = {
                'neutral': 0.5,
                'happy': 0.0,
                'sad': 0.0,
                'angry': 0.0,
                'stressed': 0.0
            }
            
            # Happy: yuqori pitch, yuqori energy
            if pitch_norm > 0.6 and energy_norm > 0.5:
                scores['happy'] = pitch_norm * 0.5 + energy_norm * 0.5
            
            # Sad: past pitch, past energy
            if pitch_norm < 0.4 and energy_norm < 0.4:
                scores['sad'] = (1 - pitch_norm) * 0.5 + (1 - energy_norm) * 0.5
            
            # Angry: yuqori energy, yuqori ZCR
            if energy_norm > 0.6 and zcr_norm > 0.5:
                scores['angry'] = energy_norm * 0.5 + zcr_norm * 0.5
            
            # Stressed: yuqori tempo, o'rta energy
            if tempo_norm > 0.7 and 0.3 < energy_norm < 0.7:
                scores['stressed'] = tempo_norm * 0.6 + energy_norm * 0.4
            
            # Eng yuqori score'ni tanlash
            emotion = max(scores, key=scores.get)
            confidence = scores[emotion]
            
            # Agar hech qanday aniq emotsiya yo'q bo'lsa, neutral
            if confidence < 0.3:
                emotion = 'neutral'
                confidence = 0.7
            
            return emotion, confidence
            
        except Exception as e:
            print(f"⚠️ Emotsiya bashorat qilishda xatolik: {str(e)}")
            return 'neutral', 0.5

    from typing import Optional
    def detect_emotion(
        self,
        audio_data: np.ndarray,
        start_time: float = 0.0,
        end_time: Optional[float] = None
    ) -> EmotionPrediction:
        """
        Audio segment uchun emotsiyani aniqlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            start_time (float): Boshlanish vaqti (soniya)
            end_time (float, optional): Tugash vaqti (soniya)
            
        Returns:
            EmotionPrediction: Emotsiya bashorati
        """
        if end_time is None:
            end_time = start_time + len(audio_data) / self.sample_rate
        
        try:
            # Audio xususiyatlarini ajratish
            features = self.extract_audio_features(audio_data)
            
            # Emotsiyani bashorat qilish
            emotion, confidence = self.predict_emotion_simple(features)
            
            return EmotionPrediction(
                emotion=emotion,
                confidence=confidence,
                start=start_time,
                end=end_time
            )
            
        except Exception as e:
            print(f"⚠️ Emotsiya aniqlashda xatolik: {str(e)}")
            return EmotionPrediction(
                emotion='neutral',
                confidence=0.5,
                start=start_time,
                end=end_time
            )
    
    def detect_emotions_segments(
        self,
        audio_data: np.ndarray,
        segments: List,
        segment_duration: float = 3.0
    ) -> List[EmotionPrediction]:
        """
        Ko'p segmentlar uchun emotsiyalarni aniqlash
        
        Args:
            audio_data (np.ndarray): Audio ma'lumotlar
            segments (List): Transkripsiya yoki spiker segmentlari
            segment_duration (float): Segment davomiyligi (soniya)
            
        Returns:
            List[EmotionPrediction]: Emotsiya bashoratlari ro'yxati
        """
        try:
            print("\n" + "="*50)
            print("😊 EMOTION DETECTION BOSHLANDI")
            print("="*50)
            
            predictions = []
            
            # Agar segmentlar berilgan bo'lsa, ulardan foydalanish
            if segments:
                print(f"  • Segmentlar soni: {len(segments)}")
                
                for seg in segments:
                    start_sample = int(seg.start * self.sample_rate)
                    end_sample = int(seg.end * self.sample_rate)
                    segment_audio = audio_data[start_sample:end_sample]
                    
                    if len(segment_audio) > 0:
                        prediction = self.detect_emotion(
                            segment_audio,
                            start_time=seg.start,
                            end_time=seg.end
                        )
                        predictions.append(prediction)
            
            # Agar segment yo'q bo'lsa, to'liq audiodni bo'laklarga ajratish
            else:
                total_duration = len(audio_data) / self.sample_rate
                segment_samples = int(segment_duration * self.sample_rate)
                
                num_segments = int(np.ceil(total_duration / segment_duration))
                print(f"  • Audio {num_segments} ta {segment_duration}s segmentga bo'linmoqda")
                
                for i in range(num_segments):
                    start_sample = i * segment_samples
                    end_sample = min(start_sample + segment_samples, len(audio_data))
                    segment_audio = audio_data[start_sample:end_sample]
                    
                    start_time = i * segment_duration
                    end_time = min(start_time + segment_duration, total_duration)
                    
                    prediction = self.detect_emotion(
                        segment_audio,
                        start_time=start_time,
                        end_time=end_time
                    )
                    predictions.append(prediction)
            
            # Statistika
            print(f"\n📊 Natijalar:")
            emotion_counts = {}
            for pred in predictions:
                emotion_counts[pred.emotion] = emotion_counts.get(pred.emotion, 0) + 1
            
            for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(predictions)) * 100
                emotion_uz = self.EMOTIONS.get(emotion, emotion)
                print(f"  • {emotion_uz}: {count} segment ({percentage:.1f}%)")
            
            print("="*50)
            print("✅ EMOTION DETECTION TUGALLANDI")
            print("="*50 + "\n")
            
            return predictions
            
        except Exception as e:
            print(f"⚠️ Emotion detection xatolik: {str(e)}")
            return []
    
    def format_emotions(
        self,
        predictions: List[EmotionPrediction],
        include_timestamps: bool = True
    ) -> str:
        """
        Emotsiya bashoratlarini formatlash
        
        Args:
            predictions (List[EmotionPrediction]): Bashoratlar ro'yxati
            include_timestamps (bool): Vaqt belgilarini qo'shish
            
        Returns:
            str: Formatlangan matn
        """
        lines = []
        
        for i, pred in enumerate(predictions, 1):
            emotion_uz = self.EMOTIONS.get(pred.emotion, pred.emotion)
            confidence_percent = pred.confidence * 100
            
            if include_timestamps:
                start = self._format_time(pred.start)
                end = self._format_time(pred.end)
                line = f"[{start} - {end}] {emotion_uz} ({confidence_percent:.1f}%)"
            else:
                line = f"Segment {i}: {emotion_uz} ({confidence_percent:.1f}%)"
            
            lines.append(line)
        
        return '\n'.join(lines)
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Vaqtni formatlash (MM:SS)
        
        Args:
            seconds (float): Soniyalar
            
        Returns:
            str: Formatlangan vaqt
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# Import uchun zarur
from typing import Optional


# Test funksiyasi
if __name__ == "__main__":
    print("EmotionDetector moduli ishga tushdi!")
    print(f"Qo'llab-quvvatlanadigan emotsiyalar:")
    for eng, uz in EmotionDetector.EMOTIONS.items():
        print(f"  - {eng}: {uz}")
