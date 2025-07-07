import fitz
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype='pdf')
    text = ""
    for page in doc:
        if page.get_text():
            text += page.get_text()

        else: 
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))
            text += pytesseract.image_to_string(img)

    return text

    