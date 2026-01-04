"""
Batch Audio Processor
=====================
Bir nechta audio/video faylni parallel qayta ishlash

Foydalanish:
    python batch_processor.py --input-dir ./audio_files --output-dir ./results
"""

import os
import argparse
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import concurrent.futures
from tqdm import tqdm

from audio_utils import AudioLoader, AudioPreprocessor, SilenceRemover
from stt import WhisperTranscriber
from diarization import SpeakerDiarizer
from emotion import EmotionDetector
from subtitles import SubtitleGenerator


class BatchAudioProcessor:
    """
    Bir nechta audio faylni parallel qayta ishlash
    """
    
    def __init__(
        self,
        whisper_model: str = 'medium',
        language: str = 'uz',
        enable_preprocessing: bool = True,
        enable_diarization: bool = True,
        enable_emotion: bool = True,
        enable_subtitles: bool = True,
        max_workers: int = 2
    ):
        """
        Args:
            whisper_model (str): Whisper model nomi
            language (str): Til kodi
            enable_preprocessing (bool): Preprocessing yoqish
            enable_diarization (bool): Speaker diarization yoqish
            enable_emotion (bool): Emotion detection yoqish
            enable_subtitles (bool): Subtitrlar yaratish
            max_workers (int): Parallel worker'lar soni (CPU uchun 2-3 tavsiya)
        """
        self.whisper_model = whisper_model
        self.language = language
        self.enable_preprocessing = enable_preprocessing
        self.enable_diarization = enable_diarization
        self.enable_emotion = enable_emotion
        self.enable_subtitles = enable_subtitles
        self.max_workers = max_workers
        
        print(f"\n{'='*60}")
        print("🚀 BATCH AUDIO PROCESSOR")
        print(f"{'='*60}")
        print(f"  • Whisper Model: {whisper_model}")
        print(f"  • Til: {language}")
        print(f"  • Preprocessing: {'✅' if enable_preprocessing else '❌'}")
        print(f"  • Speaker Diarization: {'✅' if enable_diarization else '❌'}")
        print(f"  • Emotion Detection: {'✅' if enable_emotion else '❌'}")
        print(f"  • Subtitrlar: {'✅' if enable_subtitles else '❌'}")
        print(f"  • Parallel Workers: {max_workers}")
        print(f"{'='*60}\n")
        
        # Modellarni bir marta yuklash
        print("📥 Modellar yuklanmoqda...")
        self.loader = AudioLoader()
        self.preprocessor = AudioPreprocessor()
        self.remover = SilenceRemover()
        self.transcriber = WhisperTranscriber(
            model_name=whisper_model,
            language=language
        )
        self.transcriber.load_model()  # Oldindan yuklash
        
        if enable_diarization:
            self.diarizer = SpeakerDiarizer()
        
        if enable_emotion:
            self.detector = EmotionDetector()
        
        if enable_subtitles:
            self.generator = SubtitleGenerator()
        
        print("✅ Barcha modellar yuklandi!\n")
    
    def process_single_file(
        self,
        input_path: str,
        output_dir: str
    ) -> Dict:
        """
        Bitta faylni qayta ishlash
        
        Args:
            input_path (str): Kirish fayl yo'li
            output_dir (str): Chiqish papkasi
            
        Returns:
            Dict: Natijalar
        """
        filename = Path(input_path).stem
        file_output_dir = os.path.join(output_dir, filename)
        os.makedirs(file_output_dir, exist_ok=True)
        
        result = {
            'filename': Path(input_path).name,
            'status': 'processing',
            'start_time': datetime.now().isoformat(),
            'errors': []
        }
        
        try:
            # 1. Audio yuklash
            print(f"\n📂 [{filename}] Audio yuklanmoqda...")
            audio_data, sr = self.loader.load_audio(input_path)
            result['duration'] = len(audio_data) / sr
            
            # 2. Preprocessing
            if self.enable_preprocessing:
                print(f"🔧 [{filename}] Preprocessing...")
                audio_data = self.preprocessor.preprocess_audio(
                    audio_data,
                    remove_noise=True,
                    normalize=True,
                    enhance_speech=True
                )
                
                audio_data, _ = self.remover.remove_silence(audio_data)
                
                # Tozalangan audiodni saqlash
                clean_path = os.path.join(file_output_dir, f"{filename}_clean.wav")
                self.loader.save_audio(audio_data, clean_path, sr)
                result['clean_audio'] = clean_path
            
            # 3. Transkripsiya
            print(f"📝 [{filename}] Transkripsiya...")
            segments = self.transcriber.transcribe_with_timestamps(
                audio_data,
                sample_rate=sr,
                language=self.language
            )
            result['segments_count'] = len(segments)
            
            # Transkripsiyani saqlash
            transcript_path = os.path.join(file_output_dir, f"{filename}_transcript.txt")
            self.transcriber.save_transcript(segments, transcript_path)
            result['transcript'] = transcript_path
            
            # 4. Speaker Diarization
            if self.enable_diarization:
                print(f"👥 [{filename}] Speaker diarization...")
                speaker_segments = self.diarizer.diarize(audio_data)
                aligned = self.diarizer.align_with_transcription(
                    speaker_segments,
                    segments
                )
                
                # Spikerlar bo'yicha matnni saqlash
                diarization_path = os.path.join(file_output_dir, f"{filename}_speakers.txt")
                formatted = self.diarizer.format_diarization(aligned)
                with open(diarization_path, 'w', encoding='utf-8') as f:
                    f.write(formatted)
                result['diarization'] = diarization_path
                result['speakers_count'] = len(set(seg.speaker_id for seg in speaker_segments))
            else:
                aligned = segments
            
            # 5. Emotion Detection
            if self.enable_emotion:
                print(f"😊 [{filename}] Emotion detection...")
                emotions = self.detector.detect_emotions_segments(
                    audio_data,
                    segments
                )
                
                # Emotsiyalarni saqlash
                emotion_path = os.path.join(file_output_dir, f"{filename}_emotions.txt")
                formatted_emotions = self.detector.format_emotions(emotions)
                with open(emotion_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_emotions)
                result['emotions'] = emotion_path
            
            # 6. Subtitrlar
            if self.enable_subtitles:
                print(f"📝 [{filename}] Subtitrlar yaratilmoqda...")
                srt_path, vtt_path = self.generator.generate_both(
                    aligned,
                    file_output_dir,
                    filename=filename,
                    include_speaker=self.enable_diarization
                )
                result['srt'] = srt_path
                result['vtt'] = vtt_path
            
            # To'liq hisobot
            report_path = os.path.join(file_output_dir, f"{filename}_report.txt")
            self._create_report(result, report_path, aligned, emotions if self.enable_emotion else None)
            result['report'] = report_path
            
            result['status'] = 'success'
            result['end_time'] = datetime.now().isoformat()
            
            print(f"✅ [{filename}] Tugallandi!")
            
        except Exception as e:
            result['status'] = 'failed'
            result['errors'].append(str(e))
            result['end_time'] = datetime.now().isoformat()
            print(f"❌ [{filename}] Xatolik: {str(e)}")
        
        return result
    
    def _create_report(self, result: Dict, report_path: str, segments, emotions=None):
        """To'liq hisobot yaratish"""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("AUDIO PROCESSING REPORT\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Fayl: {result['filename']}\n")
            f.write(f"Davomiylik: {result.get('duration', 0):.2f} soniya\n")
            f.write(f"Segmentlar: {result.get('segments_count', 0)} ta\n")
            if 'speakers_count' in result:
                f.write(f"Spikerlar: {result['speakers_count']} ta\n")
            f.write(f"\nStatus: {result['status']}\n")
            f.write(f"Vaqt: {result['start_time']} - {result['end_time']}\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write("TRANSKRIPSIYA\n")
            f.write("="*60 + "\n\n")
            
            if hasattr(segments, '__iter__'):
                for seg in segments:
                    if isinstance(seg, dict):
                        speaker = seg.get('speaker', '')
                        text = seg.get('text', '')
                        if speaker:
                            f.write(f"{speaker}: {text}\n")
                        else:
                            f.write(f"{text}\n")
                    else:
                        f.write(f"{seg.text}\n")
            
            if emotions:
                f.write("\n" + "="*60 + "\n")
                f.write("EMOTSIYALAR\n")
                f.write("="*60 + "\n\n")
                
                emotion_counts = {}
                for pred in emotions:
                    emotion_counts[pred.emotion] = emotion_counts.get(pred.emotion, 0) + 1
                
                for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(emotions)) * 100
                    f.write(f"{emotion}: {percentage:.1f}% ({count} segment)\n")
    
    def process_batch(
        self,
        input_files: List[str],
        output_dir: str
    ) -> List[Dict]:
        """
        Bir nechta faylni parallel qayta ishlash
        
        Args:
            input_files (List[str]): Kirish fayllar ro'yxati
            output_dir (str): Chiqish papkasi
            
        Returns:
            List[Dict]: Natijalar ro'yxati
        """
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"📊 BATCH PROCESSING")
        print(f"{'='*60}")
        print(f"  • Fayllar soni: {len(input_files)}")
        print(f"  • Chiqish papkasi: {output_dir}")
        print(f"  • Parallel workers: {self.max_workers}")
        print(f"{'='*60}\n")
        
        results = []
        
        # Parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Barcha tasklar submit qilish
            future_to_file = {
                executor.submit(self.process_single_file, file_path, output_dir): file_path
                for file_path in input_files
            }
            
            # Progress bar
            with tqdm(total=len(input_files), desc="Processing files") as pbar:
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        print(f"\n❌ {Path(file_path).name} - Xatolik: {str(e)}")
                        results.append({
                            'filename': Path(file_path).name,
                            'status': 'failed',
                            'errors': [str(e)]
                        })
                    pbar.update(1)
        
        # Summary yaratish
        self._create_summary(results, output_dir)
        
        return results
    
    def _create_summary(self, results: List[Dict], output_dir: str):
        """Umumiy natijalar xulosasi"""
        summary_path = os.path.join(output_dir, 'batch_summary.json')
        
        summary = {
            'total_files': len(results),
            'successful': sum(1 for r in results if r['status'] == 'success'),
            'failed': sum(1 for r in results if r['status'] == 'failed'),
            'results': results
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print("📊 BATCH PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"  • Jami fayllar: {summary['total_files']}")
        print(f"  • Muvaffaqiyatli: {summary['successful']} ✅")
        print(f"  • Xato: {summary['failed']} ❌")
        print(f"  • Summary fayl: {summary_path}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Batch Audio Processing - bir nechta faylni qayta ishlash'
    )
    
    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Kirish audio fayllar papkasi'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./batch_outputs',
        help='Chiqish papkasi (default: ./batch_outputs)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='medium',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Whisper model (default: medium)'
    )
    
    parser.add_argument(
        '--language',
        type=str,
        default='uz',
        help='Til kodi (default: uz)'
    )
    
    parser.add_argument(
        '--workers',
        type=int,
        default=2,
        help='Parallel workers soni (default: 2, CPU uchun 2-3 optimal)'
    )
    
    parser.add_argument(
        '--no-preprocessing',
        action='store_true',
        help='Preprocessing o\'chirish'
    )
    
    parser.add_argument(
        '--no-diarization',
        action='store_true',
        help='Speaker diarization o\'chirish'
    )
    
    parser.add_argument(
        '--no-emotion',
        action='store_true',
        help='Emotion detection o\'chirish'
    )
    
    parser.add_argument(
        '--no-subtitles',
        action='store_true',
        help='Subtitrlar yaratishni o\'chirish'
    )
    
    args = parser.parse_args()
    
    # Kirish fayllarni topish
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ Papka topilmadi: {input_dir}")
        return
    
    # Qo'llab-quvvatlanadigan formatlar
    audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.mp4', '.avi', '.mov', '.mkv']
    input_files = [
        str(f) for f in input_dir.iterdir()
        if f.suffix.lower() in audio_extensions
    ]
    
    if not input_files:
        print(f"❌ Audio fayllar topilmadi: {input_dir}")
        return
    
    print(f"\n✅ {len(input_files)} ta fayl topildi")
    
    # Batch processor yaratish
    processor = BatchAudioProcessor(
        whisper_model=args.model,
        language=args.language,
        enable_preprocessing=not args.no_preprocessing,
        enable_diarization=not args.no_diarization,
        enable_emotion=not args.no_emotion,
        enable_subtitles=not args.no_subtitles,
        max_workers=args.workers
    )
    
    # Batch processing
    results = processor.process_batch(input_files, args.output_dir)
    
    print("\n✅ Batch processing tugallandi!")


if __name__ == "__main__":
    main()
