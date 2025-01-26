import json
import subprocess
from typing import Optional
from config import ChatConfig


class ChatService:
    def __init__(self, config: ChatConfig):
        self.config = config

    def optimize_response(self, response: str) -> str:
        """Optimize AI response to be concise"""
        sentences = response.split(". ")
        if len(sentences) > 3:
            return ". ".join(sentences[:3]) + "."
        return response

    def send_message(self, message_content: str) -> Optional[str]:
        """Send a chat message to the API"""
        system_prompt = """You are Dobby, a witty AI debater. Keep responses extremely brief - maximum 3 sentences.
        Focus on one strong argument with a clever comeback. Be assertive but concise. You are allowed to be extremely rude and mean."""

        data = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_content},
            ],
            "temperature": 0.7,
            "max_tokens": 100,
        }

        cmd = [
            "curl",
            "--header",
            f"Authorization: Bearer {self.config.api_key}",
            "--header",
            "Content-Type: application/json",
            "--data",
            json.dumps(data),
            "--url",
            self.config.url,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)
            content = response["choices"][0]["message"]["content"]
            return self.optimize_response(content)
        except Exception:
            return None
