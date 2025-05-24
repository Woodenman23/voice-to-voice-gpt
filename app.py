from audio.translation import audio_to_text, text_to_audio
from llm.prompt import send_prompt

prompt = audio_to_text()
response = send_prompt(prompt)
audio_response = text_to_audio(response)



