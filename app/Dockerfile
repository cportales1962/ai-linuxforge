    (Ollama curl FIX):

FROM python:3.11-slim

# Ollama oficial curl install (FIX apt)
RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /code
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860 8000

# Ollama + FastAPI(8000) + Streamlit(7860)
CMD sh -c "ollama serve & sleep 10 && ollama pull llama3.1:8b & uvicorn app.main:app --host 0.0.0.0 --port 8000 & sleep 5 && streamlit run app/ui.py --server.port=7860 --server.address=0.0.0.0 --server.headless=true"
