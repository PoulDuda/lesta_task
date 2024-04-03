from fastapi import APIRouter, Request, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.operations.function import read_docx, calculate_tf_idf, read_pdf


router = APIRouter(
    tags=["pages"]
)

templates = Jinja2Templates(directory='src/templates')


@router.get("/", response_class=HTMLResponse)
def get_start_page(request: Request):
    return templates.TemplateResponse(name='start.html', request={'request': request})


@router.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile):
    try:
        if file.filename.endswith('.docx'):
            docx_content = await file.read()
            text = read_docx(docx_content)
            if text == []:
                raise HTTPException(status_code=404, detail='Empty file')
        elif file.filename.endswith('.pdf'):
            pdf_content = await file.read()
            text = read_pdf(pdf_content)
        tf_idf_values = calculate_tf_idf(text)
        sorted_words = sorted(tf_idf_values.items(), key=lambda x: x[1]['idf'], reverse=True)
        top_words = sorted_words[:50]
        data = {"words": top_words}
        if tf_idf_values == {}:
            raise HTTPException(status_code=404, detail='Empty file')
        return templates.TemplateResponse('output.html', {'request': request, 'data': data})
    except:
         raise HTTPException(status_code=404, detail='This file type is not supported')





