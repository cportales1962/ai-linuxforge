from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import requests
import yaml
import os
from typing import Dict, Any

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')

ARCH_PKGS = {
    'x86_64': ['mesa', 'ntfs3g'],
    'aarch64': ['mesa'],
}

def check_ollama_status() -> Dict[str, Any]:
    try:
        resp = requests.get(f'{OLLAMA_HOST}/api/tags', timeout=3)
        models = resp.json().get('models', [])
        model_loaded = any('llama3.1' in m['name'] for m in models)
        return {'available': True, 'model_loaded': model_loaded}
    except:
        return {'available': False, 'model_loaded': False}

def generate_deterministic_config(user_prompt: str, arch: str, base_distro: str) -> str:
    if base_distro == 'distrobuilder':
        return f'''image:\n  name: dvianna-os-{arch}\n  source: ubuntu:24.04\n  architecture: {arch}\n  description: "{user_prompt}"\nproperties:\n  description: D'vianna OS\npackages:\n  - xfce4\n  - mesa-utils\n  - ntfs-3g\n  - calamares\n  - wine\n  - vlc\n  - obs-studio\n  - firefox\npost-install:\n  - ||\n    apt update && apt upgrade -y\n    apt install -y grub2-common\n    echo "D'vianna OS Ready!" > /etc/motd\n'''
    elif base_distro == 'yocto':
        return f'MACHINE ?= "{arch}"\nPREFERRED_VERSION_linux-yocto = "6.9.%"\nIMAGE_INSTALL:append = " xfce4 mesa ntfs-3g calamares"'
    return f'# {user_prompt} config for {base_distro}'

def generate_blueprint(user_prompt: str, arch: str = 'x86_64', base_distro: str = 'nixos', preview_visor: str = 'qemu') -> Dict[str, Any]:
    status = check_ollama_status()
    config = generate_deterministic_config(user_prompt, arch, base_distro)
    mode = 'Deterministic' if not status['available'] else 'LLM'
    return {
        'config': config,
        'mode': mode,
        'type': base_distro,
        'iso_name': f"dvianna-os-{arch}.iso",
        'build_cmd': f"distrobuilder pack image dvianna.yaml" if base_distro=='distrobuilder' else 'build',
        'build_script': '#!/bin/bash\necho "Build D\'vianna OS"',
        'preview_script': '#!/bin/bash\necho "QEMU preview"',
        'config_ext': 'yaml' if base_distro=='distrobuilder' else 'conf',
        'arch_pkgs': ARCH_PKGS.get(arch, []),
        'arch_valid': True,
        'status': status,
        'preview_visor': preview_visor
    }
