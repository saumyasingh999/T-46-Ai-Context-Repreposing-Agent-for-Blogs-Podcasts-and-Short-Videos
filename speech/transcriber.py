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
    lang = language if language and language != "auto" else None
    try:
        import yt_dlp
        import urllib.request
        with yt_dlp.YoutubeDL({"skip_download": True, "quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)

        subtitles  = info.get("subtitles", {})
        auto_caps  = info.get("automatic_captions", {})

        # Build priority list: requested lang first, then 'en' as fallback
        langs_to_try = []
        if lang:
            langs_to_try.append(lang)
        if "en" not in langs_to_try:
            langs_to_try.append("en")

        for try_lang in langs_to_try:
            for subs in [subtitles, auto_caps]:
                if try_lang not in subs:
                    continue
                fmt_list = subs[try_lang]
                # Prefer vtt (cleanest), then srv3, then json3
                for preferred_ext in ("vtt", "srv3", "json3"):
                    for fmt in fmt_list:
                        if fmt.get("ext") == preferred_ext:
                            try:
                                with urllib.request.urlopen(fmt["url"]) as resp:
                                    raw = resp.read().decode("utf-8")
                                parsed = _parse_subtitle(raw, preferred_ext)
                                if parsed and len(parsed.strip()) > 50:
                                    return parsed
                            except Exception:
                                continue
    except Exception:
        pass
    return None


def _parse_subtitle(raw, fmt="vtt"):
    """Parse subtitle format to plain text, removing duplicate lines from sliding-window captions."""
    if fmt == "json3":
        return _parse_json3(raw)

    # VTT / SRV3 — strip timestamps, tags, headers
    text = re.sub(r"\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}[^\n]*", "", raw)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^WEBVTT.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+$", "", text, flags=re.MULTILINE)

    # Split into individual caption lines and deduplicate
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    deduped = _deduplicate_captions(lines)
    return re.sub(r"\s+", " ", " ".join(deduped)).strip()


def _deduplicate_captions(lines):
    """
    Remove repeated/overlapping lines from YouTube sliding-window captions.
    YouTube auto-captions repeat each phrase 2-3 times as the caption window slides.
    Strategy: keep a line only if it is NOT a suffix of the previous kept line
    and NOT already seen recently.
    """
    if not lines:
        return lines

    result = []
    seen = set()

    for line in lines:
        norm = re.sub(r"\s+", " ", line).strip().lower()
        if not norm:
            continue

        # Skip if exact duplicate of a recent line
        if norm in seen:
            continue

        # Skip if this line is fully contained in the last kept line
        # (handles partial overlaps like sliding windows)
        if result:
            last_norm = re.sub(r"\s+", " ", result[-1]).strip().lower()
            if norm in last_norm or last_norm.endswith(norm):
                continue
            # Also skip if last line starts with this line (prefix overlap)
            if last_norm.startswith(norm):
                continue

        result.append(line)
        seen.add(norm)
        # Only keep last 10 in seen to avoid memory bloat on long videos
        if len(seen) > 200:
            seen = set(list(seen)[-100:])

    return result


def _parse_json3(raw):
    """Parse YouTube json3 caption format to plain text, deduplicating overlapping segments."""
    try:
        data = json.loads(raw)
        words = []
        for event in data.get("events", []):
            for seg in event.get("segs", []):
                utf8 = seg.get("utf8", "")
                if utf8 and utf8 != "\n":
                    words.append(utf8.strip())
        # Join and split into lines for deduplication
        text = " ".join(w for w in words if w)
        lines = [l.strip() for l in text.split(".") if l.strip()]
        deduped = _deduplicate_captions(lines)
        result = ". ".join(deduped)
        return re.sub(r"\s+", " ", result).strip()
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
