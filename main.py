from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io

app = FastAPI(title="Image to Text OCR API")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "OCR service is running"}


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        text = pytesseract.image_to_string(image)

        return JSONResponse({
            "success": True,
            "filename": file.filename,
            "ocr_text": text.strip()
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
