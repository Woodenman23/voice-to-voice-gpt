from audio.translation import audio_to_text, text_to_audio, play_audio
from llm.prompt import send_prompt


conversation_history = ""

while True:
    prompt = audio_to_text()
    if prompt == "":
        continue
    conversation_history += prompt + "\n"
    response = send_prompt(conversation_history)
    conversation_history += response + "\n"
    audio_response = text_to_audio(response)
    play_audio(audio_response)
