
from pathlib import Path
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json

q = queue.Queue()

model_path = Path(__file__).parent / "vosk-model-small-en-us-0.15"

def callback(indata, frames, time, status):
    q.put(bytes(indata))




def audio_to_text():
    prompt_text = ""
    model = Model(
    str(model_path),
)
    samplerate = 16000
    device = None
    with sd.RawInputStream(
        samplerate=samplerate, 
        blocksize=8000, dtype='int16', 
        channels=1, callback=callback
        ):
        rec = KaldiRecognizer(model, samplerate)
        session = True
        while session:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                print(text)
                if result.get("text", "") == "exit prompt":
                    session = False
                else:
                    prompt_text += " " + text
                
    
    return prompt_text