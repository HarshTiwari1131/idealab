import speech_recognition as sr

recognizer = sr.Recognizer()

# Manually set a higher energy threshold
recognizer.energy_threshold = 300  # You can adjust this value

with sr.Microphone() as source:
    print("Say something!")
    audio = recognizer.listen(source)

try:
    print("You said: " + recognizer.recognize_google(audio))
except sr.UnknownValueError:
    print("Oops! Didn't catch that")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
