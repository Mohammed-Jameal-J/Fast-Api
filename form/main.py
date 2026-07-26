from fastapi import FastAPI, UploadFile, File
import pandas as pd
from PyPDF2 import PdfReader
import io

app = FastAPI()

# @app.post("/feedback/")
# def create_feedback(
#     name: str = Form(...),
#     email: str = Form(...),
# ):
#     return {"name": name, "email": email}

# file upload 

# @app.post("/uploadfile/")
# async def file_upload(file: UploadFile = File(...)):
#     content = await file.read()

#     try:
#         text_p = content.decode("utf-8")[:100]
#     except Exception:
#         text_p = "File is not a text file"

#     return {
#         "filename": file.filename,
#         "content_preview": text_p
#     }

# multiple file upload

# @app.post("/uploadfiles/")
# async def multiple_file_upload(files: List[UploadFile] = File(...)):
#     file_details = []
#     for file in files:
#         content = await file.read()
#         try:
#             text_p = content.decode("utf-8")[:100]
#         except Exception:
#             text_p = "File is not a text file"

#         file_details.append({
#             "filename": file.filename,
#             "content_preview": text_p
#         })

#     return {"files": file_details}

# Multi File Upload (Excel & PDF)

@app.post("/uploadfiles/")
async def multiple_file_upload(files: List[UploadFile] = File(...)):
    file_details = []
    for file in files:
        content = await file.read()
        name = file.filename.lower()
        if name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(content))
            return {"Type": "Excel","preview": df.head(3).to_dict(),"Shape": df.shape, "Columns": df.columns.tolist()}
        elif name.endswith(".pdf"):
            pdf_reader = PdfReader(io.BytesIO(content))
            text_p = "".join(page.extract_text() for page in pdf_reader.pages)[:100]
        
            return {"Type": "PDF", "preview": text_p}
        return {"error": "Unsupported file type"}

    return {"files": file_details}