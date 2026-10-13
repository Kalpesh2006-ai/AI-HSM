import asyncio
import edge_tts


# Hindi female voice
VOICE = "hi-IN-SwaraNeural"


async def generate_speech(text, output_file):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(output_file)


def text_to_speech(text, output_file):
    asyncio.run(
        generate_speech(text, output_file)
    )


if __name__ == "__main__":
    text = input("Enter text to convert to speech: ").strip()

    output_file = "ai/speech/answer.wav"

    print("\nGenerating speech...")

    text_to_speech(
        text,
        output_file
    )

    print(f"\nSpeech saved to: {output_file}")