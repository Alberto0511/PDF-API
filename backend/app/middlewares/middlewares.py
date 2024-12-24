from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import Request

async def limit_file_size(request: Request, call_next):
    max_size = 10 * 1024 * 1024  # 10 MB
    content_length = int(request.headers.get('Content-Length', 0))
    if content_length > max_size:
        return Response(content="El archivo es demasiado grande", status_code=413)
    return await call_next(request)

