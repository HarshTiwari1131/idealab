import cv2
# import face_recognition
import os
import numpy as np

# Directory containing images of known faces
KNOWN_FACES_DIR = 'known_faces'
TOLERANCE = 0.6  # Tolerance for face comparison (lower is stricter)
MODEL = 'hog'    # Model for face detection (hog or cnn)

# Load known faces and their names
known_face_encodings = []
known_face_names = []

'''
def load_known_faces(directory=KNOWN_FACES_DIR):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Load image file and get face encoding
            image_path = os.path.join(directory, filename)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            
            # Append to known faces and names
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])

load_known_faces()'''

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convert from BGR to RGB

    '''
    # Detect faces and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame, model=MODEL)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    '''
    # List to hold names of detected faces
    face_names = []

    # Compare faces with known faces
    '''
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
        name = "Unknown"

        # Find best match
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    '''
    
    # Display results
    '''
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw label with name
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    '''
    
    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close window
video_capture.release()
cv2.destroyAllWindows()
