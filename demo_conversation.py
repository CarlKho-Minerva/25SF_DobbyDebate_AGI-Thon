from Dobby_Class import process_audio_and_chat
from dobby_voice import text_to_speech, play
import time


def clear_screen():
    """Clear terminal screen"""
    print("\033[H\033[J", end="")


def print_with_animation(text: str, delay: float = 0.03):
    """Print text with typing animation"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def conversation_demo():
    """Interactive demo of Dobby with voice input/output"""
    clear_screen()
    print_with_animation("\n=== Dobby Voice Conversation Demo ===")
    print_with_animation("Talk with Dobby using your voice! 🎙️ -> 💭 -> 🔊")

    # Initial greeting
    greeting = "Hello! I am Dobby, your AI assistant. How can I help you today?"
    print_with_animation("\nDobby: " + greeting)
    audio = text_to_speech(greeting)
    if audio:
        play(audio)

    while True:
        try:
            # Visual prompt for user input
            print(
                "\n[Press Enter to start speaking (5 seconds), or type 'exit' to quit]"
            )
            user_input = input()

            if user_input.lower() == "exit":
                goodbye = "Goodbye! It was nice talking with you!"
                print_with_animation("\nDobby: " + goodbye)
                audio = text_to_speech(goodbye)
                if audio:
                    play(audio)
                break

            # Record and process user's speech
            print_with_animation("\nListening... 🎙️")
            transcription, ai_response = process_audio_and_chat(
                prompt="Conversation with user",
                timed_recording=True,
                record_seconds=5,
                is_english=True,
            )

            if transcription and ai_response:
                # Show transcription
                print_with_animation(f"\nYou said: {transcription}")

                # Show and speak AI response
                print_with_animation(f"\nDobby: {ai_response}")
                audio = text_to_speech(ai_response)
                if audio:
                    play(audio)
            else:
                error_msg = (
                    "I'm sorry, I couldn't understand that. Could you try again?"
                )
                print_with_animation(f"\nDobby: {error_msg}")
                audio = text_to_speech(error_msg)
                if audio:
                    play(audio)

        except KeyboardInterrupt:
            print_with_animation("\n\nConversation ended by user.")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Let's try again...")


if __name__ == "__main__":
    conversation_demo()
