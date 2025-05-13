import cv2
import mediapipe as mp
import pyautogui
import math


def euclidean_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

# Initialize webcam
webcam = cv2.VideoCapture(0)

# Initialize MediaPipe Face Mesh with iris refinement
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

screen_width, screen_height = pyautogui.size()

# Indices for left eye landmarks
left_eye_indices = {
    "outer_left": 133,
    "outer_right": 246,
    "top_outer": 159,
    "bottom_outer": 145,
    "top_inner": 160,
    "bottom_inner": 144
}

blink_counter = 0
blink_threshold_frames = 3
ear_threshold = 0.20


while True:
    # Capture a frame from the webcam
    success, frame = webcam.read()

    # Horizontally flip the frame for natural (mirror-like) interaction
    frame = cv2.flip(frame, flipCode=1)

    # Skip processing if the frame is invalid
    if not success or frame is None:
        continue 

    # Convert the frame from BGR (OpenCV default) to RGB (MediaPipe expects RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect facial landmarks
    result = face_mesh.process(frame_rgb)

    # Get frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Process and draw landmarks if a face is detected
    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        
        # Draw specific landmarks near the right eye (indices 474–477)
        for id, landmark in enumerate(landmarks[474:478]):
            x_px = int(landmark.x * frame_width)
            y_px = int(landmark.y * frame_height)
            cv2.circle(frame, center=(x_px, y_px), radius=3, color=(0, 255, 0))
            # print(x_px, y_px)  # Debug: Print the coordinates of the eye region
            if id == 1:
                screen_x = screen_width / frame_width * x_px
                screen_y = screen_height / frame_height * y_px
                pyautogui.moveTo(screen_x, screen_y)
        
        # After detecting landmarks:
        left_eye = {key: landmarks[idx] for key, idx in left_eye_indices.items()}

        # Draw overlay for left eye landmarks used in EAR calculation
        for name, landmark in left_eye.items():
            x_px = int(landmark.x * frame_width)
            y_px = int(landmark.y * frame_height)
            color = (0, 255, 255) if "top" in name or "bottom" in name else (255, 0, 255)
            cv2.circle(frame, center=(x_px, y_px), radius=3, color=color, thickness=-1)


        vertical_1 = euclidean_distance(left_eye["top_outer"], left_eye["bottom_outer"])
        vertical_2 = euclidean_distance(left_eye["top_inner"], left_eye["bottom_inner"])
        horizontal = euclidean_distance(left_eye["outer_left"], left_eye["outer_right"])
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)

        cv2.putText(frame, f'EAR: {ear:.3f}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if ear < ear_threshold:
            blink_counter += 1
        else:
            blink_counter = 0

        if blink_counter >= blink_threshold_frames:
            pyautogui.click()
            pyautogui.sleep(1)
            blink_counter = 0

        
        # Extract upper and lower eyelid landmarks for blink detection (left eye)
        # upper_lid = landmarks[145]
        # lower_lid = landmarks[159]

        # for lid_landmark in [upper_lid, lower_lid]:
        #     x_px = int(lid_landmark.x * frame_width)
        #     y_px = int(lid_landmark.y * frame_height)
        #     cv2.circle(frame, center=(x_px, y_px), radius=3, color=(0, 255, 255))

        # # If eyelids are close together, assume blink and trigger click
        # if (upper_lid.y - lower_lid.y) < 0.004:
        #     pyautogui.click()
        #     pyautogui.sleep(1)

    # Display the original frame in a window
    cv2.imshow("Eye Controlled Mouse", frame)

    # Wait for 1 ms and check for exit key (e.g., Esc)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to break the loop
        break

# Release camera and close windows when done
webcam.release()
cv2.destroyAllWindows()
