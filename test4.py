import speech_recognition as sr

recognizer = sr.Recognizer()

# Replace <correct_device_index> with the numerical index of the microphone you want to use
correct_device_index = 11  # Assuming this is the index of "Microphone (Realtek HD Audio Mic input)"

with sr.Microphone(device_index=correct_device_index) as source:
    print("Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(source, duration=None)
    print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

    print("Say something!")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language='en-US')
    print("You said: " + text)
except sr.UnknownValueError:
    print("Oops! Didn't catch that")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
