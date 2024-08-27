import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)

    # Listen for the first phrase
    print("Please say something:")
    audio = recognizer.listen(source)

# Try to recognize the speech in the recording
try:
    # Use Google's speech recognition to transcribe the audio
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    # Could not understand the audio
    print("Sorry, I couldn't understand that.")
except sr.RequestError:
    # Could not request results from Google Speech Recognition service
    print("Sorry, there was an error connecting to the speech recognition service.")
