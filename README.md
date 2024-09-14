**Drowsiness Detection System with Alarm:**

This project implements a real-time Drowsiness Detection System using Python, OpenCV, Dlib, and Pygame. The system detects when a person is drowsy or falling asleep and sounds an alarm to alert them. The program uses facial landmarks to monitor the state of the eyes and determine whether the user is awake, drowsy, or sleeping.

Features:

Real-time detection of drowsiness based on eye blinks.
Plays an alarm sound when the user is detected as sleeping or drowsy.
Stops the alarm automatically when the user becomes active again.
Works using a webcam to capture the video feed.
Requirements
Before running this project, you need to install the following libraries:

-opencv-python
-dlib version: 19.24.2
-imutils
-pygame
-numpy version: 1.26.4

To install these dependencies, run:
pip install opencv-python dlib imutils pygame numpy (check for the versions)

Additionally, you need to download the shape_predictor_68_face_landmarks.dat file, which is required by dlib for facial landmark detection.

How It Works:

The program uses OpenCV to capture video from your webcam.
Dlib is used to detect facial landmarks, specifically focusing on the eyes.
The system calculates the Eye Aspect Ratio (EAR) to detect if the eyes are closed or open.
Based on the ratio, the program determines if the user is awake, drowsy, or sleeping. Even works with one eye closed and open (status will be active then)
When the user is found to be sleeping or drowsy, an alarm sound is triggered using Pygame.
The alarm stops once the system detects that the user is active again (eyes are open).
