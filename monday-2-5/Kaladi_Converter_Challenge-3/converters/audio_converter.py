from .base_converter import BaseConverter
import soundfile as sf
import numpy as np
import io
import streamlit as st
import tempfile
import os
import time
import shutil

class AudioConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.title = "Audio Converter"
        self.icon = "🎵"
        self.description = "Convert audio files between different formats"
        self.supported_formats = {
            'wav': ['mp3', 'ogg', 'flac'],
            'mp3': ['wav', 'ogg', 'flac'],
            # 'ogg': ['wav', 'mp3', 'flac'],
            'flac': ['wav', 'mp3', 'ogg']
        }

    def convert(self, input_file, output_format, bitrate=192, sample_rate=44100, channels=2):
        # Create a temporary directory for our files
        temp_dir = tempfile.mkdtemp()
        temp_input_path = os.path.join(temp_dir, f"input.{input_file.name.split('.')[-1]}")
        temp_output_path = os.path.join(temp_dir, f"output.{output_format}")

        try:
            # Write input file to temporary location
            with open(temp_input_path, 'wb') as f:
                f.write(input_file.getvalue())
            
            # Verify input file was written
            if not os.path.exists(temp_input_path):
                raise FileNotFoundError(f"Failed to write input file to {temp_input_path}")
            
            # Read the input audio file
            try:
                data, input_samplerate = sf.read(temp_input_path)
            except Exception as e:
                raise Exception(f"Failed to read audio file: {str(e)}")
            
            # Resample if needed
            if input_samplerate != sample_rate:
                try:
                    from scipy import signal
                    number_of_samples = round(len(data) * float(sample_rate) / input_samplerate)
                    data = signal.resample(data, number_of_samples)
                except Exception as e:
                    raise Exception(f"Failed to resample audio: {str(e)}")
            
            # Convert to mono if needed
            if channels == 1 and len(data.shape) > 1:
                data = np.mean(data, axis=1)
            
            # Write the output file
            try:
                sf.write(temp_output_path, data, sample_rate)
            except Exception as e:
                raise Exception(f"Failed to write output file: {str(e)}")
            
            # Verify output file was created
            if not os.path.exists(temp_output_path):
                raise FileNotFoundError(f"Failed to create output file at {temp_output_path}")
            
            # Wait a moment to ensure file is written
            time.sleep(1)
            
            # Read the output file
            try:
                with open(temp_output_path, 'rb') as f:
                    output_data = f.read()
            except Exception as e:
                raise Exception(f"Failed to read output file: {str(e)}")
            
            if not output_data:
                raise Exception("Output file is empty")
            
            return output_data

        except Exception as e:
            # Log the error details
            st.error(f"Detailed error: {str(e)}")
            st.error(f"Input path: {temp_input_path}")
            st.error(f"Output path: {temp_output_path}")
            raise

        finally:
            # Clean up the temporary directory
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                st.warning(f"Warning: Could not clean up temporary files: {str(e)}")
                # Try to clean up individual files if directory removal fails
                try:
                    if os.path.exists(temp_input_path):
                        os.unlink(temp_input_path)
                    if os.path.exists(temp_output_path):
                        os.unlink(temp_output_path)
                except:
                    pass

    def convert_file(self, input_file, output_format):
        input_format = input_file.name.split('.')[-1].lower()
        
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{input_format}') as temp_input:
            temp_input.write(input_file.getvalue())
            temp_input_path = temp_input.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}') as temp_output:
            temp_output_path = temp_output.name

        try:
            # Read the audio file
            data, samplerate = sf.read(temp_input_path)
            
            # Write to the desired format
            sf.write(temp_output_path, data, samplerate)
            
            # Wait a bit to ensure file is written
            time.sleep(1)
            
            # Read the output file
            with open(temp_output_path, 'rb') as f:
                output_data = f.read()
            
            return output_data
            
        finally:
            # Clean up temporary files with retries
            max_retries = 3
            retry_delay = 1  # seconds
            
            for _ in range(max_retries):
                try:
                    if os.path.exists(temp_input_path):
                        os.unlink(temp_input_path)
                    if os.path.exists(temp_output_path):
                        os.unlink(temp_output_path)
                    break
                except Exception as e:
                    time.sleep(retry_delay)
                    if _ == max_retries - 1:
                        st.warning(f"Warning: Some temporary files could not be cleaned up: {str(e)}") 