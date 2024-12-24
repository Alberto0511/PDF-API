import io
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader, PdfWriter

MAX_FILE_SIZE = 10 * 1024 * 1024  

async def remove_password_service(file: UploadFile, pwd: str):
    if not pwd:
        raise HTTPException(status_code=400, detail="La contraseña es requerida")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="El archivo excede el peso permitido")
    try:
        render_pdf = PdfReader(file.file)
        if render_pdf.is_encrypted:
            if not render_pdf.decrypt(pwd):
                raise HTTPException(status_code=400, detail="La contraseña no es la correcta")
    except Exception:
        raise HTTPException(status_code=400, detail="Error al desbloquear el PDF")
    write_pdf = PdfWriter()
    for page in render_pdf.pages:
        write_pdf.add_page(page)
    pdf_buffer = io.BytesIO()
    write_pdf.write(pdf_buffer)
    pdf_buffer.seek(0)
    content = pdf_buffer.getvalue()
    headers = {"Content-Disposition": "attachment; filename=unlocked.pdf"}
    return content, headers