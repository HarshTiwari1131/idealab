import cv2
import speech_recognition as sr
import pyttsx3
import time

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("Recognizer must be an instance of sr.Recognizer.")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("Microphone must be an instance of sr.Microphone.")

    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
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
    
    # Detect faces with a larger minSize to avoid detecting small objects like fans
    persons = cascade.detectMultiScale(
        gray, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(80, 80),  # Increase minSize to detect only larger faces
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    return persons

def main():
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    engine.setProperty('volume', 1)  # Set volume level between 0 and 1

    # Initialize speech recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Initialize camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    # Load pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("AI Chatbot: Hello! I am here to ask you a few questions.")
    speak("Hello! I am here to ask you a few questions.", engine)

    face_detected_frames = 0  # Counter for consecutive frames with detected faces
    frames_to_confirm = 10    # Number of consecutive frames to confirm presence of a person

    while True:
        ret, frame = camera.read()

        if not ret:
            print("Failed to grab frame.")
            break

        # Person detection
        persons = detect_person(frame, face_cascade)
        
        # Check if there are any faces detected
        if len(persons) > 0:
            # Check if the detected face is near the center of the frame
            for (x, y, w, h) in persons:
                frame_center_x = frame.shape[1] // 2
                frame_center_y = frame.shape[0] // 2
                face_center_x = x + w // 2
                face_center_y = y + h // 2
                
                # Define a margin of center detection
                margin = 100
                
                # If the face is near the center, consider it a valid detection
                if (frame_center_x - margin < face_center_x < frame_center_x + margin and
                    frame_center_y - margin < face_center_y < frame_center_y + margin):
                    face_detected_frames += 1
                    break  # Only count one face per frame
            else:
                # No valid face near the center detected
                face_detected_frames = 0
        else:
            face_detected_frames = 0

        # If a face is detected for a sufficient number of consecutive frames
        if face_detected_frames >= frames_to_confirm:
            print("Person detected. Asking a question...")
            speak("What is your name?", engine)

            # Wait for a few seconds to give the person time to respond
            time.sleep(2)

            # Capture and recognize speech
            user_message = recognize_speech_from_mic(recognizer, microphone)

            if user_message is None:
                speak("Sorry, I didn't catch that. Can you repeat?", engine)
                continue

            if user_message.lower() in ['exit', 'quit', 'bye']:
                print("AI Chatbot: Goodbye! Have a great day!")
                speak("Goodbye! Have a great day!", engine)
                break

            print(f"AI Chatbot: Nice to meet you, {user_message}.")
            speak(f"Nice to meet you, {user_message}.", engine)

            # Reset face detected frames counter after interacting
            face_detected_frames = 0

        # Display the frame (for debugging purposes)
        cv2.imshow("Frame", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
