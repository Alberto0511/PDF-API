import io
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader, PdfWriter

async def split_pdf_service(file: UploadFile, start_page: int, end_page: int):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
    try:
        pdf_content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_content))
        total_pages = len(pdf_reader.pages)
        if start_page < 1 or end_page > total_pages:
            raise HTTPException(
                status_code=400,
                detail=f"El rango de páginas debe estar entre 1 y {total_pages}",
            )
        if start_page > end_page:
            raise HTTPException(
                status_code=400, detail="La página de inicio no puede ser mayor que la de fin"
            )
        pdf_writer = PdfWriter()
        for page_num in range(start_page - 1, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        output_buffer = io.BytesIO()
        pdf_writer.write(output_buffer)
        output_buffer.seek(0)
        headers = {
            "Content-Disposition": f"attachment; filename=separated_pages_{start_page}_to_{end_page}.pdf"
        }
        return output_buffer.getvalue(), headers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo PDF: {str(e)}")