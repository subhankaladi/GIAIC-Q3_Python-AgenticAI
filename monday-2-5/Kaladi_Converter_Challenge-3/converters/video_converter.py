from .base_converter import BaseConverter
from moviepy.editor import VideoFileClip
import io
import streamlit as st
import tempfile
import os

class VideoConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.title = "Video Converter"
        self.icon = "🎥"
        self.description = "Convert videos between different formats"
        self.supported_formats = {
            'mp4': ['avi', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'mpeg4'],
            'avi': ['mp4', 'mov', 'mkv', 'wmv', 'flv', 'webm', 'mpeg4'],
            'mov': ['mp4', 'avi', 'mkv', 'wmv', 'flv', 'webm', 'mpeg4'],
            'mkv': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mpeg4'],
            'wmv': ['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm', 'mpeg4'],
            'flv': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'webm', 'mpeg4'],
            'webm': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'mpeg4'],
            'mpeg4': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm']
        }

    def convert(self, input_file, output_format, resolution="Original", quality="High", codec="H.264"):
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input:
            temp_input.write(input_file.getvalue())
            temp_input_path = temp_input.name

        temp_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}').name

        try:
            # Load video using moviepy
            video = VideoFileClip(temp_input_path)

            # Set resolution
            if resolution != "Original":
                width, height = map(int, resolution.split('x'))
                video = video.resize(newsize=(width, height))

            # Set quality (approximated via bitrate)
            bitrate = "5000k"  # Default high quality
            if quality == "Low":
                bitrate = "1000k"
            elif quality == "Medium":
                bitrate = "2500k"
            elif quality == "High":
                bitrate = "5000k"

            # Set codec
            if codec == "H.264":
                video_codec = "libx264"
            elif codec == "H.265":
                video_codec = "libx265"
            elif codec == "VP9":
                video_codec = "libvpx-vp9"
            else:
                video_codec = "libx264"  # Fallback

            # Write the output file
            video.write_videofile(
                temp_output_path,
                codec=video_codec,
                bitrate=bitrate,
                audio_codec="aac",  # Default audio codec
                temp_audiofile=tempfile.NamedTemporaryFile(delete=False, suffix='.aac').name,
                remove_temp=True,
                verbose=False
            )

            # Read the output file
            with open(temp_output_path, 'rb') as f:
                output_data = f.read()

            return output_data

        except Exception as e:
            st.error(f"Error converting video: {str(e)}")
            raise

        finally:
            # Clean up temporary files and close video
            video.close() if 'video' in locals() else None
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if os.path.exists(temp_output_path):
                os.unlink(temp_output_path)