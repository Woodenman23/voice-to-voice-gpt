import time
import queue
import json
import io

from pathlib import Path
import sounddevice as sd
import webrtcvad
from vosk import Model, KaldiRecognizer
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa


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
    max_silence = 50

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
    tts = gTTS(text=text, lang='en')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    return audio

def play_audio(audio):
    play_obj = sa.play_buffer(
        audio.raw_data,
        num_channels=audio.channels,
        bytes_per_sample=audio.sample_width,
        sample_rate=audio.frame_rate
    )
    play_obj.wait_done()

# def play_audio_interruptible(audio, interrupt_event, chunk_ms=200):
#     position = 0
#     interrupted = False

#     while position < len(audio):
#         if interrupt_event.is_set():
#             interrupted = True
#             break
        
#         chunk = audio[position:position + chunk_ms]
#         play_obj = sa.play_buffer(
#             chunk.raw_data,
#             num_channels=chunk.channels,
#             bytes_per_sample=chunk.sample_width,
#             sample_rate=chunk.frame_rate
#         )
#         play_obj.wait_done()
#         position += chunk_ms

#     return interrupted
