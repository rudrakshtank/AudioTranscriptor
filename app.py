# Streamlit App for MP4 Audio Text Extraction using FFmpeg and Whisper
import streamlit as st
import tempfile
import os
import ffmpeg
import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore")

def extract_audio_with_ffmpeg(mp4_path, output_audio_path):
    """Extract audio from MP4 using ffmpeg"""
    try:
        ffmpeg.input(mp4_path).output(output_audio_path).run(quiet=True)
        return True
    except Exception as e:
        st.error(f"FFmpeg error: {str(e)}")
        return False

def transcribe_audio_with_whisper(audio_file_path):
    """Transcribe audio using Whisper via SpeechRecognition"""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
        text = recognizer.recognize_whisper(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Whisper error: {str(e)}"
    except Exception as e:
        return f"Transcription error: {str(e)}"

def main():
    st.set_page_config(page_title="MP4 Audio Text Extractor", page_icon="🎵", layout="wide")
    st.title("🎵 MP4 Audio Text Extractor (No MoviePy)")
    st.markdown("Upload an MP4 video to extract and transcribe its audio.")

    uploaded_file = st.file_uploader("Upload MP4 File", type=["mp4"])

    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.info(f"📦 File size: {file_size:.2f} MB")

        if st.button("🚀 Extract and Transcribe"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_video = os.path.join(temp_dir, "video.mp4")
                    with open(temp_video, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    progress_bar.progress(10)
                    status_text.text("📁 Video saved.")

                    temp_audio = os.path.join(temp_dir, "audio.wav")
                    if extract_audio_with_ffmpeg(temp_video, temp_audio):
                        progress_bar.progress(50)
                        status_text.text("🎧 Audio extracted.")

                        transcription = transcribe_audio_with_whisper(temp_audio)
                        progress_bar.progress(100)
                        status_text.text("✅ Done!")

                        st.markdown("## 📝 Transcribed Text")
                        if transcription.strip():
                            st.text_area("Extracted Text:", value=transcription, height=200)
                            st.download_button("💾 Download Transcript", transcription, file_name="transcript.txt")
                        else:
                            st.warning("⚠️ No text extracted.")
                    else:
                        st.error("❌ Audio extraction failed.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                progress_bar.progress(0)

    st.markdown("---")
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. Upload an MP4 video file.
    2. Click 'Extract and Transcribe'.
    3. View and download the transcript.
    """)

    with st.expander("🔧 Technical Info"):
        st.markdown("""
        - **FFmpeg**: For audio extraction from MP4
        - **SpeechRecognition + Whisper**: For transcription
        """)

if __name__ == "__main__":
    main()
