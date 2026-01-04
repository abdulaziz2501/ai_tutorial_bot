"""
Subtitles Package
=================
SRT va VTT formatlarida subtitrlar yaratish moduli

Qo'llab-quvvatlanadigan formatlar:
    - SRT (SubRip Subtitle)
    - VTT (WebVTT)
"""

from .srt_generator import SubtitleGenerator

__all__ = ['SubtitleGenerator']
