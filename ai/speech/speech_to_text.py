import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel


MODEL_SIZE = "medium"


model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def load_audio(audio_path):
    """
    Load WAV audio using SoundFile.
    """

    audio, sample_rate = sf.read(
        audio_path,
        dtype="float32"
    )

    # Convert stereo audio to mono
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    target_sample_rate = 16000

    # Resample to 16 kHz if required
    if sample_rate != target_sample_rate:

        duration = len(audio) / sample_rate

        new_length = int(
            duration * target_sample_rate
        )

        old_indices = np.linspace(
            0,
            len(audio) - 1,
            num=len(audio)
        )

        new_indices = np.linspace(
            0,
            len(audio) - 1,
            num=new_length
        )

        audio = np.interp(
            new_indices,
            old_indices,
            audio
        ).astype(np.float32)

    return audio



def transcribe_audio(audio_path, language=None):
    """
    Convert audio into text using Faster-Whisper.
    """

    print("Loading audio...")

    audio = load_audio(audio_path)

    print("Audio loaded successfully.")

    # Domain-specific Hindi vocabulary
    initial_prompt = (
        "मुद्रा योजना, प्रधानमंत्री मुद्रा योजना, "
        "प्रधानमंत्री रोजगार सृजन कार्यक्रम, "
        "महिला उद्यमी, सरकारी योजनाएं, "
        "प्रधानमंत्री सूक्ष्म खाद्य प्रसंस्करण योजना, "
        "पीएमएफएमई योजना, प्रधानमंत्री विश्वकर्मा योजना, "
        "स्वरोजगार, ऋण, लोन, व्यवसाय, उद्यमिता, "
        "बैंक, वित्तीय सहायता, सरकारी सब्सिडी।"
    )

    segments, info = model.transcribe(
        audio,
        language=language,
        beam_size=5,
        best_of=5,
        temperature=0,
        vad_filter=True,
        condition_on_previous_text=False,
        initial_prompt=initial_prompt
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return text.strip()



if __name__ == "__main__":

    audio_path = input(
        "Enter audio file path: "
    ).strip()

    language = input(
        "Enter language (mr/hi/en) "
        "or press Enter for auto-detection: "
    ).strip()

    if language == "":
        language = None

    print("\nTranscribing audio...")

    text = transcribe_audio(
        audio_path,
        language
    )

    print("\n" + "=" * 50)
    print("TRANSCRIBED TEXT")
    print("=" * 50)

    print(text)

    print("=" * 50)