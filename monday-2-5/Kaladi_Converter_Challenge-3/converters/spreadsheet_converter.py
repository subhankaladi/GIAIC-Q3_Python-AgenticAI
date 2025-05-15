from .base_converter import BaseConverter
import pandas as pd
import io
import streamlit as st
from openpyxl import Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows

class SpreadsheetConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.title = "Spreadsheet Converter"
        self.icon = "📊"
        self.description = "Convert spreadsheets between different formats"
        self.supported_formats = {
            'xlsx': ['xls', 'csv', 'ods', 'tsv'],
            'xls': ['xlsx', 'csv', 'ods', 'tsv'],
            'csv': ['xlsx', 'xls', 'ods', 'tsv'],
            'ods': ['xlsx', 'xls', 'csv', 'tsv'],
            'tsv': ['xlsx', 'xls', 'csv', 'ods']
        }

    def convert(self, input_file, output_format, encoding='utf-8', include_header=True, delimiter=','):
        # Read the input file
        input_format = input_file.name.split('.')[-1].lower()
        
        if input_format in ['xlsx', 'xls']:
            df = pd.read_excel(input_file)
        elif input_format == 'csv':
            df = pd.read_csv(input_file, encoding=encoding)
        elif input_format == 'tsv':
            df = pd.read_csv(input_file, sep='\t', encoding=encoding)
        elif input_format == 'ods':
            df = pd.read_excel(input_file, engine='odf')
        
        # Convert to output format
        output = io.BytesIO()
        
        if output_format in ['xlsx', 'xls']:
            df.to_excel(output, index=False, header=include_header)
        elif output_format == 'csv':
            df.to_csv(output, index=False, header=include_header, encoding=encoding)
        elif output_format == 'tsv':
            df.to_csv(output, index=False, header=include_header, sep='\t', encoding=encoding)
        elif output_format == 'ods':
            df.to_excel(output, index=False, header=include_header, engine='odf')
        
        output.seek(0)
        return output.getvalue() 