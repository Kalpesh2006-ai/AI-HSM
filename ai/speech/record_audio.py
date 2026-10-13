import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
CHANNELS = 1

# AudioRelay virtual microphone
INPUT_DEVICE = 1

OUTPUT_FILE = "ai/speech/user_question.wav"


def record_audio():

    print("=" * 60)
    print("AI-HSM PHONE MICROPHONE")
    print("=" * 60)

    duration = int(
        input("\nEnter recording duration in seconds: ")
    )

    print("\n📱 Your phone microphone is being used.")
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

    print("Recording completed.")

    sf.write(
        OUTPUT_FILE,
        audio,
        SAMPLE_RATE
    )

    print(f"\nAudio saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    record_audio()