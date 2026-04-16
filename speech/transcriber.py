"""
YouTube transcription pipeline
================================
Fast path  : YouTube captions via yt-dlp (requires cookies.txt — see README)
Slow path  : Audio download + faster-whisper (CPU, no API key needed)

Why cookies.txt?
  YouTube rate-limits unauthenticated caption requests (HTTP 429).
  Exporting your browser cookies lets yt-dlp authenticate as you,
  bypassing the block.  One-time setup, takes ~30 seconds.

How to create cookies.txt:
  1. Install the "Get cookies.txt LOCALLY" extension in Chrome/Edge/Firefox
  2. Go to https://www.youtube.com  (make sure you're logged in)
  3. Click the extension icon → Export  → save as  cookies.txt
  4. Place cookies.txt in the project root folder (same folder as app.py)
"""

import os
import re
import json
import shutil
import subprocess
import tempfile
import threading

# ── Whisper model cache ────────────────────────────────────────────────────
_whisper_models: dict = {}
_whisper_lock   = threading.Lock()

MAX_AUDIO_SECONDS = 600   # cap download at 10 min

# Initial prompts anchor Whisper to the correct writing system
_LANG_PROMPTS = {
    "hi": "यह हिंदी में है।",
    "ur": "یہ اردو میں ہے۔",
    "ar": "هذا باللغة العربية.",
    "bn": "এটি বাংলায়।",
    "pa": "ਇਹ ਪੰਜਾਬੀ ਵਿੱਚ ਹੈ।",
    "gu": "આ ગુજરાતીમાં છે.",
    "mr": "हे मराठीत आहे.",
    "ta": "இது தமிழில் உள்ளது.",
    "te": "ఇది తెలుగులో ఉంది.",
    "zh": "这是中文。",
    "ja": "これは日本語です。",
    "ko": "이것은 한국어입니다.",
    "ru": "Это на русском языке.",
    "he": "זה בעברית.",
    "fa": "این به فارسی است.",
    "el": "Αυτό είναι στα ελληνικά.",
}


def cookies_file_path():
    """Return path to cookies.txt if it exists, else None."""
    candidates = [
        "cookies.txt",
        "youtube_cookies.txt",
        os.path.join(os.path.dirname(__file__), "..", "cookies.txt"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return os.path.abspath(p)
    return None


def has_cookies():
    return cookies_file_path() is not None


def _get_whisper_model(lang=None):
    """
    Use 'medium' model for all languages — only model that gives
    accurate Hindi/Arabic/etc. script on CPU.
    Cached after first load so subsequent requests are fast.
    """
    size = "medium"
    if size not in _whisper_models:
        with _whisper_lock:
            if size not in _whisper_models:
                from faster_whisper import WhisperModel
                _whisper_models[size] = WhisperModel(
                    size,
                    device="cpu",
                    compute_type="int8_float32",
                    cpu_threads=8,
                    num_workers=1,
                )
    return _whisper_models[size]


def _ydl_base_opts():
    opts = {"quiet": True, "no_warnings": True}
    node = shutil.which("node") or shutil.which("nodejs")
    if node:
        opts["js_runtimes"] = {"node": {"path": node}}
    cfile = cookies_file_path()
    if cfile:
        opts["cookiefile"] = cfile
    return opts


def extract_youtube_id(url):
    match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})", url)
    return match.group(1) if match else None


def transcribe_youtube(url, upload_folder="uploads", language=None):
    """
    Extract text from a YouTube video.
    1. Captions via yt-dlp  (instant — needs cookies.txt for 429 bypass)
    2. Audio + Whisper       (always works, slower, less accurate for Hindi)
    """
    video_id = extract_youtube_id(url)
    if not video_id:
        return None, "Invalid YouTube URL."

    try:
        import yt_dlp
    except ImportError:
        return None, "yt-dlp not installed. Run: pip install yt-dlp"

    # ── Fast path: captions ────────────────────────────────────────────────
    caption_text = _get_captions_ydlp(video_id, language)
    if caption_text and len(caption_text.strip()) > 100:
        return caption_text.strip(), None

    # ── Slow path: audio + Whisper ─────────────────────────────────────────
    try:
        os.makedirs(upload_folder, exist_ok=True)
        base_path  = os.path.join(upload_folder, f"yt_{video_id}")
        audio_path = _find_audio(upload_folder, video_id)

        if not audio_path:
            ffmpeg_available = shutil.which("ffmpeg") is not None
            ydl_opts = {
                **_ydl_base_opts(),
                "format": "worstaudio/bestaudio/best",
                "outtmpl": base_path + ".%(ext)s",
            }
            # download_ranges and FFmpegExtractAudio both require ffmpeg
            if ffmpeg_available:
                ydl_opts["download_ranges"] = _make_range_func(MAX_AUDIO_SECONDS)
                ydl_opts["force_keyframes_at_cuts"] = False
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "64",
                }]
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=True)
            audio_path = _find_audio(upload_folder, video_id)

        if not audio_path:
            return None, "Audio download failed. Check your internet connection."

        transcript = transcribe_audio(audio_path, language=language)
        if transcript and len(transcript.strip()) > 20:
            return transcript.strip(), None
        return None, "Transcription produced no usable text."

    except Exception as e:
        # Strip ANSI escape codes from yt-dlp error messages before showing to user
        clean = re.sub(r'\x1b\[[0-9;]*m', '', str(e))
        return None, f"YouTube processing error: {clean}"


def _get_captions_ydlp(video_id, language=None):
    """
    Download captions using yt-dlp.
    Requires cookies.txt to avoid HTTP 429 from YouTube.
    Returns plain text or None.
    """
    if not has_cookies():
        # Without cookies YouTube blocks caption downloads (429)
        return None

    lang = language if language and language != "auto" else None
    langs = []
    if lang:
        langs.append(lang)
    if "en" not in langs:
        langs.append("en")

    try:
        import yt_dlp

        with tempfile.TemporaryDirectory() as tmpdir:
            for try_lang in langs:
                for write_auto in (False, True):   # manual first, then auto-generated
                    sub_opts = {
                        **_ydl_base_opts(),
                        "skip_download": True,
                        "writesubtitles": not write_auto,
                        "writeautomaticsub": write_auto,
                        "subtitleslangs": [try_lang],
                        "subtitlesformat": "json3",
                        "outtmpl": os.path.join(tmpdir, "cap.%(ext)s"),
                    }
                    try:
                        with yt_dlp.YoutubeDL(sub_opts) as ydl:
                            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
                    except Exception:
                        pass

                    for fname in os.listdir(tmpdir):
                        if fname.endswith(".json3"):
                            try:
                                raw    = open(os.path.join(tmpdir, fname), encoding="utf-8").read()
                                parsed = _parse_json3(raw)
                                if parsed and len(parsed.strip()) > 50:
                                    return parsed
                            except Exception:
                                continue
                        elif fname.endswith((".vtt", ".srt")):
                            try:
                                raw    = open(os.path.join(tmpdir, fname), encoding="utf-8").read()
                                parsed = _parse_subtitle(raw, "vtt" if fname.endswith(".vtt") else "srt")
                                if parsed and len(parsed.strip()) > 50:
                                    return parsed
                            except Exception:
                                continue
    except Exception:
        pass

    return None


def _make_range_func(max_seconds):
    def _range(info_dict, ydl):
        duration = info_dict.get("duration") or 0
        end = min(duration, max_seconds) if duration else max_seconds
        return [{"start_time": 0, "end_time": end}]
    return _range


def _find_audio(folder, video_id):
    for f in os.listdir(folder):
        if f.startswith(f"yt_{video_id}") and f.endswith((".mp3", ".wav", ".m4a", ".webm", ".ogg", ".opus")):
            return os.path.join(folder, f)
    return None


def transcribe_audio(audio_path, language=None):
    """
    Transcribe audio with faster-whisper.
    - Converts to 16kHz WAV first (Whisper's native format)
    - base  model for English/Latin  (~4-8s)
    - small model for Hindi/Arabic/etc (~6-12s, correct script)
    - Models cached after first load
    """
    lang   = language if language and language != "auto" else None
    model  = _get_whisper_model(lang)
    prompt = _LANG_PROMPTS.get(lang) if lang else None

    wav_path = None
    try:
        wav_path = _to_16k_wav(audio_path)
        src = wav_path
    except Exception:
        src = audio_path

    try:
        segments, _ = model.transcribe(
            src,
            language=lang,
            beam_size=1,
            vad_filter=True,
            vad_parameters={
                'threshold': 0.3,                # low = detect more as speech
                'min_speech_duration_ms': 100,
                'min_silence_duration_ms': 3000, # only skip 3s+ dead silence
                'speech_pad_ms': 600,            # pad around speech edges
            },
            task="transcribe",
            condition_on_previous_text=True,
            temperature=0.0,
            no_speech_threshold=0.95,
            initial_prompt=prompt,
        )
        transcript = " ".join(seg.text.strip() for seg in segments if seg.no_speech_prob < 0.95)
        return transcript.strip()
    except Exception as e:
        return f"Transcription error: {str(e)}"
    finally:
        if wav_path and wav_path != audio_path:
            try:
                os.remove(wav_path)
            except Exception:
                pass


def _to_16k_wav(input_path):
    if not shutil.which("ffmpeg"):
        # ffmpeg not installed — return original path, Whisper handles most formats natively
        return input_path
    out = input_path.rsplit(".", 1)[0] + "_16k.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path,
         "-ar", "16000", "-ac", "1", "-f", "wav", out],
        capture_output=True, check=True
    )
    return out


def convert_to_wav(input_path):
    return _to_16k_wav(input_path)


# ── subtitle parsers ───────────────────────────────────────────────────────
def _parse_subtitle(raw, fmt="vtt"):
    if fmt == "json3":
        return _parse_json3(raw)
    text = re.sub(r"\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}[^\n]*", "", raw)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"^WEBVTT.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+$", "", text, flags=re.MULTILINE)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return re.sub(r"\s+", " ", " ".join(_remove_exact_duplicates(lines))).strip()


def _remove_exact_duplicates(lines):
    seen, result = [], []
    for line in lines:
        norm = re.sub(r"\s+", " ", line).strip().lower()
        if norm and norm not in seen:
            result.append(line)
            seen.append(norm)
            if len(seen) > 6:
                seen.pop(0)
    return result


def _parse_json3(raw):
    try:
        data  = json.loads(raw)
        words = []
        for event in data.get("events", []):
            for seg in event.get("segs", []):
                utf8 = seg.get("utf8", "")
                if utf8 and utf8 != "\n":
                    words.append(utf8.strip())
        text  = " ".join(w for w in words if w)
        # Clean up common caption artifacts
        text  = re.sub(r"\[.*?\]", "", text)          # remove [Music], [Applause] etc
        text  = re.sub(r"\s+", " ", text).strip()
        return text
    except Exception:
        return ""
