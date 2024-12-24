import io
from fastapi import UploadFile, HTTPException
from starlette.responses import Response
from PIL import Image

async def images_to_pdf_service(files: list[UploadFile]):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"]
    images = []
    for file in files:
        if not any(file.filename.endswith(ext) for ext in image_extensions):
            raise HTTPException(status_code=400, detail="Todos los archivos deben ser imágenes")
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        if image.mode in ("RGBA", "P"): 
            image = image.convert("RGB")
        images.append(image)
    pdf_buffer = io.BytesIO()
    if images:
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
    pdf_buffer.seek(0)
    headers = {
        "Content-Disposition": "attachment; filename=converted_images.pdf"
    }
    return pdf_buffer.getvalue(), headers
