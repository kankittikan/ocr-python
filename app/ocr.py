import easyocr
from fastapi import FastAPI, UploadFile, HTTPException, Request
import jwt
import time
from fastapi.responses import JSONResponse
from token_validation import verify_access_token
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
lang_support = ['th', 'en']
reader_en = easyocr.Reader(['en'])
reader_th = easyocr.Reader(['th', 'en'])

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            verify_access_token(request)
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)

app.add_middleware(CustomMiddleware)

@app.post("/read")
async def upload_file(file: UploadFile, paragraph: bool = False, lang: str = 'en'):
    if not lang in lang_support:
        raise HTTPException(status_code=400, detail="Language not support")
    if not file.content_type or not file.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Required content-type image only")
    
    if lang == 'th':
        result = reader_th.readtext(file.file.read(), detail=0, paragraph=paragraph)
    else:
        result = reader_en.readtext(file.file.read(), detail=0, paragraph=paragraph)

    return {"result": result}