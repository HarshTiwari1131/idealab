import cv2  # For camera and face detection
import speech_recognition as sr  # For speech recognition
import pyttsx3  # For text-to-speech
import time  # For timing

# AI information response
ai_info_response = "I am an AI chatbot designed to interact with you, ask questions, and process your responses. I'm here to make your experience engaging and informative."

# Function to speak text
def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech from the microphone
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

# Function to detect persons in the frame
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

# Main function
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

    # List of questions to ask
    questions = [
        "What is your name?",
        "How are you feeling today?",
        "What is your favorite hobby?",
        "What is your favorite color?",
        "Do you like programming?",
        "What is your favorite movie?",
        "What is your favorite food?"
    ]

    # Dictionary to handle common questions about the AI
    responses = {
        "who are you": ai_info_response,
        "what is your name": ai_info_response,
        "what do you do": ai_info_response
    }

    # Start with the first question
    question_index = 0

    # Main loop
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
            # Ask the current question
            current_question = questions[question_index]
            print(f"AI Chatbot: {current_question}")
            speak(current_question, engine)

            # Wait for a few seconds to give the person time to respond
            time.sleep(2)

            # Capture and recognize speech
            user_message = recognize_speech_from_mic(recognizer, microphone)

            if user_message is None:
                speak("Sorry, I didn't catch that. Can you repeat?", engine)
                continue

            # Check if the user asks a common question
            response = responses.get(user_message.lower())
            if response:
                print(f"AI Chatbot: {response}")
                speak(response, engine)
                continue

            if user_message.lower() in ['exit', 'quit', 'bye']:
                print("AI Chatbot: Goodbye! Have a great day!")
                speak("Goodbye! Have a great day!", engine)
                break

            # Print and speak the response
            print(f"AI Chatbot: You said, {user_message}.")
            # Optionally, uncomment this line if you want the AI to speak the response
            # speak(f"You said, {user_message}.", engine)

            # Move to the next question
            question_index += 1

            # Loop back to the first question if we've asked all of them
            if question_index >= len(questions):
                question_index = 0

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

# Call the main function
if __name__ == "__main__":
    main()
