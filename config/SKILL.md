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
- A directory of `.wav` files (one per scene/chapter).
- A `list.txt` file for rapid FFmpeg concatenation.
- High-quality, human-like voice synthesis (defaulting to `af_heart`).

## How to run
1. Ensure the `local-tts-poc` environment is available.
2. Run the `tts_book.py` script located in the PoC directory.
3. Concatenate output with:
   `ffmpeg -f concat -safe 0 -i output_audio/list.txt -c copy audiobook.wav`
