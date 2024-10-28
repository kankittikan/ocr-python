import easyocr
from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()
lang_support = ['th', 'en']
reader_en = easyocr.Reader(['en'])
reader_th = easyocr.Reader(['th', 'en'])

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