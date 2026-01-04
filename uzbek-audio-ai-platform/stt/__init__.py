"""
Speech-to-Text (STT) Package
=============================
O'zbek tilidagi nutqni matnga aylantirish moduli

Qo'llab-quvvatlanadigan modellar:
    - Whisper (OpenAI)
"""

from .whisper_model import WhisperTranscriber

__all__ = ['WhisperTranscriber']
