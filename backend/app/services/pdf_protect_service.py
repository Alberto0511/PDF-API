import io
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader, PdfWriter

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

async def protect_pdf_service(file: UploadFile, pwd: str):
    if not pwd:
        raise HTTPException(status_code=400, detail="Contraseña requerida")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="El archivo excede el tamaño permitido")
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="El archivo no es un PDF")
    try:
        render_pdf = PdfReader(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al leer el archivo PDF: {str(e)}")
    writer_pdf = PdfWriter()
    for page in render_pdf.pages:
        writer_pdf.add_page(page)
    try:
        writer_pdf.encrypt(user_password=pwd, use_128bit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al encriptar el archivo: {str(e)}")
    protected_pdf_buffer = io.BytesIO()
    
    try:
        writer_pdf.write(protected_pdf_buffer)
        protected_pdf_buffer.seek(0) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir el archivo PDF: {str(e)}")
    content = protected_pdf_buffer.getvalue()
    headers = {"Content-Disposition": "attachment; filename=protected.pdf"}
    
    return content, headers