# from .base_converter import BaseConverter
# from PIL import Image
# import io
# import streamlit as st
# from pdf2image import convert_from_bytes
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM
# import tempfile
# import os
# import numpy as np
# from skimage import measure
# from skimage.filters import threshold_otsu

# class ImageConverter(BaseConverter):
#     def __init__(self):
#         super().__init__()
#         self.title = "Image Converter"
#         self.icon = "📸"
#         self.description = "Convert between various image formats including PNG, JPG, SVG, WEBP, and more."
#         self.supported_formats = {
#             'jpg': ['png', 'gif', 'bmp', 'webp', 'tiff'],
#             'jpeg': ['png', 'gif', 'bmp', 'webp', 'tiff'],
#             'png': ['jpg', 'gif', 'bmp', 'webp', 'tiff'],
#             'gif': ['jpg', 'png', 'bmp', 'webp', 'tiff'],
#             'bmp': ['jpg', 'png', 'gif', 'webp', 'tiff'],
#             'webp': ['jpg', 'png', 'gif', 'bmp', 'tiff'],
#             'tiff': ['jpg', 'png', 'gif', 'bmp', 'webp'],
#             'tif': ['jpg', 'png', 'gif', 'bmp', 'webp']
#         }

#     def _bitmap_to_svg(self, image):
#         # Convert image to grayscale
#         if image.mode != 'L':
#             image = image.convert('L')
        
#         # Convert to numpy array
#         data = np.array(image)
        
#         # Apply Otsu's thresholding
#         thresh = threshold_otsu(data)
#         binary = data > thresh
        
#         # Find contours
#         contours = measure.find_contours(binary, 0.5)
        
#         # Create SVG path data
#         svg_paths = []
#         for contour in contours:
#             # Simplify the contour
#             contour = measure.approximate_polygon(contour, tolerance=2.0)
            
#             # Convert to SVG path
#             path_data = "M "
#             for i, point in enumerate(contour):
#                 if i == 0:
#                     path_data += f"{point[1]:.1f},{point[0]:.1f} "
#                 else:
#                     path_data += f"L {point[1]:.1f},{point[0]:.1f} "
#             path_data += "Z"
#             svg_paths.append(f'<path d="{path_data}" fill="black"/>')
        
#         # Create SVG document
#         svg_doc = f"""<?xml version="1.0" standalone="no"?>
# <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
# <svg width="{image.width}" height="{image.height}" version="1.1" xmlns="http://www.w3.org/2000/svg">
# {''.join(svg_paths)}
# </svg>"""
        
#         return svg_doc.encode('utf-8')

#     def convert(self, input_file, output_format, quality=85):
#         input_format = input_file.name.split('.')[-1].lower()
#         file_bytes = input_file.getvalue()
        
#         # Handle PDF to image conversion
#         if input_format == 'pdf':
#             images = convert_from_bytes(file_bytes)
#             if not images:
#                 raise ValueError("No images found in PDF")
            
#             # Convert first page to desired format
#             output = io.BytesIO()
#             if output_format in ['jpg', 'jpeg']:
#                 images[0].convert('RGB').save(output, format='JPEG', quality=95)
#             else:
#                 images[0].save(output, format=output_format.upper())
#             output.seek(0)
#             return output.getvalue()
        
#         # Handle SVG to other formats
#         if input_format == 'svg':
#             try:
#                 # Create temporary file for SVG
#                 with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as temp_svg:
#                     temp_svg.write(file_bytes)
#                     temp_svg_path = temp_svg.name

#                 try:
#                     # Convert SVG to ReportLab drawing
#                     drawing = svg2rlg(temp_svg_path)
#                     if drawing is None:
#                         raise ValueError("Could not parse SVG file")

#                     # Create output buffer
#                     output = io.BytesIO()

#                     # Convert to desired format
#                     if output_format == 'pdf':
#                         renderPM.drawToFile(drawing, output, fmt="PDF")
#                     else:  # PNG
#                         renderPM.drawToFile(drawing, output, fmt="PNG")

#                     output.seek(0)
#                     return output.getvalue()

#                 finally:
#                     # Clean up temporary file
#                     if os.path.exists(temp_svg_path):
#                         os.unlink(temp_svg_path)

#             except Exception as e:
#                 raise ValueError(f"Error converting SVG: {str(e)}")
        
#         # Handle other image conversions
#         try:
#             image = Image.open(input_file)
            
#             # Handle conversion to SVG
#             if output_format == 'svg':
#                 return self._bitmap_to_svg(image)
            
#             # Convert to RGB if needed (for JPG conversion)
#             if output_format in ['jpg', 'jpeg'] and image.mode in ['RGBA', 'LA']:
#                 background = Image.new('RGB', image.size, (255, 255, 255))
#                 background.paste(image, mask=image.split()[-1])
#                 image = background
            
#             # Prepare output
#             output = io.BytesIO()
            
#             # Save in the desired format with proper format name
#             if output_format == 'pdf':
#                 image.save(output, format='PDF', resolution=100.0)
#             elif output_format in ['jpg', 'jpeg']:
#                 image.save(output, format='JPEG', quality=quality)
#             elif output_format in ['gif', 'bmp']:
#                 image.save(output, format=output_format.upper())
#             elif output_format in ['webp']:
#                 image.save(output, format='WEBP', quality=quality)
#             elif output_format in ['tiff', 'tif']:
#                 image.save(output, format='TIFF')
#             else:
#                 raise ValueError(f"Unsupported output format: {output_format}")
            
#             output.seek(0)
#             return output.getvalue()
            
#         except Exception as e:
#             raise ValueError(f"Error converting image: {str(e)}") 






from .base_converter import BaseConverter
from PIL import Image
import io
import streamlit as st
from pdf2image import convert_from_bytes
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import tempfile
import os
import numpy as np
from skimage import measure
from skimage.filters import threshold_otsu

class ImageConverter(BaseConverter):
    def __init__(self):
        super().__init__()
        self.title = "Image Converter"
        self.icon = "📸"
        self.description = "Convert between various image formats including PNG, JPG, SVG, WEBP, and more."
        self.supported_formats = {
            'jpg': ['png', 'gif', 'bmp', 'webp', 'tiff'],
            'jpeg': ['png', 'gif', 'bmp', 'webp', 'tiff'],
            'png': ['jpg', 'gif', 'bmp', 'webp', 'tiff'],
            'gif': ['jpg', 'png', 'bmp', 'webp', 'tiff'],
            'bmp': ['jpg', 'png', 'gif', 'webp', 'tiff'],
            'webp': ['jpg', 'png', 'gif', 'bmp', 'tiff'],
            'tiff': ['jpg', 'png', 'gif', 'bmp', 'webp'],
            'tif': ['jpg', 'png', 'gif', 'bmp', 'webp']
        }

    def _bitmap_to_svg(self, image):
        # Convert image to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert to numpy array
        data = np.array(image)
        
        # Apply Otsu's thresholding
        thresh = threshold_otsu(data)
        binary = data > thresh
        
        # Find contours
        contours = measure.find_contours(binary, 0.5)
        
        # Create SVG path data
        svg_paths = []
        for contour in contours:
            # Simplify the contour
            contour = measure.approximate_polygon(contour, tolerance=2.0)
            
            # Convert to SVG path
            path_data = "M "
            for i, point in enumerate(contour):
                if i == 0:
                    path_data += f"{point[1]:.1f},{point[0]:.1f} "
                else:
                    path_data += f"L {point[1]:.1f},{point[0]:.1f} "
            path_data += "Z"
            svg_paths.append(f'<path d="{path_data}" fill="black"/>')
        
        # Create SVG document
        svg_doc = f"""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="{image.width}" height="{image.height}" version="1.1" xmlns="http://www.w3.org/2000/svg">
{''.join(svg_paths)}
</svg>"""
        
        return svg_doc.encode('utf-8')

    def convert(self, input_file, output_format, quality=85):
        input_format = input_file.name.split('.')[-1].lower()
        file_bytes = input_file.getvalue()
        
        # Handle PDF to image conversion
        if input_format == 'pdf':
            images = convert_from_bytes(file_bytes)
            if not images:
                raise ValueError("No images found in PDF")
            
            # Convert first page to desired format
            output = io.BytesIO()
            if output_format in ['jpg', 'jpeg']:
                images[0].convert('RGB').save(output, format='JPEG', quality=95)
            else:
                images[0].save(output, format=output_format.upper())
            output.seek(0)
            return output.getvalue()
        
        # Handle SVG to other formats
        if input_format == 'svg':
            try:
                # Create temporary file for SVG
                with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as temp_svg:
                    temp_svg.write(file_bytes)
                    temp_svg_path = temp_svg.name

                try:
                    # Convert SVG to ReportLab drawing
                    drawing = svg2rlg(temp_svg_path)
                    if drawing is None:
                        raise ValueError("Could not parse SVG file")

                    # Create output buffer
                    output = io.BytesIO()

                    # Convert to desired format
                    if output_format == 'pdf':
                        renderPM.drawToFile(drawing, output, fmt="PDF")
                    else:  # PNG
                        renderPM.drawToFile(drawing, output, fmt="PNG")

                    output.seek(0)
                    return output.getvalue()

                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_svg_path):
                        os.unlink(temp_svg_path)

            except Exception as e:
                raise ValueError(f"Error converting SVG: {str(e)}")
        
        # Handle other image conversions
        try:
            image = Image.open(input_file)
            
            # Handle conversion to SVG
            if output_format == 'svg':
                return self._bitmap_to_svg(image)
            
            # Convert to RGB if needed (for JPG conversion)
            if output_format in ['jpg', 'jpeg'] and image.mode in ['RGBA', 'LA']:
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            # Prepare output
            output = io.BytesIO()
            
            # Save in the desired format with proper format name
            if output_format == 'pdf':
                image.save(output, format='PDF', resolution=100.0)
            elif output_format in ['jpg', 'jpeg']:
                image.save(output, format='JPEG', quality=quality)
            elif output_format == 'png':
                image.save(output, format='PNG')
            elif output_format in ['gif', 'bmp']:
                image.save(output, format=output_format.upper())
            elif output_format == 'webp':
                image.save(output, format='WEBP', quality=quality)
            elif output_format in ['tiff', 'tif']:
                image.save(output, format='TIFF')
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            raise ValueError(f"Error converting image: {str(e)}")