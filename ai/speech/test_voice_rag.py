from ai.speech.speech_to_text import transcribe_audio
from ai.rag.rag_pipeline import ask_question
from ai.speech.text_to_speech import text_to_speech


AUDIO_FILE = "ai/speech/user_question.wav"
OUTPUT_AUDIO = "ai/speech/answer.wav"


def main():

    print("=" * 60)
    print("AI-HSM COMPLETE VOICE PIPELINE")
    print("=" * 60)

    # --------------------------------------------------
    # 1. SPEECH TO TEXT
    # --------------------------------------------------

    print("\n[1] Converting microphone audio to text...")

    question = transcribe_audio(
        AUDIO_FILE,
        language="hi"
    )

    print("\nTranscribed Question:")
    print(question)

    # --------------------------------------------------
    # 2. RAG + GEMINI
    # --------------------------------------------------

    print("\n[2] Searching government knowledge base...")

    result = ask_question(question)

    answer = result["answer"]

    print("\nAI Answer:")
    print(answer)

    # --------------------------------------------------
    # 3. TEXT TO SPEECH
    # --------------------------------------------------

    print("\n[3] Converting AI answer to speech...")

    text_to_speech(
        answer,
        OUTPUT_AUDIO
    )

    print("\nVoice answer created successfully.")

    # --------------------------------------------------
    # 4. SOURCES
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
    print("PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()