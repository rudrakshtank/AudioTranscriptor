import streamlit as st
import ffmpeg
import tempfile
import os

st.title("🎥 MP4 to MP3 Converter using FFmpeg")

# Step 1: Upload MP4 video
video_file = st.file_uploader("Upload MP4 Video", type=["mp4"])

if video_file is not None:
    # Step 2: Save video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        temp_video_path = temp_video.name

    st.video(temp_video_path)

    # Step 3: Convert to MP3
    if st.button("🎵 Convert to MP3"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio_path = temp_audio.name

        try:
            ffmpeg.input(temp_video_path).output(temp_audio_path).run()
            st.success("✅ MP3 file created!")

            # Step 4: Download button
            with open(temp_audio_path, "rb") as audio_file:
                st.download_button(
                    label="📥 Download MP3",
                    data=audio_file,
                    file_name="extracted_audio.mp3",
                    mime="audio/mpeg"
                )

        except ffmpeg.Error as e:
            st.error("FFmpeg failed. Make sure it's installed and available in your system PATH.")
            st.code(e.stderr.decode(), language='bash')

        # Cleanup
        os.remove(temp_video_path)
        os.remove(temp_audio_path)
