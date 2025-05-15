import streamlit as st
from converters.code_converter import CodeConverter

# Set page configuration
st.set_page_config(
    page_title="Code Converter - KaladiConverter",
    page_icon="💻",
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
    .code-preview {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 10px;
        font-family: 'Consolas', monospace;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Page header
st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #333; font-size: 2.5rem;">💻 Code Converter</h1>
        <p style="color: #666; font-size: 1.2rem;">Convert your code between different programming languages</p>
    </div>
""", unsafe_allow_html=True)

# Initialize the converter
converter = CodeConverter()

# Main converter container
with st.container():
    st.markdown('<div class="converter-container">', unsafe_allow_html=True)
    
    # File upload section
    # st.markdown("### Upload Your Code File")
    # uploaded_file = st.file_uploader(
    #     "Choose a code file",
    #     type=['py', 'js', 'java', 'cpp', 'cs', 'php', 'rb', 'go', 'rs', 'swift'],
    #     help="Supported languages: Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift"
    # )
    
    # if uploaded_file:
    #     # Display file info
    #     st.markdown('<div class="file-info">', unsafe_allow_html=True)
    #     st.write(f"**File Name:** {uploaded_file.name}")
    #     st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
    #     st.write(f"**File Type:** {uploaded_file.type}")
    #     st.markdown('</div>', unsafe_allow_html=True)
        
        # Code preview
        # code_content = uploaded_file.getvalue().decode('utf-8')
        # st.markdown("### Code Preview")
        # st.code(code_content, language=uploaded_file.name.split('.')[-1])
        
        # # Conversion options
        # st.markdown("### Conversion Options")
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     target_language = st.selectbox(
        #         "Select target language",
        #         ["Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Rust", "Swift"],
        #         help="Choose the programming language you want to convert your code to"
        #     )
        
        # with col2:
        #     code_style = st.selectbox(
        #         "Select code style",
        #         ["Standard", "Compact", "Verbose"],
        #         help="Choose the style of the converted code"
        #     )
        
        # # Additional options
        # st.markdown("### Additional Options")
        # col3, col4 = st.columns(2)
        
        # with col3:
        #     include_comments = st.checkbox("Include comments", value=True)
        #     optimize_code = st.checkbox("Optimize code", value=True)
        
        # with col4:
        #     preserve_formatting = st.checkbox("Preserve formatting", value=True)
        #     add_error_handling = st.checkbox("Add error handling", value=True)
        
        # # Convert button
        # if st.button("Convert Code", type="primary"):
        #     try:
        #         with st.spinner("Converting your code..."):
        #             # Perform conversion
        #             result = converter.convert(
        #                 uploaded_file,
        #                 target_language.lower(),
        #                 code_style=code_style,
        #                 include_comments=include_comments,
        #                 optimize_code=optimize_code,
        #                 preserve_formatting=preserve_formatting,
        #                 add_error_handling=add_error_handling
        #             )
                    
        #             # Show converted code
        #             st.markdown("### Converted Code")
        #             st.code(result.decode('utf-8'), language=target_language.lower())
                    
        #             # Download button
        #             st.download_button(
        #                 label="Download Converted Code",
        #                 data=result,
        #                 file_name=f"converted_code.{target_language.lower()}",
        #                 mime="text/plain"
        #             )
        #             st.success("Conversion completed successfully! 🎉")
        #     except Exception as e:
        #         st.error(f"An error occurred during conversion: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("""
    <div class="converter-container">
        <h2 style="color: #4CAF50;">Features</h2>
        <ul style="color: #666; font-size: 1.1rem;">
            <li>Convert between multiple programming languages</li>
            <li>Maintain code structure and logic</li>
            <li>Choose code style and formatting</li>
            <li>Add error handling and optimization</li>
            <li>Preview code before and after conversion</li>
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