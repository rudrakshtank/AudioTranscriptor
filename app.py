import streamlit as st
from moviepy import VideoFileClip
import os

st.title("🎥 MP4 to MP3 Converter")

# File uploader
video_file = st.file_uploader("Upload MP4 Video", type=["mp4"])

if video_file is not None:
    # Save uploaded video to disk
    with open("uploaded_video.mp4", "wb") as f:
        f.write(video_file.read())

    st.video("uploaded_video.mp4")

    # Convert video to audio
    st.write("Converting to MP3...")
    video = VideoFileClip("uploaded_video.mp4")
    video.audio.write_audiofile("converted_audio.mp3")
    video.close()

    # Download button for audio
    with open("converted_audio.mp3", "rb") as audio_file:
        st.download_button("Download MP3", audio_file, file_name="audio.mp3", mime="audio/mpeg")

    # Optional: clean up files
    os.remove("uploaded_video.mp4")
    os.remove("converted_audio.mp3")
