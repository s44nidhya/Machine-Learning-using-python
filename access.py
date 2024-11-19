import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime

# Directory to store known face encodings and names
known_faces_dir = "known_faces"

# Creating the directory in case it doesn't exist
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)

# List of known face encodings and names
known_face_encodings = []
known_face_names = []

# Loading known faces from the directory
def load_known_faces():
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(os.path.join(known_faces_dir, filename))
            encoding = face_recognition.face_encodings(image)[0]
            name = filename.split('.')[0]  # Use the filename as the person's name
            known_face_encodings.append(encoding)
            known_face_names.append(name)

# Function inorder to register a new face
def register_new_face(name):
    print(f"Please face the camera for enrollment, {name}!")
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        if len(face_encodings) > 0:
            print("Face detected! Registering...")
            cv2.imwrite(f"{known_faces_dir}/{name}.jpg", frame)
            video_capture.release()
            print(f"{name}'s face has been registered successfully.")
            return

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Function inorder to authenticate a person
def authenticate_person():
    print("Looking for a face to authenticate...")
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Display the results
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            if name != "Unknown":
                print(f"Access granted to {name}")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Access granted at {timestamp}")
                video_capture.release()
                cv2.destroyAllWindows()
                return name, timestamp
            else:
                print("Access denied. No matching face found.")
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Loading known faces
    load_known_faces()

    action = input("Do you want to (r)egister a new face or (a)uthenticate? ")

    if action.lower() == 'r':
        name = input("Enter the name for the new face: ")
        register_new_face(name)
    elif action.lower() == 'a':
        authenticate_person()
    else:
        print("Invalid choice.")
