# Opencode Local Audio Toolkit

This toolkit provides high-performance, local **Speech-to-Text (STT)** and **Text-to-Speech (TTS)** capabilities for the Opencode environment. It is designed to offset cloud costs by utilizing local GPU (NVIDIA RTX 4060) and CPU resources.

## 🚀 Purpose
This toolkit is intended to be used as a **Subagent** or **Tool Process** within Opencode. It allows for the automated processing of novels, scripts, and audio data without incurring API fees from providers like OpenAI or ElevenLabs.

## 🛠 Features
- **Local STT (stt/):** Powered by `faster-whisper` (Whisper Large V3 Distilled).
- **Local TTS (tts/):** Powered by `kokoro-82M` (ONNX).
- **Novel Processing:** Automatically splits manuscripts into scenes and handles batch synthesis.
- **Background Synthesis:** Includes a robust background runner to handle long-running novel synthesis tasks without blocking the main agent session.

## 📦 Setup

### 1. Requirements
- Python 3.12+
- FFmpeg (on PATH)
- NVIDIA GPU with CUDA support (Recommended)

### 2. Installation
It is highly recommended to install the modules into a virtual environment named `venv` within the toolkit folder. This ensures the background synthesis runner can always find the correct dependencies.

```bash
# From the toolkit root:
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 3. Model Downloads
The scripts will automatically download models on the first run, but you can pre-load them using the provided `download_models.py`.

### 4. Windows DLL Path Fix
The toolkit includes automatic DLL injection for Windows environments to ensure `nvidia-*` pip packages are correctly linked to `onnxruntime-gpu`.

## 🤖 Opencode Integration
The `config/` directory contains template `AGENT.md` and `SKILL.md` files. Copy these to your `.opencode/agents/` and `.opencode/skills/` directories respectively to enable the `local-tts` agent.

## 📂 Structure
- `stt/`: Scripts for transcription and recording.
- `tts/`: Scripts for novel synthesis and background processing.
- `config/`: Opencode agent and skill definitions.

## 📜 Usage via Opencode
To process a novel:
1. Place the novel as a `.md` or `.txt` file in the toolkit root.
2. Ask Opencode to "Use the local-tts agent to synthesize [BookName].md".
3. The agent will launch `run_background_tts.py` and monitor the `synthesis.log`.
4. Once complete, run the FFmpeg concatenation command provided in the log.

---
*Created by opencode for Falstar Publishing Dev.*
