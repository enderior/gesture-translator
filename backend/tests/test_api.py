from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_job_mock():
    # Создаем фейковый видеофайл
    file_content = b"fake video content"
    file = {"file": ("test.mp4", io.BytesIO(file_content), "video/mp4")}
    
    response = client.post("/api/jobs", files=file)
    assert response.status_code == 202
    assert "job_id" in response.json()