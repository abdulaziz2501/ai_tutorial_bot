"""
Subtitle Generator Module
==========================
SRT va VTT formatlarida subtitrlar yaratish
"""

import os
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SubtitleEntry:
    """
    Subtitl yozuvi ma'lumotlari
    
    Attributes:
        index (int): Subtitl raqami
        start (float): Boshlanish vaqti (soniya)
        end (float): Tugash vaqti (soniya)
        text (str): Subtitl matni
        speaker (str, optional): Spiker nomi
    """
    index: int
    start: float
    end: float
    text: str
    speaker: Optional[str] = None


class SubtitleGenerator:
    """
    SRT va VTT formatlarida subtitrlar yaratish klassi
    """
    
    def __init__(self):
        """SubtitleGenerator yaratish"""
        pass
    
    def create_subtitle_entries(
        self,
        segments: List,
        include_speaker: bool = False
    ) -> List[SubtitleEntry]:
        """
        Segmentlardan subtitl yozuvlarini yaratish
        
        Args:
            segments (List): Transkripsiya yoki aligned segmentlar
            include_speaker (bool): Spiker nomini qo'shish
            
        Returns:
            List[SubtitleEntry]: Subtitl yozuvlari ro'yxati
        """
        entries = []
        
        for i, seg in enumerate(segments, 1):
            # Segment turini aniqlash
            if hasattr(seg, 'text'):
                # TranscriptionSegment
                text = seg.text
                start = seg.start
                end = seg.end
                speaker = None
            elif isinstance(seg, dict):
                # Dictionary format (aligned segments)
                text = seg.get('text', '')
                start = seg.get('start', 0.0)
                end = seg.get('end', 0.0)
                speaker = seg.get('speaker') if include_speaker else None
            else:
                continue
            
            # Subtitl matni
            if speaker and include_speaker:
                subtitle_text = f"{speaker}: {text}"
            else:
                subtitle_text = text
            
            entry = SubtitleEntry(
                index=i,
                start=start,
                end=end,
                text=subtitle_text.strip()
            )
            entries.append(entry)
        
        return entries
    
    def generate_srt(
        self,
        entries: List[SubtitleEntry],
        output_path: str
    ) -> str:
        """
        SRT format subtitl yaratish
        
        Format:
            1
            00:00:00,000 --> 00:00:05,000
            Subtitl matni birinchi
            
            2
            00:00:05,000 --> 00:00:10,000
            Subtitl matni ikkinchi
        
        Args:
            entries (List[SubtitleEntry]): Subtitl yozuvlari
            output_path (str): Chiqish fayl yo'li
            
        Returns:
            str: Yaratilgan fayl yo'li
        """
        try:
            print(f"\n📝 SRT subtitl yaratilmoqda...")
            
            # Papkani yaratish
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # SRT mazmunini yaratish
            srt_content = []
            
            for entry in entries:
                # Subtitl raqami
                srt_content.append(str(entry.index))
                
                # Vaqt oralig'i
                start_time = self._format_srt_time(entry.start)
                end_time = self._format_srt_time(entry.end)
                srt_content.append(f"{start_time} --> {end_time}")
                
                # Matn
                srt_content.append(entry.text)
                
                # Bo'sh qator
                srt_content.append("")
            
            # Faylga yozish
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(srt_content))
            
            print(f"✅ SRT subtitl yaratildi: {os.path.basename(output_path)}")
            print(f"  • Subtitllar soni: {len(entries)}")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"SRT yaratishda xatolik: {str(e)}")
    
    def generate_vtt(
        self,
        entries: List[SubtitleEntry],
        output_path: str
    ) -> str:
        """
        VTT (WebVTT) format subtitl yaratish
        
        Format:
            WEBVTT
            
            1
            00:00:00.000 --> 00:00:05.000
            Subtitl matni birinchi
            
            2
            00:00:05.000 --> 00:00:10.000
            Subtitl matni ikkinchi
        
        Args:
            entries (List[SubtitleEntry]): Subtitl yozuvlari
            output_path (str): Chiqish fayl yo'li
            
        Returns:
            str: Yaratilgan fayl yo'li
        """
        try:
            print(f"\n📝 VTT subtitl yaratilmoqda...")
            
            # Papkani yaratish
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # VTT mazmunini yaratish
            vtt_content = ["WEBVTT", ""]
            
            for entry in entries:
                # Subtitl raqami
                vtt_content.append(str(entry.index))
                
                # Vaqt oralig'i
                start_time = self._format_vtt_time(entry.start)
                end_time = self._format_vtt_time(entry.end)
                vtt_content.append(f"{start_time} --> {end_time}")
                
                # Matn
                vtt_content.append(entry.text)
                
                # Bo'sh qator
                vtt_content.append("")
            
            # Faylga yozish
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(vtt_content))
            
            print(f"✅ VTT subtitl yaratildi: {os.path.basename(output_path)}")
            print(f"  • Subtitllar soni: {len(entries)}")
            
            return output_path
            
        except Exception as e:
            raise Exception(f"VTT yaratishda xatolik: {str(e)}")
    
    def generate_both(
        self,
        segments: List,
        output_dir: str,
        filename: str = "subtitles",
        include_speaker: bool = False
    ) -> tuple:
        """
        Bir vaqtning o'zida SRT va VTT yaratish
        
        Args:
            segments (List): Transkripsiya segmentlari
            output_dir (str): Chiqish papkasi
            filename (str): Fayl nomi (kengaytmasiz)
            include_speaker (bool): Spiker nomini qo'shish
            
        Returns:
            tuple: (srt_path, vtt_path)
        """
        print("\n" + "="*50)
        print("📝 SUBTITRLAR YARATILMOQDA")
        print("="*50)
        
        # Subtitl yozuvlarini yaratish
        entries = self.create_subtitle_entries(segments, include_speaker)
        
        if not entries:
            print("⚠️ Subtitl yozuvlari topilmadi")
            return None, None
        
        # SRT yaratish
        srt_path = os.path.join(output_dir, f"{filename}.srt")
        self.generate_srt(entries, srt_path)
        
        # VTT yaratish
        vtt_path = os.path.join(output_dir, f"{filename}.vtt")
        self.generate_vtt(entries, vtt_path)
        
        print("="*50)
        print("✅ SUBTITRLAR TAYYOR")
        print("="*50 + "\n")
        
        return srt_path, vtt_path
    
    @staticmethod
    def _format_srt_time(seconds: float) -> str:
        """
        SRT format uchun vaqtni formatlash (HH:MM:SS,mmm)
        
        Args:
            seconds (float): Soniyalar
            
        Returns:
            str: Formatlangan vaqt
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    @staticmethod
    def _format_vtt_time(seconds: float) -> str:
        """
        VTT format uchun vaqtni formatlash (HH:MM:SS.mmm)
        
        Args:
            seconds (float): Soniyalar
            
        Returns:
            str: Formatlangan vaqt
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    def merge_short_subtitles(
        self,
        entries: List[SubtitleEntry],
        max_chars: int = 80,
        max_duration: float = 7.0
    ) -> List[SubtitleEntry]:
        """
        Qisqa subtitllarni birlashtirish (o'qish uchun qulay)
        
        Args:
            entries (List[SubtitleEntry]): Subtitl yozuvlari
            max_chars (int): Maksimal belgilar soni
            max_duration (float): Maksimal davomiylik (soniya)
            
        Returns:
            List[SubtitleEntry]: Birlashtirilgan subtitllar
        """
        if not entries:
            return []
        
        merged = []
        current = entries[0]
        current_index = 1
        
        for i in range(1, len(entries)):
            next_entry = entries[i]
            
            # Birlashtirilgan matn
            combined_text = f"{current.text} {next_entry.text}"
            combined_duration = next_entry.end - current.start
            
            # Birlashtirish shartlari
            can_merge = (
                len(combined_text) <= max_chars and
                combined_duration <= max_duration
            )
            
            if can_merge:
                # Birlashtiramiz
                current = SubtitleEntry(
                    index=current_index,
                    start=current.start,
                    end=next_entry.end,
                    text=combined_text,
                    speaker=current.speaker
                )
            else:
                # Joriyni saqlaymiz va yangisiga o'tamiz
                merged.append(current)
                current_index += 1
                current = SubtitleEntry(
                    index=current_index,
                    start=next_entry.start,
                    end=next_entry.end,
                    text=next_entry.text,
                    speaker=next_entry.speaker
                )
        
        # Oxirgi yozuvni qo'shish
        merged.append(current)
        
        return merged


# Test funksiyasi
if __name__ == "__main__":
    print("SubtitleGenerator moduli ishga tushdi!")
    print("Qo'llab-quvvatlanadigan formatlar:")
    print("  - SRT (SubRip Subtitle)")
    print("  - VTT (WebVTT)")
    print("\nFunksiyalar:")
    print("  - generate_srt(): SRT subtitl yaratish")
    print("  - generate_vtt(): VTT subtitl yaratish")
    print("  - generate_both(): Ikkala formatni yaratish")
