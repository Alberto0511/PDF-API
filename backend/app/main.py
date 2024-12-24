from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.middlewares.middlewares import limit_file_size
from app.routers import pdfs

# uvicorn app.main:app --reload
app = FastAPI()
origins = [
    "http://localhost:5173",  
]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.middleware("http")(limit_file_size)
app.include_router(pdfs.router)

@app.on_event("startup")
async def startup_event():
    print("El servidor se está iniciando...")

@app.on_event("shutdown")
async def shutdown_event():
    print("El servidor se está apagando...")