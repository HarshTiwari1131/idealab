import cv2
import speech_recognition as sr
import pyttsx3
import time

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

def detect_person(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    persons = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(persons) > 0

def main():
    # Initialize camera
    camera = cv2.VideoCapture(0)
    
    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("AI Chatbot: Hello! I am here to ask you a few questions.")
    speak("Hello! I am here to ask you a few questions.")
    
    while True:
        ret, frame = camera.read()
        
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Person detection
        if detect_person(frame, face_cascade):
            print("Person detected. Asking a question...")
            speak("What is your name?")
            
            
            # Wait for a few seconds to give the person time to respond
            time.sleep(5)
            
            # Capture and recognize speech
            user_message = recognize_speech_from_mic()
            
            if user_message is None:
                speak("Sorry, I didn't catch that. Can you repeat?")
                continue
            
            if user_message.lower() in ['exit', 'quit', 'bye']:
                print("AI Chatbot: Goodbye! Have a great day!")
                speak("Goodbye! Have a great day!")
                break
            
            print(f"AI Chatbot: Nice to meet you, {user_message}.")
            speak(f"Nice to meet you, {user_message}.")
        
        # Display the frame (for debugging purposes)
        cv2.imshow("Frame", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
