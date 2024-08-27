import speech_recognition as sr
import pyttsx3
import random

def get_ai_response(user_message):
    responses = [
        "That's interesting. Can you tell me more?",
        "I see. What else can you share?",
        "Hmm, let me think about that.",
        "That's a good point. How do you feel about it?",
        "I'm not sure, but I can look it up for you.",
        "What do you think about it?"
    ]
    return random.choice(responses)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")
            return None

def conversation():
    print("AI Chatbot: Hello! How can I assist you today?")
    speak("Hello! How can I assist you today?")
    
    while True:
        user_message = recognize_speech_from_mic()
        if user_message is None:
            continue
        
        if user_message.lower() in ['exit', 'quit', 'bye']:
            print("AI Chatbot: Goodbye! Have a great day!")
            speak("Goodbye! Have a great day!")
            break
        
        ai_response = get_ai_response(user_message)
        print(f"AI Chatbot: {ai_response}")
        speak(ai_response)

if __name__ == "__main__":
    conversation()
