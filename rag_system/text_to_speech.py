"""Simple Text-to-Speech utilities for the chatbot UI.

Primary: gTTS (no API key required). Fallback: edge-tts (Microsoft) if available.
Returns MP3 bytes suitable for st.audio.
"""

from __future__ import annotations

from io import BytesIO
from typing import Optional

try:
    from gtts import gTTS
except Exception:  # pragma: no cover
    gTTS = None  # type: ignore

try:  # optional fallback provider
    import asyncio
    import edge_tts  # type: ignore
except Exception:  # pragma: no cover
    edge_tts = None  # type: ignore
    asyncio = None  # type: ignore


def synthesize_to_mp3_bytes(text: str, lang: str = "en") -> Optional[bytes]:
    """Synthesize speech using gTTS and return MP3 bytes.

    Args:
        text: Text to speak
        lang: Language code (e.g., 'en', 'vi')

    Returns:Show Play button under answers”
        MP3 bytes or None if synthesis failed or gTTS missing
    """
    if not text:
        return None

    # Try gTTS first
    if gTTS is not None:
        try:
            tts = gTTS(text=text, lang=lang)
            buf = BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()
        except Exception:
            pass

    # Fallback to edge-tts if installed
    if edge_tts is not None and asyncio is not None:
        try:
            voice = _select_edge_voice(lang)

            async def _run() -> bytes:
                communicate = edge_tts.Communicate(text, voice)
                buf = BytesIO()
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        buf.write(chunk["data"])
                return buf.getvalue()

            return asyncio.run(_run())
        except Exception:
            return None

    return None


def _select_edge_voice(lang: str) -> str:
    """Map ISO language code to a reasonable Edge TTS neural voice."""
    normalized = (lang or "en").lower()
    if normalized.startswith("vi"):
        return "vi-VN-HoaiMyNeural"
    if normalized.startswith("en"):
        return "en-US-AriaNeural"
    if normalized.startswith("ja"):
        return "ja-JP-NanamiNeural"
    if normalized.startswith("ko"):
        return "ko-KR-SunHiNeural"
    if normalized.startswith("zh"):
        return "zh-CN-XiaoxiaoNeural"
    return "en-US-AriaNeural"


