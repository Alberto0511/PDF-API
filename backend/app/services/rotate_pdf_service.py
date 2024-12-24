import io
import os
import tempfile
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader, PdfWriter

async def rotate_pdf_service(file: UploadFile, angle: int):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    try:
        contenido = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al leer el archivo")
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
            temp_pdf.write(contenido)
            temp_pdf.flush()
            pdf_reader = PdfReader(temp_pdf.name)
            pdf_writer = PdfWriter()
            for page in pdf_reader.pages:
                rotated_page = page.rotate(angle)
                pdf_writer.add_page(rotated_page)
            rotated_pdf_buffer = io.BytesIO()
            pdf_writer.write(rotated_pdf_buffer)
            rotated_pdf_buffer.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=rotated.pdf"
        }
        return rotated_pdf_buffer.getvalue(), headers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al rotar el PDF: {str(e)}")
    finally:
        os.unlink(temp_pdf.name)