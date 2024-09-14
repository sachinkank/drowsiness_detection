import cv2
import numpy as np
import dlib
from imutils import face_utils
import pygame  # Import pygame for sound control

# Initialize the pygame mixer for playing sound
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm.wav")  # Load the alarm sound file

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)

def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    # Checking if the eye is blinked
    if ratio > 0.25:  # Eye is closed
        return 0
    elif ratio > 0.21 and ratio <= 0.25:  # Eye is partially closed
        return 1
    else:  # Eye is open
        return 2

# Variable to track if the alarm is playing
alarm_on = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    face_frame = frame.copy()

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Determine the status based on the state of both eyes
        if left_blink == 2 and right_blink == 2:
            # Both eyes are closed
            sleep += 1
            drowsy = 0
            active = 0
            if sleep > 6:
                status = "SLEEPING !!!"
                color = (255, 0, 0)

                # Play the alarm sound when sleeping, if not already playing
                if not alarm_on:
                    alarm_sound.play(loops=-1)  # Play alarm in a loop
                    alarm_on = True  # Mark alarm as on

        elif left_blink == 1 or right_blink == 1:
            # One or both eyes are partially closed
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                status = "Drowsy !"
                color = (0, 0, 255)
                if not alarm_on:
                    alarm_sound.play(loops=-1)  # Play alarm in a loop
                    alarm_on = True 

        else:
            # Both eyes are open
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                status = "Active :)"
                color = (0, 255, 0)

                # Stop the alarm sound if user is active
                if alarm_on:
                    alarm_sound.stop()  # Stop the alarm sound immediately
                    alarm_on = False  # Reset alarm status

        # Calculate the size of the text to be displayed
        (text_width, text_height), _ = cv2.getTextSize(status, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)

        # Get the frame's dimensions
        frame_height, frame_width = frame.shape[:2]

        # Calculate the center of the frame for text placement
        text_x = (frame_width - text_width) // 2
        text_y = (frame_height + text_height) // 2 - 50  # Subtract 50 to move the text up

        # Display the status slightly above the center of the frame
        cv2.putText(frame, status, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Result of detector", face_frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()
