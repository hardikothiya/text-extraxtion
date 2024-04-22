from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import requests
from helper_functions import send_email_notification, extract_text_from_docx, extract_text_from_doc, extract_text_from_pdf, extract_text

app = FastAPI()
import uuid

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ExtractedText(Base):
    __tablename__ = "extracted_texts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    text = Column(String)
    email = Column(String)

# Create database tables
Base.metadata.create_all(bind=engine)

class FileUploadForm:
    def __init__(
            self,
            file: UploadFile = File(''),
            url: str = Form(''),
            email: str = Form(''),
    ):
        self.file = file
        self.url = url
        self.email = email


@app.post("/extract-text/")
async def extract_text_api(background_tasks: BackgroundTasks, form_data: FileUploadForm = Depends(), db: Session = Depends(get_db)):
    if form_data.url:
        print("cccccccccc")
        filename = os.path.basename(form_data.url)
        file_extension = filename.split('.')[1].lower()

        if file_extension not in ['pdf', 'doc', 'docx']:
            print('aaa')
            raise HTTPException(status_code=400, detail="Unsupported file type")
        # extract_text_background_from_url(form_data.url, filename,file_extension, form_data.email, db)
        background_tasks.add_task(extract_text_background_from_url, form_data.url, filename,file_extension, form_data.email, db)
    if form_data.file:
        filename = form_data.file.filename
        file_extension = filename.split('.')[1].lower()

        if file_extension not in ['pdf', 'doc', 'docx']:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        # extract_text_background(form_data.file.file.read(), file_extension, filename, form_data.email, db)
        background_tasks.add_task(extract_text_background, form_data.file.file.read(), file_extension, filename, form_data.email, db)
    if not form_data.file and not form_data.url:
        raise HTTPException(status_code=400, detail="Invalid input")
    return JSONResponse(content={"message": "Text extraction process started in the background."})

def extract_text_background_from_url(url: str, filename: str, file_extension:str, email: str, db: Session):
    try:
        file_path = download_file_from_url(url,file_extension)
        text = read_text_from_file(file_path,file_extension)
        save_text_to_db(db, filename, text,email)
    except Exception as e:
        print(e)


def save_text_to_db(db: Session, filename: str, text: str, email: str):
    extracted_text = ExtractedText(filename=filename, text=text, email=email)
    db.add(extracted_text)
    db.commit()

def download_file_from_url(url: str, file_extension:str):
    name  = uuid.uuid4()
    with open(f'{name}.{file_extension}', 'wb') as f:
        response = requests.get(url)
        if response.status_code == 200:
            f.write(response.content)
            return f"{name}.{file_extension}"
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to download file from URL")





def extract_text_background(file: bytes, file_extension: str, filename: str, email: str, db: Session):
    name = uuid.uuid4()

    file_name = f"{name}.{file_extension}"

    try:
        open(file_name, 'wb').write(file)
        text = read_text_from_file(file_name, file_extension)
        save_text_to_db(db, filename, text, email)
        if email:
            send_email_notification(email, "Extraction-Service",f"Your requested for text extraction complete.")
    except Exception as e:

        print(f"Error extracting text from {filename}: {str(e)}")


def read_text_from_file(file, file_extension: str):

    if file_extension == 'pdf':
        return extract_text_from_pdf(file)
    elif file_extension == 'doc':
        return extract_text_from_doc(file)
    elif file_extension == 'docx':
        return extract_text_from_docx(file)
