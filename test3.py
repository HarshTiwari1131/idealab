import speech_recognition as sr

recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"Set minimum energy threshold to {recognizer.energy_threshold}")

        print("Say something!")
        audio = recognizer.listen(source)

    try:
        # Enable verbose logging
        print("Recognizing...")
        text = recognizer.recognize_google(audio, show_all=True)
        if isinstance(text, dict) and len(text['alternative']) > 0:
            print("You said: " + text['alternative'][0]['transcript'])
        else:
            print("No valid response")
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    recognize_speech()
