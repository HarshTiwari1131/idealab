import os
import cv2
import face_recognition
import numpy as np

# Constants
KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog'  # or 'cnn' for GPUs

# Colors for drawing
GREEN = [0, 255, 0]
RED = [0, 0, 255]

# Load known faces
print("Loading known faces...")
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    # Create a subdirectory for each known person
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

# Load the video stream or video file
print("Processing unknown faces...")
video_capture = cv2.VideoCapture(0)  # Use 0 for webcam or provide a video file path

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convert BGR to RGB

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame, model=MODEL)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Iterate over each face found in the current frame
    for face_encoding, face_location in zip(face_encodings, face_locations):
        # See if the face is a match for the known faces
        matches = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        name = "Unknown"

        # Use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top_left = (face_location[3] * 4, face_location[0] * 4)
        bottom_right = (face_location[1] * 4, face_location[2] * 4)

        # Draw a box around the face
        color = GREEN if name != "Unknown" else RED
        cv2.rectangle(frame, top_left, bottom_right, color, FRAME_THICKNESS)

        # Draw a label with a name below the face
        top_left = (face_location[3] * 4, face_location[2] * 4)
        bottom_right = (face_location[1] * 4, face_location[2] * 4 + 22)
        cv2.rectangle(frame, top_left, bottom_right, color, cv2.FILLED)
        cv2.putText(frame, name, (face_location[3] * 4 + 10, face_location[2] * 4 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), FONT_THICKNESS)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
video_capture.release()
cv2.destroyAllWindows()
