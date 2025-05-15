from abc import ABC, abstractmethod
import streamlit as st

class BaseConverter(ABC):
    def __init__(self):
        self.supported_formats = {}
        self.title = ""
        self.icon = ""
        self.description = ""

    @abstractmethod
    def convert(self, input_file, output_format):
        pass

    def get_supported_formats(self):
        return self.supported_formats

    def render_ui(self):
        st.markdown(f"## {self.icon} {self.title}")
        st.write(self.description)
        
        uploaded_file = st.file_uploader("Choose a file", type=list(self.supported_formats.keys()))
        
        if uploaded_file:
            output_format = st.selectbox(
                "Select output format",
                options=self.supported_formats.get(uploaded_file.name.split('.')[-1].lower(), [])
            )
            
            if st.button("Convert"):
                try:
                    output_file = self.convert(uploaded_file, output_format)
                    st.success("Conversion completed successfully!")
                    st.download_button(
                        label="Download converted file",
                        data=output_file,
                        file_name=f"converted.{output_format}",
                        mime=f"application/{output_format}"
                    )
                except Exception as e:
                    st.error(f"Error during conversion: {str(e)}") 