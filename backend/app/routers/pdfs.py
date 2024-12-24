from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from starlette.responses import Response
from app.services.merge import merge_pdfs_service
from app.services.pdf_protect_service import protect_pdf_service
from app.services.image_to_pdf_service import images_to_pdf_service
from app.services.rotate_pdf_service import rotate_pdf_service
from app.services.remove_password_service import remove_password_service
from app.services.split_pdf_service import split_pdf_service
from app.services.pdf_to_word_service import pdf_to_word_service

router = APIRouter()

@router.post("/merge-pdfs")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    return await merge_pdfs_service(files)

@router.post("/protect-pdfs")
async def protect_pdf(file: UploadFile = File(...), pwd: str = Form(...)):
    content, headers = await protect_pdf_service(file, pwd)
    return Response(
        content=content,
        media_type="application/pdf",
        headers=headers)

@router.post("/images-to-pdfs")
async def images_to_pdf(files: list[UploadFile] = File(...)):
    content, headers = await images_to_pdf_service(files)
    return Response(
        content=content,
        media_type="application/pdf",
        headers=headers)

@router.post("/rotate-pdf")
async def rotate_pdf(file: UploadFile = File(...), angle: int = Form(...)):
    content, headers = await rotate_pdf_service(file, angle)
    return Response(
        content=content,
        media_type="application/pdf",
        headers=headers)

@router.post("/remove-password")
async def remove_password(file: UploadFile = File(...), pwd: str = Form(...)):
    content, headers = await remove_password_service(file, pwd)
    return Response(
        content=content,
        media_type="application/pdf",
        headers=headers)

@router.post("/split-pdf")
async def split_pdf(file: UploadFile = File(...), start_page: int = Form(...), end_page: int = Form(...)):
    content, headers = await split_pdf_service(file, start_page, end_page)
    return Response(
        content=content,
        media_type="application/pdf",
        headers=headers)

@router.post("/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    content, headers = await pdf_to_word_service(file)
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers)