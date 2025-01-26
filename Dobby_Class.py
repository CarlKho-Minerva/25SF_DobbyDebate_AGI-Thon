import subprocess
import json
from config import API_KEY, URL, MODEL


def extract_content(response: dict) -> str:
    """Extract just the content from the API response"""
    if not response or "choices" not in response:
        return None
    return response["choices"][0]["message"]["content"]


def send_chat_message(message_content: str) -> str:
    """
    Send a chat message to the API and return just the response content

    Args:
        message_content (str): The message to send to the API

    Returns:
        str: The response content from the AI
    """
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": message_content}],
    }

    cmd = [
        "curl",
        "--header",
        f"Authorization: Bearer {API_KEY}",
        "--header",
        "Content-Type: application/json",
        "--data",
        json.dumps(data),
        "--url",
        URL,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        return extract_content(response)
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return None


if __name__ == "__main__":
    # Example usage
    response = send_chat_message("Say this is a test hate")
    print("AI response:", response)  # Will print just the content
