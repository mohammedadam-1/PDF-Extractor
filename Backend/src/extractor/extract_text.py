import io
from PIL import Image
import pdfplumber
import pymupdf
import pytesseract
from src.utils import structure_text


class ExtractText:

    def __init__(self):
        pass

    def get_text(self, pdf_bytes) -> str:
        """Extracts structured text or tables from a PDF."""
        try:
            full_output = []

            # 1. Try extracting native digital tables first using pdfplumber
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    tables = page.extract_tables()

                    if tables:
                        # Process found tables into structured, readable strings
                        page_text = f"--- Page {page_num + 1} (Table Data) ---\n"
                        for table in tables:
                            for row in table:
                                # Clean None values and join cells with tabs to maintain alignment
                                cleaned_row = [
                                    str(cell).strip() if cell else ""
                                    for cell in row
                                ]
                                page_text += "\t|\t".join(cleaned_row) + "\n"
                        full_output.append(page_text)
                        continue  # Skip OCR for this page since we got the digital text/table

            # 2. Fallback to PyMuPDF + Tesseract if pdfplumber found no tables/text (Scanned Image PDF)
            if not full_output:
                doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

                for page in doc:
                    # 300 DPI is optimal for Tesseract accuracy
                    pix = page.get_pixmap(dpi=300)
                    img_data = pix.tobytes("png")
                    image = Image.open(io.BytesIO(img_data))

                    # Using PSM 6 assuming uniform block of text or PSM 4 for column-like structures
                    custom_config = r"--psm 6"
                    page_text = pytesseract.image_to_string(
                        image, config=custom_config
                    )
                    full_output.append(page_text)

            return "\n\n".join(full_output)
                

        except Exception as e:
            print(f"Error during extraction: {e}")
            return ""


    def process_text(self, pdf_bytes):
        """Process raw text and return structured list of row lists"""
        try:
            raw_text = self.get_text(pdf_bytes=pdf_bytes)
            processed_data = structure_text(raw_text=raw_text)
            return processed_data
        except Exception as e:
            print(e)
            
extract_text = ExtractText()  
    
