import sounddevice as sd
import numpy as np

fs = 44100  # Sample rate
duration = 5  # Duration of recording in seconds

# Record audio
print("Recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()  # Wait until recording is finished
print("Recording complete")

# Play audio
print("Playing...")
sd.play(myrecording, fs)
sd.wait()
print("Playing complete")