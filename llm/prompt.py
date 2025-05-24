from openai import OpenAI
from pathlib import Path

TOKEN = (Path.home() / ".ssh/openai").read_text().strip()

client = OpenAI(api_key=TOKEN)

model = "gpt-4o"

def send_prompt(prompt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. You are recieving prompts via audio input.",
        },
        {
            "role": "user",
            "content": prompt,

        }
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=600,
    )

    response = completion.choices[0].message.content

    return response