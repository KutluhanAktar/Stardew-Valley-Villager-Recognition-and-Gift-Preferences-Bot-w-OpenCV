# Stardew Valley Villager Recognition and Gift Preferences Bot w/ OpenCV
#
# Via OpenCV, recognize villagers to display their birthdays, loves, likes, and hates
# while playing Stardew Valley on LattePanda Alpha.
#
# LattePanda Alpha 864s
#
# By Kutluhan Aktar

import cv2 as cv
import numpy as np
from windowframe import captureWindowFrame
from vision import computerVision
from arduino_serial_comm import arduino_serial_comm
from pics import character_pics

# Define a character (villager) name in Stardew Valley:
_character = 'Penny'
# Create a list of cropped images:
cropped_images_to_detect = [character_pics[_character][0], character_pics[_character][1], character_pics[_character][2]]

# Define the class objects:
winframe = captureWindowFrame('Stardew Valley')
game_vision = computerVision(cropped_images_to_detect)

# Define the detection status to avoid repetitive messages to the Arduino Leonardo:
detection_status = True

def detect_character(character, result_type, port):
    global detection_status
    # Get a new frame (screenshot):
    new_frame = winframe.get_frames()
    # Detect the cropped images in the given list:
    game_vision.detect_cropped_image(new_frame, 0.65)
    # Get the output image:
    output = game_vision.get_and_draw_points(result_type)
    # Get the detected cropped image points:
    points = len(game_vision.get_center_points())
    print(points)
    # Send message (data) to the Arduino Leonardo via serial communication:
    if(points == 0):
        detection_status = True
    elif (points > 0 and detection_status):
        detection_status = False
        arduino_serial_comm(port, character)
        # Save the output image:
        cv.imwrite('result_{}.jpg'.format(character), output)
    # Show the output image:
    cv.imshow('OpenCV Computer Vision on LattePanda', output)

while True:
    # Initialize villager (character) recognition:
    detect_character(_character, 'boxes', 'COM6')
    #detect_character(_character, 'markers', 'COM6')
    
    # Press 'q' to exit:
    if(cv.waitKey(1) == ord('q')):
        cv.destroyAllWindows()
        break
    
print('Window Closed!')
