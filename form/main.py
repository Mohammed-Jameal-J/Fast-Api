import datetime
from typing import Optional
import uuid

from fastapi import FastAPI, HTTPException, UploadFile, File, Cookie, Response
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

# @app.post("/uploadfiles/")
# async def multiple_file_upload(files: List[UploadFile] = File(...)):
#     file_details = []
#     for file in files:
#         content = await file.read()
#         name = file.filename.lower()
#         if name.endswith((".xls", ".xlsx")):
#             df = pd.read_excel(io.BytesIO(content))
#             return {"Type": "Excel","preview": df.head(3).to_dict(),"Shape": df.shape, "Columns": df.columns.tolist()}
#         elif name.endswith(".pdf"):
#             pdf_reader = PdfReader(io.BytesIO(content))
#             text_p = "".join(page.extract_text() for page in pdf_reader.pages)[:100]
        
#             return {"Type": "PDF", "preview": text_p}
#         return {"error": "Unsupported file type"}

#     return {"files": file_details}

# session

couname = "admin"
copass = "1234"


session = {}
time=10

@app.post("/login/")
def login(username: str, password: str , response: Response):
    if username == couname and password == copass:
        sid = str(uuid.uuid4())
        cur_time = datetime.now()
        expiration_time = cur_time + timedelta(second=time)
        sess
        print("current time:", cur_time)
        print("expiration time:", expiration_time)
        session[sid] = {"username": username, "expiration_time": expiration_time}
        response.set_cookie(key="session_id", value=sid, httponly=True,max_age=time)
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/home")
def home(sid: Optional[str] = Cookie(None)):
    if sid is None or sid not in session:
        raise HTTPException(status_code=401, detail="Unauthorized")
    session_data = session[sid]
    if session_data["expiration_time"] < datetime.now():
        session.pop(sid)
        raise HTTPException(status_code=401, detail="Session expired")
    return {"user": session[sid]}

