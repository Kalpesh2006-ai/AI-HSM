
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


def record_audio(duration):

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

    sf.write(INPUT_AUDIO, audio, SAMPLE_RATE)

    print("✅ Recording completed.")


def play_audio():

    audio, sample_rate = sf.read(
        OUTPUT_AUDIO,
        dtype="float32"
    )

    sd.play(audio, sample_rate)
    sd.wait()

    print("✅ AI answer playback completed.")


def display_sources(sources):

    print("\n" + "=" * 60)
    print("SOURCES")
    print("=" * 60)

    for source in sources:
        print(
            f"- {source['source']} | "
            f"Page {source['page']}"
        )


def main():

    print("\n" + "=" * 60)
    print("🎤 AI-HSM CONTINUOUS VOICE ASSISTANT")
    print("=" * 60)

    print("\nYou can ask multiple questions.")
    print("Say 'बंद करो' or 'exit' to stop.")

    try:
        duration = int(
            input("\nEnter recording duration in seconds: ")
        )

        if duration <= 0:
            print("❌ Recording duration must be greater than zero.")
            return

    except ValueError:
        print("❌ Please enter a valid number.")
        return

    try:
        while True:

            print("\n" + "-" * 60)
            print("🎤 Waiting for your question...")
            print("-" * 60)

            # 1. RECORD QUESTION
            record_audio(duration)

            # 2. SPEECH TO TEXT
            print("\n[1] Converting speech to text...")

            question = transcribe_audio(
                INPUT_AUDIO,
                language="hi"
            )

            print("\n📝 Transcribed Question:")
            print(question)

            if not question.strip():
                print("\n⚠️ No speech detected. Please try again.")
                continue

            # 3. CHECK EXIT COMMAND
            exit_commands = [
                "बंद करो",
                "बंद कर दो",
                "बंद",
                "exit",
                "stop"
            ]

            if any(
                command in question.lower()
                for command in exit_commands
            ):
                print("\n👋 Voice assistant stopped.")
                break

            # 4. RAG + GEMINI
            print("\n[2] Searching government knowledge base...")

            result = ask_question(question)
            answer = result["answer"]

            print("\n🤖 AI Answer:")
            print(answer)

            # 5. TEXT TO SPEECH
            print("\n[3] Converting AI answer to speech...")

            text_to_speech(answer, OUTPUT_AUDIO)

            # 6. PLAY AI ANSWER
            print("\n🔊 Playing AI answer...")
            play_audio()

            # 7. DISPLAY SOURCES
            display_sources(result["sources"])

            print("\n✅ Question completed.")
            print("You can ask another question now.")

    except KeyboardInterrupt:
        print("\n\n👋 AI-HSM voice assistant stopped by user.")

    print("\n" + "=" * 60)
    print("AI-HSM SESSION ENDED")
    print("=" * 60)


if __name__ == "__main__":
    main()
