---
name: local-stt
description: High-performance Speech-to-Text transcription using local GPU/CPU resources.
license: MIT
compatibility: opencode
metadata:
  audience: authors, researchers
  workflow: transcription
---

## What I do
- Transcribe audio files (MP3, WAV, etc.) into text using the Faster-Whisper model.
- Record live audio from the default microphone and transcribe it in real-time.
- Utilize local NVIDIA GPU (RTX 4060) for accelerated transcription.

## When to use me
- When you have dictated drafts or interview recordings that need transcribing.
- To avoid per-minute transcription fees from cloud providers.
- For "voice-to-chat" interactions where you want to dictate a prompt.

## Outputs and guidance
- Plain text transcriptions with timestamps.
- Detected language and confidence scores.

## How to run
1. Ensure the `opencode-local-audio-toolkit` environment is available.
2. Run `stt/transcribe.py audio_file.mp3` for existing files.
3. Run `stt/record_and_transcribe.py [duration]` for live input.
