from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import os

from services.ocr_service import extract_text_from_image
from services.handwriting_service import generate_handwriting_pdf

app = FastAPI()

# Create folders automatically
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Static files
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

@app.get("/")
def home():
    return {"message": "AI Handwriting Backend Running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:

        # Unique filename
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        upload_path = f"uploads/{unique_name}"

        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # OCR Extract
        extracted_text = extract_text_from_image(upload_path)

        # Generate handwriting pdf
        output_pdf = generate_handwriting_pdf(extracted_text)

        pdf_url = f"https://ai-handwritting.onrender.com/outputs/{output_pdf}"

        return JSONResponse({
            "success": True,
            "text": extracted_text,
            "pdf_url": pdf_url
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )