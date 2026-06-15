# 4fd3
# Smart Medical Assistant — Backend (Docker)

The backend is a Flask API that serves an AI model (Qwen 2.5 3B) to answer
symptom questions. It runs in Docker.

## Prerequisites
- Docker Desktop installed and running

## Files
- `app.py` — the Flask backend (includes CORS so the frontend can call it)
- `Dockerfile` — builds the container
- `requirements.txt` — Python dependencies
- The AI model (`*.gguf`) is **not** in this repo (too large for git) — download it first, see below.

## 1. Download the model (one time)
The model is ~2 GB and isn't stored in git. Download it into this folder:

    curl.exe -L -o qwen2.5-3b-instruct-q4_k_m.gguf "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf?download=true"

## 2. Build the image
    docker build -t qwen-app .

(First build takes several minutes — it compiles dependencies and copies the
model into the image. After that it's cached.)

## 3. Run the backend
    docker run --init -p 8000:8000 -e PYTHONUNBUFFERED=1 qwen-app

Wait for `Running on http://0.0.0.0:8000`. The API is now at http://localhost:8000.

## 4. Test it
    curl.exe -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d "{\"prompt\": \"I have a headache\"}"

You should get back a JSON response with the model's answer.

## Notes
- The model is baked into the image, so the container starts quickly with no
  download at runtime.
- To stop the backend, press Ctrl+C in its terminal window.
