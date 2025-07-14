from openai import OpenAI
from pathlib import Path

TOKEN = (Path.home() / ".api_keys/openai_key").read_text().strip()

client = OpenAI(api_key=TOKEN)

model = "gpt-4o"


def send_prompt(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, voice-based assistant."
                "Speak naturally, like you are talking to a friend."
                "Keep your answers short and to the point."
                "Use conversational language, contractions."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=100,
    )

    response = (
        (completion.choices[0].message.content).replace("*", " ").replace("#", "")
    )

    return response
