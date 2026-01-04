"""
Uzbek Speech-to-Text & Audio Intelligence Platform
===================================================
Streamlit Web Interface

Funksiyalar:
    - Audio/video yuklash
    - Audio preprocessing (shovqin tozalash, sukut kesish)
    - Speech-to-Text (Whisper)
    - Speaker Diarization
    - Emotion Detection
    - Subtitle Generation (SRT/VTT)
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
import numpy as np
import time

# Modullarni import qilish
from audio_utils import AudioLoader, AudioPreprocessor, SilenceRemover
from stt import WhisperTranscriber
from diarization import SpeakerDiarizer
from emotion import EmotionDetector
from subtitles import SubtitleGenerator


# Streamlit konfiguratsiya
st.set_page_config(
    page_title="🎙️ Uzbek AI Audio Platform",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .stDownloadButton button {
        background-color: #1f77b4;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# Sessiya state'larini yaratish
if 'audio_loaded' not in st.session_state:
    st.session_state.audio_loaded = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'sample_rate' not in st.session_state:
    st.session_state.sample_rate = 16000
if 'processed_audio' not in st.session_state:
    st.session_state.processed_audio = None
if 'transcription_segments' not in st.session_state:
    st.session_state.transcription_segments = None
if 'speaker_segments' not in st.session_state:
    st.session_state.speaker_segments = None
if 'emotion_predictions' not in st.session_state:
    st.session_state.emotion_predictions = None
if 'aligned_segments' not in st.session_state:
    st.session_state.aligned_segments = None


def main():
    """Asosiy funksiya"""
    
    # Header
    st.markdown('<h1 class="main-header">🎙️ Uzbek Audio AI Platform</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar - Sozlamalar
    with st.sidebar:
        st.header("⚙️ Sozlamalar")
        
        # Whisper model tanlash
        st.subheader("🤖 Speech-to-Text Model")
        whisper_model = st.selectbox(
            "Whisper Model",
            options=['tiny', 'base', 'small', 'medium', 'large'],
            index=2,
            help="large - eng aniq, lekin sekin"
        )
        
        # Til tanlash
        language = st.selectbox(
            "Til",
            options=['uz', 'ru', 'en'],
            index=0,
            help="Transkripsiya tili"
        )
        
        st.markdown("---")
        
        # Preprocessing sozlamalari
        st.subheader("🔧 Preprocessing")
        
        enable_noise_reduction = st.checkbox("Shovqin tozalash", value=True)
        enable_silence_removal = st.checkbox("Sukut kesish", value=True)
        enable_normalization = st.checkbox("Audio normalizatsiya", value=True)
        
        st.markdown("---")
        
        # Qo'shimcha funksiyalar
        st.subheader("🎯 Qo'shimcha Funksiyalar")
        
        enable_diarization = st.checkbox("Speaker Diarization", value=True)
        enable_emotion = st.checkbox("Emotion Detection", value=True)
        enable_subtitles = st.checkbox("Subtitrlar yaratish", value=True)
        
        st.markdown("---")
        
        # Ma'lumot
        st.info("""
        **Loyiha haqida:**
        
        O'zbek tilidagi audio va video fayllarni 
        AI texnologiyalari bilan qayta ishlash platformasi.
        
        **Yaratuvchi:** AI Engineer
        """)
    
    # Asosiy qism
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📤 Yuklash",
        "🔧 Preprocessing",
        "📝 Transkripsiya",
        "👥 Speaker & Emotsiya",
        "💾 Natijalar"
    ])
    
    # Tab 1: Fayl yuklash
    with tab1:
        st.markdown('<div class="sub-header">📤 Audio/Video Yuklash</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Audio yoki video faylni yuklang",
            type=['mp3', 'wav', 'flac', 'ogg', 'm4a', 'mp4', 'avi', 'mov', 'mkv', 'webm'],
            help="Qo'llab-quvvatlanadigan formatlar: mp3, wav, mp4, va boshqalar"
        )
        
        if uploaded_file is not None:
            # Faylni saqlash
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(f"**📁 Fayl:** {uploaded_file.name}")
                st.write(f"**📊 Hajmi:** {uploaded_file.size / 1024 / 1024:.2f} MB")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Yuklash tugmasi
            if st.button("🚀 Audio Yuklash", type="primary"):
                with st.spinner("Audio yuklanmoqda..."):
                    try:
                        # AudioLoader yaratish
                        loader = AudioLoader(sample_rate=16000)
                        
                        # Audio yuklash
                        audio_data, sr = loader.load_audio(tmp_path)
                        
                        # Session state'ga saqlash
                        st.session_state.audio_data = audio_data
                        st.session_state.sample_rate = sr
                        st.session_state.audio_loaded = True
                        
                        # Audio ma'lumotlari
                        duration = len(audio_data) / sr
                        
                        with col2:
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.success("✅ Audio yuklandi!")
                            st.write(f"**⏱️ Davomiylik:** {duration:.2f} soniya")
                            st.write(f"**🔊 Sample Rate:** {sr} Hz")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Audio player
                        st.audio(tmp_path)
                        
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
            
            # Faylni o'chirish
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass
    
    # Tab 2: Preprocessing
    with tab2:
        st.markdown('<div class="sub-header">🔧 Audio Preprocessing</div>', unsafe_allow_html=True)
        
        if not st.session_state.audio_loaded:
            st.warning("⚠️ Avval audio faylni yuklang!")
        else:
            if st.button("🔄 Preprocessing Boshlash", type="primary"):
                with st.spinner("Audio qayta ishlanmoqda..."):
                    try:
                        audio_data = st.session_state.audio_data
                        sr = st.session_state.sample_rate
                        
                        # Preprocessor yaratish
                        preprocessor = AudioPreprocessor(sample_rate=sr)
                        remover = SilenceRemover(sample_rate=sr)
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # 1. Preprocessing
                        status_text.text("1/2 - Shovqin tozalash va normalizatsiya...")
                        processed_audio = preprocessor.preprocess_audio(
                            audio_data,
                            remove_noise=enable_noise_reduction,
                            normalize=enable_normalization,
                            enhance_speech=True,
                            highpass_filter=True
                        )
                        progress_bar.progress(50)
                        
                        # 2. Sukut kesish
                        if enable_silence_removal:
                            status_text.text("2/2 - Sukut qismlari olib tashlanmoqda...")
                            processed_audio, removed_intervals = remover.remove_silence(
                                processed_audio,
                                threshold_db=-40.0,
                                min_silence_duration=0.5
                            )
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Preprocessing tugallandi!")
                        
                        # Session state'ga saqlash
                        st.session_state.processed_audio = processed_audio
                        
                        # Natijalarni ko'rsatish
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown('<div class="info-box">', unsafe_allow_html=True)
                            st.write("**📊 Asl Audio:**")
                            st.write(f"Davomiylik: {len(audio_data)/sr:.2f}s")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.write("**✨ Tozalangan Audio:**")
                            st.write(f"Davomiylik: {len(processed_audio)/sr:.2f}s")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.success("🎉 Audio muvaffaqiyatli qayta ishlandi!")
                        
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
    
    # Tab 3: Transkripsiya
    with tab3:
        st.markdown('<div class="sub-header">📝 Speech-to-Text Transkripsiya</div>', unsafe_allow_html=True)
        
        if st.session_state.processed_audio is None:
            st.warning("⚠️ Avval audio preprocessing qiling!")
        else:
            if st.button("🎤 Transkripsiya Boshlash", type="primary"):
                with st.spinner("Transkripsiya amalga oshirilmoqda... Bu biroz vaqt olishi mumkin."):
                    try:
                        audio_data = st.session_state.processed_audio
                        sr = st.session_state.sample_rate
                        
                        # Transcriber yaratish
                        transcriber = WhisperTranscriber(
                            model_name=whisper_model,
                            device='cpu',
                            language=language
                        )
                        
                        # Progress bar
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("🤖 Whisper modeli yuklanmoqda...")
                        progress_bar.progress(20)
                        
                        # Transkripsiya
                        status_text.text("📝 Audio matnga aylantirilmoqda...")
                        segments = transcriber.transcribe_with_timestamps(
                            audio_data,
                            sample_rate=sr,
                            language=language
                        )
                        progress_bar.progress(100)
                        status_text.text("✅ Transkripsiya tugallandi!")
                        
                        # Session state'ga saqlash
                        st.session_state.transcription_segments = segments
                        
                        # Natijalarni ko'rsatish
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success(f"✅ {len(segments)} ta segment transkripsiya qilindi!")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # To'liq matn
                        full_text = transcriber.get_full_text(segments)
                        
                        st.subheader("📄 To'liq Matn")
                        st.text_area("Transkripsiya", full_text, height=200)
                        
                        # Segmentlar
                        st.subheader("📋 Segmentlar (vaqt belgilari bilan)")
                        for i, seg in enumerate(segments[:10], 1):  # Birinchi 10 ta
                            with st.expander(f"Segment {i} [{seg.start:.2f}s - {seg.end:.2f}s]"):
                                st.write(seg.text)
                        
                        if len(segments) > 10:
                            st.info(f"... va yana {len(segments) - 10} ta segment")
                        
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
    
    # Tab 4: Speaker & Emotsiya
    with tab4:
        st.markdown('<div class="sub-header">👥 Speaker Diarization & Emotsiya</div>', unsafe_allow_html=True)
        
        if st.session_state.transcription_segments is None:
            st.warning("⚠️ Avval transkripsiya qiling!")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                # Speaker Diarization
                if enable_diarization:
                    st.subheader("👥 Speaker Diarization")
                    
                    if st.button("🎯 Spikerlarni Aniqlash"):
                        with st.spinner("Spikerlar aniqlanmoqda..."):
                            try:
                                audio_data = st.session_state.processed_audio
                                sr = st.session_state.sample_rate
                                
                                # Diarizer yaratish
                                diarizer = SpeakerDiarizer(sample_rate=sr)
                                
                                # Diarization
                                speaker_segments = diarizer.diarize(
                                    audio_data,
                                    num_speakers=None,  # Auto detect
                                    segment_duration=1.0
                                )
                                
                                # Session state'ga saqlash
                                st.session_state.speaker_segments = speaker_segments
                                
                                # Transkripsiya bilan moslashtirish
                                aligned = diarizer.align_with_transcription(
                                    speaker_segments,
                                    st.session_state.transcription_segments
                                )
                                st.session_state.aligned_segments = aligned
                                
                                # Natijalar
                                unique_speakers = len(set(seg.speaker_id for seg in speaker_segments))
                                st.success(f"✅ {unique_speakers} ta spiker aniqlandi!")
                                
                                # Formatlangan matn
                                formatted_text = diarizer.format_diarization(aligned)
                                st.text_area("Spikerlar bo'yicha matn", formatted_text, height=300)
                                
                            except Exception as e:
                                st.error(f"❌ Xatolik: {str(e)}")
            
            with col2:
                # Emotion Detection
                if enable_emotion:
                    st.subheader("😊 Emotion Detection")
                    
                    if st.button("🎭 Emotsiyalarni Aniqlash"):
                        with st.spinner("Emotsiyalar aniqlanmoqda..."):
                            try:
                                audio_data = st.session_state.processed_audio
                                sr = st.session_state.sample_rate
                                segments = st.session_state.transcription_segments
                                
                                # Emotion detector yaratish
                                detector = EmotionDetector(sample_rate=sr)
                                
                                # Emotion detection
                                predictions = detector.detect_emotions_segments(
                                    audio_data,
                                    segments,
                                    segment_duration=3.0
                                )
                                
                                # Session state'ga saqlash
                                st.session_state.emotion_predictions = predictions
                                
                                st.success(f"✅ {len(predictions)} ta segment uchun emotsiya aniqlandi!")
                                
                                # Formatlangan natija
                                formatted_emotions = detector.format_emotions(predictions)
                                st.text_area("Emotsiya natijalari", formatted_emotions, height=300)
                                
                                # Statistika
                                emotion_counts = {}
                                for pred in predictions:
                                    emotion_counts[pred.emotion] = emotion_counts.get(pred.emotion, 0) + 1
                                
                                st.write("**📊 Emotsiya Statistikasi:**")
                                for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
                                    percentage = (count / len(predictions)) * 100
                                    emotion_uz = EmotionDetector.EMOTIONS.get(emotion, emotion)
                                    st.write(f"• {emotion_uz}: {percentage:.1f}%")
                                
                            except Exception as e:
                                st.error(f"❌ Xatolik: {str(e)}")
    
    # Tab 5: Natijalar
    with tab5:
        st.markdown('<div class="sub-header">💾 Natijalarni Yuklab Olish</div>', unsafe_allow_html=True)
        
        if st.session_state.transcription_segments is None:
            st.warning("⚠️ Avval transkripsiya qiling!")
        else:
            st.subheader("📥 Fayllarni Yuklab Olish")
            
            # Output papkasini yaratish
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Transkripsiya matni
                if st.button("📄 Transkripsiya (TXT)"):
                    try:
                        transcriber = WhisperTranscriber()
                        full_text = transcriber.get_full_text(st.session_state.transcription_segments)
                        
                        txt_path = os.path.join(output_dir, "transcription.txt")
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(full_text)
                        
                        st.success("✅ Transkripsiya saqlandi!")
                        with open(txt_path, 'rb') as f:
                            st.download_button(
                                label="📥 TXT Yuklab Olish",
                                data=f,
                                file_name="transcription.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
            
            with col2:
                # Subtitrlar
                if enable_subtitles and st.button("📝 Subtitrlar (SRT/VTT)"):
                    try:
                        generator = SubtitleGenerator()
                        
                        # Aligned segments yoki oddiy transkripsiya
                        segments = st.session_state.aligned_segments if st.session_state.aligned_segments else st.session_state.transcription_segments
                        
                        srt_path, vtt_path = generator.generate_both(
                            segments,
                            output_dir,
                            filename="subtitles",
                            include_speaker=enable_diarization
                        )
                        
                        st.success("✅ Subtitrlar yaratildi!")
                        
                        # Download buttons
                        with open(srt_path, 'rb') as f:
                            st.download_button(
                                label="📥 SRT Yuklab Olish",
                                data=f,
                                file_name="subtitles.srt",
                                mime="application/x-subrip"
                            )
                        
                        with open(vtt_path, 'rb') as f:
                            st.download_button(
                                label="📥 VTT Yuklab Olish",
                                data=f,
                                file_name="subtitles.vtt",
                                mime="text/vtt"
                            )
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
            
            with col3:
                # To'liq hisobot
                if st.button("📊 To'liq Hisobot"):
                    try:
                        report_path = os.path.join(output_dir, "full_report.txt")
                        
                        with open(report_path, 'w', encoding='utf-8') as f:
                            f.write("="*60 + "\n")
                            f.write("UZBEK AUDIO AI PLATFORM - TO'LIQ HISOBOT\n")
                            f.write("="*60 + "\n\n")
                            
                            # Transkripsiya
                            f.write("📝 TRANSKRIPSIYA:\n")
                            f.write("-"*60 + "\n")
                            transcriber = WhisperTranscriber()
                            full_text = transcriber.get_full_text(st.session_state.transcription_segments)
                            f.write(full_text + "\n\n")
                            
                            # Speaker diarization
                            if st.session_state.aligned_segments:
                                f.write("👥 SPEAKER DIARIZATION:\n")
                                f.write("-"*60 + "\n")
                                diarizer = SpeakerDiarizer()
                                formatted_text = diarizer.format_diarization(st.session_state.aligned_segments)
                                f.write(formatted_text + "\n\n")
                            
                            # Emotion detection
                            if st.session_state.emotion_predictions:
                                f.write("😊 EMOTION DETECTION:\n")
                                f.write("-"*60 + "\n")
                                detector = EmotionDetector()
                                formatted_emotions = detector.format_emotions(st.session_state.emotion_predictions)
                                f.write(formatted_emotions + "\n\n")
                        
                        st.success("✅ To'liq hisobot yaratildi!")
                        
                        with open(report_path, 'rb') as f:
                            st.download_button(
                                label="📥 Hisobotni Yuklab Olish",
                                data=f,
                                file_name="full_report.txt",
                                mime="text/plain"
                            )
                    except Exception as e:
                        st.error(f"❌ Xatolik: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <p>🎙️ Uzbek Speech-to-Text & Audio Intelligence Platform</p>
            <p>Powered by Whisper, PyTorch & Streamlit | Made with ❤️ in Uzbekistan</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
