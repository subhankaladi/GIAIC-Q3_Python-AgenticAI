from .base_converter import BaseConverter
import zipfile
import py7zr
import rarfile
import tarfile
import io
import streamlit as st
import os
import tempfile
import shutil

class ArchiveConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.title = "Archive Converter"
        self.icon = "📦"
        self.description = "Convert archives between different formats"
        self.supported_formats = {
            'zip': ['rar', '7z', 'tar', 'gz', 'bz2'],
            'rar': ['zip', '7z', 'tar', 'gz', 'bz2'],
            '7z': ['zip', 'rar', 'tar', 'gz', 'bz2'],
            'tar': ['zip', 'rar', '7z', 'gz', 'bz2'],
            'gz': ['zip', 'rar', '7z', 'tar', 'bz2'],
            'bz2': ['zip', 'rar', '7z', 'tar', 'gz']
        }

    def convert(self, input_file, output_format, compression_level="Normal", password=None, split_size=None):
        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary file for input
            with tempfile.NamedTemporaryFile(delete=False) as temp_input:
                temp_input.write(input_file.getvalue())
                temp_input_path = temp_input.name

            try:
                # Extract the input archive
                input_format = input_file.name.split('.')[-1].lower()
                
                if input_format == 'zip':
                    with zipfile.ZipFile(temp_input_path, 'r') as zip_ref:
                        if password:
                            zip_ref.setpassword(password.encode())
                        zip_ref.extractall(temp_dir)
                elif input_format == 'rar':
                    with rarfile.RarFile(temp_input_path, 'r') as rar_ref:
                        if password:
                            rar_ref.setpassword(password.encode())
                        rar_ref.extractall(temp_dir)
                elif input_format == '7z':
                    with py7zr.SevenZipFile(temp_input_path, 'r') as sz_ref:
                        if password:
                            sz_ref.setpassword(password.encode())
                        sz_ref.extractall(temp_dir)
                elif input_format in ['tar', 'gz', 'bz2']:
                    with tarfile.open(temp_input_path, 'r:*') as tar_ref:
                        tar_ref.extractall(temp_dir)

                # Create output archive
                output = io.BytesIO()
                
                if output_format == 'zip':
                    compression = {
                        "Store": zipfile.ZIP_STORED,
                        "Fast": zipfile.ZIP_DEFLATED,
                        "Normal": zipfile.ZIP_DEFLATED,
                        "Maximum": zipfile.ZIP_DEFLATED
                    }.get(compression_level, zipfile.ZIP_DEFLATED)
                    
                    with zipfile.ZipFile(output, 'w', compression=compression) as zip_out:
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, temp_dir)
                                zip_out.write(file_path, arcname)
                
                elif output_format == '7z':
                    with py7zr.SevenZipFile(output, 'w') as sz_out:
                        sz_out.writeall(temp_dir, os.path.basename(temp_dir))
                
                elif output_format in ['tar', 'gz', 'bz2']:
                    mode = {
                        'tar': 'w',
                        'gz': 'w:gz',
                        'bz2': 'w:bz2'
                    }.get(output_format, 'w')
                    
                    with tarfile.open(fileobj=output, mode=mode) as tar_out:
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, temp_dir)
                                tar_out.add(file_path, arcname)

                output.seek(0)
                return output.getvalue()

            finally:
                # Clean up temporary input file
                if os.path.exists(temp_input_path):
                    os.unlink(temp_input_path) 