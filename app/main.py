from fastapi import FastAPI
from pydantic import BaseModel
import sys
sys.path.append('.')
from core.parser import check_ollama_status, generate_blueprint

app = FastAPI()

class PromptRequest(BaseModel):
    user_prompt: str
    arch: str = "x86_64"
    base_distro: str = "nixos"
    preview_visor: str = "qemu"

@app.get('/api/ollama/status')
def ollama_status():
    return check_ollama_status()

@app.post('/api/parse')
def parse(req: PromptRequest):
    return generate_blueprint(req.user_prompt, req.arch, req.base_distro, req.preview_visor)
