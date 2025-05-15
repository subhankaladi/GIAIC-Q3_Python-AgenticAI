import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from io import StringIO

# Load environment variables
load_dotenv()

# Configure Gemini
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Supported languages and formats
SUPPORTED_FORMATS = {
    'python': ['javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'javascript': ['python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'js': ['python', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'java': ['python', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'c++': ['python', 'javascript', 'java', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'cpp': ['python', 'javascript', 'java', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
    'c#': ['python', 'javascript', 'java', 'c++', 'php', 'ruby', 'go', 'rust', 'swift'],
    'php': ['python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift'],
    'ruby': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'go', 'rust', 'swift'],
    'go': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'rust', 'swift'],
    'rust': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'swift'],
    'swift': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust'],
    'py': ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust'],
}

def generate_conversion_prompt(source_code, source_lang, target_lang):
    return f"""
    Convert the following {source_lang} code to {target_lang}. 
    Maintain all functionality and include appropriate comments.
    Preserve the original structure as much as possible.
    
    {source_lang} code:
    ```{source_lang}
    {source_code}
    ```
    
    Converted {target_lang} code:
    """

def CodeConverter():
    st.title("AI Code Converter with KaladiConverter")
    st.write("Upload your code file and select the target language for conversion")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your code file", type=list(SUPPORTED_FORMATS.keys()))
    
    if uploaded_file is not None:
        # Read file content
        file_content = uploaded_file.read().decode("utf-8")
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Determine source language
        source_lang = file_extension
        if source_lang == 'py':
            source_lang = 'python'
        elif source_lang == 'js':
            source_lang = 'javascript'
        elif source_lang == 'cpp':
            source_lang = 'c++'
        elif source_lang == 'cs':
            source_lang = 'c#'
        elif source_lang == 'rb':
            source_lang = 'ruby'
        elif source_lang == 'rs':
            source_lang = 'rust'
        
        # Target language selection
        target_lang = st.selectbox(
            "Select target language",
            options=SUPPORTED_FORMATS.get(source_lang, [])
        )
        
        # Conversion options
        st.subheader("Conversion Options")
        col1, col2 = st.columns(2)
        with col1:
            include_comments = st.checkbox("Include comments", value=True)
            optimize_code = st.checkbox("Optimize code", value=True)
        with col2:
            preserve_formatting = st.checkbox("Preserve formatting", value=True)
            add_error_handling = st.checkbox("Add error handling", value=False)
        
        # Convert button
        if st.button("Convert Code"):
            with st.spinner("Converting code with AI..."):
                try:
                    # Generate prompt for Gemini
                    prompt = generate_conversion_prompt(
                        file_content, 
                        source_lang, 
                        target_lang
                    )
                    
                    # Add conversion options to prompt
                    options = []
                    if include_comments:
                        options.append("include appropriate comments")
                    if optimize_code:
                        options.append("optimize the code")
                    if preserve_formatting:
                        options.append("preserve the original formatting")
                    if add_error_handling:
                        options.append("add comprehensive error handling")
                    
                    if options:
                        prompt += "\n\nAdditional requirements:\n- " + "\n- ".join(options)
                    
                    # Get response from Gemini
                    response = model.generate_content(prompt)
                    converted_code = response.text
                    
                    # Display converted code
                    st.subheader(f"Converted {target_lang} Code")
                    st.code(converted_code, language=target_lang)
                    
                    # Download button
                    download_ext = target_lang
                    if target_lang == 'python':
                        download_ext = 'py'
                    elif target_lang == 'javascript':
                        download_ext = 'js'
                    elif target_lang == 'c++':
                        download_ext = 'cpp'
                    elif target_lang == 'c#':
                        download_ext = 'cs'
                    elif target_lang == 'ruby':
                        download_ext = 'rb'
                    elif target_lang == 'rust':
                        download_ext = 'rs'
                    
                    st.download_button(
                        label="Download Converted Code",
                        data=converted_code,
                        file_name=f"converted_code.{download_ext}",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error during conversion: {str(e)}")

