# Streamlit App for MP4 Audio Text Extraction
import streamlit as st
import tempfile
import os
import shutil
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import warnings
warnings.filterwarnings("ignore")

def extract_audio_from_mp4(mp4_file, output_audio_path):
    """Extract audio from MP4 file using MoviePy"""
    try:
        # Load the video file
        video = VideoFileClip(mp4_file)
        
        # Extract audio
        audio = video.audio
        
        # Write audio to temporary file
        audio.write_audiofile(output_audio_path, verbose=False, logger=None)
        
        # Close video and audio clips to free memory
        audio.close()
        video.close()
        
        return True
    except Exception as e:
        st.error(f"Error extracting audio: {str(e)}")
        return False

def transcribe_audio_with_whisper(audio_file_path):
    """Transcribe audio using Whisper through SpeechRecognition library"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Load audio file
        with sr.AudioFile(audio_file_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            # Record the audio
            audio_data = recognizer.record(source)
        
        # Transcribe using Whisper
        text = recognizer.recognize_whisper(audio_data)
        return text
    
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Error with Whisper service: {str(e)}"
    except Exception as e:
        return f"Error during transcription: {str(e)}"

def main():
    st.set_page_config(
        page_title="MP4 Audio Text Extractor",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 MP4 Audio Text Extractor")
    st.markdown("Upload an MP4 video file to extract and transcribe its audio content.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an MP4 file", 
        type=['mp4'],
        help="Upload an MP4 video file to extract text from its audio"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Show file size
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)  # Convert to MB
        st.info(f"📊 File size: {file_size:.2f} MB")
        
        # Process button
        if st.button("🚀 Extract and Transcribe Audio", type="primary"):
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Create temporary directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Save uploaded file to temporary location
                    status_text.text("📁 Saving uploaded file...")
                    progress_bar.progress(10)
                    
                    temp_video_path = os.path.join(temp_dir, "temp_video.mp4")
                    with open(temp_video_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Extract audio
                    status_text.text("🎵 Extracting audio from video...")
                    progress_bar.progress(30)
                    
                    temp_audio_path = os.path.join(temp_dir, "temp_audio.wav")
                    audio_extracted = extract_audio_from_mp4(temp_video_path, temp_audio_path)
                    
                    if audio_extracted:
                        progress_bar.progress(60)
                        
                        # Transcribe audio
                        status_text.text("🎤 Transcribing audio to text...")
                        progress_bar.progress(80)
                        
                        transcribed_text = transcribe_audio_with_whisper(temp_audio_path)
                        
                        # Complete
                        progress_bar.progress(100)
                        status_text.text("✅ Processing complete!")
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("## 📝 Transcribed Text")
                        
                        if transcribed_text and transcribed_text.strip():
                            st.text_area(
                                "Extracted Text:",
                                value=transcribed_text,
                                height=200,
                                help="The text extracted from the audio in your MP4 file"
                            )
                            
                            # Download button for text
                            st.download_button(
                                label="💾 Download Text File",
                                data=transcribed_text,
                                file_name=f"{uploaded_file.name}_transcription.txt",
                                mime="text/plain"
                            )
                        else:
                            st.warning("⚠️ No text could be extracted from the audio.")
                    
                    else:
                        st.error("❌ Failed to extract audio from the video file.")
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                progress_bar.progress(0)
                status_text.text("❌ Processing failed")
    
    # Instructions
    st.markdown("---")
    st.markdown("## 📋 Instructions")
    st.markdown("""
    1. **Upload**: Click 'Browse files' and select an MP4 video file
    2. **Process**: Click 'Extract and Transcribe Audio' to start processing
    3. **Download**: Once complete, you can download the transcribed text
    
    **Note**: Processing time depends on the length of your video file.
    """)
    
    # Technical info
    with st.expander("🔧 Technical Information"):
        st.markdown("""
        **This app uses:**
        - **MoviePy**: For extracting audio from MP4 files
        - **OpenAI Whisper**: For high-quality speech-to-text transcription
        - **SpeechRecognition**: Python library for audio processing
        
        **Supported formats**: MP4 video files
        **Processing**: All processing is done locally on the server
        """)

if __name__ == "__main__":
    main()
