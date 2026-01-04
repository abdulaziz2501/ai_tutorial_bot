"""
Emotion Detection Package
==========================
Audio orqali hissiy holatni aniqlash moduli

Qo'llab-quvvatlanadigan emotsiyalar:
    - neutral (neytral)
    - happy (quvonchli)
    - sad (xafa)
    - angry (g'azablangan)
    - stressed (stressda)
"""

from .emotion_model import EmotionDetector

__all__ = ['EmotionDetector']
