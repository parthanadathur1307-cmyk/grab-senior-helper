import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def extract_menu_items(pdf_path):
    # Extract text from PDF using pdfplumber
    menu_items = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()  # Extract text from each page
            if text:
                menu_items.extend(text.split('\n'))  # Split items by newline
    
    return menu_items


def extract_menu_items_with_ocr(pdf_path):
    # Extract images from PDF then perform OCR
    menu_items = []
    images = convert_from_path(pdf_path)
    for image in images:
        text = pytesseract.image_to_string(image)  # use OCR to extract text from image
        menu_items.extend(text.split('\n'))  # Split items by newline
    
    return menu_items


# Example usage:
if __name__ == '__main__':
    pdf_path = 'path_to_your_pdf.pdf'  # Update this with your PDF file path
    items = extract_menu_items(pdf_path)
    ocr_items = extract_menu_items_with_ocr(pdf_path)
    print("Menu items from text:", items)
    print("Menu items from OCR:", ocr_items)