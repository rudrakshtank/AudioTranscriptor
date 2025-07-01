import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
import tempfile
import os

st.set_page_config(page_title="MP4 to Text Transcriber", layout="centered")
st.title("🎬 MP4 to Text Transcriber")
st.markdown("Upload an English `.mp4` video, and get the audio transcribed using Whisper!")

uploaded_file = st.file_uploader("Upload MP4 Video", type=["mp4"])

if uploaded_file is not None:
    # Save uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_file:
        video_file.write(uploaded_file.read())
        video_path = video_file.name

    # Show video preview
    st.video(video_path)

    if st.button("🎙 Extract & Transcribe Audio"):
        with st.spinner("Extracting audio..."):
            # Extract audio from video using moviepy
            audio_path = video_path.replace(".mp4", ".mp3")
            video_clip = VideoFileClip(video_path)
            video_clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

        with st.spinner("Loading Whisper model..."):
            model = whisper.load_model("base")

        with st.spinner("Transcribing..."):
            result = model.transcribe(audio_path)
            st.success("✅ Transcription Complete!")

            # Display transcript
            st.subheader("📄 Transcribed Text:")
            st.write(result["text"])

            # Download button
            st.download_button("📥 Download Transcript", result["text"], file_name="transcript.txt")

        # Cleanup
        video_clip.close()
        os.remove(video_path)
        os.remove(audio_path)
