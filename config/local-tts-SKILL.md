---
name: local-tts
description: High-fidelity Text-to-Speech synthesis using local GPU/CPU resources to offset cloud costs.
license: MIT
compatibility: opencode
metadata:
  audience: authors, publishers
  workflow: audiobook-production
---

## What I do
- Convert long-form text (Markdown/TXT) into high-quality audio using the Kokoro-82M model.
- Automatically split novels into scenes and chunks for stable, memory-efficient synthesis.
- Generate scene-by-scene WAV files and an FFmpeg-compatible concatenation list.
- Utilize local NVIDIA GPU (RTX 4060) or CPU for zero-marginal-cost production.

## When to use me
- When you want to generate a full audiobook or proof-listening track for a manuscript.
- To avoid high per-character or per-hour fees from cloud providers like ElevenLabs or OpenAI.
- For rapid prototyping of audio content from blog posts, newsletters, or short stories.

## Outputs and guidance
- A subdirectory per book containing `.wav` files (prefixed with sanitized book name).
- A book-specific `list.txt` file for rapid FFmpeg concatenation.
- High-quality, human-like voice synthesis (defaulting to `af_heart`).

## How to run
1. Ensure the `opencode-local-audio-toolkit` environment is available at `C:\Users\mwyant\OneDrive\Falstar Publishing Dev\opencode-local-audio-toolkit`.
2. Run the `tts/tts_book.py [path_to_book.md]` script.
3. Use `tts/run_background_tts.py [path_to_book.md]` for background synthesis.
4. Check script output for the exact `ffmpeg` command to concatenate results.
