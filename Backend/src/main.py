from fastapi import FastAPI, Response, HTTPException, status, middleware, UploadFile
from src.models import Filetype
from fastapi.responses import StreamingResponse
import io
from src.extractor.extract_text import extract_text      
from src.save_data.convert_to_csv import convert_to_csv
from src.utils import get_file_buffer 
from fastapi.middleware.cors import CORSMiddleware
from src.config.config import settings
from pathlib import Path
import pandas as pd

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=['GET', 'HEAD', 'OPTIONS', 'POST'],
    allow_headers=["Authorization", "Accept", "Content-Type", "X-CSRF-Token", "Baggage", "X-Requested-With", "Sentry-Trace"],
    max_age=86200,
)


@app.get("/home")
async def health_check():
    return {"health": "ok"}

# @app.head("/")
# async def server():
#     return {"alive": True}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):

    if file.content_type != Filetype.pdf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Upload a pdf file"
        )

    contents = await file.read()

    if len(contents) > 2_097_500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Accepts file below 2 Mb"
        )

    data = extract_text.process_text(contents)
    if not data:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract text from the PDF"
        )   
    df = pd.DataFrame(data)

    buffer = io.StringIO()

    df.to_csv(
        buffer,
        header=False,
        index=False
    )

    csv_bytes = buffer.getvalue().encode("utf-8")

    filename = f"{Path(file.filename).stem}.csv"

    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f'attachment; filename="{filename}"'
        }
    )

# class CSVStreamingResponse(StreamingResponse):
#     media_type = "text/csv"

# @app.get("/downloadfile", response_class=CSVStreamingResponse)
# def download_file():
#     file_bytes = convert_to_csv.convert_df_to_bytes()
#     with get_file_buffer(fileBytes=file_bytes) as file_buffer:
#         for chunk in file_buffer:
#             yield chunk
        
        
        
backend_root = Path(__file__).resolve().parent.parent
static_path = backend_root / "static_dist"


app.frontend("/", directory=str(static_path))        
    
    
    



    


