This is an app to communicate verbally with an LLM.

The response will be visualised using an LED matrix.

First take the audio and convert to text string with capture_input.py.

Then send the string to an LLM via an api.

Then bring the response back from the LLM, convert it to audio, and visualise it using the LED matrix.