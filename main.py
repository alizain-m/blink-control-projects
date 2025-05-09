import cv2
import mediapipe as mp

# Initialize webcam
camera = cv2.VideoCapture(0)

# Initialize MediaPipe Face Mesh solution
face_mesh_detector = mp.solutions.face_mesh.FaceMesh()

while True:
    # Capture a frame from the webcam
    success, frame = camera.read()
    if not success or frame is None:
        continue  # Skip to next iteration if frame isn't valid

    # Convert the frame from BGR (OpenCV default) to RGB (MediaPipe expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the RGB frame to detect face mesh landmarks
    detection_results = face_mesh_detector.process(frame_rgb)

    # Extract the list of detected face landmarks (if any)
    face_landmarks = detection_results.multi_face_landmarks

    # Print landmark data (can be replaced with visualization or logic later)
    print(face_landmarks)

    # Display the original frame in a window
    cv2.imshow("Eye Controlled Mouse", frame)

    # Wait for 1 ms and check for exit key (e.g., Esc)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to break the loop
        break

# Release camera and close windows when done
camera.release()
cv2.destroyAllWindows()
