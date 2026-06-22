import os
import fitz
import pymupdf
from PIL import Image
import pytesseract
import pdfplumber
from config import *
from utils.logger import logger
from schemas.graph_state import GraphState

def parser_node(state: GraphState):
    try:
        file_paths = state.get("file_paths") or []
        file_paths = [fp for fp in file_paths if fp]

        if not file_paths:
            state["error"] = "No file paths provided"
            return state

        pages = []
        text = ""
        images =[]

        for file_path in file_paths:
            ext = os.path.splitext(file_path)[1].lower()

            if ext in [".jpg", ".jpeg", ".png", ".tiff", ".webp"]:
                # image
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                pages = [{"page": 1, "text": text, "type": "image", "source": file_path}]
            else:
                # PDF
                with pdfplumber.open(file_path) as pdf:
                  doc = fitz.open(file_path)
                  for page_num, page in enumerate(pdf.pages, start=1):
                        text = page.extract_text() or ""
                        tables = page.extract_tables() or []
                        if tables:
                          table_text = "\n".join([" | ".join(map(str, row)) for row in tables])
                          text += "\n\nTables:\n" + table_text
                        try:
                          pdf_page = doc[page_num-1]
                          pdf_image = pdf_page.get_images(full=True)
                          for img_index, img in enumerate(pdf_image):
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            image_filename = f"page_{page_num}_img_{img_index}.{image_ext}"
                            image_path = str(IMAGES_DIR / image_filename)
                            with open(image_path, "wb") as image_file:
                              image_file.write(image_bytes)
                            images.append(image_path)
                        except Exception as e:
                          logger.warning(f"Error converting page {page_num} to image: {e}")
                        if len(text.strip()) < 10 and image_path:
                          ocr_text = pytesseract.image_to_string(image_path)
                          text = (text + "\n" + ocr_text).strip()

                        pages.append({
                            "page": page_num,
                            "text": text.strip(),
                            "image":images or "",
                            "source": file_path
                        })

        state["structured_pages"] = pages
        state["raw_text"] = text.strip()
        image_count = sum(len(p.get("image", [])) for p in pages)
        logger.info(f"Parser completed: {len(pages)} pages | images count {image_count} ")
        return state

    except Exception as e:
        logger.error(f"Parser failed: {e}")
        state["error"] = str(e)
        return state
