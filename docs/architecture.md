# Архитектура проекта

Документ описывает взаимодействие компонентов модуля перевода языка жестов.

## 1. Общая схема пайплайна

```text
[Chrome Extension]
       │ 1. POST /api/jobs (video.mp4)
       ▼
[FastAPI Backend] ──(2. job_id)──► [Extension]
       │
       ├─► 3. Video Service (OpenCV) -> извлекает кадры
       ├─► 4. Landmarks Service (MediaPipe) -> извлекает координаты рук
       ├─► 5. Recognizer Service (ML Model) -> выдает Gloss-строку
       └─► 6. Translator Service (GigaChat API) -> переводит в текст
       │
       │ 7. GET /api/jobs/{job_id} (status: done, text: "...")
       ▼
[Chrome Extension] ──► 8. Вставляет текст в VK
```

## 2. API Контракты (FastAPI)

### Загрузка видео на обработку

**POST** `/api/jobs`

- **Body:** `multipart/form-data` (файл `video`)
- **Response (202 Accepted):**
    ```json
    {
        "job_id": "uuid-v4-string",
        "status": "processing"
    }
    ```

### Получение результата

**GET** `/api/jobs/{job_id}`

- **Response (200 OK):**
    ```json
    {
        "job_id": "uuid-v4-string",
        "status": "done", // processing, failed
        "glosses": ["Я", "ХОТЕТЬ", "ЕСТЬ"],
        "text": "Я хочу есть",
        "error": null
    }
    ```

### Проверка работоспособности

**GET** `/api/health`

- **Response (200 OK):** `{"status": "ok"}`

## 3. Модули (внутри `backend/app/`)

- `services/video.py`: Принимает файл, сохраняет во временную папку, нарезает на кадры через `cv2.VideoCapture`. Удаляет файл после обработки.
- `services/landmarks.py`: Прогоняет кадры через `mediapipe.solutions.holistic` (или `hands`). Возвращает numpy-массив формы `[T, 21, 3]` (T — количество кадров).
- `services/recognizer.py`: Принимает массив лендмарков, прогоняет через ML-модель (PyTorch), возвращает список предсказанных глоссов.
- `services/translator.py`: Принимает список глоссов (например, `["Я", "ХОТЕТЬ", "ЕСТЬ"]`), формирует промпт для GigaChat, возвращает естественный текст.

## 4. Формат Gloss-строки

_На текущий момент_(v0.1) договорились использовать JSON-массив строк в верхнем регистре:
`["ПРИВЕТ", "КАК", "ДЕЛА"]`
Ожидаемый результат от LLM: `"Привет, как дела?"`

## 5. Безопасность и приватность

- Видеофайлы не хранятся на сервере. После извлечения кадров и лендмарков оригинальный файл и кадры удаляются.
- Временные файлы живут в папке `tmp/` и чистятся при старте приложения.
