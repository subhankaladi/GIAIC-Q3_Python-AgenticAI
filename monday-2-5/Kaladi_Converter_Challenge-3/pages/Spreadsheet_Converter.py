import streamlit as st
from converters.spreadsheet_converter import SpreadsheetConverter

# Set page configuration
st.set_page_config(
    page_title="Spreadsheet Converter - KaladiConverter",
    page_icon="📊",
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
        <h1 style="color: #333; font-size: 2.5rem;">📊 Spreadsheet Converter</h1>
        <p style="color: #666; font-size: 1.2rem;">Convert your spreadsheets between various formats</p>
    </div>
""", unsafe_allow_html=True)

# Initialize the converter
converter = SpreadsheetConverter()

# Main converter container
with st.container():
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### Upload Your Spreadsheet")
    uploaded_file = st.file_uploader(
        "Choose a spreadsheet file",
        type=['xlsx', 'xls', 'csv', 'ods', 'tsv'],
        help="Supported formats: XLSX, XLS, CSV, ODS, TSV"
    )
    
    if uploaded_file:
        # Display file info
        st.markdown('<div class="file-info">', unsafe_allow_html=True)
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
        st.write(f"**File Type:** {uploaded_file.type}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Conversion options
        st.markdown("### Conversion Options")
        col1, col2 = st.columns(2)
        
        with col1:
            target_format = st.selectbox(
                "Select target format",
                ["XLSX", "XLS", "CSV", "ODS", "TSV"],
                help="Choose the format you want to convert your spreadsheet to"
            )
        
        with col2:
            encoding = st.selectbox(
                "Select encoding",
                ["UTF-8", "ASCII", "ISO-8859-1"],
                help="Choose the character encoding for the output file"
            )
        
        # Additional options
        st.markdown("### Additional Options")
        include_header = st.checkbox("Include header row", value=True)
        delimiter = st.selectbox(
            "Select delimiter (for CSV/TSV)",
            [",", ";", "\t", "|"],
            help="Choose the delimiter for CSV/TSV files"
        ) if target_format in ["CSV", "TSV"] else None
        
        # Convert button
        if st.button("Convert Spreadsheet", type="primary"):
            try:
                with st.spinner("Converting your spreadsheet..."):
                    # Perform conversion
                    result = converter.convert(
                        uploaded_file,
                        target_format.lower(),
                        encoding=encoding,
                        include_header=include_header,
                        delimiter=delimiter
                    )
                    
                    # Download button
                    st.download_button(
                        label="Download Converted File",
                        data=result,
                        file_name=f"converted_spreadsheet.{target_format.lower()}",
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
            <li>Convert between multiple spreadsheet formats</li>
            <li>Maintain data formatting and formulas</li>
            <li>Choose character encoding</li>
            <li>Customize delimiter for CSV/TSV files</li>
            <li>Fast and efficient conversion</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #666; border-top: 1px solid #e0e0e0;">
        <p style="font-size: 1.2rem;">Made with ❤️ by Subhan Kaladi  </p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Your one-stop solution for all conversion needs</p>
    </div>
""", unsafe_allow_html=True) 