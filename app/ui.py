python import streamlit as st import requests import yaml import time

st.set_page_config(page_title="AI-LinuxForge", layout="wide")

st.title("🛠️ AI-LinuxForge v1.0.9")
Ollama status

try: status = requests.get('http://localhost:8000/api/ollama/status', timeout=3).json() if statusOllama Ready') else: st.warning('🟡 Deterministic Mode') except: st.info('🔄 Starting...')

col1, col2, col3, col4 = st.columns(4) with col1: user_prompt = st.text_area("Describe tu SO:", "D'vianna OS: Ubuntu ligera XFCE gaming CUDA", height=80) with col2: arch = st.selectbox("Arch", ["x86_64", "aarch64"]) with col3: base_distro = st.selectbox("Builder", ["distrobuilder", "yocto", "buildroot", "nixos"]) with col4: preview_visor = st.selectbox("Preview", ["qemu"])

if st.button("🚀 Generar Blueprint", type="primary"): with st.spinner("Generando..."): resp = requests.post("http://localhost:8000/api/parse", json={"user_prompt": user_prompt, "arch": arch, "base_distro": base_distro, "preview_visor": preview_visor}, timeout=30) data = resp.json()

st.success(f"✅ {data['type'].upper()} Blueprint para {user_prompt.split(':')[0]}!")
st.code(data['config'], language='yaml' if 'distrobuilder' in data['type'] else None)

col1, col2 = st.columns(2)
with col1:
    st.download_button("↓ YAML/Config", data=data['config'], file_name=f"dvianna-{data['type']}.{data['config_ext']}")
with col2:
    st.download_button("↓ build.sh", data=data['build_script'], file_name="build-dvianna.sh")
