from pydantic import BaseModel
from typing import List, Optional

class JobCreateResponse(BaseModel):
    job_id: str
    status: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    glosses: Optional[List[str]] = None
    text: Optional[str] = None
    error: Optional[str] = None