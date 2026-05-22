from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from route import department

origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:8000'
]

app = FastAPI(
    root_path='/api',
)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(department)

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)