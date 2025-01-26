from Dobby_Class import process_audio_and_chat


def demo_audio_chat():
    """Demo: Speak to AI and get response"""
    print("\n=== Audio Chat Demo ===")
    print("Speak your message when recording starts...")
    print("(Recording for 5 seconds...)")

    transcription, ai_response = process_audio_and_chat(
        prompt="This is a conversation with AI.",
        timed_recording=True,
        record_seconds=2,
        is_english=True,
    )

    if transcription and ai_response:
        print("\nAI response:", ai_response)
    else:
        print("\nError: Failed to process audio or get AI response")


if __name__ == "__main__":
    demo_audio_chat()
