from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from app.schemas import JobCreateResponse, JobStatusResponse
from app.services import video, landmarks, recognizer, translator

router = APIRouter()

# Временная память для хранения задач (в будущем заменим на БД или Redis)
fake_db = {}

@router.post("/jobs", response_model=JobCreateResponse, status_code=202)
async def create_job(file: UploadFile = File(...)):
    # 1. Сохраняем файл (пока просто в память/временную папку)
    job_id = str(uuid.uuid4())
    
    # 2. Прогоняем через заглушки пайплайна
    frames = video.process_video(file.filename)
    lm = landmarks.extract_landmarks(frames)
    glosses = recognizer.recognize_gestures(lm)
    text = translator.translate_glosses(glosses)
    
    # 3. Сохраняем результат
    fake_db[job_id] = {
        "status": "done",
        "glosses": glosses,
        "text": text,
        "error": None
    }
    
    return {"job_id": job_id, "status": "processing"}

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    if job_id not in fake_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job_id,
        **fake_db[job_id]
    }