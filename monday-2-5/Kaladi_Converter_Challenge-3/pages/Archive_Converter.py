import streamlit as st
from converters.archive_converter import ArchiveConverter

# Set page configuration
st.set_page_config(
    page_title="Archive Converter - KaladiConverter",
    page_icon="📦",
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
    </style>
    """, unsafe_allow_html=True)

# Page header
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #333; font-size: 2.5rem;">📦 Archive Converter</h1>
        <p style="color: #666; font-size: 1.2rem;">Convert your archives between different formats</p>
    </div>
""", unsafe_allow_html=True)

# Initialize the converter
converter = ArchiveConverter()

# Main converter container
with st.container():
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### Upload Your Archive")
    uploaded_file = st.file_uploader(
        "Choose an archive file",
        type=['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
        help="Supported formats: ZIP, RAR, 7Z, TAR, GZ, BZ2"
    )
    
    if uploaded_file:
        # Display file info
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / (1024*1024):.2f} MB")
        st.write(f"**File Type:** {uploaded_file.type}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversion options
        st.markdown("### Conversion Options")
        col1, col2 = st.columns(2)
        
        with col1:
            target_format = st.selectbox(
                "Select target format",
                ["ZIP", "RAR", "7Z", "TAR", "GZ", "BZ2"],
                help="Choose the format you want to convert your archive to"
            )
        
        with col2:
            compression_level = st.select_slider(
                "Compression Level",
                options=["Store", "Fast", "Normal", "Maximum"],
                value="Normal",
                help="Choose the compression level for the output archive"
            )
        
        # Additional options
        st.markdown("### Additional Options")
        col3, col4 = st.columns(2)
        
        with col3:
            password_protect = st.checkbox("Password protect archive", value=False)
            if password_protect:
                password = st.text_input("Enter password", type="password")
        
        with col4:
            split_archive = st.checkbox("Split archive into parts", value=False)
            if split_archive:
                part_size = st.number_input("Part size (MB)", min_value=1, value=100)
        
        # Convert button
        if st.button("Convert Archive", type="primary"):
            try:
                with st.spinner("Converting your archive..."):
                    # Perform conversion
                    result = converter.convert(
                        uploaded_file,
                        target_format.lower(),
                        compression_level=compression_level,
                        password=password if password_protect else None,
                        split_size=part_size * 1024 * 1024 if split_archive else None
                    )
                    
                    # Download button
                    st.download_button(
                        label="Download Converted Archive",
                        data=result,
                        file_name=f"converted_archive.{target_format.lower()}",
                        mime=f"application/{target_format.lower()}"
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
            <li>Convert between multiple archive formats</li>
            <li>Adjust compression level</li>
            <li>Password protect archives</li>
            <li>Split large archives into parts</li>
            <li>Fast and efficient conversion</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666; border-top: 1px solid #e0e0e0;">
        <p style="font-size: 1.2rem;">Made with ❤️ by Subhan Kaladi </p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Your one-stop solution for all conversion needs</p>
    </div>
""", unsafe_allow_html=True) 