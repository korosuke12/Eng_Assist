import os
from PIL import Image
import pytesseract
import pdfplumber
from utils.logger import logger
from schemas.graph_state import GraphState

def parser_node(state: GraphState):
    try:
        file_paths = state.get("file_paths") or state.get("filePaths") or []
        file_paths = [fp for fp in file_paths if fp]

        if not file_paths:
            state["error"] = "No file paths provided"
            return state

        all_pages = []
        full_text = ""

        for file_path in file_paths:
            ext = os.path.splitext(file_path)[1].lower()

            if ext in [".jpg", ".jpeg", ".png", ".tiff", ".webp"]:
                # image
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                pages = [{"page": 1, "text": text, "type": "image", "source": file_path}]
            else:
                # PDF - Handle text with images pdf's
                pages = []
                with pdfplumber.open(file_path) as pdf:
                    for page_num, page in enumerate(pdf.pages, start=1):
                        # Try to extract text normally
                        text = page.extract_text() or ""

                        if len(text.strip()) < 50:   
                            try:
                                img = page.to_image(resolution=300).original
                                image_path = f"./data/images/page_{page_num}.png"
                                img.save(image_path)
                                ocr_text = pytesseract.image_to_string(img)
                                text = (text + "\n" + ocr_text).strip()
                            except:
                                pass

                        pages.append({
                            "page": page_num,
                            "text": text,
                            "image":image_path,
                            "source": file_path
                        })

        state["structured_pages"] = all_pages
        state["raw_text"] = full_text.strip()
        logger.info(f"Parser completed: {len(all_pages)} pages")
        return state

    except Exception as e:
        logger.error(f"Parser failed: {e}")
        state["error"] = str(e)
        return state