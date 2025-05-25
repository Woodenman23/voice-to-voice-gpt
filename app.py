from audio.translation import audio_to_text, text_to_audio, play_audio
from llm.prompt import send_prompt


converstaion_history = ""

while True:
    prompt = audio_to_text()
    if prompt == "":
        continue
    converstaion_history += prompt + "\n"
    response = send_prompt(converstaion_history)
    converstaion_history += response + "\n"
    audio_response = text_to_audio(response)
    play_audio(audio_response)