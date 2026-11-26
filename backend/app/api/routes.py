from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
import shutil
from app.schemas import JobCreateResponse, JobStatusResponse
from app.services import video, landmarks, recognizer, translator

router = APIRouter()
fake_db = {}

# Папка для временных файлов
TEMP_DIR = "tmp"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/jobs", response_model=JobCreateResponse, status_code=202)
async def create_job(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    
    # 1. Сохраняем загруженный файл во временную папку
    file_path = os.path.join(TEMP_DIR, f"{job_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Прогоняем через заглушки
        frames = video.process_video(file_path)
        lm = landmarks.extract_landmarks(frames)
        glosses = recognizer.recognize_gestures(lm)
        text = translator.translate_glosses(glosses)
        
        fake_db[job_id] = {
            "status": "done",
            "glosses": glosses,
            "text": text,
            "error": None
        }
    finally:
        # 3. Обязательно удаляем файл после обработки
        if os.path.exists(file_path):
            os.remove(file_path)
            
    return {"job_id": job_id, "status": "processing"}

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    if job_id not in fake_db:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, **fake_db[job_id]}