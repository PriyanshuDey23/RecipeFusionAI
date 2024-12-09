from gtts import gTTS
import os

# Define the multiline text
text = """Bruschetta with Tomato and Basil
A classic Italian appetizer with toasted bread, fresh tomatoes, basil, and olive oil."""

# Create a gTTS object
tts = gTTS(text=text, lang='en')

# Save the audio file
tts.save("test_audio.mp3")

# Optionally, play the audio (if on a system with a sound player)
os.system("start test_audio.mp3")  # For Windows