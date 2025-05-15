import streamlit as st
from converters.audio_converter import AudioConverter

# Set page configuration
st.set_page_config(
    page_title="Audio Converter - KaladiConverter",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS for the page
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .converter-container {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    .converter-title {
        color: #4CAF50;
        font-size: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .converter-description {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.5;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .file-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .audio-player {
        width: 100%;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Page header
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #333; font-size: 2.5rem;">🎵 Audio Converter</h1>
        <p style="color: #666; font-size: 1.2rem;">Convert your audio files between various formats</p>
    </div>
""", unsafe_allow_html=True)

# Initialize the converter
converter = AudioConverter()

# Main converter container
with st.container():
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### Upload Your Audio")
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav','flac'],
        help="Supported formats: MP3, WAV, FLAC"
    )
    
    if uploaded_file:
        # Display file info
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / (1024*1024):.2f} MB")
        st.write(f"**File Type:** {uploaded_file.type}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Audio preview
        st.audio(uploaded_file, format=f"audio/{uploaded_file.type.split('/')[-1]}")
        
        # Conversion options
        st.markdown("### Conversion Options")
        col1, col2 = st.columns(2)
        
        with col1:
            target_format = st.selectbox(
                "Select target format",
                ["MP3", "WAV", "FLAC", "AAC"],
                help="Choose the format you want to convert your audio to"
            )
            
            bitrate = st.selectbox(
                "Select bitrate",
                ["128 kbps", "192 kbps", "256 kbps", "320 kbps"],
                help="Choose the audio quality (higher bitrate = better quality but larger file size)"
            )
        
        with col2:
            sample_rate = st.selectbox(
                "Select sample rate",
                ["44100 Hz", "48000 Hz", "96000 Hz"],
                help="Choose the audio sample rate"
            )
            
            channels = st.selectbox(
                "Select channels",
                ["Mono", "Stereo"],
                help="Choose the number of audio channels"
            )
        
        # Convert button
        if st.button("Convert Audio", type="primary"):
            try:
                with st.spinner("Converting your audio..."):
                    # Parse numeric values from UI selections
                    bitrate_value = int(bitrate.split()[0])  # Extract number from "128 kbps"
                    sample_rate_value = int(sample_rate.split()[0])  # Extract number from "44100 Hz"
                    channels_value = 1 if channels == "Mono" else 2  # Convert to numeric value
                    
                    # Perform conversion
                    result = converter.convert(
                        uploaded_file,
                        target_format.lower(),
                        bitrate=bitrate_value,
                        sample_rate=sample_rate_value,
                        channels=channels_value
                    )
                    
                    # Download button
                    st.download_button(
                        label="Download Converted Audio",
                        data=result,
                        file_name=f"converted_audio.{target_format.lower()}",
                        mime=f"audio/{target_format.lower()}"
                    )
                    st.success("Conversion completed successfully! 🎉")
            except Exception as e:
                st.error(f"An error occurred during conversion: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("""
    <div class="converter-container">
        <h2 style="color: #4CAF50;">Features</h2>
        <ul style="color: #666; font-size: 1.1rem;">
            <li>Convert between multiple audio formats</li>
            <li>Adjust audio quality and bitrate</li>
            <li>Preview audio before conversion</li>
            <li>Choose sample rate and channels</li>
            <li>Fast and efficient conversion</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666; border-top: 1px solid #e0e0e0;">
        <p style="font-size: 1.2rem;">Made with ❤️ by Subhan Kaladi</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Your one-stop solution for all conversion needs</p>
    </div>
""", unsafe_allow_html=True) 