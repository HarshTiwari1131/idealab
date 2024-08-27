import cv2
import speech_recognition as sr
import pyttsx3
import time
import numpy as np

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

def display_text(text):
    # Create a blank image for text display
    text_image = np.zeros((400, 400, 3), dtype=np.uint8)
    text_image.fill(255)  # Fill with white background

    # Set the font and size
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 0, 0)  # Black color
    thickness = 2

    # Calculate text size and position
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (text_image.shape[1] - text_size[0]) // 2
    text_y = (text_image.shape[0] + text_size[1]) // 2

    # Put text on the image
    cv2.putText(text_image, text, (text_x, text_y), font, font_scale, color, thickness)

    return text_image

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
        person_detected = detect_person(frame, face_cascade)
        if person_detected:
            print("Person detected. Asking a question...")
            speak("What is your name?")
            
            # Display a prompt for the question
            text_display = display_text("What is your name?")
            cv2.imshow("Text Display", text_display)
            
            # Wait for a few seconds to give the person time to respond
            time.sleep(5)
            
            # Capture and recognize speech
            user_message = recognize_speech_from_mic()
            
            if user_message is None:
                response_text = "Sorry, I didn't catch that. Can you repeat?"
                speak(response_text)
            else:
                if user_message.lower() in ['exit', 'quit', 'bye']:
                    response_text = "Goodbye! Have a great day!"
                    speak(response_text)
                    break
                response_text = f"Nice to meet you, {user_message}."
                speak(response_text)
            
            # Display the response
            text_display = display_text(response_text)
            cv2.imshow("Text Display", text_display)
        
        # Display the camera feed
        cv2.imshow("Camera Feed", frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
