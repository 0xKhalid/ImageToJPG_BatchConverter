
# Batch Images to JPG Converter
A Python GUI tool for batch conversion of images in various formats (including HEIC) to high-quality JPG. This tool scans a selected directory for image files, displays the count, and prompts the user for confirmation before converting and saving the images to a chosen output directory.

## Features
- Supports multiple image formats: PNG, BMP, TIFF, WEBP, GIF, and HEIC.
- Allows users to select both input and output directories.
- Displays the count of images found before conversion.
- Converts images to high-quality JPG (95% quality).

## Requirements
- **Python 3.x**
- **Pillow**: for image processing
- **pillow-heif**: for HEIC support
- **threading**: to keep the GUI responsive during conversions (included with Python)

### Install Requirements
``` pip install pillow pillow-heif ```

## Usage
1. **Clone the Repository**:
   ```git clone https://github.com/0xKhalid/ImageToJPG_BatchConverter
   cd ImageToJPG_BatchConverter.py```

2. **Run the Application**:
   ```python ImageToJPG_BatchConverter.py```

3. **Using the Tool**:
   - Select a directory containing images to scan.
   - The tool displays the count of image files found.
   - Choose an output directory.
   - Confirm conversion to JPG format. Converted images are saved in the selected output directory.

## License
This project is licensed under the MIT License.