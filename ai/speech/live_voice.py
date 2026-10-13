import sounddevice as sd
import soundfile as sf

from ai.speech.speech_to_text import transcribe_audio
from ai.rag.rag_pipeline import ask_question
from ai.speech.text_to_speech import text_to_speech


# AudioRelay virtual microphone
INPUT_DEVICE = 1

SAMPLE_RATE = 16000
CHANNELS = 1

INPUT_AUDIO = "ai/speech/user_question.wav"
OUTPUT_AUDIO = "ai/speech/answer.wav"


def record_audio():

    print("\n" + "=" * 60)
    print("🎤 AI-HSM VOICE ASSISTANT")
    print("=" * 60)

    duration = int(
        input("\nEnter recording duration in seconds: ")
    )

    print("\n📱 Phone microphone connected")
    print("🎤 Recording started...")
    print("Speak your question now.")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=INPUT_DEVICE
    )

    sd.wait()

    sf.write(
        INPUT_AUDIO,
        audio,
        SAMPLE_RATE
    )

    print("✅ Recording completed.")


def main():

    # --------------------------------------------------
    # 1. RECORD QUESTION
    # --------------------------------------------------

    record_audio()


    # --------------------------------------------------
    # 2. SPEECH TO TEXT
    # --------------------------------------------------

    print("\n[1] Converting speech to text...")

    question = transcribe_audio(
        INPUT_AUDIO,
        language="hi"
    )

    print("\n📝 Transcribed Question:")
    print(question)


    # --------------------------------------------------
    # 3. RAG + GEMINI
    # --------------------------------------------------

    print("\n[2] Searching government knowledge base...")

    result = ask_question(question)

    answer = result["answer"]

    print("\n🤖 AI Answer:")
    print(answer)


    # --------------------------------------------------
    # 4. TEXT TO SPEECH
    # --------------------------------------------------

    print("\n[3] Converting AI answer to speech...")

    text_to_speech(
        answer,
        OUTPUT_AUDIO
    )

    print("\n🔊 Voice answer created:")
    print(OUTPUT_AUDIO)


    # --------------------------------------------------
    # 4.5. PLAY AI ANSWER
    # --------------------------------------------------

    print("\n🔊 Playing AI answer...")

    audio, sample_rate = sf.read(
        OUTPUT_AUDIO,
        dtype="float32"
    )

    sd.play(
        audio,
        sample_rate
    )

    sd.wait()

    print("✅ AI answer playback completed.")


    # --------------------------------------------------
    # 5. SOURCES
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in result["sources"]:

        print(
            f"- {source['source']} | "
            f"Page {source['page']}"
        )


    print("\n" + "=" * 60)
    print("✅ AI-HSM PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()