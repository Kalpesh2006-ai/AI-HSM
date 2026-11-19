
from pathlib import Path
import sys
import tempfile
import uuid
import threading
import traceback

import numpy as np
import soundfile as sf

from flask import Flask, jsonify, render_template, request, send_file

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai.rag.rag_pipeline import ask_question
from ai.speech.speech_to_text import transcribe_audio
from ai.speech.text_to_speech import text_to_speech

app = Flask(__name__)

SUPPORTED_LANGUAGES = ("en-IN", "hi-IN", "mr-IN")
MAX_AUDIO_BYTES = 1024 * 1024
AUDIO_SAMPLE_RATE = 16000

AUDIO_FOLDER = Path(__file__).resolve().parent / "static" / "generated_audio"
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)

jobs = {}
jobs_lock = threading.Lock()


def get_sources(result):
    return [
        {
            "file": Path(item["source"]).name,
            "page": item["page"]
        }
        for item in result.get("sources", [])
    ]


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}

    question = str(data.get("question", "")).strip()
    language = str(data.get("language", "en-IN")).strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if len(question) > 1000:
        return jsonify({"error": "Question is too long."}), 400

    if language not in SUPPORTED_LANGUAGES:
        language = "en-IN"

    try:
        result = ask_question(question, language)

        return jsonify({
            "answer": result.get("answer", "No answer returned."),
            "sources": get_sources(result),
            "language": language
        })

    except Exception:
        app.logger.exception("Chat processing failed")
        return jsonify({"error": "Answer generation failed."}), 500


def process_audio_job(job_id, raw_audio, language):

    audio_path = None

    try:
        samples = np.frombuffer(raw_audio, dtype="<i2")

        if len(samples) < AUDIO_SAMPLE_RATE:
            raise ValueError("Recording is too short.")

        audio = samples.astype(np.float32) / 32768.0

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp_file:
            audio_path = Path(temp_file.name)

        sf.write(
            str(audio_path),
            audio,
            AUDIO_SAMPLE_RATE,
            subtype="PCM_16"
        )

        # Whisper
        question = transcribe_audio(
            str(audio_path),
            language=None
        )

        if not question or not question.strip():
            raise ValueError("No speech detected.")

        question = question.strip()

        with jobs_lock:
            jobs[job_id]["transcription"] = question
            jobs[job_id]["stage"] = "generating_answer"

        app.logger.info(
            "ESP32 transcription [%s]: %s",
            job_id,
            question
        )

        # RAG + Gemini
        result = ask_question(question, language)

        answer = result.get("answer", "No answer returned.")
        sources = get_sources(result)

        with jobs_lock:
            jobs[job_id]["stage"] = "generating_voice"

        # Edge TTS
        audio_filename = f"esp32_answer_{job_id}.mp3"
        generated_path = AUDIO_FOLDER / audio_filename

        text_to_speech(
            answer,
            str(generated_path)
        )

        with jobs_lock:
            jobs[job_id].update({
                "status": "completed",
                "stage": "completed",
                "answer": answer,
                "sources": sources,
                "audio_filename": audio_filename
            })

        app.logger.info("ESP32 job completed: %s", job_id)

    except Exception as error:

        app.logger.error(
            "ESP32 job failed: %s\n%s",
            error,
            traceback.format_exc()
        )

        with jobs_lock:
            jobs[job_id].update({
                "status": "failed",
                "stage": "failed",
                "error": str(error)
            })

    finally:
        if audio_path is not None:
            audio_path.unlink(missing_ok=True)


@app.post("/api/esp32-audio")
def esp32_audio():

    raw_audio = request.get_data()

    if not raw_audio:
        return jsonify({"error": "No audio received."}), 400

    if len(raw_audio) > MAX_AUDIO_BYTES:
        return jsonify({"error": "Audio is too large."}), 413

    if len(raw_audio) % 2 != 0:
        return jsonify({"error": "Invalid PCM audio."}), 400

    language = request.headers.get("X-Language", "hi-IN").strip()

    if language not in SUPPORTED_LANGUAGES:
        language = "hi-IN"

    job_id = uuid.uuid4().hex

    with jobs_lock:
        jobs[job_id] = {
            "status": "processing",
            "stage": "queued",
            "transcription": "",
            "answer": "",
            "sources": []
        }

    thread = threading.Thread(
        target=process_audio_job,
        args=(job_id, raw_audio, language),
        daemon=True
    )

    thread.start()

    return jsonify({
        "success": True,
        "job_id": job_id,
        "status": "processing"
    }), 202


@app.get("/api/esp32-job/<job_id>")
def esp32_job_status(job_id):

    with jobs_lock:
        job = jobs.get(job_id)

        if job is None:
            return jsonify({"error": "Job not found."}), 404

        response = {
            "job_id": job_id,
            "status": job["status"],
            "stage": job["stage"],
            "transcription": job.get("transcription", ""),
            "answer": job.get("answer", ""),
            "sources": job.get("sources", []),
            "error": job.get("error")
        }

    return jsonify(response)


@app.get("/api/esp32-audio-result/<job_id>")
def esp32_audio_result(job_id):

    with jobs_lock:
        job = jobs.get(job_id)

        if job is None:
            return jsonify({"error": "Job not found."}), 404

        if job["status"] != "completed":
            return jsonify({"error": "Audio is not ready."}), 409

        filename = job.get("audio_filename")

    audio_path = AUDIO_FOLDER / filename

    if not audio_path.is_file():
        return jsonify({"error": "Audio file not found."}), 404

    return send_file(
        audio_path,
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name=filename
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        threaded=True
    )
