import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.energy_threshold = 10000  # Set a suitable energy threshold
            recognizer.adjust_for_ambient_noise(source, duration=1.2)
            
            print("Listening...")
            audio = recognizer.listen(source)
            
            try:
                print("Recognizing...")
                query = recognizer.recognize_google(audio)
                print(f"You said: {query}")
                return query
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
                speak("Sorry, I didn't understand that.")
                return None
            except sr.RequestError:
                print("Sorry, there was an issue with the request.")
                speak("Sorry, there was an issue with the request.")
                return None
    except OSError as e:
        print("Microphone not accessible.")
        speak("Microphone not accessible.")
        return None

def main():
    speak("Hello! How can I assist you today?")
    while True:
        query = listen()
        if query:
            if 'hello' in query.lower():
                speak("Hi there! How can I help you?")
            elif 'your name' in query.lower():
                speak("I am a voice assistant created by OpenAI.")
            elif 'bye' in query.lower():
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("Sorry, I didn't understand that. Can you please repeat?")
                
if __name__ == "__main__":
    main()
