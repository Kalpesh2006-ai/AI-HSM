
import asyncio
import re
import edge_tts


# Hindi female voice
VOICE = "hi-IN-SwaraNeural"


def convert_amounts_to_hindi(text):
    """
    Convert common Indian currency amounts into
    natural Hindi words before speech synthesis.
    """

    replacements = {
        "₹20,00,000": "बीस लाख रुपये",
        "₹10,00,000": "दस लाख रुपये",
        "₹5,00,000": "पाँच लाख रुपये",
        "₹50,000": "पचास हजार रुपये",
        "20,00,000": "बीस लाख रुपये",
        "10,00,000": "दस लाख रुपये",
        "5,00,000": "पाँच लाख रुपये",
        "50,000": "पचास हजार रुपये",
        "₹20 लाख": "बीस लाख रुपये",
        "₹10 लाख": "दस लाख रुपये",
        "₹5 लाख": "पाँच लाख रुपये",
        "₹50 हजार": "पचास हजार रुपये",
    }

    for amount, words in replacements.items():
        text = text.replace(amount, words)

    return text


async def generate_speech(text, output_file):
    speech_text = convert_amounts_to_hindi(text)

    print("\nText being spoken:")
    print(speech_text)

    communicate = edge_tts.Communicate(
        text=speech_text,
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

    text_to_speech(text, output_file)

    print(f"\nSpeech saved to: {output_file}")
