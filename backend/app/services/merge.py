from fastapi import UploadFile, HTTPException
from starlette.responses import Response
from PyPDF2 import PdfMerger
import io
import tempfile
import os

MAX_FINAL_SIZE = 20 * 1024 * 1024  
async def merge_pdfs_service(files: list[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="Debes subir al menos un archivo PDF")
    merger = PdfMerger()
    temp_files = []  
    try:
        for file in files:
            if not file.filename.endswith(".pdf"):
                raise HTTPException(status_code=400, detail=f"El archivo {file.filename} no es un PDF")
            pdf_bytes = await file.read()
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                temp_pdf.write(pdf_bytes)
                temp_pdf.flush()
                temp_files.append(temp_pdf.name)  
                merger.append(temp_pdf.name)
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()
        final_size = output_buffer.getbuffer().nbytes
        if final_size > MAX_FINAL_SIZE:
            raise HTTPException(status_code=413, detail=f"El archivo final unido es demasiado grande: {final_size / (1024 * 1024):.2f} MB. El límite es de {MAX_FINAL_SIZE / (1024 * 1024):.2f} MB.")
        output_buffer.seek(0)
        headers = {
            "Content-Disposition": "attachment; filename=merged.pdf"
        }
        return Response(
            content=output_buffer.getvalue(),
            media_type="application/pdf",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al unir los PDFs: {str(e)}")
    finally:
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)