from fastapi import FastAPI, Response, HTTPException, status, middleware, UploadFile
from src.models import Filetype
from fastapi.responses import StreamingResponse
import io
from src.extractor.extract_text import extract_text      
from src.save_data.convert_to_csv import convert_to_csv
from src.utils import get_file_buffer 

app = FastAPI()
@app.get("/")
async def health_check():
    return {"health": "ok"}

@app.head("/")
async def server():
    return {"alive": True}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    try:
        if file.content_type != Filetype.pdf:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload a pdf file")
        contents = await file.read()
        file_size = len(contents)
        max_size = 2_097_500  
        if file_size > max_size:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Accepts file below 2 Mb")
        data = extract_text.process_text(contents)
        convert_to_csv.save_as_csv(rows_list=data, filename=file.filename)
        await file.seek(0)
        return {"filename": file.filename, "message": "File uploaded Successfully"}
    except HTTPException:
        raise
    except Exception as e:
        print(e)

class CSVStreamingResponse(StreamingResponse):
    media_type = "text/csv"

@app.get("/downloadfile", response_class=CSVStreamingResponse)
def download_file():
    file_bytes = convert_to_csv.convert_df_to_bytes()
    with get_file_buffer(fileBytes=file_bytes) as file_buffer:
        for chunk in file_buffer:
            yield chunk
        
    
    
    



    


