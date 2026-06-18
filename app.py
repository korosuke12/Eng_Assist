# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from main import ingest_documents, ask_question
import shutil
from pathlib import Path

app = FastAPI(title="Engineering Assist - Multimodal")

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/ingest")
async def ingest_files(files: list[UploadFile] = File(...)):
    saved_paths = []
    
    for file in files:
        if not file.filename.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.docx', '.txt')):
            raise HTTPException(400, "Unsupported file type")
        
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(str(file_path))

    result = ingest_documents(saved_paths)
    
    return {
        "status": "success",
        "files_uploaded": len(saved_paths),
        "chunks_created": len(result.get("chunks", [])),
        "message": "Files processed successfully. You can now ask questions."
    }


@app.post("/query")
async def query(query: str, use_reranker: bool = True):
    result = ask_question(query, use_reranker)
    
    return {
        "query": query,
        "answer": result.get("response", "No relevant information found."),
        "sources": len(result.get("retrieved_docs", [])),
        "status": result.get("status")
    }