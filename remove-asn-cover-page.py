import PyPDF2
from pyzbar.pyzbar import decode
from PIL import Image, ImageEnhance
import re
import sys
import os

def get_image_extension(image):
    filters = image.get('/Filter', [])
    if '/DCTDecode' in filters:
        return 'jpg'  # JPEG extension for color scans
    elif '/FlateDecode' in filters:
        return 'png'  # PNG extension for color scans
    elif '/CCITTFaxDecode' in filters:
        return 'tif'  # TIFF extension for B&W scans
    else:
        print(f"Unknown image type: {filters}")
        return 'unknown'  # Unknown extension

# This is necessary for color scans
# However paperless won't detect the QR code if the
# scanned page was in color
def preprocess_image_for_qr_detection(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    enhancer = ImageEnhance.Contrast(image)
    adjusted_image = enhancer.enhance(2.0)
    adjusted_image.save(image_path)

def extract_images(pdf_path, page_num):
    images = []
    with open(pdf_path, 'rb') as pdf_file:
        pdf = PyPDF2.PdfReader(pdf_file)
        page = pdf.pages[page_num]
        xObject = page['/Resources']['/XObject'].get_object()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                images.append(xObject[obj])
    return images

def contains_specific_qr_code(image_path, qr_data_pattern):
    image = Image.open(image_path)
    decoded_objects = decode(image)
    for obj in decoded_objects:
        if re.match(qr_data_pattern, obj.data.decode()):
            return True
    return False

def calculate_text_match_percentage(page, text_pattern):
    page_text = page.extract_text()
    page_text = re.sub(r'[\s\r\n]', '', page_text)
    match = re.search(text_pattern, page_text)
    if match:
        matched_text = match.group(0)
        percentage_match = len(matched_text) / len(page_text)
        return percentage_match
    return 0.0

def contains_valid_content(pdf, page_num, qr_data_pattern, text_pattern, text_threshold):
    images = extract_images(pdf_path, page_num)
    qr_code_found = False
    
    for index, image in enumerate(images):
        image_data = image.get_data()
        image_extension = get_image_extension(image)
        if image_extension == 'unknown': continue
        image_filename = f"page_{page_num}_image_{index}.{image_extension}"
        with open(image_filename, 'wb') as f:
            f.write(image_data)
        
        # Preprocess the image to enhance QR code contrast
        preprocess_image_for_qr_detection(image_filename)
        if contains_specific_qr_code(image_filename, qr_data_pattern):
            qr_code_found = True
            
        # remove temp image file
        os.remove(image_filename)
    
    text_match_percent = calculate_text_match_percentage(pdf.pages[page_num], text_pattern)
    cover_page_found = qr_code_found and (text_match_percent >= text_threshold)
    print(f"Page Number: {page_num}")
    print(f"ASN Cover Page Found: {cover_page_found}")
    print(f"QR Code Found: {qr_code_found}")
    print(f"Match Percent: {text_match_percent}")
    return cover_page_found

def main(pdf_path, qr_data_pattern, text_pattern, text_threshold):
    pdf = PyPDF2.PdfReader(pdf_path)
    num_pages = len(pdf.pages)
    pages_to_remove = []
    
    for page_num in range(num_pages):
        if contains_valid_content(pdf, page_num, qr_data_pattern, text_pattern, text_threshold):
            pages_to_remove.append(page_num)

    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(num_pages):
        if page_num not in pages_to_remove:
            pdf_writer.add_page(pdf.pages[page_num])
    
    with open(pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove-asn-cover-page.py /path/to/your/document.pdf <text_threshold>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    # the text_threshold is the percentage match
    # of the text_pattern listed below.
    # Sometimes there is an extra character 
    # parsed when using PDFReader. Usually 0.80 is a good start.
    text_threshold = float(sys.argv[2])

    # Define the patterns for QR code and text to match
    # Modify as needed for your specific text pattern
    qr_data_pattern = r"^ASN\d{7}$"
    text_pattern = r"ASN\d{7}"  

    main(pdf_path, qr_data_pattern, text_pattern, text_threshold)
