import io
import os
import tempfile
from fastapi import UploadFile, HTTPException
from pdf2docx import Converter

async def pdf_to_word_service(file: UploadFile):
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
            doc_buffer = io.BytesIO()
            keep_images = True
            keep_tables = True
            keep_styles = True
            convertir = Converter(temp_pdf.name)
            convertir.convert(doc_buffer, keep_images=keep_images, keep_tables=keep_tables, keep_styles=keep_styles)
            convertir.close()
        doc_buffer.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=converted.docx"
        }
        return doc_buffer.getvalue(), headers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conversión: {str(e)}")
    finally:
        os.unlink(temp_pdf.name)