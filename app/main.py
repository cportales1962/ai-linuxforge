from fastapi import FastAPI
from pydantic import BaseModel
from core.parser import check_ollama_status, generate_blueprint

app = FastAPI(title="AI-LinuxForge v1.0.1")

class PromptRequest(BaseModel):
    user_prompt: str
    arch: str = "x86_64"

@app.get('/api/ollama/status')
def ollama_status():
    return check_ollama_status()

@app.post('/api/ollama/refresh')
def ollama_refresh():
    return check_ollama_status()  # Force recheck

@app.post('/api/parse')
def parse(req: PromptRequest):
    result = generate_blueprint(req.user_prompt, req.arch)
    return {
        'nix_flake': result['nix_flake'],
        'mode': result['mode'],
        'status': result['status'],
        'nix_command': f'nix build .#universal',
        'iso': 'demo.iso'
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
