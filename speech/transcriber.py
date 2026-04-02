import os
import re
import json
import subprocess


def extract_youtube_id(url):
    match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else None


def transcribe_youtube(url, upload_folder="uploads", language=None):
    """
    Extract text from a YouTube video.
    1. Try captions first (fast, no model needed).
    2. Fall back to faster-whisper audio transcription.
    language: ISO 639-1 code e.g. 'en', 'hi', 'ur', or None for auto-detect.
    """
    video_id = extract_youtube_id(url)
    if not video_id:
        return None, "Invalid YouTube URL. Please provide a valid YouTube link."

    try:
        import yt_dlp
    except ImportError:
        return None, "yt-dlp not installed. Run: pip install yt-dlp"

    # Step 1: Try captions
    caption_text = _get_youtube_captions(url, language)
    if caption_text and len(caption_text.strip()) > 100:
        return caption_text.strip(), None

    # Step 2: Download audio and transcribe with faster-whisper
    try:
        os.makedirs(upload_folder, exist_ok=True)
        base_path = os.path.join(upload_folder, f"yt_{video_id}")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": base_path + ".%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }],
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)

        audio_path = None
        for f in os.listdir(upload_folder):
            if f.startswith(f"yt_{video_id}") and (f.endswith(".mp3") or f.endswith(".wav") or f.endswith(".m4a")):
                audio_path = os.path.join(upload_folder, f)
                break

        if not audio_path or not os.path.exists(audio_path):
            return None, "Audio download failed. Check your internet connection."

        transcript = transcribe_audio(audio_path, language=language)
        if transcript and len(transcript.strip()) > 20:
            return transcript.strip(), None
        return None, "Transcription produced no usable text."

    except Exception as e:
        return None, f"YouTube processing error: {str(e)}"


def _get_youtube_captions(url, language=None):
    """Try to extract auto-generated or manual captions via yt-dlp."""
    lang = language if language and language != "auto" else "en"
    try:
        import yt_dlp
        import urllib.request
        with yt_dlp.YoutubeDL({"skip_download": True, "quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)

        # Try requested language first, then English fallback
        for try_lang in ([lang, "en"] if lang != "en" else ["en"]):
            for subs in [info.get("subtitles", {}), info.get("automatic_captions", {})]:
                if try_lang in subs:
                    # Prefer vtt > srv3, avoid json3 (hard to parse)
                    fmt_list = subs[try_lang]
                    for preferred_ext in ("vtt", "srv3", "json3"):
                        for fmt in fmt_list:
                            if fmt.get("ext") == preferred_ext:
                                with urllib.request.urlopen(fmt["url"]) as resp:
                                    raw = resp.read().decode("utf-8")
                                parsed = _parse_subtitle(raw, preferred_ext)
                                if parsed and len(parsed.strip()) > 50:
                                    return parsed
    except Exception:
        pass
    return None


def _parse_subtitle(raw, fmt="vtt"):
    """Parse subtitle format to plain text."""
    if fmt == "json3":
        return _parse_json3(raw)
    # VTT / SRV3
    text = re.sub(r"\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}[^\n]*", "", raw)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^WEBVTT.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+$", "", text, flags=re.MULTILINE)  # remove sequence numbers
    text = re.sub(r"\n{2,}", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_json3(raw):
    """Parse YouTube json3 caption format to plain text."""
    try:
        data = json.loads(raw)
        words = []
        for event in data.get("events", []):
            for seg in event.get("segs", []):
                utf8 = seg.get("utf8", "")
                if utf8 and utf8 != "\n":
                    words.append(utf8.strip())
        text = " ".join(w for w in words if w)
        return re.sub(r"\s+", " ", text).strip()
    except Exception:
        return ""


def transcribe_audio(audio_path, language=None):
    """
    Transcribe audio using faster-whisper (offline, no API key needed).
    language: ISO 639-1 code e.g. 'en', 'hi', 'ur', or None/auto for auto-detect.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return "faster-whisper not installed. Run: pip install faster-whisper"

    try:
        lang = language if language and language != "auto" else None
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, beam_size=5, language=lang)
        transcript = " ".join(seg.text.strip() for seg in segments)
        return transcript.strip()
    except Exception as e:
        return f"Transcription error: {str(e)}"


def convert_to_wav(input_path):
    """Convert any audio to WAV 16kHz mono using ffmpeg."""
    output_path = input_path.rsplit(".", 1)[0] + "_converted.wav"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1", "-f", "wav", output_path
        ], capture_output=True, check=True)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")
