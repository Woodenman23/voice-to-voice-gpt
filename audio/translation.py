import queue
import json
import os

from elevenlabs import play
from elevenlabs.client import ElevenLabs
from pathlib import Path
import sounddevice as sd
import webrtcvad
from vosk import Model, KaldiRecognizer


q = queue.Queue()

model_path = Path(__file__).parent / "vosk-model-small-en-us-0.15"

vad = webrtcvad.Vad()
vad.set_mode(1) # How aggressively non-speech is filtered out (0=least, 3=most)

# audio settings
samplerate = 16000
frame_duration = 30
frame_size = int(samplerate * frame_duration / 1000)
frame_bytes = frame_size * 2 

def callback(indata, frames, time, status):
    q.put(bytes(indata))


def audio_to_text():
    prompt_text = ""
    model = Model(str(model_path))
    rec = KaldiRecognizer(model, samplerate)
    
    silence_counter = 0
    max_silence = 33

    with sd.RawInputStream(
        samplerate=samplerate, 
        blocksize=frame_size,
        dtype='int16', 
        channels=1, 
        callback=callback,
    ):
        print("Say something")
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print(text)
                prompt_text += " " + text

            if len(data) == frame_bytes and vad.is_speech(data, samplerate):
                silence_counter = 0
            else:
                silence_counter += 1
            if silence_counter > max_silence:
                break
                
    return prompt_text

def text_to_audio(text):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("no elevenlabs api key env var found.")
        return None
    
    client = ElevenLabs(api_key=api_key)
    
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="Oe8Lhg3t63j9BsrTQBjx",
        model_id="eleven_multilingual_v2"
    )

    return audio

def play_audio(audio):
    play(audio)
