import streamlit as st
import tempfile
import os
import ffmpeg
import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore")

def extract_audio(v_path, a_path):
    try:
        ffmpeg.input(v_path).output(a_path).run(quiet=True)
        return True
    except Exception as e:
        st.error(f"FFmpeg error: {str(e)}")
        return False

def transcribe_audio(a_path):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(a_path) as src:
            r.adjust_for_ambient_noise(src)
            data = r.record(src)
        return r.recognize_whisper(data)
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Whisper error: {str(e)}"
    except Exception as e:
        return f"Transcription error: {str(e)}"

def main():
    st.set_page_config(page_title="MP4 to Text", page_icon="🎵", layout="wide")
    st.title("🎵 MP4 Audio Text Extractor")
    st.markdown("Upload an MP4 video to extract and transcribe its audio.")

    file = st.file_uploader("Upload MP4 File", type=["mp4"])

    if file is not None:
        st.success(f"✅ Uploaded: {file.name}")
        size = len(file.getvalue()) / (1024 * 1024)
        st.info(f"📦 Size: {size:.2f} MB")

        if st.button("🚀 Extract and Transcribe"):
            bar = st.progress(0)
            status = st.empty()

            try:
                with tempfile.TemporaryDirectory() as tmp:
                    v_path = os.path.join(tmp, "video.mp4")
                    with open(v_path, "wb") as f:
                        f.write(file.getvalue())
                    bar.progress(10)
                    status.text("Video saved.")

                    a_path = os.path.join(tmp, "audio.wav")
                    if extract_audio(v_path, a_path):
                        bar.progress(50)
                        status.text("Audio extracted.")

                        text = transcribe_audio(a_path)
                        bar.progress(100)
                        status.text("Done!")

                        st.markdown("## 📝 Transcribed Text")
                        if text.strip():
                            st.text_area("Text:", value=text, height=200)
                            st.download_button("💾 Download", text, file_name="transcript.txt")
                        else:
                            st.warning("⚠️ No text extracted.")
                    else:
                        st.error("❌ Extraction failed.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                bar.progress(0)

    st.markdown("---")
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. Upload an MP4 video file.
    2. Click 'Extract and Transcribe'.
    3. View and download the transcript.
    """)

    with st.expander("🔧 Info"):
        st.markdown("""
        - **FFmpeg**: For audio extraction
        - **Whisper**: For transcription
        """)

if __name__ == "__main__":
    main()
